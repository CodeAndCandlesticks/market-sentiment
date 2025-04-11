# 📰 Market Sentiment Checker

This Python script fetches the latest stock market update from [Schwab's daily open report](https://www.schwab.com/learn/story/stock-market-update-open), analyzes it using a language model (OpenAI or Anthropic), and logs whether the current market sentiment is **Bullish**, **Bearish**, or **Mixed**.

Sentiment results are stored in a local `.log` file with the date, sentiment, model used, and model version — perfect for integrating with trading scripts or position sizing strategies.

---

## 🚀 Features

- ✅ Pulls latest article from Schwab's Market Open page
- ✅ Supports **OpenAI GPT-4** or **Anthropic Claude 3.5 Sonnet**
- ✅ Logs sentiment in `.csv`-style `.log` file
- ✅ Automatically overwrites duplicate entries by date
- ✅ Lightweight and fast (no database required)

---

## 📦 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file

```env
USE_MODEL=openai        # or "anthropic"
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

---

## 🧠 Example Output

Running the script will print and log:

```bash
📊 Today's Market Sentiment: Bullish (Model: anthropic / claude-3-5-sonnet-20241022)
```

And log it as:

```
2025-04-11,Bullish,anthropic,claude-3-5-sonnet-20241022
```

in the file: `market_sentiment.log`

---

## 🛠 Customization

- Change the `.log` filename in the script to customize location
- Add logic to adjust trading size or strategy based on sentiment
- To view historical sentiment: load `market_sentiment.log` with `pandas`

---

## 📁 Files

- `market_sentiment_checker.py` — Main script
- `.env` — Stores your API keys securely
- `market_sentiment.log` — Local log file (ignored via `.gitignore`)
- `requirements.txt` — Dependency list

---

## 🤖 Models

| Provider   | Model                             | Use Case              |
|------------|-----------------------------------|------------------------|
| OpenAI     | `gpt-4`                           | Deep analysis          |
| Anthropic  | `claude-3-5-sonnet-20241022`      | Fast + accurate (latest) |
| Anthropic  | `claude-3-opus-20240229`          | Most powerful          |
| Anthropic  | `claude-3-sonnet-20240229`        | Balanced performance   |
| Anthropic  | `claude-3-haiku-20240307`         | Fast & lightweight     |

---

## 🔒 Notes

- API keys are never committed — make sure `.env` and `.log` are in your `.gitignore`.
- This script is designed for **local automation** — adapt it to your trading system or cron schedule.

---

## 📬 Questions or Ideas?

Feel free to open an issue or tweak the prompt for your use case!
