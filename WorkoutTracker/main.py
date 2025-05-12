import os
from dotenv import load_dotenv
from api_managers import NutritionixClient, SheetyClient


# Local environment variables from a local .env file
load_dotenv()

# Load username and API key
API_ID = os.getenv("NUTRITIONIX_APP_ID")
API_KEY = os.getenv("NUTRITIONIX_API_KEY")

# print(f"API_APP_ID: {API_ID}")
# print(f"API_KEY: {API_KEY}")

# Instantiate API Clients
nutritionix_client = NutritionixClient(api_id=API_ID, api_key=API_KEY)
sheety_client = SheetyClient()

# Ask the user to describe what exercises they did
answer = input("What exercises did you do today? ")
exercise_data = nutritionix_client.process_exercise(query=answer)
sheety_client.post_exercise(exercise_data)



