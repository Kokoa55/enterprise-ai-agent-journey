def validate_case(case):
    customer = case.get("customer")
     # case["customer"] 字段不存在会报 KeyError
    issue = case.get("issue")
    priority = case.get("priority")


    if not isinstance(customer, str) or not customer.strip():
        return False

    if not isinstance(issue, str) or not issue.strip():
        return False

    if not isinstance(priority, str) or not priority.strip():
        return False

    return True