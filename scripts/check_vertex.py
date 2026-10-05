"""
Step 0 smoke test: can this machine talk to Gemini and an embedding model
on Google Cloud?

Run:  python scripts/check_vertex.py

It tries a few model IDs (newest first), because model names change often,
and prints the first one that works so you can put it in .env.
"""

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GEN_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
EMB_LOCATION = os.getenv("EMBEDDING_LOCATION", "europe-west1")

GEMINI_CANDIDATES = [
    os.getenv("GEMINI_MODEL") or None,
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]
EMBEDDING_CANDIDATES = [
    os.getenv("EMBEDDING_MODEL") or None,
    "gemini-embedding-2",
    "gemini-embedding-001",
    "text-embedding-005",
]

if not PROJECT or PROJECT == "your-project-id":
    sys.exit("Set GOOGLE_CLOUD_PROJECT in .env first (cp .env.example .env).")


def first_working(label, candidates, try_fn):
    print(f"\n== {label} ==")
    for model in [m for m in candidates if m]:
        try:
            detail = try_fn(model)
            print(f"  OK   {model}  ->  {detail}")
            return model
        except Exception as e:  # we want to see every failure reason here
            msg = str(e).splitlines()[0][:140]
            print(f"  FAIL {model}  ->  {msg}")
    return None


# One client per location: Gemini on "global", embeddings on a region.
gen_client = genai.Client(vertexai=True, project=PROJECT, location=GEN_LOCATION)
emb_client = genai.Client(vertexai=True, project=PROJECT, location=EMB_LOCATION)


def try_gemini(model):
    resp = gen_client.models.generate_content(
        model=model,
        contents="In one short sentence: what is retrieval-augmented generation?",
    )
    return resp.text.strip()


def try_embedding(model):
    resp = emb_client.models.embed_content(
        model=model,
        contents="What does my travel insurance cover?",
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    vec = resp.embeddings[0].values
    return f"vector of {len(vec)} numbers, first 3: {[round(v, 4) for v in vec[:3]]}"


print(f"Project: {PROJECT} | Gemini location: {GEN_LOCATION} | Embedding location: {EMB_LOCATION}")
gemini = first_working("Gemini (text generation)", GEMINI_CANDIDATES, try_gemini)
embedder = first_working("Embedding model", EMBEDDING_CANDIDATES, try_embedding)

print("\n== Result ==")
if gemini and embedder:
    print("All good. Put these in your .env:")
    print(f"  GEMINI_MODEL={gemini}")
    print(f"  EMBEDDING_MODEL={embedder}")
else:
    print("Something failed - paste this whole output back to Claude.")
    sys.exit(1)
