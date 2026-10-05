"""
Ingestion: load -> chunk -> embed -> store.

Run from the project root:
  python -m scripts.ingest --dry-run    # just show the chunks, no API calls
  python -m scripts.ingest              # embed and store new chunks

Idempotent: every chunk gets a SHA-256 hash of its text. Chunks whose hash is
already in the database are skipped *before* embedding, so re-running costs
nothing, and only changed or new content gets embedded.
"""

import argparse
import hashlib
from pathlib import Path

from app.chunking import chunk_document
from app.db import connect
from app.embeddings import embed_document

DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "docs"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="chunk only, print a sample")
    args = parser.parse_args()

    # 1. Load + 2. Chunk
    chunks = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        doc_chunks = chunk_document(path.read_text(), path.stem)
        print(f"  {path.name}: {len(doc_chunks)} chunks")
        chunks.extend(doc_chunks)

    sizes = [len(c.text) for c in chunks]
    print(f"\n{len(chunks)} chunks | avg {sum(sizes) // len(sizes)} chars | min {min(sizes)} | max {max(sizes)}")

    if args.dry_run:
        sample = chunks[len(chunks) // 2]
        print(f"\n--- sample chunk #{sample.index} from {sample.source} ---\n{sample.text}\n---")
        return

    # 3. Embed + 4. Store
    with connect() as conn:
        existing = {row[0] for row in conn.execute("SELECT content_hash FROM chunks")}
        new = [(c, hashlib.sha256(c.text.encode()).hexdigest()) for c in chunks]
        new = [(c, h) for c, h in new if h not in existing]
        print(f"{len(chunks) - len(new)} already stored, {len(new)} to embed\n")

        for i, (chunk, content_hash) in enumerate(new, 1):
            vector = embed_document(chunk.text, title=chunk.title)
            conn.execute(
                """
                INSERT INTO chunks (source, chunk_index, content, content_hash, embedding)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (content_hash) DO NOTHING
                """,
                (chunk.source, chunk.index, chunk.text, content_hash, vector),
            )
            if i % 25 == 0 or i == len(new):
                conn.commit()  # commit in batches so a crash doesn't lose everything
                print(f"  embedded and stored {i}/{len(new)}")

        total = conn.execute("SELECT count(*) FROM chunks").fetchone()[0]
        print(f"\nDone. {total} chunks in the database.")


if __name__ == "__main__":
    main()
