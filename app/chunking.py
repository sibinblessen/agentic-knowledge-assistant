"""
Splitting Markdown documents into chunks for embedding.

Strategy: structure first, size second.
1. Split on Markdown headings, so a chunk never mixes two unrelated sections.
2. If a section is still too long, pack whole paragraphs up to MAX_CHARS,
   carrying a small OVERLAP of text into the next chunk so an idea that
   straddles the boundary is not lost.
3. Prefix every chunk with "document title > section heading". A chunk that
   just says "Set the --max-instances flag" is ambiguous on its own; with the
   header it clearly belongs to Cloud Run. This makes both the embedding and
   the agent's citations better.
"""

import re
from dataclasses import dataclass

MAX_CHARS = 1000
OVERLAP_CHARS = 150

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


@dataclass
class Chunk:
    source: str       # source URL, used for citations
    title: str        # document title
    section: str      # heading path, e.g. "Pricing > Free tier"
    index: int        # position within the document
    text: str         # header + body, this is what gets embedded and stored


def parse_front_matter(raw: str) -> tuple[dict, str]:
    meta = {}
    if raw.startswith("---"):
        _, header, body = raw.split("---", 2)
        for line in header.strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        return meta, body
    return meta, raw


def _clean_title(title: str) -> str:
    # "Create budgets | Cloud Billing | Google Cloud Documentation" -> "Create budgets (Cloud Billing)"
    parts = [p.strip() for p in title.split("|") if "Google Cloud Documentation" not in p]
    return f"{parts[0]} ({parts[1]})" if len(parts) > 1 else parts[0]


def _sections(body: str) -> list[tuple[str, str]]:
    """Return (heading_path, text) pairs. The heading path tracks nesting: H2 > H3."""
    stack: list[tuple[int, str]] = []
    sections, buf = [], []

    def flush():
        text = "\n".join(buf).strip()
        if text:
            path = " > ".join(h for _, h in stack[1:])  # skip H1, it's the title
            sections.append((path, text))
        buf.clear()

    for line in body.splitlines():
        m = HEADING.match(line)
        if m:
            flush()
            level, heading = len(m.group(1)), m.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, heading))
        else:
            buf.append(line)
    flush()
    return sections


def _pack(text: str) -> list[str]:
    """Pack paragraphs into pieces of at most MAX_CHARS, with overlap between pieces."""
    if len(text) <= MAX_CHARS:
        return [text]
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    # A single giant paragraph: fall back to splitting on sentences.
    units = []
    for p in paragraphs:
        units.extend(re.split(r"(?<=[.!?])\s+", p) if len(p) > MAX_CHARS else [p])

    pieces, current = [], ""
    for unit in units:
        if current and len(current) + len(unit) + 2 > MAX_CHARS:
            pieces.append(current)
            current = current[-OVERLAP_CHARS:].split(" ", 1)[-1]  # overlap, starting at a word
        current = f"{current}\n\n{unit}" if current else unit
    if current:
        pieces.append(current)
    # Last resort: hard-split only pieces with no usable breaks at all.
    limit = MAX_CHARS + OVERLAP_CHARS
    result = []
    for p in pieces:
        result.extend([p] if len(p) <= limit else [p[i : i + MAX_CHARS] for i in range(0, len(p), MAX_CHARS)])
    return result


def chunk_document(raw: str, fallback_name: str) -> list[Chunk]:
    meta, body = parse_front_matter(raw)
    title = _clean_title(meta.get("title", fallback_name))
    source = meta.get("source_url", fallback_name)

    chunks = []
    for section, text in _sections(body):
        for piece in _pack(text):
            if len(piece) < 80:  # skip fragments too short to carry meaning
                continue
            header = f"{title} > {section}" if section else title
            chunks.append(Chunk(source, title, section, len(chunks), f"{header}\n\n{piece}"))
    return chunks
