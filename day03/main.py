
from data_loader import load_customer_cases
from sla import get_sla

tools = {
    "get_sla": get_sla
}

tool_name = "get_sla"
priority = "high"

result = tools[tool_name](priority)

print(result)