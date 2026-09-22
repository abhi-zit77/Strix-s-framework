import json
import shutil
from pathlib import Path

from scripts.validate_package import ROOT, markdown_links, validate


def test_complete_package() -> None:
    assert validate() == []


def test_fenced_examples_are_not_file_links() -> None:
    text = "[real](real.md)\n```md\n[example](missing.md)\n```\n[next](next.md)"
    assert markdown_links(text) == ["real.md", "next.md"]


def test_inline_code_is_not_a_file_link() -> None:
    text = "Call `lookup[key](...)`; ``literal ` [example](missing)``; [real](real.md)"
    assert markdown_links(text) == ["real.md"]


def test_missing_reference_fails_validation(tmp_path: Path) -> None:
    package = tmp_path / "package"
    shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns(".git", ".*cache"))
    reference = package / (
        "plugins/strix-framewok/skills/strix-framewok/references/vulnerabilities--idor.md"
    )
    reference.unlink()
    errors = validate(package)
    assert any("Missing reference: vulnerabilities/idor" in error for error in errors)


def test_standalone_dependency_escape_is_rejected(tmp_path: Path) -> None:
    package = tmp_path / "package"
    shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns(".git", ".*cache"))
    reference = package / "plugins/strix-framewok/skills/strix-framewok/references/escape.md"
    reference.write_text("[outside](../../../../README.md)\n", encoding="utf-8")
    assert any("local link" in error or "dependency" in error for error in validate(package))


def test_empty_marketplace_is_reported_without_crashing(tmp_path: Path) -> None:
    package = tmp_path / "package"
    shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns(".git", ".*cache"))
    path = package / ".claude-plugin/marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["plugins"] = []
    path.write_text(json.dumps(data), encoding="utf-8")
    assert "Expected one canonical plugin" in validate(package)
