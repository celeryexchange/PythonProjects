import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta
from twilio.rest import Client


load_dotenv()

STOCK = "TSLA"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

COMPANY_NAME = "Tesla Inc"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")


def is_yesterday(date: str) -> bool:
    # get current and yesterday's date
    today = datetime.now().date()
    yesterday = today + timedelta(days=-1)

    return date == yesterday.strftime('%Y-%m-%d')


def get_stock_prices() -> pd.DataFrame:

    url = STOCK_ENDPOINT
    payload = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    r = requests.get(url, params=payload)
    ticker_data = r.json()
    # print(ticker_data)

    # Transform the data into a Pandas DataFrame
    df = pd.DataFrame.from_dict(ticker_data["Time Series (Daily)"], orient='index')

    # Rename columns for simplicity
    df.columns = ['open', 'high', 'low', 'close', 'volume']

    # Ensure data types are correct (convert strings to floats/integers where needed)
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(int)

    # sort from latest to oldest and calculate Net Change %
    # Net change is the difference between the closing price of a stock in the current trading period
    # and the closing price in the previous trading period.
    df = df.sort_index(ascending=False)
    df['net_change'] = df['close'].diff(periods=-1)
    df['net_change_pct'] = df['close'].pct_change(periods=-1) * 100

    return df


def get_news() -> pd.DataFrame:

    url = NEWS_ENDPOINT
    payload = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "language": "en",
        "pageSize": 20,  # number of results to return per page
        "sortBy": "relevancy",  # relevancy, publishedAt, popularity
    }
    r = requests.get(url, params=payload)
    news_data = r.json()
    # print(news_data["articles"])

    # Clean up the news data
    df = pd.DataFrame.from_dict(news_data["articles"])
    df['source.id'] = df['source'].apply(lambda x: x["id"])
    df['source.name'] = df['source'].apply(lambda x: x["name"])
    df = df.drop(labels="source", axis=1)

    return df


def send_text(text: str):

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=text,
        from_="+16283000722",
        to="+447464806057",
    )

def get_emoji(change: float):
    return "🟢" if change > 0 else "🔻"


# Step 1: Get the latest stock prices for STOCK & check if the price increased/decreased by at least 5 percent
prices = get_stock_prices()
latest_close_date = prices.index[0]
latest_net_change_pct = prices.loc[latest_close_date].net_change_pct
was_net_change_over_5_pct = abs(latest_net_change_pct) > 5

# # manually change the latest index to yesterday - for testing only
# df.index.values[0] = '2024-10-20'

if is_yesterday(latest_close_date) and was_net_change_over_5_pct:
    # Step 2: If the net change was at least 5 percent yesterday then fetch the latest headlines
    latest_news = get_news()

    # Step 3: Send me a text and include the top news story
    article_source = latest_news["source.name"][0]
    article_title = latest_news["title"][0]
    article_url = latest_news["url"][0]
    text_message = f"{STOCK}: {latest_net_change_pct:.2f}% {get_emoji(latest_net_change_pct)} {article_source}: {article_title} at {article_url}"

    send_text(text_message)
