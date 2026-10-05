"""All settings in one place, read from .env. Shared by ingestion, the API and the agent."""

import os

from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing {name} in .env")
    return value


PROJECT = _required("GOOGLE_CLOUD_PROJECT")
GEN_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
EMB_LOCATION = os.getenv("EMBEDDING_LOCATION", "europe-west1")
GEMINI_MODEL = _required("GEMINI_MODEL")
EMBEDDING_MODEL = _required("EMBEDDING_MODEL")
EMBEDDING_DIM = 768  # must match vector(768) in db/init.sql
DATABASE_URL = _required("DATABASE_URL")

# Measured: relevant matches score ~0.72-0.80, off-topic questions ~0.51.
# 0.6 sits in the gap, so unrelated questions return nothing.
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.6"))

# Where the agent finds the retrieval API (Cloud Run URL later)
SEARCH_API_URL = os.getenv("SEARCH_API_URL", "http://localhost:8000").rstrip("/")

# How many times the agent may rewrite the query before giving up
MAX_REWRITES = int(os.getenv("MAX_REWRITES", "2"))
