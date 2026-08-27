#!/usr/bin/env python3
import os
import sys

venv_python = os.path.join(os.path.dirname(os.path.realpath(__file__)), "venv", "bin", "python3")

if os.path.exists(venv_python) and sys.executable != venv_python:
    os.execv(venv_python, [venv_python] + sys.argv)

import questionary


def main():
  choice = questionary.select(
    "What do you want to do?",
    choices=["Say hello", "Say goodbye"],
  ).ask()

  if choice == "Say hello":
    print("hello world!")
  elif choice == "Say goodbye":
    print("goodbye world!")


if __name__ == '__main__':
  main()