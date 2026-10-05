def get_sla(priority):
    sla_map = {
        "high": "1 hour",
        "medium": "4 hours",
        "low": "24 hours"
    }

    return sla_map.get(priority, "Unknown")