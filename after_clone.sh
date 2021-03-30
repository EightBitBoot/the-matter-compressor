#!/bin/bash

git update-index --skip-worktree network.json

python3 -m venv .env && source .env/bin/activate && pip install -r requirements.txt