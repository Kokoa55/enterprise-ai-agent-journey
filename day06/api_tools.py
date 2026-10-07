import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_task(title, user_id):
    token = os.getenv("API_TOKEN")

    if not token:
        raise ValueError("API_TOKEN is missing")

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Task title must be a non-empty string")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "title": title.strip(),
        "completed": False,
        "userId": user_id
    }

    try:
        response = requests.post(
            "https://jsonplaceholder.typicode.com/todos",
            headers = headers,
            json = payload,
            timeout = 5
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"Create task failed: {error}")
        return None