"""Copy the reverse-engineering toolkit and notes from the local workspace into this repo's re/ folder.

Only code and notes travel: nothing read from a ROM. ROM-derived outputs live under the workspace's games/, build/
and trace/ folders, which are skipped here and ignored by .gitignore anyway.

    python re/sync_from_workspace.py            # copy and list what changed
    python re/sync_from_workspace.py --check    # list only
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

WORKSPACE = Path(r"C:\Users\aaron\Documents\UnboundHack")
HERE = Path(__file__).resolve().parent

# (workspace path, repo path under re/). Directories are copied recursively with the filters below.
ITEMS = [
    ("gbax", "gbax"),
    ("notes", "notes"),
    ("tools", "tools"),
    ("reports", "reports"),
    ("PROCEDURE.md", "PROCEDURE.md"),
    ("README.md", "UNBOUNDHACK_README.md"),
]

SKIP_DIRS = {"__pycache__", "out", "build", "games", "external", "apps", "ghidra", "trace", ".venv", ".pytest_cache"}
KEEP_SUFFIXES = {".py", ".md", ".txt", ".json", ".csv", ".sh", ".ps1", ".toml", ".cfg", ".ini", ".yaml", ".yml", ".c", ".h"}
MAX_BYTES = 2 * 1024 * 1024


def wanted(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.suffix.lower() not in KEEP_SUFFIXES:
        return False
    return path.stat().st_size <= MAX_BYTES


def sync(check_only: bool) -> int:
    changed: list[str] = []
    for src_name, dst_name in ITEMS:
        src = WORKSPACE / src_name
        dst = HERE / dst_name
        if not src.exists():
            print(f"missing in workspace: {src}", file=sys.stderr)
            continue
        files = [src] if src.is_file() else [p for p in src.rglob("*") if p.is_file()]
        for f in files:
            if not wanted(f):
                continue
            target = dst if src.is_file() else dst / f.relative_to(src)
            if target.exists() and filecmp.cmp(f, target, shallow=False):
                continue
            changed.append(str(target.relative_to(HERE)))
            if not check_only:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)
    for line in sorted(changed):
        print(("would copy " if check_only else "copied ") + line)
    print(f"{len(changed)} file(s) {'to copy' if check_only else 'copied'}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="list the files that would change, copy nothing")
    sys.exit(sync(ap.parse_args().check))
