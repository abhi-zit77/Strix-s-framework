"""Validate packaging, reference reachability, attribution and pinned coverage."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, cast
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME = "strix-framewok"
SHA = "56e9ae982c2fdd00c7c0b9afc49af035470dd310"
EXPECTED = {
    "analysis": 4, "cloud": 4, "coordination": 2, "custom": 4,
    "frameworks": 4, "protocols": 2, "reconnaissance": 2,
    "scan_modes": 4, "technologies": 7, "tooling": 13, "vulnerabilities": 29,
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return cast(dict[str, Any], value)


def markdown_links(text: str) -> list[str]:
    """Extract local file links outside fenced examples and inline code."""
    plain: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match[1][0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            plain.append(line)
    prose = re.sub(r"(`+)(?!`)(.*?)(?<!`)\1(?!`)", "", "\n".join(plain), flags=re.S)
    return re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", prose)


def validate(root: Path = ROOT, upstream: Path | None = None) -> list[str]:
    root = root.resolve()
    plugin = root / "plugins" / NAME
    skill = plugin / "skills" / NAME
    problems: list[str] = []

    def require(ok: bool, message: str) -> None:
        if not ok:
            problems.append(message)

    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        return ["Missing skill frontmatter"]
    front = yaml.safe_load(match[1])
    if not isinstance(front, dict):
        return ["Skill frontmatter must be a mapping"]
    require(front.get("name") == NAME, "Skill name differs from requested invocation")
    description = front.get("description", "")
    require(isinstance(description, str) and 0 < len(description) <= 1024,
            "Invalid skill description")
    require(len(text.splitlines()) < 500, "Entrypoint exceeds progressive-disclosure limit")
    require("[TODO:" not in text, "Unfinished scaffold in skill")
    require(front.get("metadata", {}).get("version") == "1.0.0", "Skill version mismatch")

    for host in ("claude", "codex"):
        manifest = read_json(plugin / f".{host}-plugin/plugin.json")
        require(manifest.get("name") == NAME, f"{host} plugin name mismatch")
        require(manifest.get("version") == "1.0.0", f"{host} plugin version mismatch")
        require(manifest.get("license") == "Apache-2.0", f"{host} plugin license missing")
    claude = read_json(root / ".claude-plugin/marketplace.json")
    codex = read_json(root / ".agents/plugins/marketplace.json")
    for market in (claude, codex):
        require(market.get("name") == "strix-framework", "Marketplace name mismatch")
        entries = market.get("plugins")
        if not isinstance(entries, list) or len(entries) != 1:
            problems.append("Expected one canonical plugin")
            return problems
        entry = entries[0]
        if not isinstance(entry, dict):
            problems.append("Marketplace plugin must be an object")
            return problems
        require(entry.get("name") == NAME, "Marketplace plugin name mismatch")
        source = entry.get("source")
        path = source.get("path") if isinstance(source, dict) else source
        require(path == f"./plugins/{NAME}", "Marketplace source path mismatch")
    require(bool(claude.get("owner", {}).get("name")), "Claude marketplace owner missing")
    policy = codex["plugins"][0].get("policy", {})
    require(policy.get("installation") == "AVAILABLE", "Codex install policy mismatch")
    require(policy.get("authentication") == "ON_INSTALL", "Codex auth policy mismatch")
    metadata = yaml.safe_load((skill / "agents/openai.yaml").read_text(encoding="utf-8"))
    require(metadata.get("policy", {}).get("allow_implicit_invocation") is True,
            "Skill discovery policy mismatch")
    require(f"${NAME}" in metadata.get("interface", {}).get("default_prompt", ""),
            "Codex invocation missing from default prompt")

    inventory = read_json(root / "docs/upstream-inventory.json")
    require(inventory.get("commit") == SHA, "Upstream revision drift")
    rows = inventory.get("internal", [])
    require(len(rows) == 75 and inventory.get("internal_count") == 75,
            "Incomplete internal inventory")
    require(len(inventory.get("external", [])) == 9, "Incomplete external skill mapping")
    require(len({row["id"] for row in rows}) == len(rows), "Duplicate inventory ID")
    counts: dict[str, int] = {}
    for row in rows:
        category = row["id"].split("/")[0]
        counts[category] = counts.get(category, 0) + 1
        destination = (root / row["destination"]).resolve()
        require(destination.is_relative_to(skill), "Reference escapes skill package")
        require(destination.is_file(), f"Missing reference: {row['id']}")
        if destination.is_file():
            body = destination.read_text(encoding="utf-8")
            require(row["source_url"] in body and SHA in body,
                    f"Missing attribution: {row['id']}")
            require("Adapted and modified" in body, f"Missing change notice: {row['id']}")
        require(f"references/{destination.name}" in text,
                f"Reference not reachable from entrypoint: {row['id']}")
        if upstream is not None:
            raw = upstream / row["source"]
            require(raw.is_file(), f"Missing upstream source: {row['id']}")
            if raw.is_file():
                require(hashlib.sha256(raw.read_bytes()).hexdigest() == row["upstream_sha256"],
                        f"Upstream source hash mismatch: {row['id']}")
    require(counts == EXPECTED, "Playbook categories differ from pinned inventory")
    if upstream is not None:
        for external in inventory.get("external", []):
            raw = upstream / external["source"]
            require(raw.is_file(), f"Missing upstream consumer skill: {external['source']}")
            if raw.is_file():
                require(hashlib.sha256(raw.read_bytes()).hexdigest() == external["upstream_sha256"],
                        f"Upstream consumer hash mismatch: {external['source']}")
    catalog = read_json(skill / "assets/test-catalog.json")
    require({row["id"] for row in catalog.get("playbooks", [])} ==
            {row["id"] for row in rows}, "Catalog/inventory mismatch")

    for directory in (root, plugin, skill):
        for filename in ("LICENSE", "NOTICE"):
            require((directory / filename).is_file(), f"Missing {filename} at {directory}")
    for file in skill.rglob("*"):
        require(not file.is_symlink(), f"Skill contains symlink: {file}")
    for file in root.rglob("*.md"):
        if any(part.startswith(".") for part in file.relative_to(root).parts):
            continue
        body = file.read_text(encoding="utf-8")
        for link in markdown_links(body):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", link) or link.startswith("#"):
                continue
            target = (file.parent / unquote(link.split("#")[0])).resolve()
            require(target.is_relative_to(root) and target.exists(),
                    f"Broken/outside local link: {file.relative_to(root)} -> {link}")
            if file.is_relative_to(skill):
                require(target.is_relative_to(skill), f"Standalone skill dependency: {link}")
    for asset in (skill / "assets").glob("*.json"):
        read_json(asset)
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path)
    args = parser.parse_args()
    try:
        problems = validate(upstream=args.upstream)
    except (
        OSError, KeyError, IndexError, AttributeError, TypeError, ValueError, yaml.YAMLError,
    ) as exc:
        parser.exit(1, f"Package validation failed: {exc}\n")
    if problems:
        parser.exit(1, "\n".join(problems) + "\n")
    print("Package valid: 75 playbooks, 9 mappings, standalone references, both host manifests.")


if __name__ == "__main__":
    main()
