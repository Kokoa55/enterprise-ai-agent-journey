def normalize_priority(priority):
    return priority.strip().lower()

def get_sla(priority):
    priority = normalize_priority(priority)
    sla_map = {
        "high": "4 hour",
        "medium": "8 hours",
        "low": "24 hours"
    }

    return sla_map.get(priority, "Unknow SLA")

def is_supported_priority(priority):
    priority = normalize_priority(priority)
    supported_priority = ["high", "medium", "low"]

    return priority in supported_priority