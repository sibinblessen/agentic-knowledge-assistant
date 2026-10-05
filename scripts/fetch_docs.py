"""
Download the Google Cloud doc pages listed in data/sources.txt and save each
one as clean Markdown in data/docs/.

Run:  python scripts/fetch_docs.py

Why a script instead of saving pages by hand?
- Repeatable: edit sources.txt, run again, same result.
- Clean input: trafilatura strips menus, footers and cookie banners, so we
  only embed the actual article text. Junk in = junk retrieved.
- Each file starts with its source URL, so the agent can cite it later.
"""

import re
import sys
import time
from pathlib import Path

import requests
import trafilatura

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "data" / "sources.txt"
OUT_DIR = ROOT / "data" / "docs"
HEADERS = {"User-Agent": "Mozilla/5.0 (personal RAG learning project)"}


def slug_from_url(url: str) -> str:
    path = url.split("://", 1)[-1].split("?")[0].strip("/")
    path = path.replace("cloud.google.com/", "").replace("docs.cloud.google.com/", "")
    return re.sub(r"[^a-zA-Z0-9]+", "-", path).strip("-").lower()


def main() -> None:
    urls = [
        line.strip()
        for line in SOURCES.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok, failed = 0, []

    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)  # follows redirects
            resp.raise_for_status()
            markdown = trafilatura.extract(
                resp.text,
                output_format="markdown",
                include_links=False,
                include_tables=True,
                favor_precision=True,
            )
            if not markdown or len(markdown) < 300:
                raise ValueError("almost no article text extracted")

            title = trafilatura.extract_metadata(resp.text).title or slug_from_url(url)
            out = OUT_DIR / f"{slug_from_url(url)}.md"
            out.write_text(
                f"---\ntitle: {title}\nsource_url: {resp.url}\n"
                f"license: CC BY 4.0, Google Cloud documentation\n---\n\n"
                f"# {title}\n\n{markdown}\n"
            )
            print(f"  OK   {out.name}  ({len(markdown):,} chars)")
            ok += 1
        except Exception as e:
            print(f"  FAIL {url}  ->  {e}")
            failed.append(url)
        time.sleep(1)  # be polite to the server

    print(f"\nSaved {ok} of {len(urls)} pages to {OUT_DIR.relative_to(ROOT)}/")
    if failed:
        print("Failed URLs (page may have moved - check in a browser):")
        for u in failed:
            print(f"  {u}")
        sys.exit(1)


if __name__ == "__main__":
    main()
