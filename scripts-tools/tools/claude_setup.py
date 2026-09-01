#!/usr/bin/env python3
import os
import sys

venv_python = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "venv", "bin", "python3"))

if os.path.exists(venv_python) and sys.executable != venv_python:
    os.execv(venv_python, [venv_python] + sys.argv)

MODES = {
    "super-easy": {
        "env": {"MAX_THINKING_TOKENS": "0"},
        "args": ["claude", "--permission-mode", "plan", "--model", "sonnet", "--effort", "medium"],
    },
    "easy": {
        "env": {"MAX_THINKING_TOKENS": "0"},
        "args": ["claude", "--permission-mode", "plan", "--model", "sonnet", "--effort", "high"],
    },
    "normal": {
        "env": {},
        "args": ["claude", "--permission-mode", "plan", "--model", "opus", "--effort", "medium"],
    },
    "hard": {
        "env": {},
        "args": ["claude", "--permission-mode", "plan", "--model", "opus", "--effort", "high"],
    },
}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in MODES:
        print(f"Usage: {os.path.basename(sys.argv[0])} <{'|'.join(MODES)}>", file=sys.stderr)
        sys.exit(1)

    mode = MODES[sys.argv[1]]
    env = {**os.environ, **mode["env"]}
    os.execvpe(mode["args"][0], mode["args"], env)


if __name__ == '__main__':
    main()
