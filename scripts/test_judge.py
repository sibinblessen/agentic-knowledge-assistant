"""
How do we know the grounding check works?

We call the `check` node directly with hand-made inputs whose correct verdict we
already know. No database, retrieval API or full agent run needed: LangGraph
nodes are plain functions, so they're easy to test in isolation.

Run:  python -m scripts.test_judge
"""

import sys

from app.agent import check

# Fixed test passages (short excerpts in the style of the Cloud Run secrets doc).
# Fixed inputs make the test repeatable.
PASSAGES = [
    {
        "content": (
            "Configure secrets for services (Cloud Run) > Make a secret accessible to Cloud Run\n\n"
            "You can make a secret available to your containers in either of two ways: mount each "
            "secret as a volume, which makes the secret available to the container as files, or "
            "pass a secret using environment variables. Environment variables are resolved at "
            "instance startup time, so if you use them, pin the secret to a particular version "
            "rather than using latest."
        )
    },
    {
        "content": (
            "Configure secrets for services (Cloud Run) > Required roles\n\n"
            "To access secrets, the service account running the Cloud Run service needs the "
            "Secret Manager Secret Accessor role (roles/secretmanager.secretAccessor) on the secret."
        )
    },
]

GOOD = (
    "You can expose a secret to Cloud Run either as files, by mounting it as a volume, or as an "
    "environment variable [1]. Environment variables are resolved when the instance starts, so "
    "pin a specific secret version [1]. The service account running the service needs the "
    "Secret Manager Secret Accessor role on the secret [2]."
)

FABRICATED_CLAIM = "Cloud Run also rotates secrets automatically every 24 hours [1]."

CASES = [
    # (name, answer, expected_grounded, what it proves)
    ("good answer", GOOD, True,
     "the judge accepts a correct answer"),
    ("planted fabrication", GOOD + " " + FABRICATED_CLAIM, False,
     "the judge CATCHES an invented fact"),
    ("faithful paraphrase",
     "There are two options: read the secret from files by mounting it as a volume, or read it "
     "from an environment variable [1]. With environment variables the value is fetched once at "
     "startup, so use a pinned version [1]. Grant the running service account "
     "roles/secretmanager.secretAccessor on the secret [2].",
     True, "the judge does NOT over-flag different wording"),
    ("wrong citation",
     "The service account running the service needs the Secret Manager Secret Accessor role "
     "on the secret [1].",
     False, "the judge checks citations, not just content"),
]


def main() -> None:
    failures = 0
    for name, answer, expected, proves in CASES:
        state = {
            "in_scope": True,
            "passages": PASSAGES,
            "answer": answer,
            "generations": 1,  # below MAX_GENERATIONS, so no warning is added
        }
        verdict = check(state)
        ok = verdict["grounded"] == expected
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name:<20} expected grounded={expected}, got {verdict['grounded']}"
              f"   ({proves})")
        for claim in verdict["unsupported_claims"]:
            print(f"        flagged: {claim}")

    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
