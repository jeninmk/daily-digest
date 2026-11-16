"""Fetch RSS feeds for the user's interests and store new articles."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import feedparser
import yaml

from digest.db import Article, Store
from digest.profile import Profile

SOURCES_PATH = Path("sources.yaml")
MAX_ENTRIES_PER_FEED = 10


def load_sources(path: Path = SOURCES_PATH) -> dict[str, list[dict[str, str]]]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _iso(parsed_time: Any) -> str | None:
    if parsed_time is None:
        return None
    return datetime(*parsed_time[:6], tzinfo=timezone.utc).isoformat()


def fetch_feed(name: str, feed: str, interest: str) -> list[Article]:
    """Fetch one feed. `feed` may be a URL or raw XML (useful for tests)."""
    articles: list[Article] = []
    for e in feedparser.parse(feed).entries[:MAX_ENTRIES_PER_FEED]:
        link, title = e.get("link"), e.get("title")
        if not link or not title:
            continue
        articles.append(
            Article(
                url=link,
                title=title.strip(),
                source=name,
                interest=interest,
                published=_iso(e.get("published_parsed")),
            )
        )
    return articles


def ingest(profile: Profile, store: Store, sources_path: Path = SOURCES_PATH) -> dict[str, int]:
    """Fetch all feeds for the profile's interests; store new articles. Returns new counts."""
    sources = load_sources(sources_path)
    counts: dict[str, int] = {}
    for interest in profile.interests:
        fresh: list[Article] = []
        for f in sources.get(interest.name, []):
            fresh.extend(fetch_feed(f["name"], f["url"], interest.name))
        counts[interest.name] = len(store.add_new(fresh))
    return counts
