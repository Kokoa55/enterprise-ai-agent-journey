# Day 10 — 2026-10-09
# FastAPI + SQLite Integration

## 1. Day 10 Goal

Day 10 connected:

```text
Day 08
SQLite / CRUD

+

Day 09
FastAPI / Pydantic / HTTP

=

Client
↓
HTTP API
↓
FastAPI
↓
Pydantic
↓
Python handler
↓
database.py
↓
SQLite
↓
HTTP Response
```

The goal was to build a minimal backend API that can:

```text
POST /cases
→ create a customer case

GET /cases
→ list all customer cases

GET /cases?priority=high
→ filter customer cases by priority

GET /cases/{case_id}
→ retrieve one customer case

missing case
→ return 404

successful creation
→ return 201 Created
```

---

## 2. Project Structure

```text
day10/
├── main.py
├── database.py
├── README.md
└── support.db
```

Mental model:

```text
main.py
→ API layer / route layer

database.py
→ data access layer

support.db
→ persistence layer
```

---

## 3. Database Constant

```python
DB_NAME = "support.db"
```

Mental model:

```text
DB_NAME
→ one source of truth for the database filename
```

---

## 4. create_database()

```python
def create_database():
    connection = sqlite3.connect(DB_NAME)
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
```

Flow:

```text
open database
↓
create cursor
↓
create table if needed
↓
commit
↓
close connection
```

---

## 5. insert_case()

```python
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

    connection.close()

    return case_id
```

Flow:

```text
Python values
↓
parameterized SQL
↓
INSERT
↓
database creates a new row
↓
cursor.lastrowid
↓
return new id
```

---

## 6. cursor.lastrowid

```python
case_id = cursor.lastrowid
```

After an INSERT, SQLite creates a new primary key.

Example:

```text
new row created
↓
id = 7
↓
cursor.lastrowid = 7
```

The API can return that id to the client.

---

## 7. get_all_cases()

```python
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
```

This powers:

```text
GET /cases
```

---

## 8. get_case_by_id()

```python
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
```

Difference:

```text
fetchall()
→ many rows

fetchone()
→ one row
```

---

## 9. get_cases_by_priority()

```python
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
```

This powers:

```text
GET /cases?priority=high
```

Mental model:

```text
Query Parameter
↓
priority = "high"
↓
SQL WHERE priority = ?
↓
filter rows
```

---

## 10. FastAPI Setup

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from typing import Literal

app = FastAPI()
```

Uvicorn command:

```bash
python3 -m uvicorn main:app --reload
```

Meaning:

```text
main
→ main.py

app
→ variable named app inside main.py
```

---

## 11. Pydantic Request Model

```python
class CaseCreate(BaseModel):
    customer: constr(strip_whitespace=True, min_length=1)
    issue: constr(strip_whitespace=True, min_length=1)
    priority: Literal["high", "medium", "low"]
```

Flow:

```text
JSON Request Body
↓
Pydantic
↓
field check
↓
type / constraint check
↓
valid data only
```

---

## 12. POST /cases

```python
@app.post("/cases", status_code=201)
def create_case(case: CaseCreate):
    case_id = insert_case(
        case.customer,
        case.issue,
        case.priority
    )

    return {
        "id": case_id,
        "customer": case.customer,
        "issue": case.issue,
        "priority": case.priority
    }
```

Full flow:

```text
Client
↓
POST /cases
↓
FastAPI
↓
Pydantic CaseCreate
↓
create_case()
↓
insert_case()
↓
SQLite INSERT
↓
lastrowid
↓
HTTP 201 response
```

---

## 13. Why status_code=201?

```python
@app.post("/cases", status_code=201)
```

Semantics:

```text
200 OK
→ request succeeded

201 Created
→ request succeeded and created a new resource
```

Important distinction:

```text
insert_case()
→ controls database operation

status_code=201
→ controls HTTP response meaning
```

---

## 14. GET /cases

```python
@app.get("/cases")
def list_cases(priority: str = None):
    if priority is None:
        return get_all_cases()

    return get_cases_by_priority(priority)
```

Behavior:

```text
GET /cases
→ get_all_cases()

GET /cases?priority=high
→ get_cases_by_priority("high")
```

---

## 15. GET /cases/{case_id}

```python
@app.get("/cases/{case_id}")
def get_case(case_id: int):
    row = get_case_by_id(case_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return row
```

Flow:

```text
GET /cases/1
↓
case_id = 1
↓
get_case_by_id(1)
↓
SQLite SELECT WHERE id = ?
↓
row found?
├─ yes → return row
└─ no  → 404
```

---

## 16. HTTPException

```python
raise HTTPException(
    status_code=404,
    detail="Case not found"
)
```

Mental model:

```text
resource does not exist
↓
FastAPI returns HTTP 404
```

HTTP status code is a standardized result label.

---

## 17. Status Codes Used So Far

```text
200 OK
→ request succeeded

201 Created
→ new resource created successfully

404 Not Found
→ requested resource does not exist

422 Validation Error
→ request data does not satisfy Pydantic schema

500 Internal Server Error
→ server-side failure
```

---

## 18. Debugging: Attribute app not found

Error:

```text
Error loading ASGI app.
Attribute "app" not found in module "main".
```

Meaning:

```text
Uvicorn found main.py
↓
but could not find variable named app
```

Checklist:

```text
Is app = FastAPI() present?
Is the spelling exactly "app"?
Is it top-level?
Was the file saved?
Am I in the correct directory?
```

---

## 19. Debugging: ImportError

Example:

```text
ImportError: cannot import name 'insert_case' from 'database'
```

Meaning:

```text
Python found database.py
↓
but database.py does not expose a top-level name called insert_case
```

Typical causes:

```text
wrong spelling
function missing
wrong indentation
file not saved
```

---

## 20. Debugging: NameError

Example:

```text
NameError: name 'issue' is not defined
```

Meaning:

```text
Python reached the name issue
↓
but no variable named issue exists in the current scope
```

Mental model:

```text
arguments passed
↓
function parameters
↓
local variable names
↓
SQL parameters

must line up correctly
```

---

## 21. Swagger UI and 422 Documentation

In /docs, Swagger may display:

```text
422 Validation Error
```

as a possible response schema.

Important distinction:

```text
Swagger documentation says 422 is possible
≠
actual request returned 422
```

Actual status should be checked under:

```text
Try it out
↓
Execute
↓
Server response
```

---

## 22. Full Day 10 Architecture

```text
Client
↓
HTTP Request
↓
FastAPI route
↓
Pydantic validation
↓
Python handler function
↓
database.py
↓
SQLite
↓
database result
↓
handler logic
↓
HTTP status code + response body
↓
Client
```

---

## 23. Layer Responsibilities

```text
FastAPI
→ HTTP / routing

Pydantic
→ input schema and validation

Python handler
→ orchestration / business decision

database.py
→ SQL access

SQLite
→ persisted state
```

---

## 24. Connection to Enterprise Agent Engineering

Future architecture:

```text
User / Frontend
↓
FastAPI
↓
Pydantic
↓
Agent Orchestrator
↓
Business Rules
↓
Tools
├─ Database
├─ Internal API
├─ External API
└─ MCP server
↓
Response
```

Day 10 matters because production Agents still need:

```text
API boundary
input validation
state storage
tool execution
error handling
HTTP semantics
```

---

## 25. Key Takeaways

1. FastAPI and SQLite connect through normal Python functions.
2. main.py should focus on API behavior.
3. database.py should focus on data access.
4. Pydantic validates input before database operations.
5. cursor.lastrowid returns the new row id.
6. fetchall() returns multiple records.
7. fetchone() returns one record.
8. Query Parameters map naturally to SQL WHERE.
9. 201 Created means resource creation succeeded.
10. 404 Not Found means the requested resource does not exist.
11. HTTP status codes communicate result semantics to clients.
12. ImportError often means the requested name is missing from the module.
13. NameError often means a variable is not defined in the current scope.
14. Swagger documentation and actual server response are different things.
15. The most important flow is request → validation → database → response.

---

## 26. What I Should Be Able to Explain After Day 10

```text
How FastAPI connects to SQLite
Why main.py and database.py are separated
What DB_NAME does
What cursor.lastrowid does
Difference between fetchall() and fetchone()
How POST /cases creates a database record
How GET /cases reads records
How GET /cases?priority=high maps to SQL WHERE
How GET /cases/{case_id} retrieves one record
Why missing data should return 404
Why successful creation should return 201
What HTTPException does
How Pydantic protects the database layer from bad input
How to interpret common ImportError / NameError problems
```

---

## Next: Day 11

```text
Complete CRUD API
↓
UPDATE
↓
DELETE
↓
PUT vs PATCH concepts
↓
HTTP status semantics
```
