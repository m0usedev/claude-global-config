#!/usr/bin/env python3
"""Remove the symlinks in ~/.local/bin created by install.py for scripts in tools/."""
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent / "tools"
BIN_DIR = Path.home() / ".local" / "bin"


def main():
    scripts = sorted(TOOLS_DIR.glob("*.py"))
    if not scripts:
        print(f"No scripts found in {TOOLS_DIR}")
        return

    for script in scripts:
        link = BIN_DIR / script.stem

        if not link.exists() and not link.is_symlink():
            print(f"Skipping {link}: not found.")
            continue

        if not link.is_symlink():
            print(f"Skipping {link}: not a symlink, leaving it alone.")
            continue

        if link.resolve() != script.resolve():
            print(f"Skipping {link}: points elsewhere ({link.resolve()}), leaving it alone.")
            continue

        link.unlink()
        print(f"Removed {link}")

    print("\nDone.")


if __name__ == "__main__":
    main()
