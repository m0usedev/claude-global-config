#!/usr/bin/env python3
import os
import subprocess
import sys

venv_python = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "venv", "bin", "python3"))

if os.path.exists(venv_python) and sys.executable != venv_python:
    os.execv(venv_python, [venv_python] + sys.argv)

LINKS = [
    "https://www.zerogpt.com/grammar-checker",
    "https://translate.google.com/?hl=es&sl=en&tl=es&op=translate",
]


def open_url(url):
    # WSL has no browser of its own; hand the URL to Windows, whose "start"
    # opens it as a new tab in the existing browser window.
    subprocess.run(
        ["cmd.exe", "/c", "start", "", url],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main():
    for url in LINKS:
        open_url(url)


if __name__ == '__main__':
    main()
