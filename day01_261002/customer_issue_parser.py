customer_cases = [
    {
        "customer": "Toyota",
        "issue": "Cannot login to the system",
        "priority": "high"
    },
    {
        "customer": "Honda",
        "issue": "Need new user accounts",
        "priority": "medium"
    },
    {
        "customer": "Nissan",
        "issue": "Dashboard loading slowly",
        "priority": "urgent"
    }
]

    
priority_count = {
    "high": 0,
    "medium": 0,
    "low": 0,
    "unknown": 0
}


for customer in customer_cases:
    

    if customer["priority"] in priority_count:
        priority_count[customer["priority"]]+= 1
    else:
        priority_count["unknown"] += 1



print("Priority Summary")
for key,value in priority_count.items(): 
    print(f'{key}: {value}')


