#!/bin/bash
cd "$(dirname "$0")/.."
pwd
./.venv/bin/python3 market-sentiment-check.py
