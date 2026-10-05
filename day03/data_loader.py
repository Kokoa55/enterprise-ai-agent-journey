import json

def load_customer_cases(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {filename} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {filename} is not valid JSON.")
        return []