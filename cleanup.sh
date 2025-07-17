#!/bin/bash
echo "Cleaning Python cache and venv..."
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
rm -rf .venv
echo "Done."
# python3 -m venv .venv
# source .venv/bin/activate
# pip install -r requirements.txt
# pip install -r examples/dev-requirements.txt
