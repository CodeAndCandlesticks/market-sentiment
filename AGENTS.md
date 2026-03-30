# AGENTS.md

## Purpose
This repository fetches the latest Schwab market-open article, classifies the day's sentiment with an LLM, records the result in `market_sentiment.csv`, and optionally sends a Pushover notification.

Use this file as the baseline guide for contributors and agents making changes in this repo.

## Project Snapshot
- Language: Python
- Runtime: local `.venv` Python environment
- Main entrypoint: `market-sentiment-check.py`
- Convenience runner: `scripts/run_market_sentiment.sh`
- Primary outputs:
  - `market_sentiment.csv`
  - `market_sentiment_debug.log`
  - `article.log`
  - `article_html.log`

## Repo Layout
- `market-sentiment-check.py`: Main script for fetching, parsing, classifying, logging, and notifying.
- `scripts/run_market_sentiment.sh`: Shell wrapper that runs the script from the repo root using `.venv`.
- `market_sentiment.csv`: Historical sentiment log.
- `images/`: Project assets.
- `README.md`: End-user setup and usage notes.
- `CHANGELOG.md`: Release history.
- `requirements.txt`: Python dependencies.

## Setup Expectations
- Create and use a local virtual environment at `.venv`.
- Install dependencies with `pip install -r requirements.txt`.
- Store secrets in `.env`. Do not hardcode API keys or notification credentials.
- Keep `.env` out of version control. `.gitignore` already includes it.

Recommended bootstrap:

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

## Required Environment Variables
- `USE_MODEL`: `openai` or `anthropic`
- `OPENAI_API_KEY`: required when `USE_MODEL=openai`
- `ANTHROPIC_API_KEY`: required when `USE_MODEL=anthropic`
- `PUSHOVER_USER_KEY`: optional unless notifications are expected
- `PUSHOVER_API_TOKEN`: optional unless notifications are expected
- `LOG_LEVEL`: optional, defaults to `INFO`

Example:

```env
USE_MODEL=anthropic
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=
PUSHOVER_USER_KEY=...
PUSHOVER_API_TOKEN=...
LOG_LEVEL=INFO
```

## Common Commands
- Run directly:

```bash
./.venv/bin/python3 market-sentiment-check.py
```

- Run via helper script:

```bash
bash scripts/run_market_sentiment.sh
```

## Output and Artifact Rules
- Treat `market_sentiment.csv` as a durable artifact. Preserve existing rows unless the script is intentionally changing log format.
- The script currently overwrites or appends by `today_date`, so schema changes must be handled carefully.
- `market_sentiment_debug.log`, `article.log`, and `article_html.log` are generated runtime artifacts and should not be relied on as source-of-truth documentation.
- If you add new generated outputs, update `.gitignore`, `README.md`, and this file.

## Contributor Guidelines
- Prefer small, targeted edits. This repo is currently a single-script project.
- Maintain compatibility with the existing `.env` workflow unless there is a strong reason to introduce a config file.
- Keep failure handling partial-success friendly. If one step fails, avoid losing already-fetched or already-computed outputs.
- Prefer `logging` over ad hoc file writes if you are refactoring observability behavior.
- Update `CHANGELOG.md` for meaningful behavior changes.
- Keep `README.md` aligned with actual filenames, models, and outputs.

## Known Sharp Edges
- `README.md` references `market_sentiment_checker.py`, but the actual script is `market-sentiment-check.py`.
- The code logs with a custom `log_message()` helper rather than Python's `logging` module.
- Generated files `article.log` and `article_html.log` are not called out in `.gitignore`.
- `extract_publish_datetime()` writes `"ERROR"` messages, but the current log level map does not define an `ERROR` level.
- Runtime behavior depends on the external Schwab page structure and current model SDK behavior, so changes should be tested carefully.

## When Making Changes
- If you change environment variables, update `README.md`, this file, and `.env` examples together.
- If you change CSV columns, document the migration or compatibility impact clearly.
- If you change the model provider integration, verify both dependency requirements and response parsing.
- If you add tests, keep them lightweight and avoid introducing unnecessary framework complexity.

## Definition of Done
- The script still runs from the repo root.
- `.env`-based setup still works.
- README instructions match the real commands and filenames.
- `CHANGELOG.md` reflects user-visible changes.
- Generated artifacts and secrets remain out of version control.
