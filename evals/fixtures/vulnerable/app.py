"""Deliberately vulnerable functions. Use only synthetic isolated evaluation data."""
from __future__ import annotations

import sqlite3
from pathlib import Path

RECORDS = {"one": ("alice", "ALICE_TEST_RECORD"), "two": ("bob", "BOB_TEST_RECORD")}


def record(record_id: str, principal: str) -> str:
    """Return a record; the caller supplies an already authenticated principal."""
    return RECORDS[record_id][1]


def search(query: str) -> list[str]:
    """Search an ephemeral database containing only synthetic records."""
    with sqlite3.connect(":memory:") as connection:
        connection.execute("CREATE TABLE items (name TEXT)")
        connection.executemany("INSERT INTO items VALUES (?)", [("apple",), ("banana",)])
        sql = f"SELECT name FROM items WHERE name = '{query}'"
        return [row[0] for row in connection.execute(sql).fetchall()]


def download(root: Path, requested: str) -> str:
    """Read a UTF-8 fixture file relative to the public directory."""
    return (root / requested).read_text(encoding="utf-8")
