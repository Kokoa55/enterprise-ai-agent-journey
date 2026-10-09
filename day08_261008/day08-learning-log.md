# Day 08 - 2026-10-08
# SQL + SQLite Fundamentals

## 1. Day 08 Goal

Day 08 moved the project from file-based storage toward database-backed storage.

Before Day 08, customer cases were mainly stored in:

```text
customer_cases.json
```

Today we introduced:

```text
support.db
```

using SQLite.

The main goal was to understand:

```text
Database
Table
Row
Column
Primary Key
CREATE TABLE
INSERT
SELECT
WHERE
UPDATE
DELETE
CRUD
Python sqlite3
Parameterized Query
Tuple
```

---

## 2. JSON vs Database

JSON is useful for:

```text
small test data
configuration
API request/response
temporary data exchange
```

But as data grows, we often need to:

```text
search
filter
update
delete
query by condition
store many records
```

A database is better suited for this.

Mental model:

```text
JSON
= file-based storage

SQLite
= database-based storage
```

---

## 3. SQLite

SQLite was chosen because:

```text
No separate database server required
No username/password required
Python includes sqlite3
Database is stored in one local file
```

Example:

```python
import sqlite3
```

Connection:

```python
connection = sqlite3.connect("support.db")
```

If the file does not exist, SQLite creates it.

---

## 4. What is `connection`?

Important distinction:

```text
support.db
= the database file

connection
= Python's active connection to that database
```

Example:

```python
connection = sqlite3.connect("support.db")
```

Mental model:

```text
support.db
↓
sqlite3.connect(...)
↓
connection
```

The `connection` object is not the database itself.

It is the communication channel between Python and the database.

---

## 5. Cursor

From the connection we create a cursor:

```python
cursor = connection.cursor()
```

The cursor is used to execute SQL.

Mental model:

```text
Python
↓
connection
↓
cursor
↓
SQL
↓
SQLite
```

Example:

```python
cursor.execute("SELECT * FROM customer_cases")
```

---

## 6. Why not chain everything?

This is technically possible:

```python
sqlite3.connect("support.db").cursor().execute(...)
```

But it is usually less readable and less convenient.

The clearer form is:

```python
connection = sqlite3.connect("support.db")
cursor = connection.cursor()

cursor.execute(...)

connection.commit()
connection.close()
```

This keeps responsibilities clear.

---

## 7. Creating the Database Table

The table creation function:

```python
def create_database():
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS customer_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL
        )
        '''
    )

    connection.commit()
    connection.close()
```

Important SQL:

```sql
CREATE TABLE IF NOT EXISTS customer_cases
```

Meaning:

```text
Create the table only if it does not already exist.
```

---

## 8. Table / Row / Column / Primary Key

Example table:

| id | customer | issue | priority |
|---:|---|---|---|
| 1 | Toyota | Cannot login | high |
| 2 | Honda | Need accounts | medium |

Concepts:

```text
Table
= customer_cases

Row
= one complete record

Column
= id / customer / issue / priority

Primary Key
= unique identifier for a row
```

In our table:

```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
```

means:

```text
id is an integer
id uniquely identifies each row
SQLite generates the id automatically
```

---

## 9. SQL Typo Encountered

A mistake occurred:

```sql
AUTOINCERMENT
```

Correct:

```sql
AUTOINCREMENT
```

This was an SQL keyword spelling problem.

Mental model:

```text
Python parsed the SQL string correctly
↓
SQLite received the SQL
↓
SQLite rejected the invalid keyword
```

---

# 10. INSERT

We added:

```python
def insert_case(customer, issue, priority):
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        '''
        INSERT INTO customer_cases (customer, issue, priority)
        VALUES (?, ?, ?)
        ''',
        (customer, issue, priority)
    )

    connection.commit()
    connection.close()
```

SQL:

```sql
INSERT INTO customer_cases (customer, issue, priority)
VALUES (?, ?, ?)
```

Meaning:

```text
Add one new row to customer_cases
```

The `id` is not provided manually because SQLite generates it automatically.

---

## 11. Parameterized Query

Instead of building SQL with f-strings, we used:

```sql
VALUES (?, ?, ?)
```

and passed the real values separately:

```python
(customer, issue, priority)
```

This is called:

```text
Parameterized Query
```

It improves:

```text
safety
clarity
SQL injection protection
```

---

## 12. Table Name Error

An error occurred:

```text
sqlite3.OperationalError: no such table: customer_case
```

Reason:

The created table was:

```text
customer_cases
```

but the INSERT statement used:

```text
customer_case
```

Useful debugging rule:

If you see:

```text
no such table
```

check:

```text
table name spelling
database file
whether CREATE TABLE ran
singular vs plural naming
```

---

# 13. SELECT

We added:

```python
def get_all_cases():
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT * FROM customer_cases
        '''
    )

    cases = cursor.fetchall()

    connection.close()

    return cases
```

SQL:

```sql
SELECT * FROM customer_cases
```

Meaning:

```text
SELECT
→ query data

*
→ all columns

FROM customer_cases
→ from this table
```

---

## 14. `fetchall()`

After executing a SELECT:

```python
cases = cursor.fetchall()
```

This retrieves all query results.

Example result:

```python
[
    (1, "Toyota", "Cannot login", "high"),
    (2, "Honda", "Need accounts", "medium")
]
```

By default, SQLite returns:

```text
list of tuples
```

---

## 15. Repeated INSERT Behavior

We observed multiple Toyota rows.

Reason:

```python
insert_case(...)
```

was executed every time `main.py` ran.

Important:

```text
INSERT
= always creates a new row
```

unless additional constraints or logic prevent duplication.

Example:

```text
first run  → id 1
second run → id 2
third run  → id 3
```

Even if the content is identical, the rows are different because their IDs are different.

---

# 16. WHERE

We added:

```python
def get_cases_by_priority(priority):
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT * FROM customer_cases
        WHERE priority = ?
        ''',
        (priority,)
    )

    cases = cursor.fetchall()

    connection.close()

    return cases
```

SQL:

```sql
SELECT * FROM customer_cases
WHERE priority = ?
```

Meaning:

```text
Return only rows whose priority matches the supplied value.
```

---

## 17. Function Argument Error

An error occurred:

```text
TypeError:
get_cases_by_priority() takes 0 positional arguments but 1 was given
```

Cause:

```python
def get_cases_by_priority():
```

but call:

```python
get_cases_by_priority("high")
```

Correct:

```python
def get_cases_by_priority(priority):
```

Mental model:

```text
Function definition parameter count
must match
Function call argument count
```

---

# 18. What is a Tuple?

A tuple is:

```text
an ordered collection of values
```

Example:

```python
("medium", 1)
```

A tuple is similar to a list, but is commonly used for fixed groups of values.

---

## 19. Why `(priority,)` Has a Comma

For one SQL placeholder:

```sql
WHERE priority = ?
```

we pass one value:

```python
(priority,)
```

The comma is necessary because:

```python
("high")
```

is just a string inside parentheses.

But:

```python
("high",)
```

is a one-element tuple.

Examples:

```python
type(("high"))
# str

type(("high",))
# tuple
```

---

## 20. Why Two Values Do Not Need a Trailing Comma

Example:

```python
(new_priority, case_id)
```

This already clearly contains two elements, so Python knows it is a tuple.

For two SQL placeholders:

```sql
SET priority = ?
WHERE id = ?
```

the values map in order:

```text
first ?  → new_priority
second ? → case_id
```

So:

```python
(new_priority, case_id)
```

is sufficient.

---

# 21. UPDATE

We added:

```python
def update_priority(case_id, new_priority):
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        '''
        UPDATE customer_cases
        SET priority = ?
        WHERE id = ?
        ''',
        (new_priority, case_id)
    )

    connection.commit()
    connection.close()
```

SQL:

```sql
UPDATE customer_cases
SET priority = ?
WHERE id = ?
```

Meaning:

```text
Find the row with the specified id
↓
Change its priority
```

---

## 22. Why WHERE Matters in UPDATE

Safe:

```sql
UPDATE customer_cases
SET priority = ?
WHERE id = ?
```

Dangerous:

```sql
UPDATE customer_cases
SET priority = ?
```

Without `WHERE`, every row could be updated.

Important habit:

```text
When using UPDATE or DELETE,
always ask:

"Where is my WHERE?"
```

---

# 23. DELETE

We added:

```python
def delete_case(case_id):
    connection = sqlite3.connect("support.db")
    cursor = connection.cursor()

    cursor.execute(
        '''
        DELETE FROM customer_cases
        WHERE id = ?
        ''',
        (case_id,)
    )

    connection.commit()
    connection.close()
```

SQL:

```sql
DELETE FROM customer_cases
WHERE id = ?
```

Meaning:

```text
Delete one specific row
```

Again, `WHERE` is critical.

Without it:

```sql
DELETE FROM customer_cases
```

could delete all rows.

---

# 24. CRUD

Today we completed the four core database operations:

```text
C = Create
R = Read
U = Update
D = Delete
```

Mapped to SQL:

```text
Create → INSERT
Read   → SELECT
Update → UPDATE
Delete → DELETE
```

This CRUD concept will be used heavily in FastAPI.

---

# 25. `commit()`

For operations that modify the database:

```text
CREATE
INSERT
UPDATE
DELETE
```

we use:

```python
connection.commit()
```

Meaning:

```text
Persist the changes to the database.
```

Important:

Git commit and database commit are different concepts.

---

# 26. `close()`

After database operations:

```python
connection.close()
```

closes the active database connection.

Good habit:

```text
Open connection
↓
Use database
↓
Commit if necessary
↓
Close connection
```

---

# 27. `main()` and Repeated Inserts

Important clarification:

The `main()` engineering entry point is not what causes duplicate records.

This:

```python
if __name__ == "__main__":
    main()
```

controls:

```text
when the program executes
```

But this:

```python
insert_case(...)
```

controls:

```text
whether a new row is inserted
```

Example:

```python
def main():
    create_database()
    insert_case("Toyota", "Cannot login", "high")
```

Every direct run will insert another row.

But:

```python
def main():
    create_database()
    print(get_all_cases())
```

only reads data.

Mental model:

```text
main() entry point
= controls WHEN program logic runs

insert_case()
= controls WHAT the program does
```

---

# 28. Final Day 08 Main Structure

A cleaner final `main.py` can avoid automatically inserting data:

```python
from database import (
    create_database,
    get_all_cases,
    get_cases_by_priority,
    update_priority,
    delete_case
)


def main():
    create_database()

    print("All cases:")
    print(get_all_cases())

    print("High priority cases:")
    print(get_cases_by_priority("high"))


if __name__ == "__main__":
    main()
```

This can be run repeatedly without inserting duplicate test rows.

---

# 29. Day 08 Debugging Summary

### SQL keyword typo

```text
AUTOINCERMENT
```

Correct:

```text
AUTOINCREMENT
```

### Wrong table name

Error:

```text
no such table: customer_case
```

Cause:

```text
customer_case
≠
customer_cases
```

### Wrong function parameter definition

Error:

```text
takes 0 positional arguments but 1 was given
```

Cause:

```python
def get_cases_by_priority():
```

instead of:

```python
def get_cases_by_priority(priority):
```

---

# 30. Engineering Mental Model

The database flow is now:

```text
Python
↓
sqlite3.connect()
↓
connection
↓
cursor
↓
SQL
↓
SQLite database
↓
fetch / commit
↓
close
```

For a query:

```text
SELECT
↓
cursor.fetchall()
↓
Python list of tuples
```

For a write:

```text
INSERT / UPDATE / DELETE
↓
connection.commit()
```

---

# 31. Agent / Backend Connection

Today was not directly about LLMs, but it is foundational for future Agent systems.

Future architecture:

```text
User / Agent
↓
FastAPI
↓
Business Logic
↓
Database
↓
Tool / External System
```

Agents often need persistent state:

```text
customer cases
task status
workflow history
user data
audit logs
tool results
```

A database is one way to store this state.

---

# 32. Key Takeaways

1. A database is not the same as a JSON file.
2. `connection` is a connection to the database, not the database itself.
3. `cursor` executes SQL.
4. Parameterized queries use `?` placeholders.
5. One SQL parameter requires a one-element tuple such as `(priority,)`.
6. `INSERT` creates a new row every time it runs.
7. `SELECT` reads data.
8. `WHERE` filters rows.
9. `UPDATE` changes existing rows.
10. `DELETE` removes rows.
11. `UPDATE` and `DELETE` without `WHERE` can affect all rows.
12. `commit()` persists changes.
13. CRUD is a core backend concept.
14. `main()` controls execution flow; it does not automatically prevent duplicate inserts.

---

# 33. What I Should Be Able to Explain After Day 08

```text
What SQLite is
What support.db is
What connection means
What cursor does
What a table / row / column is
What a primary key is
What AUTOINCREMENT does
How INSERT works
How SELECT works
How WHERE works
How UPDATE works
How DELETE works
What CRUD means
What a parameterized query is
Why ? placeholders are used
What a tuple is
Why (priority,) needs the comma
Why UPDATE / DELETE need WHERE
Why repeated insert_case() calls create duplicates
```

---

# Next: Day 09

Planned focus:

```text
FastAPI fundamentals
API endpoints
GET
POST
Path parameters
Query parameters
Request body
Pydantic models
Local API server
```

Day 09 will move from:

```text
Python directly calling database functions
```

toward:

```text
Client
↓
HTTP API
↓
Python backend
↓
SQLite
```
