import sqlite3

def create_database():
    connection = sqlite3.connect("support.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        
        CREATE TABLE IF NOT EXISTS customer_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()

def insert_case(customer,issue,priority):
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO customer_cases(customer,issue,priority)
        VALUES(?,?,?)
        """,
        (customer, issue, priority)
    )

    connection.commit()
    connection.close()

def get_all_cases():
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM customer_cases
        """
    )

    cases = cursor.fetchall()
    connection.close()
    return cases

def get_cases_by_priority(priority):
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM customer_cases
        WHERE priority =?
        """,
        (priority,)
    )

    cases = cursor.fetchall()

    connection.close()
    return cases

def update_priority(case_id, new_priority):
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE customer_cases
        SET priority = ?
        WHERE id = ?    
        """,
        (new_priority, case_id)

    )

    connection.commit()
    connection.close()

def delete_case(case_id):
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM customer_cases
        WHERE id = ?    
        """,
        (case_id,)

    )

    connection.commit()
    connection.close()