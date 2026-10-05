import json

with open("customer_cases.json", "r") as file:
    customer_cases = json.load(file)


summary = {
    "total_cases": len(customer_cases),
    "status": "processed"
}

with open("summary.json", "w") as file:
    json.dump(summary, file, indent=4)

    