import requests


class NutritionixClient:
    def __init__(self, api_id: str, api_key:str):
        self.api_id = api_id
        self.api_key = api_key
        self.api_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

    def configure_user(self, weight_kg: int, height_cm: int, year_born: int):
        self.weight_kg = weight_kg
        self.height_cm = height_cm
        self.year_born = year_born

    def process_exercise(self, query: str):

        # Authenticate
        headers = {
            "x-app-id": app_id,
            "x-app-key": app_key,

        }
        #
        parameters = {
            "query": "ran for 3 kilometers",
        }



# Retrieve a bearer token
api_exercise_endpoint = f"https://trackapi.nutritionix.com/v2/natural/exercise"

def get_exercise_data(api_url, app_id, app_key):



    try:
        # Send the GET request to the API
        response = requests.post(api_url, headers=headers, json=parameters)

        # Check if the response status is successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print(data)

        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")