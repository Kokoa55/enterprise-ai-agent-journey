print("__name__ =", __name__)

from data_loader import load_customer_cases
from validator import validate_case
from business_rules import get_sla, is_supported_priority
from api_tools import create_task

def process_case(case):
    if not validate_case(case):
            print("Invalid case")
            return
            #continue change to return
            # 触发continue直接进入下一个for

    if not is_supported_priority(case["priority"]):
        print(f"Unsupported priority: {case['priority']}")
        return
        #continue change to return

    sla = get_sla(case["priority"])
    print(f"Customer: {case['customer']}")
    print(f"SLA: {sla}")

    task = create_task(
        title=f'[{case["customer"]}-{case["issue"]}]',
        user_id = 1
    )

    print("Created task:")
    print(task)

def main():
    cases = load_customer_cases("customer_cases.json")

    for case in cases:
        print("---------------")
        print(case)
        process_case(case)

        

if __name__=="__main__":
    main()