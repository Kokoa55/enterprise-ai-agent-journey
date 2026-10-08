from database import (
    create_database, 
    insert_case, 
    get_all_cases,
    get_cases_by_priority,
    update_priority,
    delete_case
)

print("Before update:")
print(get_all_cases())

delete_case(3)

print("After update:")
print(get_all_cases())