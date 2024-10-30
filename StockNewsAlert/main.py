import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta
from twilio.rest import Client
import logging
import sys
import yaml
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# variables
STOCK = "TSLA"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
COMPANY_NAME = "Tesla Inc"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# settings
with open("config.yaml", "r") as f:
    config_d = yaml.safe_load(f)

get_secrets_from_setting = config_d["get_secrets_from"].lower()
azure_key_vault_name = config_d["azure_key_vault_name"].lower()

# secrets
logging.info("Loading API secrets.")

if get_secrets_from_setting not in ('azure', 'env'):
    raise ValueError("The `get_secrets_from` setting encountered an invalid value. Possible options are `azure` or `env`.")

if get_secrets_from_setting == 'env':
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the secrets
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

    logging.info("Loaded API secrets from environment.")

elif get_secrets_from_setting == 'azure':

    # Initialize credentials using the Managed Identity
    azure_credential = DefaultAzureCredential()

    # Key Vault URL
    key_vault_url = f"https://{azure_key_vault_name}.vault.azure.net/"

    # Initialize the SecretClient with Key Vault URL and credential
    azure_client = SecretClient(vault_url=key_vault_url, credential=azure_credential)

    # Retrieve the secrets
    ALPHA_VANTAGE_API_KEY = azure_client.get_secret("ALPHA-VANTAGE-API-KEY").value
    NEWS_API_KEY = azure_client.get_secret("NEWS-API-KEY").value
    TWILIO_ACCOUNT_SID = azure_client.get_secret("TWILIO-ACCOUNT-SID").value
    TWILIO_AUTH_TOKEN = azure_client.get_secret("TWILIO-AUTH-TOKEN").value

    logging.info("Loaded API secrets from Azure Key Vault.")

if not ALPHA_VANTAGE_API_KEY or not NEWS_API_KEY or not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
    raise ValueError("API Secrets must not be null.")


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

    today = datetime.now().date()
    yesterday = (today + timedelta(days=-1)).strftime('%Y-%m-%d')

    url = NEWS_ENDPOINT
    payload = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "language": "en",
        "pageSize": 20,  # number of results to return per page
        "sortBy": "relevancy",  # relevancy, publishedAt, popularity
        "from": yesterday,
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


def main():
    # Step 1: Get the latest stock prices for STOCK & check if the price increased/decreased by at least 5 percent
    logging.info("Getting stock prices...")
    prices = get_stock_prices()
    latest_close_date = prices.index[0]
    latest_net_change_pct = prices.loc[latest_close_date].net_change_pct
    was_net_change_over_5_pct = abs(latest_net_change_pct) > 5

    # # manually change the latest index to yesterday - for testing only
    # df.index.values[0] = '2024-10-20'

    logging.info("Deciding what to do next.")
    if is_yesterday(latest_close_date) and was_net_change_over_5_pct:
        logging.info("Net change was over 5 percent - fetching news...")
        # Step 2: If the net change was at least 5 percent yesterday then fetch the latest headlines
        latest_news = get_news()

        # Step 3: Send me a text and include the top news story
        logging.info("Sending a text...")
        article_source = latest_news["source.name"][0]
        article_title = latest_news["title"][0]
        article_url = latest_news["url"][0]
        text_message = f"{STOCK}: {latest_net_change_pct:.2f}% {get_emoji(latest_net_change_pct)} {article_source}: {article_title} at {article_url}"

        send_text(text_message)
        logging.info("Message has been sent.")
    else:
        logging.info("Nothing to do.")
    sys.exit(0)

if __name__ == "__main__":
    main()
