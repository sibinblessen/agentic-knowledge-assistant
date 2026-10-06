"""
The LangGraph agent.

Step 3c graph (rewrite/retrieve loop from 3b, plus a grounding check):

    START -> rewrite --(out of scope)--> generate ("I only cover Google Cloud docs")
                |
                v
             retrieve --(found relevant passages)--> generate -> END
                ^           |
                |           +--(nothing relevant, attempts left)--+
                +-------------------------------------------------+
                            |
                            +--(nothing relevant, no attempts left)--> generate ("not found")

    generate -> check --(grounded)--> END
       ^          |
       |          +--(not grounded, generations left)--> generate (told which claims failed)
       |          +--(not grounded, none left)--> END with a warning
"""

from functools import lru_cache
from typing import TypedDict

import httpx
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from app import config, llm


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
class AgentState(TypedDict, total=False):
    question: str          # what the user asked (never changed)
    in_scope: bool         # is this a question our knowledge base could answer?
    search_query: str      # the rewritten query used for search
    attempts: int          # how many rewrites we've done
    best_score: float      # best similarity seen in the last search (feedback for retries)
    passages: list[dict]   # relevant passages (score >= MIN_SCORE)
    answer: str
    sources: list[str]
    generations: int              # how many answers we've written
    grounded: bool                # judge verdict on the latest answer
    unsupported_claims: list[str] # sentences the judge could not verify
    warning: str                  # set if we give up while still not grounded
    check_skipped: bool           # True for fixed replies that make no factual claims


# ---------------------------------------------------------------------------
# Tool: the retrieval API
# ---------------------------------------------------------------------------
def _search(query: str) -> list[dict]:
    # min_score=0: we want ALL top results back, so we can report the best score
    # as feedback. We apply the real threshold ourselves in retrieve().
    resp = httpx.get(
        f"{config.SEARCH_API_URL}/search",
        params={"q": query, "k": 5, "min_score": 0},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["results"]


@lru_cache(maxsize=1)
def known_titles() -> list[str]:
    """Titles of the documents in the knowledge base, fetched once from the API."""
    resp = httpx.get(f"{config.SEARCH_API_URL}/sources", timeout=30)
    resp.raise_for_status()
    return [s["title"] for s in resp.json()]


# ---------------------------------------------------------------------------
# Node 1: rewrite - map the user's wording onto the documentation's wording
# ---------------------------------------------------------------------------
class RewrittenQuery(BaseModel):
    in_scope: bool = Field(
        description="True if the question is about Google Cloud or cloud engineering topics; "
        "false for anything unrelated (general knowledge, chit-chat, other domains)"
    )
    query: str = Field(description="The search query, under 15 words. Empty if not in scope.")


REWRITE_SYSTEM = """You turn user questions into search queries for a vector database
of Google Cloud documentation.

The knowledge base contains these documentation pages:
{titles}

Rules:
- First decide if the question is in scope (about Google Cloud or cloud engineering).
  If not, set in_scope to false and leave the query empty.
- Preserve the user's intent. Never change the topic to fit the knowledge base.
- Use the terminology the documentation would use, not the user's informal wording.
- Name the specific Google Cloud products and concepts involved.
- Write one query, under 15 words.

Example:
User question: my app keeps getting permission denied when calling the AI model
Query: IAM permissions service account access Gemini API from Cloud Run"""


def rewrite(state: AgentState) -> dict:
    attempts = state.get("attempts", 0)
    prompt = f"User question: {state['question']}"
    if attempts > 0:
        # Retry: tell Gemini what didn't work, so it tries a genuinely different query.
        prompt += (
            f"\n\nYour previous query \"{state['search_query']}\" found nothing relevant "
            f"(best similarity {state['best_score']:.2f}, needed {config.MIN_SCORE}). "
            "Try a different angle: other terminology, or a broader or narrower scope."
        )
    titles = "\n".join(f"- {t}" for t in known_titles())
    result = llm.generate_json(prompt, REWRITE_SYSTEM.format(titles=titles), RewrittenQuery)
    return {"in_scope": result.in_scope, "search_query": result.query, "attempts": attempts + 1}


# ---------------------------------------------------------------------------
# Node 2: retrieve - search with the rewritten query AND the original question
# ---------------------------------------------------------------------------
def retrieve(state: AgentState) -> dict:
    merged: dict[int, dict] = {}
    for query in {state["search_query"], state["question"]}:
        for p in _search(query):
            # Same chunk found by both queries: keep the higher score.
            if p["id"] not in merged or p["score"] > merged[p["id"]]["score"]:
                merged[p["id"]] = p

    ranked = sorted(merged.values(), key=lambda p: p["score"], reverse=True)
    best = ranked[0]["score"] if ranked else 0.0
    relevant = [p for p in ranked if p["score"] >= config.MIN_SCORE][:5]
    return {"passages": relevant, "best_score": best}


# ---------------------------------------------------------------------------
# Router: the conditional edge after rewrite
# ---------------------------------------------------------------------------
def after_rewrite(state: AgentState) -> str:
    return "retrieve" if state["in_scope"] else "generate"


# ---------------------------------------------------------------------------
# Router: the conditional edge after retrieve
# ---------------------------------------------------------------------------
def after_retrieve(state: AgentState) -> str:
    if state["passages"]:
        return "generate"
    if state["attempts"] < config.MAX_REWRITES:
        return "rewrite"       # loop back and try a different query
    return "generate"          # give up; generate will say "not found"


# ---------------------------------------------------------------------------
# Node 3: generate - answer only from the passages (+ feedback when regenerating)
# ---------------------------------------------------------------------------
def format_passages(passages: list[dict]) -> str:
    return "\n\n".join(f"[{i}] {p['content']}" for i, p in enumerate(passages, 1))

ANSWER_SYSTEM = """You are a Google Cloud documentation assistant.
Answer the question using ONLY the numbered passages provided.
Rules:
- Cite every factual sentence with the passage number(s) in square brackets, e.g. [1] or [2][3].
- If the passages answer the question only partly, answer the part they support and say briefly what they don't cover.
- Only if NOTHING in the passages is relevant, say exactly: "I couldn't find that in the documentation I have."
- Do not use outside knowledge, even if you know the answer.
- Be concise: a short paragraph or a few bullet points."""

NOT_FOUND = "I couldn't find that in the documentation I have."
OUT_OF_SCOPE = "That's outside what I can help with. I answer questions about Google Cloud, based on its documentation."


def generate(state: AgentState) -> dict:
    if not state.get("in_scope", True):
        return {"answer": OUT_OF_SCOPE, "sources": [], "generations": 0}
    passages = state.get("passages", [])
    if not passages:
        return {"answer": NOT_FOUND, "sources": [], "generations": 0}

    prompt = (
        f"Passages:\n\n{format_passages(passages)}\n\n"
        f"Question: {state['question']}\n"
        f"(Interpreted as: {state['search_query']})"
    )
    if state.get("unsupported_claims"):
        # Regeneration: tell Gemini exactly what the judge rejected last time.
        failed = "\n".join(f"- {c}" for c in state["unsupported_claims"])
        prompt += (
            "\n\nA fact-checker found these statements in your previous answer NOT supported "
            f"by the passages:\n{failed}\n"
            "Write the answer again. Remove those statements or rephrase them so they say only "
            "what the passages say, with correct citations."
        )
    answer = llm.generate(prompt, system=ANSWER_SYSTEM)

    cited = []
    for i, p in enumerate(passages, 1):
        if f"[{i}]" in answer and p["source"] not in cited:
            cited.append(p["source"])
    return {"answer": answer, "sources": cited, "generations": state.get("generations", 0) + 1}


# ---------------------------------------------------------------------------
# Node 4: check - a second Gemini call acts as a fact-checker (LLM-as-judge)
# ---------------------------------------------------------------------------
class GroundingVerdict(BaseModel):
    grounded: bool = Field(description="True only if every factual statement is supported by the passages")
    unsupported_claims: list[str] = Field(
        default_factory=list,
        description="Each statement that is not supported, copied exactly from the answer",
    )


JUDGE_SYSTEM = """You are a strict fact-checker. You receive numbered source passages and an answer.
Check the answer one statement at a time.

A statement is SUPPORTED only if:
- the passages state it, or it follows directly from them (paraphrasing is fine), AND
- the passage number(s) it cites actually contain that information.

A statement is UNSUPPORTED if it adds facts not in the passages (even if true in reality),
overstates them (e.g. "always" where the passages say "by default"), or cites the wrong passage.

Ignore statements that only say what the passages do NOT cover.
Set grounded to true only if there are no unsupported statements.
List every unsupported statement exactly as written in the answer."""


def check(state: AgentState) -> dict:
    passages = state.get("passages", [])
    if not state.get("in_scope", True) or not passages:
        # Fixed refusal messages make no factual claims: nothing to verify.
        return {"grounded": True, "unsupported_claims": [], "check_skipped": True}

    prompt = f"Passages:\n\n{format_passages(passages)}\n\nAnswer to check:\n{state['answer']}"
    verdict = llm.generate_json(prompt, JUDGE_SYSTEM, GroundingVerdict, model=config.JUDGE_MODEL)

    update = {"grounded": verdict.grounded, "unsupported_claims": verdict.unsupported_claims}
    if not verdict.grounded and state.get("generations", 0) >= config.MAX_GENERATIONS:
        update["warning"] = (
            "Some statements in this answer could not be verified against the documentation: "
            + "; ".join(verdict.unsupported_claims)
        )
    return update


# ---------------------------------------------------------------------------
# Router: the conditional edge after check
# ---------------------------------------------------------------------------
def after_check(state: AgentState) -> str:
    if state["grounded"] or state.get("warning"):
        return END            # done: either verified, or out of retries (with a warning)
    return "generate"         # regenerate once, with the judge's feedback


# ---------------------------------------------------------------------------
# The graph
# ---------------------------------------------------------------------------
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("rewrite", rewrite)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_node("check", check)

    graph.add_edge(START, "rewrite")
    graph.add_conditional_edges("rewrite", after_rewrite, ["retrieve", "generate"])
    # Conditional edge: after_retrieve() looks at the state and picks the next node.
    graph.add_conditional_edges("retrieve", after_retrieve, ["rewrite", "generate"])
    graph.add_edge("generate", "check")
    graph.add_conditional_edges("check", after_check, ["generate", END])
    return graph.compile()


agent = build_graph()
