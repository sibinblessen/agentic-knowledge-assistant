"""
Turning text into vectors with the Gemini embedding model.

Key idea: documents and questions are embedded with different *task types*.
RETRIEVAL_DOCUMENT tells the model "this is something to be found",
RETRIEVAL_QUERY tells it "this is someone searching". Using the matching pair
noticeably improves search quality compared to embedding both the same way.
"""

import time

from google import genai
from google.genai import types

from app import config

_client = genai.Client(vertexai=True, project=config.PROJECT, location=config.EMB_LOCATION)


def _embed(text: str, task_type: str, title: str | None = None, retries: int = 5) -> list[float]:
    cfg = types.EmbedContentConfig(
        task_type=task_type,
        output_dimensionality=config.EMBEDDING_DIM,
        title=title,  # only used for documents; gives the model extra context
    )
    for attempt in range(retries):
        try:
            resp = _client.models.embed_content(model=config.EMBEDDING_MODEL, contents=text, config=cfg)
            return resp.embeddings[0].values
        except Exception as e:
            # 429 = rate limited. Back off and retry: 2s, 4s, 8s ...
            if attempt == retries - 1:
                raise
            wait = 2 ** (attempt + 1)
            print(f"    embedding failed ({str(e)[:80]}), retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def embed_document(text: str, title: str | None = None) -> list[float]:
    return _embed(text, "RETRIEVAL_DOCUMENT", title)


def embed_query(text: str) -> list[float]:
    return _embed(text, "RETRIEVAL_QUERY")
