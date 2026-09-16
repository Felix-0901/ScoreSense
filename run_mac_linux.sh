#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
.venv/bin/python main.py web --host 127.0.0.1 --port 8000
