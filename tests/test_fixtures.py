from pathlib import Path

import pytest

from evals.fixtures.safe import app as safe
from evals.fixtures.vulnerable import app as vulnerable


@pytest.mark.parametrize("app", [safe, vulnerable])
def test_legitimate_owner_access(app: object) -> None:
    if app is safe:
        assert safe.record("one", "alice") == "ALICE_TEST_RECORD"
    else:
        assert vulnerable.record("one", "alice") == "ALICE_TEST_RECORD"


@pytest.mark.parametrize("principal", ["alice", ""])
def test_cross_identity_controls(principal: str) -> None:
    assert vulnerable.record("two", principal) == "BOB_TEST_RECORD"
    with pytest.raises(PermissionError):
        safe.record("two", principal)


@pytest.mark.parametrize("query", ["' OR '1'='1", "' OR 2=2 --"])
def test_sql_alternate_payloads(query: str) -> None:
    assert vulnerable.search(query) == ["apple", "banana"]
    assert safe.search(query) == []


def test_sql_legitimate_and_negative_controls() -> None:
    for query, expected in [("apple", ["apple"]), ("missing", [])]:
        assert safe.search(query) == vulnerable.search(query) == expected


def test_file_escape_and_alternate_absolute_path(tmp_path: Path) -> None:
    public = tmp_path / "public"
    public.mkdir()
    (public / "hello.txt").write_text("PUBLIC_TEST_DATA", encoding="utf-8")
    private = tmp_path / "private.txt"
    private.write_text("PRIVATE_SYNTHETIC_MARKER", encoding="utf-8")
    assert safe.download(public, "hello.txt") == "PUBLIC_TEST_DATA"
    assert vulnerable.download(public, "hello.txt") == "PUBLIC_TEST_DATA"
    for requested in ("../private.txt", str(private.resolve())):
        assert vulnerable.download(public, requested) == "PRIVATE_SYNTHETIC_MARKER"
        with pytest.raises(PermissionError):
            safe.download(public, requested)


def test_path_prefix_collision(tmp_path: Path) -> None:
    public = tmp_path / "public"
    sibling = tmp_path / "public-other"
    public.mkdir()
    sibling.mkdir()
    (sibling / "data.txt").write_text("SIBLING_MARKER", encoding="utf-8")
    with pytest.raises(PermissionError):
        safe.download(public, "../public-other/data.txt")


def test_nonexistent_input_is_not_a_security_pass(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        safe.download(tmp_path, "missing")
