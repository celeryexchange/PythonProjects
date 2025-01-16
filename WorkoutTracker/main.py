import requests
from dotenv import load_dotenv
import os
from api_managers import NutritionixClient


# Local environment variables from a local .env file
load_dotenv()

# Load username and API key
API_ID = os.getenv("NUTRITIONIX_APP_ID")
API_KEY = os.getenv("NUTRITIONIX_API_KEY")

print(f"API_APP_ID: {API_ID}")
print(f"API_KEY: {API_KEY}")




# Example usage
get_exercise_data(api_exercise_endpoint, API_ID, API_KEY)




# response = requests.post(api_authentication_endpoint, headers=headers)
# print(response.text)

