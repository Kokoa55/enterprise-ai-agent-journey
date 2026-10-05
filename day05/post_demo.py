import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("API_TOKEN")
print(token)


# import requests

# def create_todo(title,user_id):
#     url = "https://jsonplaceholder.typicode.com/todos"

#     payload = {
#         "title": "Prepare customer meeting",
#         "completed": False,
#         "userId": 1
#     }

#     try:
#         response = requests.post(
#         url,
#         json=payload,
#         timeout=5
#          )

#         response.raise_for_status()
#         return response.json()

#     except requests.RequestException as error:
#         print(f"API request failed:{error}")
#         return None

# result = create_todo("Prepare customer meeting",1)

# print(result)