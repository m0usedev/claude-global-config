#!/usr/bin/env python3
"""Symlink every script in tools/ into ~/.local/bin so it's runnable from anywhere."""
import os
import stat
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent / "tools"
BIN_DIR = Path.home() / ".local" / "bin"


def main():
    BIN_DIR.mkdir(parents=True, exist_ok=True)

    scripts = sorted(TOOLS_DIR.glob("*.py"))
    if not scripts:
        print(f"No scripts found in {TOOLS_DIR}")
        return

    for script in scripts:
        script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        link = BIN_DIR / script.stem

        if link.is_symlink():
            link.unlink()
        elif link.exists():
            print(f"Skipping {link}: file already exists and is not a symlink.")
            continue

        link.symlink_to(script)
        print(f"Linked {link} -> {script}")

    print(f"\nDone. Make sure {BIN_DIR} is in your PATH.")


if __name__ == "__main__":
    main()
