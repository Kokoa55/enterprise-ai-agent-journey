import sqlite3

DB_NAME = "support.db"

def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customer_cases(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()

def insert_case(customer, issue, priority):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO customer_cases (customer, issue, priority)
        VALUES (?, ?, ?)
        """,
        (customer, issue, priority)
    )

    connection.commit()
    case_id = cursor.lastrowid
    #最后一行

    connection.close()
    return case_id


def get_all_cases():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, customer, issue, priority
        FROM customer_cases
        """
    )

    rows = cursor.fetchall()
    connection.close()

    return rows

def get_case_by_id(case_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, customer, issue, priority
        FROM customer_cases
        WHERE id = ?
        """,
        (case_id,)
    )

    row = cursor.fetchone()
    connection.close()

    return row

def get_cases_by_priority(priority):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, customer, issue, priority
        FROM customer_cases
        WHERE priority = ?
        """,
        (priority,)
    )

    rows = cursor.fetchall()
    connection.close()

    return rows
