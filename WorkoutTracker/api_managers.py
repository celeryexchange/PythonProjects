import requests
from datetime import datetime

# constants
sheety_project_endpoint = "https://api.sheety.co/c6f8b9788c5c073a746d10c302de896a/workoutTracker"
sheety_sheet_name = "exerciseHistory"


class NutritionixClient:
    def __init__(self, api_id: str, api_key: str):
        """
        Initialize the NutritionixClient with API credentials.

        :param api_id: The API ID provided by Nutritionix.
        :param api_key: The API Key provided by Nutritionix.
        """
        self.api_id = api_id
        self.api_key = api_key
        self.api_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

        # optional user configuration
        self.weight_kg = None
        self.height_cm = None
        self.age = None

    def configure_user(self, weight_kg: int, height_cm: int, age: int) -> None:
        """
        Configure user-specific data.

        :param weight_kg: User's weight in kilograms.
        :param height_cm: User's height in centimeters.
        :param age: User's age.
        """
        if weight_kg <= 0 or height_cm <= 0 or age <= 0:
            raise ValueError("Weight, height, and year born must be positive values.")
        if weight_kg < 30 or weight_kg > 300:
            raise ValueError("Weight must be between 30 and 300 kg.")
        if height_cm < 100 or height_cm >= 250:
            raise ValueError("Height must be between 100 and 250 cm.")
        if age > 100:
            raise ValueError("Age cannot be more than 100.")

        self.weight_kg = weight_kg
        self.height_cm = height_cm
        self.age = age

    def process_exercise(self, query: str):

        # Authenticate
        headers = {
            "x-app-id": self.api_id,
            "x-app-key": self.api_key,
        }
        parameters = {
            "query": query,
        }
        try:
            response = requests.post(self.api_exercise_endpoint, headers=headers, json=parameters)
            response.raise_for_status()
            return response.json()['exercises']

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")


class SheetyClient:
    def __init__(self, token: str = None):
        self.sheety_api_endpoint = "https://api.sheety.co/c6f8b9788c5c073a746d10c302de896a/workoutTracker/exerciseHistory"
        self.token = token

    def post_exercise(self, exercise_data: list, sheet_name: str = sheety_sheet_name) -> None:
        for entry in exercise_data:
            # Sheety camelCases all JSON keys, so if your column is called "First Name" then enter "firstName".
            payload = {
                sheet_name: {
                    "date": datetime.today().strftime("%Y-%m-%d"),
                    "exerciseType": entry["name"],
                    "durationMinutes": entry["duration_min"],
                    "calories": entry["nf_calories"],
                }
            }
            try:
                response = requests.post(self.sheety_api_endpoint, json=payload)
                response.raise_for_status()
                print(f"Response from Sheety: {response.text}")

            except requests.exceptions.RequestException as e:
                raise Exception(f"API request failed: {e}")