# Download the helper library from https://www.twilio.com/docs/python/install
import requests
import os
import pandas as pd
from twilio.rest import Client
from dotenv import load_dotenv

# load secrets from .env
load_dotenv()

# https://console.twilio.com/
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# https://www.latlong.net/
# Reading, UK
MY_LAT = 51.455040
MY_LONG = -0.969090

# https://openweathermap.org/api
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

# https://openweathermap.org/forecast5
url = "https://api.openweathermap.org/data/2.5/forecast"
payload = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "cnt": 4,  # next 12 hours (4 x 3 hours)
    "appid": OPENWEATHER_API_KEY,
}


r = requests.get(url, params=payload)
r.raise_for_status()
weather_data = r.json()

df = pd.json_normalize(weather_data["list"])

# Extract "id", "main", and "description" from the "weather" column
df['weather.id'] = df['weather'].apply(lambda x: x[0]['id'])
df['weather.main'] = df['weather'].apply(lambda x: x[0]['main'])
df['weather.description'] = df['weather'].apply(lambda x: x[0]['description'])
df = df.drop(columns=['weather'])

# https://openweathermap.org/weather-conditions
is_forecast_to_rain = df["weather.main"].isin(["Rain", "Thunderstorm", "Drizzle"])
if is_forecast_to_rain.any():
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella ☂",
        from_="+16283000722",
        to="+447464806057",
    )

    print(message.body)

# has been deployed to PythonAnywhere
# https://www.pythonanywhere.com/user/celery/tasks_tab/