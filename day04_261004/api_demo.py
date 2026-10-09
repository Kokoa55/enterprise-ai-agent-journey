import requests

def get_todo(todo_id):
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        return response.json()
    
    except requests.RequestException as error:
        print(f"API request failed: {error}")
        return None

def get_user_todo(user_id)
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        return response.json()
    
    except requests.RequestException as error:
        print(f"API request failed: {error}")
        return None

params = {
    "userId": user_id
}

print(get_user_todo(params["userId"]))
