#!/usr/bin/env python3
"""Fetch recent papers for this awesome list.

Examples:
    python tools/fetch_latest_papers.py --days 180 --limit 30 --output latest_papers.md
    python tools/fetch_latest_papers.py --format json --output latest_papers.json
    python tools/fetch_latest_papers.py --source searxng --searxng-url http://localhost:8080
    python tools/fetch_latest_papers.py --seed-from outputs/daily/latest_papers_2026-07-04.md --seed-only
    python tools/fetch_latest_papers.py --include-seen

Sources:
    - arXiv
    - OpenAlex
    - SearXNG, when SEARXNG_URL or --searxng-url is set

Optional environment variable:
    - OPENALEX_EMAIL
    - SEARXNG_URL
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


QUERIES = [
    '"large language model" "self-driving lab"',
    '"large language model" "autonomous laboratory"',
    '"LLM" "autonomous science"',
    '"LLM agents" "scientific discovery"',
    '"AI co-scientist"',
    '"AI scientist" "scientific discovery"',
    '"large language model" "laboratory automation"',
    '"LLM" "robotic" "chemistry"',
]

LLM_TERMS = [
    "large language model",
    "llm",
    "language model",
    "generative ai",
    "co-scientist",
    "ai scientist",
]

SCIENCE_TERMS = [
    "self-driving lab",
    "self driving lab",
    "self-driving laboratory",
    "autonomous laboratory",
    "autonomous science",
    "scientific discovery",
    "laboratory automation",
    "robotic chemistry",
    "robotic ai chemist",
    "agent-to-instrument",
]


@dataclass
class Paper:
    title: str
    url: str
    source: str
    published: str | None = None
    authors: list[str] | None = None
    venue: str | None = None
    abstract: str | None = None
    citations: int | None = None

    @property
    def year(self) -> str:
        return self.published[:4] if self.published else ""


def load_env(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def get_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{url}?{urllib.parse.urlencode(params)}",
        headers={"User-Agent": "awesome-llm-self-driving-labs/0.1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_text(url: str, params: dict[str, Any]) -> str:
    request = urllib.request.Request(
        f"{url}?{urllib.parse.urlencode(params)}",
        headers={"User-Agent": "awesome-llm-self-driving-labs/0.1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    try:
        return dt.date.fromisoformat(value[:10])
    except ValueError:
        return None


def normalize_title(title: str) -> str:
    title = clean(title).lower()
    return re.sub(r"[^a-z0-9]+", " ", title).strip()


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    if netloc == "arxiv.org" and path.startswith("/abs/"):
        path = re.sub(r"v\d+$", "", path)
    return urllib.parse.urlunsplit((parsed.scheme.lower(), netloc, path, "", ""))


def paper_keys(paper: Paper) -> set[str]:
    keys = {f"title:{normalize_title(paper.title)}"}
    if paper.url:
        keys.add(f"url:{normalize_url(paper.url)}")
    return {key for key in keys if not key.endswith(":")}


def load_seen(path: Path) -> set[str]:
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    if isinstance(data, list):
        return {str(item) for item in data}
    if isinstance(data, dict):
        return {str(item) for item in data.get("keys", [])}
    return set()


def save_seen(path: Path, keys: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "keys": sorted(keys),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seed_seen_from_markdown(path: Path, keys: set[str]) -> int:
    if not path.exists():
        return 0
    count = 0
    pattern = re.compile(r"^- \*\*(?P<title>.+?)\*\*.*?\[link\]\((?P<url>.+?)\)")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.search(line)
        if not match:
            continue
        before = len(keys)
        keys.update(
            paper_keys(
                Paper(
                    title=match.group("title"),
                    url=match.group("url"),
                    source="seed",
                )
            )
        )
        if len(keys) > before:
            count += 1
    return count


def reconstruct_openalex_abstract(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    words = sorted((pos, word) for word, poses in index.items() for pos in poses)
    return " ".join(word for _, word in words)


def relevant(paper: Paper) -> bool:
    text = f"{paper.title} {paper.abstract or ''}".lower()
    return any(term in text for term in LLM_TERMS) and any(term in text for term in SCIENCE_TERMS)


def search_arxiv(query: str, since: dt.date, limit: int) -> list[Paper]:
    xml_text = get_text(
        "https://export.arxiv.org/api/query",
        {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        },
    )
    root = ET.fromstring(xml_text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers: list[Paper] = []

    for entry in root.findall("atom:entry", ns):
        published = clean(entry.findtext("atom:published", namespaces=ns))
        if (date := parse_date(published)) and date < since:
            continue
        authors = [
            clean(author.findtext("atom:name", namespaces=ns))
            for author in entry.findall("atom:author", ns)
        ]
        papers.append(
            Paper(
                title=clean(entry.findtext("atom:title", namespaces=ns)),
                url=clean(entry.findtext("atom:id", namespaces=ns)),
                source="arXiv",
                published=published[:10] if published else None,
                authors=[a for a in authors if a],
                abstract=clean(entry.findtext("atom:summary", namespaces=ns)),
            )
        )
    return papers


def search_openalex(query: str, since: dt.date, limit: int) -> list[Paper]:
    params: dict[str, Any] = {
        "search": query.replace('"', ""),
        "per_page": min(limit, 200),
        "sort": "publication_date:desc",
        "filter": f"from_publication_date:{since.isoformat()}",
    }
    if email := os.environ.get("OPENALEX_EMAIL"):
        params["mailto"] = email

    data = get_json("https://api.openalex.org/works", params)
    papers: list[Paper] = []

    for work in data.get("results", []):
        authors = [
            ((authorship.get("author") or {}).get("display_name") or "").strip()
            for authorship in work.get("authorships", [])[:6]
        ]
        location = work.get("primary_location") or {}
        source = location.get("source") or {}
        papers.append(
            Paper(
                title=clean(work.get("title")),
                url=work.get("doi") or work.get("id") or "",
                source="OpenAlex",
                published=work.get("publication_date"),
                authors=[a for a in authors if a],
                venue=source.get("display_name"),
                abstract=clean(reconstruct_openalex_abstract(work.get("abstract_inverted_index"))),
                citations=work.get("cited_by_count"),
            )
        )
    return papers


def search_searxng(query: str, _since: dt.date, limit: int, base_url: str) -> list[Paper]:
    data = get_json(
        base_url.rstrip("/") + "/search",
        {
            "q": query,
            "format": "json",
            "language": "en",
            "safesearch": 1,
        },
    )
    papers: list[Paper] = []
    for item in data.get("results", [])[:limit]:
        papers.append(
            Paper(
                title=clean(item.get("title")),
                url=item.get("url") or "",
                source="SearXNG",
                venue=item.get("engine"),
                abstract=clean(item.get("content")),
            )
        )
    return papers


def collect(
    days: int,
    per_query: int,
    sources: list[str],
    delay: float,
    seen_keys: set[str] | None = None,
    searxng_url: str | None = None,
) -> list[Paper]:
    since = dt.date.today() - dt.timedelta(days=days)
    seen_keys = seen_keys or set()
    current: dict[str, Paper] = {}
    current_keys: set[str] = set()

    for query in QUERIES:
        source_funcs = []
        if "arxiv" in sources:
            source_funcs.append(search_arxiv)
        if "openalex" in sources:
            source_funcs.append(search_openalex)
        if "searxng" in sources and searxng_url:
            source_funcs.append(lambda q, s, l: search_searxng(q, s, l, searxng_url))

        for source in source_funcs:
            try:
                results = source(query, since, per_query)
            except Exception as exc:
                name = getattr(source, "__name__", "search_searxng")
                print(f"warning: {name} failed for {query!r}: {exc}")
                continue

            for paper in results:
                if not paper.title or not paper.url or not relevant(paper):
                    continue
                keys = paper_keys(paper)
                if keys & seen_keys or keys & current_keys:
                    continue
                key = next(iter(sorted(keys)))
                existing = current.get(key)
                if not existing or (paper.citations or 0) > (existing.citations or 0):
                    current[key] = paper
                    current_keys.update(keys)
            if delay:
                import time

                time.sleep(delay)

    return sorted(current.values(), key=lambda p: (p.published or "", p.citations or 0), reverse=True)


def authors_text(authors: list[str] | None) -> str:
    if not authors:
        return ""
    shown = authors[:3]
    return ", ".join(shown) + (" et al." if len(authors) > 3 else "")


def render_markdown(papers: list[Paper], days: int) -> str:
    lines = [
        "# Latest LLM-Driven Self-Driving Labs Papers",
        "",
        f"Generated: {dt.datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Lookback: {days} days",
        "",
    ]
    for paper in papers:
        meta = [item for item in [paper.year, paper.venue, paper.source] if item]
        if paper.citations is not None:
            meta.append(f"{paper.citations} citations")
        author_part = f" - {authors_text(paper.authors)}" if paper.authors else ""
        meta_part = f" ({'; '.join(meta)})" if meta else ""
        lines.append(f"- **{paper.title}**{author_part}{meta_part} - [link]({paper.url})")
    return "\n".join(lines) + "\n"


def render_json(papers: list[Paper]) -> str:
    return json.dumps([asdict(paper) for paper in papers], ensure_ascii=False, indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=180)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--per-query", type=int, default=20)
    parser.add_argument(
        "--source",
        action="append",
        choices=["arxiv", "openalex", "searxng"],
        help="Source to use. Repeat for multiple sources. Default: arxiv + openalex, plus searxng when configured.",
    )
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between API calls in seconds.")
    parser.add_argument("--searxng-url", help="SearXNG base URL, e.g. http://localhost:8080")
    parser.add_argument("--seen-file", default="outputs/seen_papers.json", help="Persistent dedupe state file.")
    parser.add_argument("--seed-from", action="append", help="Seed dedupe state from an existing markdown output.")
    parser.add_argument("--seed-only", action="store_true", help="Only update dedupe state from --seed-from files.")
    parser.add_argument("--include-seen", action="store_true", help="Do not filter previously seen papers.")
    parser.add_argument("--no-update-seen", action="store_true", help="Do not update the seen state file.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", "-o")
    return parser.parse_args()


def main() -> int:
    load_env()
    args = parse_args()
    searxng_url = args.searxng_url or os.environ.get("SEARXNG_URL")
    sources = args.source or ["arxiv", "openalex"]
    if searxng_url and "searxng" not in sources:
        sources.append("searxng")
    seen_path = Path(args.seen_file)
    seen_keys = set() if args.include_seen else load_seen(seen_path)
    if args.seed_from:
        seeded = sum(seed_seen_from_markdown(Path(path), seen_keys) for path in args.seed_from)
        save_seen(seen_path, seen_keys)
        print(f"seeded {seeded} entries into {seen_path}")
        if args.seed_only:
            return 0
    papers = collect(
        days=args.days,
        per_query=args.per_query,
        sources=sources,
        delay=args.delay,
        seen_keys=seen_keys,
        searxng_url=searxng_url,
    )[: args.limit]
    if not args.include_seen and not args.no_update_seen:
        for paper in papers:
            seen_keys.update(paper_keys(paper))
        save_seen(seen_path, seen_keys)
    output = render_json(papers) if args.format == "json" else render_markdown(papers, args.days)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
