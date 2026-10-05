-- Schema for the knowledge base. Same SQL will run on Cloud SQL later.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    id           BIGSERIAL PRIMARY KEY,
    source       TEXT        NOT NULL,          -- file name, used for citations
    chunk_index  INT         NOT NULL,          -- position of the chunk within the file
    content      TEXT        NOT NULL,          -- the chunk text itself
    content_hash TEXT        NOT NULL UNIQUE,   -- lets re-runs skip chunks already stored
    embedding    vector(768) NOT NULL,          -- gemini-embedding-001 at 768 dimensions
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- HNSW = approximate nearest-neighbour index. Cosine distance matches how
-- embedding similarity is usually measured.
CREATE INDEX IF NOT EXISTS chunks_embedding_idx
    ON chunks USING hnsw (embedding vector_cosine_ops);
