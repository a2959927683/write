#!/usr/bin/env python3
"""Install repository-local Git guardrails for this checkout."""

from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> str:
    result = subprocess.run(
        list(args),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f"Command failed: {' '.join(args)}")
    return result.stdout.strip()


def make_executable(path: Path) -> None:
    if os.name == "nt":
        return
    current = path.stat().st_mode
    path.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main() -> int:
    hooks_dir = ROOT / ".githooks"
    if not hooks_dir.exists():
        raise SystemExit(".githooks directory is missing")

    for hook in ("pre-commit", "commit-msg"):
        hook_path = hooks_dir / hook
        if not hook_path.exists():
            raise SystemExit(f"Missing hook: {hook_path}")
        make_executable(hook_path)

    run("git", "config", "core.hooksPath", ".githooks")
    run("git", "config", "gc.reflogExpire", "90.days")
    run("git", "config", "gc.reflogExpireUnreachable", "90.days")

    print("Git guard installed.")
    print("core.hooksPath=.githooks")
    print("gc.reflogExpire=90.days")
    print("gc.reflogExpireUnreachable=90.days")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
