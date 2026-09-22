"""Protected negative controls. These are examples, not a production application."""
from __future__ import annotations

import sqlite3
from pathlib import Path

RECORDS = {"one": ("alice", "ALICE_TEST_RECORD"), "two": ("bob", "BOB_TEST_RECORD")}


def record(record_id: str, principal: str) -> str:
    """Only the owning authenticated principal can read a record."""
    owner, value = RECORDS[record_id]
    if principal != owner:
        raise PermissionError("Not permitted")
    return value


def search(query: str) -> list[str]:
    """User input is bound as a SQL value, never query syntax."""
    with sqlite3.connect(":memory:") as connection:
        connection.execute("CREATE TABLE items (name TEXT)")
        connection.executemany("INSERT INTO items VALUES (?)", [("apple",), ("banana",)])
        rows = connection.execute("SELECT name FROM items WHERE name = ?", (query,))
        return [row[0] for row in rows.fetchall()]


def download(root: Path, requested: str) -> str:
    """Contain requested paths; root must be trusted application configuration.

    This helper does not authorize a caller-supplied root. The independent
    evaluation deliberately tests that different contract as a separate finding.
    """
    root = root.resolve()
    selected = (root / requested).resolve()
    if not selected.is_relative_to(root):
        raise PermissionError("Not permitted")
    return selected.read_text(encoding="utf-8")
