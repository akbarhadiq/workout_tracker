from dotenv import load_dotenv
import os
import requests
import datetime as dt

# Load Env Key
load_dotenv("secrets.env")
nutritionix_app_id = os.getenv("NUTRITIONIX_APP_ID")
nutritionix_app_key = os.getenv("NUTRITIONIX_API_KEYS")
sheety_auth = os.getenv("sheety_auth")

# Url Needed
exercise_url_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_url_endpoint = "https://api.sheety.co/2b7440464c17d783b68e68faf726e0a3/myWorkouts/workouts"
sheety_post_url = "https://api.sheety.co/2b7440464c17d783b68e68faf726e0a3/myWorkouts/workouts"

headers = {
    "x-app-id": nutritionix_app_id,
    "x-app-key": nutritionix_app_key
}

sheety_headers = {
    "Authorization": sheety_auth
}


def params_get(query):
    params = {
        "query": query
    }

    return params


def get_workout_data():
    exercise_input = input("What exercise you did today? : ").title()
    parameters = params_get(exercise_input)
    exercise_response = requests.post(url=exercise_url_endpoint, json=parameters, headers=headers)
    exercise_response.raise_for_status()
    exercise_result = exercise_response.json()['exercises']
    return exercise_result


def post_workout(workout_to_post):
    today_date = dt.datetime.now()
    today_time_formatted = today_date.strftime("%H:%M:%S")
    today_date_formatted = today_date.strftime("%d/%m/%Y")
    post_list = []

    for x in range(len(workout_to_post)):
        post_this = {
            "workout": {
                "date": today_date_formatted,
                "time": today_time_formatted,
                "exercise": workout_to_post[x]['user_input'].title(),
                "duration": workout_to_post[x]['duration_min'],
                "calories": workout_to_post[x]['nf_calories']
            }
        }
        post_list.append(post_this)

    for exercise in post_list:
        post_exercise = requests.post(url=sheety_post_url, headers=sheety_headers, json=exercise)
        if post_exercise.raise_for_status() == 200:
            print(f"Successful, HTTP Status {post_exercise.status_code}")
        else:
            post_exercise.raise_for_status()


def program():
    exercises = get_workout_data()
    post_workout(exercises)


run_program = True
while run_program:
    program()
    ask_yes_or_no = input("Still have other workout to post? (Y/N): ").lower()

    if ask_yes_or_no == "y":
        run_program = True
    else:
        run_program = False
