import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
import csv

# Load .env variables
load_dotenv()

USE_MODEL = os.getenv("USE_MODEL", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# API imports
if USE_MODEL == "openai" and OPENAI_API_KEY:
    import openai
    openai.api_key = OPENAI_API_KEY
elif USE_MODEL == "anthropic" and ANTHROPIC_API_KEY:
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
else:
    raise ValueError("Missing or invalid API configuration.")

# 1. Fetch article content
def fetch_market_update_text():
    URL = "https://www.schwab.com/learn/story/stock-market-update-open"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    return "\n".join(p.get_text() for p in paragraphs).strip()

# 2. Generate sentiment using OpenAI
def get_openai_sentiment(article):
    prompt = f"""
You are a financial analyst. Based on the following article, determine whether the market sentiment for today is bullish, bearish, or mixed.
Respond with only one word: Bullish, Bearish, or Mixed.

Article:
{article[:3000]}
"""
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()

# 3. Generate sentiment using Anthropic
def get_anthropic_sentiment(article):
    prompt = f"""
You are a financial analyst. Based on the following article, determine whether the market sentiment for today is bullish, bearish, or mixed.
Respond with only one word: Bullish, Bearish, or Mixed.

Article:
{article[:3000]}
"""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=3,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    sentiment = response.content[0].text.strip().capitalize()
    if sentiment not in {"Bullish", "Bearish", "Mixed"}:
        sentiment = "Undetermined"
    return sentiment

def write_sentiment_log(sentiment, model_used, model_version, filename="market_sentiment.log"):
    from datetime import datetime
    import csv
    import os

    today = datetime.now().strftime("%Y-%m-%d")
    file_exists = os.path.isfile(filename)

    # Load existing log
    rows = []
    if file_exists:
        with open(filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)

    header = ["date", "sentiment", "model", "model_version"]
    updated = False

    # Overwrite today's entry
    for i, row in enumerate(rows):
        if row and row[0] == today:
            rows[i] = [today, sentiment, model_used, model_version]
            updated = True
            break

    # Append new row if today's entry wasn't found
    if not updated:
        if not rows:
            rows.append(header)
        rows.append([today, sentiment, model_used, model_version])

    # Write updated log
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


# 4. Execute
if __name__ == "__main__":
    article = fetch_market_update_text()

    if USE_MODEL == "openai":
        sentiment = get_openai_sentiment(article)
        model_version = "gpt-4"
    elif USE_MODEL == "anthropic":
        sentiment = get_anthropic_sentiment(article)
        model_version = "claude-3-5-sonnet-20241022"
    else:
        sentiment = "Undetermined"
        model_version = "unknown"

    write_sentiment_log(sentiment, model_used=USE_MODEL, model_version=model_version)
    print(f"📊 Today's Market Sentiment: {sentiment} (Model: {USE_MODEL} / {model_version})")



