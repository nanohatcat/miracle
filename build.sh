#!/bin/bash
set -e

python -m venv .venv
source .venv/bin/activate

pip install pyinstaller

export TERM=xterm-256color

pyinstaller --onefile main.py

echo "done → dist/main"
