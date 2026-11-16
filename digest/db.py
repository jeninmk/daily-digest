"""SQLite storage: remembers every article we've seen so nothing is sent twice."""

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("digest.db")

_SCHEMA = """CREATE TABLE IF NOT EXISTS articles (
    url TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    source TEXT NOT NULL,
    interest TEXT NOT NULL,
    published TEXT,
    seen_at TEXT NOT NULL
);"""


@dataclass
class Article:
    url: str
    title: str
    source: str
    interest: str
    published: str | None


class Store:
    def __init__(self, path: Path = DB_PATH) -> None:
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)

    def add_new(self, articles: list[Article]) -> list[Article]:
        """Insert articles, skipping URLs already seen. Returns only the new ones."""
        fresh: list[Article] = []
        now = datetime.now(timezone.utc).isoformat()
        with self._conn:
            for a in articles:
                cur = self._conn.execute(
                    "INSERT OR IGNORE INTO articles VALUES (?,?,?,?,?,?)",
                    (a.url, a.title, a.source, a.interest, a.published, now),
                )
                if cur.rowcount:
                    fresh.append(a)
        return fresh

    def count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]

    def close(self) -> None:
        self._conn.close()
