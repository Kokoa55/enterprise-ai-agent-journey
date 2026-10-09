import json

def load_customer_cases(filename):
    try:
        with open(filename,"r") as file:
            return json.load(file) 
            # 核心 JSON文件➡ -> Python数据
       
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
        # 返回1个空List
    except json.JSONDecodeError:
        print(f"Invalid JSON format: {filename}")
        return []

