#!/usr/bin/env python3
import os
import sys
from pathlib import Path

venv_python = os.path.join(os.path.dirname(os.path.realpath(__file__)), "venv", "bin", "python3")

if os.path.exists(venv_python) and sys.executable != venv_python:
    os.execv(venv_python, [venv_python] + sys.argv)


def main():
    claude_dir = Path.home() / ".claude"

    try:
        os.execvp("code", ["code", str(claude_dir)])
    except FileNotFoundError:
        print(
            "Error: 'code' command not found. Install the VS Code CLI "
            "(Command Palette > Shell Command: Install 'code' command in PATH).",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
