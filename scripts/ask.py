"""
Ask the agent a question from the terminal and watch each step.

Needs the retrieval API running in another terminal:  uvicorn app.api:app --reload

Run:  python -m scripts.ask "How do I give Cloud Run access to a secret?"
"""

import sys

from app import config
from app.agent import agent


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('Usage: python -m scripts.ask "your question"')
    question = " ".join(sys.argv[1:])
    print(f"\nQ: {question}\n")

    # stream(..., stream_mode="updates") yields {node_name: what_that_node_returned}
    # after each step, so we can print the agent's progress as it happens.
    final = {}
    for step in agent.stream({"question": question}, stream_mode="updates"):
        for node, update in step.items():
            if node == "rewrite":
                if not update["in_scope"]:
                    print("[rewrite]  out of scope -> skipping search")
                else:
                    print(f"[rewrite]  attempt {update['attempts']}: \"{update['search_query']}\"")
            elif node == "retrieve":
                ps = update["passages"]
                if not ps:
                    print(f"[retrieve] nothing above {config.MIN_SCORE} (best {update['best_score']:.2f})")
                else:
                    print(f"[retrieve] {len(ps)} relevant passages")
                for p in ps:
                    print(f"           {p['score']:.2f}  {'/'.join(p['source'].rstrip('/').split('/')[-2:])}")
            elif node == "generate":
                print("[generate] answer written")
            final.update(update)

    print(f"\nA: {final['answer']}\n")
    if final.get("sources"):
        print("Sources:")
        for s in final["sources"]:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
