import requests
from dotenv import load_dotenv
import os
from datetime import datetime


# Load environment variables from .env file
load_dotenv()

# Access the variables
PIXELA_USERNAME = os.getenv("PIXELA_USERNAME")
PIXELA_TOKEN = os.getenv("PIXELA_TOKEN")

# print(f"Username: {PIXELA_USERNAME}")
# print(f"Token: {PIXELA_TOKEN}")

# Constants and endpoints
PIXELA_URL = "https://pixe.la"
PIXELA_ENDPOINT_USER = f"{PIXELA_URL}/v1/users"
PIXELA_ENDPOINT_GRAPH = f"{PIXELA_URL}/v1/users/{PIXELA_USERNAME}/graphs"
PIXELA_GRAPH_ID = "l67a26w112"
PIXELA_GRAPH_NAME = "Python Daily"
PIXELA_GRAPH_UNIT = "Session"
PIXELA_GRAPH_TYPE = "int"
PIXELA_GRAPH_COLOR = "ajisai"
PIXELA_ENDPOINT_GRAPH_A = f"{PIXELA_ENDPOINT_GRAPH}/{PIXELA_GRAPH_ID}"

# Step 0: Delete existing user

# target_url = f"{PIXELA_ENDPOINT_USER}/{PIXELA_USERNAME}"
# header = {
#   "X-USER-TOKEN": PIXELA_TOKEN,
# }
# response = requests.delete(target_url, headers=header)
# print(response.text)


# Step 1: Create a new user

target_url = PIXELA_ENDPOINT_USER
# print(target_url)
payload = {
  "token": PIXELA_TOKEN,
  "username": PIXELA_USERNAME,
  "agreeTermsOfService": "yes",
  "notMinor": "yes",
}
response = requests.post(target_url, json=payload)
print(response.text)


# Step 2: Create a new graph

target_url = PIXELA_ENDPOINT_GRAPH
# print(target_url)
header = {
  "X-USER-TOKEN": PIXELA_TOKEN,
}
payload = {
  "id": PIXELA_GRAPH_ID,
  "name": PIXELA_GRAPH_NAME,
  "unit": PIXELA_GRAPH_UNIT,
  "type": PIXELA_GRAPH_TYPE,
  "color": PIXELA_GRAPH_COLOR,
}
response = requests.post(target_url, headers=header, json=payload)
print(response.text)


# Step 3: Add an activity

target_url = PIXELA_ENDPOINT_GRAPH_A
# print(target_url)
today = datetime.today()
today_as_string = today.strftime("%Y%m%d")
header = {
  "X-USER-TOKEN": PIXELA_TOKEN,
}
payload = {
  "date": today_as_string,
  "quantity": "1",
}
response = requests.post(target_url, headers=header, json=payload)
print(response.text)