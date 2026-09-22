from pathlib import Path

import pytest

from scripts.install_skill import SOURCE, install


def test_standalone_install_is_complete(tmp_path: Path) -> None:
    target = install(tmp_path / ".claude/skills")
    for file in SOURCE.rglob("*"):
        if file.is_file():
            assert (target / file.relative_to(SOURCE)).read_bytes() == file.read_bytes()
    assert not (target / ".claude-plugin").exists()
    assert (target / "LICENSE").exists()
    assert (target / "NOTICE").exists()


def test_existing_install_is_preserved(tmp_path: Path) -> None:
    target = install(tmp_path)
    marker = target / "local-note.md"
    marker.write_text("keep this", encoding="utf-8")
    with pytest.raises(FileExistsError):
        install(tmp_path)
    assert marker.read_text(encoding="utf-8") == "keep this"


def test_recursive_destination_rejected(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "SKILL.md").write_text("skill", encoding="utf-8")
    with pytest.raises(ValueError, match="outside"):
        install(source / "nested", source=source)


def test_invalid_source_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="SKILL.md"):
        install(tmp_path / "dest", source=tmp_path)
