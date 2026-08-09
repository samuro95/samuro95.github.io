#!/usr/bin/env python3
"""Import missing works from a public Google Scholar profile into Hugo.

The sync is intentionally additive: hand-written publication pages are never
modified or deleted. Every newly imported publication also gets a news item.
"""

from __future__ import annotations

import argparse
from datetime import date
from difflib import SequenceMatcher
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


PROFILE_ID = "f_rtYCAAAAAJ"
PROFILE_URL = "https://scholar.google.com/citations"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


class ScholarProfileParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.works: list[dict[str, str]] = []
        self.current: dict[str, str] | None = None
        self.capture: tuple[str, str] | None = None
        self.buffer: list[str] = []
        self.gray_index = 0

    @staticmethod
    def _classes(attrs: list[tuple[str, str | None]]) -> set[str]:
        value = dict(attrs).get("class") or ""
        return set(value.split())

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = self._classes(attrs)
        attr_map = dict(attrs)
        if tag == "tr" and "gsc_a_tr" in classes:
            self.current = {}
            self.gray_index = 0
        elif self.current is not None and tag == "a" and "gsc_a_at" in classes:
            self.capture = (tag, "title")
            self.buffer = []
            self.current["url"] = urljoin(PROFILE_URL, attr_map.get("href") or "")
        elif self.current is not None and tag == "div" and "gs_gray" in classes:
            key = "authors" if self.gray_index == 0 else "venue"
            self.gray_index += 1
            self.capture = (tag, key)
            self.buffer = []
        elif self.current is not None and tag == "span" and (
            "gsc_a_y" in classes or "gsc_a_h" in classes
        ):
            self.capture = (tag, "year")
            self.buffer = []

    def handle_data(self, data: str) -> None:
        if self.capture is not None:
            self.buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.capture is not None and tag == self.capture[0]:
            if self.current is not None:
                value = html.unescape(" ".join(self.buffer)).strip()
                value = re.sub(r"\s+", " ", value)
                self.current[self.capture[1]] = value
            self.capture = None
            self.buffer = []
        if tag == "tr" and self.current is not None:
            if self.current.get("title"):
                self.works.append(self.current)
            self.current = None


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def slugify(value: str) -> str:
    slug = normalize_title(value).replace(" ", "-")
    return slug[:72].strip("-") or "publication"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def existing_titles(root: Path) -> set[str]:
    titles: set[str] = set()
    pattern = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
    for source in (root / "content" / "publication").glob("**/index.md"):
        match = pattern.search(source.read_text(encoding="utf-8"))
        if not match:
            continue
        raw = match.group(1).strip()
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
            raw = raw[1:-1]
        titles.add(normalize_title(raw.replace("''", "'")))
    return titles


def matches_existing_title(title: str, known: set[str]) -> bool:
    normalized = normalize_title(title)
    if normalized in known:
        return True
    title_tokens = set(normalized.split())
    for existing in known:
        ratio = SequenceMatcher(None, normalized, existing).ratio()
        existing_tokens = set(existing.split())
        union = title_tokens | existing_tokens
        overlap = len(title_tokens & existing_tokens) / len(union) if union else 0
        if ratio >= 0.88 or overlap >= 0.84:
            return True
    return False


def parse_authors(value: str) -> list[str]:
    authors = [part.strip() for part in value.split(",") if part.strip()]
    mapped: list[str] = []
    for author in authors:
        normalized = normalize_title(author)
        if re.search(r"\b(s|samuel) hurault\b", normalized) or normalized.startswith("hurault s"):
            mapped.append("admin")
        else:
            mapped.append(author)
    return mapped or ["admin"]


def fetch_page(profile_id: str, start: int) -> str:
    query = urlencode(
        {"user": profile_id, "hl": "en", "pagesize": 100, "cstart": start, "sortby": "pubdate"}
    )
    request = Request(f"{PROFILE_URL}?{query}", headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        raise RuntimeError(f"Google Scholar returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach Google Scholar: {exc.reason}") from exc


def fetch_works(profile_id: str) -> list[dict[str, str]]:
    works: list[dict[str, str]] = []
    for start in range(0, 1000, 100):
        parser = ScholarProfileParser()
        parser.feed(fetch_page(profile_id, start))
        if not parser.works:
            break
        works.extend(parser.works)
        if len(parser.works) < 100:
            break
    if not works:
        raise RuntimeError(
            "No publications were found. Check that the Scholar profile is public, "
            "or retry later if Google temporarily blocked the request."
        )
    return works


def unique_bundle_path(parent: Path, title: str) -> Path:
    base = f"scholar-{slugify(title)}"
    candidate = parent / base
    if not candidate.exists():
        return candidate
    digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:8]
    return parent / f"{base}-{digest}"


def publication_markdown(work: dict[str, str], year: int, scholar_key: str) -> str:
    authors = parse_authors(work.get("authors", ""))
    author_lines = "\n".join(f"  - {yaml_string(author)}" for author in authors)
    venue = re.sub(r"\s+,", ",", work.get("venue", ""))
    arxiv_match = re.search(r"arXiv:\s*(\d{4}\.\d{4,5})", venue, re.IGNORECASE)
    pdf_url = f"https://arxiv.org/pdf/{arxiv_match.group(1)}" if arxiv_match else ""
    return f"""---
title: {yaml_string(work['title'])}
authors:
{author_lines}
date: {yaml_string(f'{year}-01-01')}
publishDate: {yaml_string(f'{year}-01-01')}
publication_types: ['3']
publication: {yaml_string(venue)}
publication_short: ''
abstract: ''
featured: false
url_pdf: {yaml_string(pdf_url)}
url_code: ''
url_scholar: {yaml_string(work.get('url', ''))}
scholar_key: {yaml_string(scholar_key)}
scholar_imported: true
---
"""


def news_markdown(work: dict[str, str], publication_path: str, synced_on: date) -> str:
    title = f"New publication: {work['title']}"
    summary = "A new publication has been added from Samuel Hurault's Google Scholar profile."
    return f"""---
title: {yaml_string(title)}
date: {yaml_string(synced_on.isoformat())}
summary: {yaml_string(summary)}
publication_url: {yaml_string(publication_path)}
scholar_imported: true
---

{summary}
"""


def load_seen(root: Path) -> set[str]:
    state_path = root / "data" / "scholar-sync.json"
    if not state_path.exists():
        return set()
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(f"Could not read {state_path}: {exc}") from exc
    return set(data.get("seen", []))


def save_seen(root: Path, seen: set[str], profile_id: str) -> None:
    state_path = root / "data" / "scholar-sync.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "profile_id": profile_id,
                "last_checked_month": date.today().strftime("%Y-%m"),
                "seen": sorted(seen),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def sync(
    root: Path,
    works: list[dict[str, str]],
    profile_id: str,
    dry_run: bool = False,
    initialize: bool = False,
    since_year: int | None = None,
) -> int:
    publication_root = root / "content" / "publication"
    news_root = root / "content" / "news"
    known = existing_titles(root)
    seen = load_seen(root)
    created = 0
    today = date.today()

    for work in works:
        title = work.get("title", "").strip()
        year_match = re.search(r"(?:19|20)\d{2}", work.get("year", ""))
        scholar_key = work.get("url", "").strip() or normalize_title(title)
        if not title or not year_match or scholar_key in seen:
            continue

        year = int(year_match.group())
        if matches_existing_title(title, known) or (
            initialize and since_year is not None and year < since_year
        ):
            seen.add(scholar_key)
            continue

        publication_bundle = unique_bundle_path(publication_root, title)
        news_bundle = unique_bundle_path(news_root, title)
        relative_publication = f"/publication/{publication_bundle.name}/"

        print(f"Importing: {title} ({year})")
        if not dry_run:
            publication_bundle.mkdir(parents=True, exist_ok=False)
            news_bundle.mkdir(parents=True, exist_ok=False)
            (publication_bundle / "index.md").write_text(
                publication_markdown(work, year, scholar_key), encoding="utf-8"
            )
            (news_bundle / "index.md").write_text(
                news_markdown(work, relative_publication, today), encoding="utf-8"
            )
        known.add(normalize_title(title))
        seen.add(scholar_key)
        created += 1

    if not dry_run:
        save_seen(root, seen, profile_id)
    print(f"Scholar sync complete: {created} new publication(s).")
    return created


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-id", default=PROFILE_ID)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--initialize", action="store_true")
    parser.add_argument("--since-year", type=int)
    args = parser.parse_args()

    try:
        works = fetch_works(args.profile_id)
        sync(
            args.root.resolve(),
            works,
            args.profile_id,
            args.dry_run,
            args.initialize,
            args.since_year,
        )
    except RuntimeError as exc:
        print(f"Scholar sync failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
