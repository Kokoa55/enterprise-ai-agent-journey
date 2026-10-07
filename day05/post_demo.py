import requests
import os
from dotenv import load_dotenv

load_dotenv()

def create_task(title, user_id):
    token = os.getenv("API_TOKEN")

    # Security Check 1: Secret validation
    if not token:
        raise ValueError("API_TOKEN is missing")
    
    # Security Check 2: Input validation
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Task title must be a non-empty string")

    headers = {
    "Authorization": f"Bearer{token}",
    "Content-Type":"application/json"
    }
    
    payload = {
         "title": title,
         "completed": False,
         "userId": user_id
     }

    url = "https://jsonplaceholder.typicode.com/todos"

    
    try:
        response = requests.post(
         url,
        #  headers=headers,
         json=payload,
         timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(f"Creat task failed:{error}")
        return None

result = create_task("Prepare customer meeting",1)

print(result)