"""
Semantic search over the stored chunks.

The whole RAG "retrieval" idea in one function:
  1. Embed the question (as a QUERY, to match the DOCUMENT embeddings).
  2. Ask Postgres for the chunks whose vectors are closest to it.

`<=>` is pgvector's cosine *distance* operator (0 = same direction, 2 = opposite).
We return `1 - distance` as a similarity score, so higher = more relevant.
ORDER BY on the distance lets Postgres use the HNSW index instead of comparing
the question against every row.
"""

from dataclasses import dataclass

from psycopg_pool import ConnectionPool
from pgvector import Vector
from pgvector.psycopg import register_vector

from app import config
from app.embeddings import embed_query

# A pool keeps a few connections open and reuses them across requests,
# instead of paying the cost of a new database connection every time.
pool = ConnectionPool(
    config.DATABASE_URL,
    min_size=1,
    max_size=5,
    configure=register_vector,
    open=False,
)

SEARCH_SQL = """
SELECT id, source, chunk_index, content,
       1 - (embedding <=> %(q)s) AS score
FROM chunks
ORDER BY embedding <=> %(q)s
LIMIT %(k)s
"""


@dataclass
class SearchResult:
    id: int
    source: str
    chunk_index: int
    content: str
    score: float


def search(question: str, k: int = 5, min_score: float = 0.0) -> list[SearchResult]:
    # Wrap the plain Python list in pgvector's Vector type. A bare list is sent
    # to Postgres as double precision[], and the <=> operator only accepts vector.
    query_vector = Vector(embed_query(question))
    with pool.connection() as conn:
        rows = conn.execute(SEARCH_SQL, {"q": query_vector, "k": k}).fetchall()
    results = [SearchResult(*row) for row in rows]
    # Drop weak matches so the agent isn't fed irrelevant text.
    return [r for r in results if r.score >= min_score]
