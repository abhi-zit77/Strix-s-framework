"""Copy the self-contained skill into an explicitly chosen skills directory."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

NAME = "strix-framewok"
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins" / NAME / "skills" / NAME


def install(skills_dir: Path, source: Path = SOURCE) -> Path:
    """Install without overwriting, deleting, or editing host configuration."""
    source = source.resolve(strict=True)
    if not (source / "SKILL.md").is_file():
        raise ValueError("Source does not contain SKILL.md")
    if any(path.is_symlink() for path in source.rglob("*")):
        raise ValueError("Skill source must not contain symlinks")
    target = skills_dir.expanduser().resolve() / NAME
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Refusing to overwrite existing installation: {target}")
    if target.is_relative_to(source) or source.is_relative_to(target):
        raise ValueError("Install destination must be outside the source skill")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        target = install(args.skills_dir)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Installation failed: {exc}\n")
    print(f"Installed {NAME} at {target}")
    print("Claude standalone: /strix-framewok | Codex: $strix-framewok")


if __name__ == "__main__":
    main()
