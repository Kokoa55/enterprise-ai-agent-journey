from database import (
    create_database, 
    insert_case, 
    get_all_cases,
    get_cases_by_priority,
    update_priority,
    delete_case
)

def main():
    create_database()
    print("All cases:")
    print(get_all_cases())

    print("High priority case:")
    print(get_cases_by_priority("high"))

if__name__ == "__main__"
    main()

