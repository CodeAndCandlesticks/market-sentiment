# Changelog

## 2025-04-11: Initial version
- Integrated Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`) as the default Anthropic model.

## 2025-04-11

### Added
- Changed sentiment log file extension to `.csv` for structured data output.
- Added article content hashing to detect duplicate content day over day.
- Logged publish date extracted from Schwab article HTML.
- Stored full raw LLM response in the sentiment log for debugging and transparency.
- Introduced a separate log file (`market_sentiment_debug.log`) with support for INFO and DEBUG levels.
- Added a global `LOG_LEVEL` setting controlled by `.env`.
- Replaced standard print output with Pushover push notifications including date and sentiment.

