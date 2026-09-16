#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python main.py web --host 127.0.0.1 --port 8000
