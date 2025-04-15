import os
import requests
import hashlib
import csv
import re
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USE_MODEL = os.getenv("USE_MODEL", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

if USE_MODEL == "openai" and OPENAI_API_KEY:
    import openai
    openai.api_key = OPENAI_API_KEY
elif USE_MODEL == "anthropic" and ANTHROPIC_API_KEY:
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
else:
    raise ValueError("Missing or invalid API configuration.")

def log_message(level, message, debug_file="market_sentiment_debug.log"):
    levels = {"DEBUG": 10, "INFO": 20, "WARNING": 30}
    current_level = levels.get(LOG_LEVEL.upper(), 20)
    message_level = levels.get(level.upper(), 100)
    if message_level >= current_level:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(debug_file, "a") as log:
            log.write(f"[{level.upper()}] {timestamp} — {message}\n")

def send_push_notification(message):
    if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
        log_message("WARNING", "Pushover credentials not found. Skipping notification.")
        return

    payload = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message
    }
    response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
    if response.status_code != 200:
        log_message("WARNING", f"Pushover notification failed: {response.text}")
    else:
        log_message("INFO", "Push notification sent successfully.")

def fetch_article():
    url = "https://www.schwab.com/learn/story/stock-market-update-open"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    return response.text

def extract_article_text(html):
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")
    return "\n".join(p.get_text() for p in paragraphs).strip()

def extract_publish_date(html):
    soup = BeautifulSoup(html, "html.parser")
    match = soup.find(string=re.compile("Published as of:"))
    if match:
        date_text = re.search(r"Published as of: (.+?),", match)
        if date_text:
            try:
                dt = datetime.strptime(date_text.group(1), "%B %d, %Y")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass
    return datetime.now().strftime("%Y-%m-%d")

def get_article_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def get_sentiment_openai(article):
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

def get_sentiment_anthropic(article):
    prompt = f"""
You are a financial analyst. Based on the following article, determine whether the market sentiment for today is bullish, bearish, or mixed.
Respond with only one word: Bullish, Bearish, or Mixed.

Article:
{article[:3000]}
"""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()

def clean_sentiment(raw_response):
    cleaned = raw_response.strip().lower().rstrip(".")
    if cleaned in {"bullish", "bearish", "mixed"}:
        return cleaned.capitalize()
    return "Undetermined"

def write_log_csv(publish_date, sentiment, model_used, model_version, article_hash, raw_response, filename="market_sentiment.csv"):
    file_exists = os.path.isfile(filename)
    rows = []

    if file_exists:
        with open(filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)

    header = ["publish_date", "sentiment", "model", "model_version", "article_hash", "raw_response"]
    log_row = [publish_date, sentiment, model_used, model_version, article_hash, raw_response]
    updated = False

    for i, row in enumerate(rows):
        if row and row[0] == publish_date:
            rows[i] = log_row
            updated = True
            break

    if not updated:
        if not rows:
            rows.append(header)
        rows.append(log_row)

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

if __name__ == "__main__":
    html = fetch_article()
    log_message("INFO", "Article HTML fetched successfully.")

    article = extract_article_text(html)
    log_message("INFO", "Article content extracted.")
    log_message("DEBUG", f"Full article text:\n{article}")

    publish_date = extract_publish_date(html)
    article_hash = get_article_hash(article)

    if USE_MODEL == "openai":
        raw_response = get_sentiment_openai(article)
        model_version = "gpt-4"
    elif USE_MODEL == "anthropic":
        raw_response = get_sentiment_anthropic(article)
        model_version = "claude-3-5-sonnet-20241022"
    else:
        raw_response = "Undetermined"
        model_version = "unknown"

    sentiment = clean_sentiment(raw_response)
    write_log_csv(publish_date, sentiment, USE_MODEL, model_version, article_hash, raw_response)

    log_message("INFO", f"Sentiment result saved for {publish_date}: {sentiment}")
    log_message("DEBUG", f"Model response: {raw_response}")

    push_message = f"Publish Date: {publish_date}, Sentiment: {sentiment} (Model: {USE_MODEL} / {model_version})"
    send_push_notification(push_message)
