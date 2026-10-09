# Day 09 - 2026-10-08
# FastAPI Fundamentals

## 1. Day 09 Goal

Day 09 introduced FastAPI and the basic structure of a backend API service.

Before Day 09:

```text
Python script
↓
direct function calls
↓
SQLite / external API
```

After Day 09:

```text
Client
↓
HTTP Request
↓
FastAPI
↓
Python Function
↓
HTTP Response
```

Main concepts:

```text
FastAPI
Uvicorn
Endpoint / Route
GET
POST
Path Parameter
Query Parameter
Request Body
Pydantic
BaseModel
Validation
Literal
Swagger UI
OpenAPI
Response
```

---

## 2. FastAPI and Uvicorn

```python
from fastapi import FastAPI

app = FastAPI()
```

`FastAPI()` creates the API application.

Uvicorn runs the web server:

```bash
python3 -m uvicorn main:app --reload
```

Meaning:

```text
main
→ main.py

app
→ the app variable inside main.py

--reload
→ restart automatically when code changes
```

Mental model:

```text
FastAPI
→ define the API

Uvicorn
→ run the API server
```

A normal Python script usually runs once and exits.

A web server must keep running:

```text
start
↓
wait for request
↓
process request
↓
return response
↓
wait for next request
```

To stop Uvicorn:

```text
Ctrl + C
```

---

## 3. Endpoint / Route

An endpoint is:

```text
HTTP method + URL path
```

Examples:

```text
GET /cases
POST /cases
GET /cases/1
```

Example:

```python
@app.get("/")
def root():
    return {
        "message": "Hello FastAPI"
    }
```

Meaning:

```text
GET /
↓
FastAPI matches @app.get("/")
↓
root() executes
↓
return value becomes response
```

When a browser opens:

```text
http://127.0.0.1:8000/
```

it normally sends:

```text
GET /
```

---

## 4. Swagger UI and OpenAPI

FastAPI automatically provides:

```text
/docs
```

This is Swagger UI.

Swagger UI is generated from FastAPI's OpenAPI schema.

Flow:

```text
FastAPI code
↓
OpenAPI schema
↓
Swagger UI
↓
/docs
```

OpenAPI is a machine-readable API specification.

FastAPI exposes it at:

```text
/openapi.json
```

Mental model:

```text
OpenAPI
= API machine-readable manual

Swagger UI
= visual interface for that manual
```

---

## 5. Path Parameter

Example:

```python
@app.get("/cases/{case_id}")
def get_case(case_id: int):
    return {
        "case_id": case_id
    }
```

Request:

```text
GET /cases/1
```

FastAPI extracts:

```python
case_id = 1
```

and executes:

```python
get_case(1)
```

`case_id: int` tells FastAPI that the parameter should be an integer.

---

## 6. Query Parameter

Example:

```python
@app.get("/cases")
def get_cases(priority: str = None):
    return {
        "priority": priority
    }
```

Request:

```text
GET /cases?priority=high
```

FastAPI extracts:

```python
priority = "high"
```

Difference:

```text
/cases/123
→ Path Parameter
→ identify one resource

/cases?priority=high
→ Query Parameter
→ filter a group of resources
```

This maps naturally to SQL:

```sql
SELECT * FROM customer_cases
WHERE id = 123;
```

↔

```text
GET /cases/123
```

and:

```sql
SELECT * FROM customer_cases
WHERE priority = 'high';
```

↔

```text
GET /cases?priority=high
```

---

## 7. `priority: str = None`

```python
priority: str
```

means the value is expected to be a string.

```python
= None
```

means the parameter is optional.

So:

```text
/cases
→ priority = None

/cases?priority=high
→ priority = "high"
```

---

## 8. POST and Request Body

POST commonly sends data to the server.

Example JSON:

```json
{
  "customer": "Toyota",
  "issue": "Cannot login",
  "priority": "high"
}
```

This is sent inside the:

```text
Request Body
```

Ways to send POST requests:

```text
/docs
curl
Postman
Python requests
frontend JavaScript
another backend service
```

`/docs` is only a test client.

---

## 9. Pydantic

Pydantic is used for:

```text
data modeling
data validation
type checking
parsing
```

Mental model:

```text
Pydantic
= data model + validation tool
```

---

## 10. Why `class`?

Example:

```python
class CaseCreate(BaseModel):
    customer: str
    issue: str
    priority: str
```

This does not create one concrete customer case.

It defines a:

```text
data model
template
schema
new Python type
```

Mental model:

```text
CaseCreate
= blueprint

actual request data
= object created from that blueprint
```

---

## 11. What is `BaseModel`?

`BaseModel` comes from Pydantic.

```python
from pydantic import BaseModel
```

Then:

```python
class CaseCreate(BaseModel):
```

means:

```text
CaseCreate inherits Pydantic's modeling and validation capabilities
```

These capabilities include:

```text
field validation
type validation
error messages
serialization
JSON conversion
```

---

## 12. How JSON Becomes `case`

Endpoint:

```python
@app.post("/cases")
def create_case(case: CaseCreate):
```

The important part is:

```python
case: CaseCreate
```

Meaning:

```text
FastAPI expects the request body to match CaseCreate.
```

Flow:

```text
Client sends JSON
↓
FastAPI receives Request Body
↓
Pydantic checks CaseCreate
↓
valid
↓
CaseCreate object is created
↓
create_case(case) executes
```

Then:

```python
case.customer
case.issue
case.priority
```

can be used inside the function.

---

## 13. Pydantic Validation

If the client sends:

```json
{
  "customer": "Toyota",
  "issue": "Cannot login"
}
```

but `priority` is required, Pydantic rejects the request before the business function normally runs.

Flow:

```text
Request
↓
Pydantic validation
↓
invalid
↓
reject request
↓
business function does not run
```

This connects to Day 06:

```text
Day 06
→ manual validate_case()

Day 09
→ schema-driven Pydantic validation
```

---

## 14. `constr`

Example:

```python
from pydantic import constr
```

```python
customer: constr(
    strip_whitespace=True,
    min_length=1
)
```

Meaning:

```text
remove surrounding whitespace
↓
require at least one character
```

Examples:

```text
"Toyota"
→ valid

"  Toyota  "
→ valid

"   "
→ invalid

""
→ invalid
```

---

## 15. `Literal`

Example:

```python
from typing import Literal
```

```python
priority: Literal["high", "medium", "low"]
```

Meaning:

```text
priority can only be:

high
medium
low
```

Examples:

```text
high
→ valid

medium
→ valid

urgent
→ invalid
```

This replaces part of the manual Day 06 business-rule validation.

---

## 16. Response

Example:

```python
return {
    "message": "Case received",
    "case": case
}
```

FastAPI converts the Python return value into an HTTP JSON response.

Flow:

```text
Python return value
↓
FastAPI
↓
JSON Response
↓
Client
```

---

## 17. Full Day 09 Flow

```text
Client
↓
HTTP Request
↓
FastAPI Route
↓
Path / Query / Body parsing
↓
Pydantic Validation
↓
Python Function
↓
return
↓
FastAPI builds HTTP Response
↓
Client
```

---

## 18. Important Errors / Confusions

### Uvicorn could not import `main`

Error:

```text
Could not import module "main"
```

Cause:

Uvicorn was started from the wrong directory.

Correct:

```bash
cd ~/enterprise-ai-agent-journey/day09
python3 -m uvicorn main:app --reload
```

---

### Wrong response syntax

Incorrect:

```python
return(
    "message": "Case received",
    "case": case
)
```

Correct:

```python
return {
    "message": "Case received",
    "case": case
}
```

Because:

```text
{}
→ dictionary

()
→ parentheses / tuple-style grouping
```

---

## 19. Concepts to Remember, Not Syntax to Memorize

```text
FastAPI()
→ create application

@app.get(...)
→ define GET endpoint

@app.post(...)
→ define POST endpoint

BaseModel
→ define data model

constr(...)
→ string constraint

Literal[...]
→ allowed value constraint

Uvicorn
→ run server
```

The goal is not to memorize every library function.

The goal is to remember:

```text
what problem each tool solves
```

---

## 20. Connection to Previous Days

Day 04–06:

```text
Python acted as API client
↓
requests.get/post()
↓
external API
```

Day 09:

```text
Python FastAPI acts as API server
↓
receives requests
↓
executes Python functions
```

Now both sides are visible:

```text
Client side
and
Server side
```

---

## 21. Agent Engineering Connection

Future architecture:

```text
User
↓
FastAPI
↓
Pydantic Input Schema
↓
Agent / LLM
↓
Tool Call
↓
Database / External API
↓
Response
```

Pydantic schemas will later connect directly to:

```text
Structured Output
Tool Schemas
Agent Tool Calling
MCP
API Contracts
```

---

## 22. Key Takeaways

1. FastAPI defines HTTP APIs.
2. Uvicorn runs the server.
3. Endpoint = HTTP method + path.
4. Browser URL access usually sends GET.
5. Path parameters identify resources.
6. Query parameters usually filter resources.
7. POST commonly sends data in Request Body.
8. `/docs` is Swagger UI.
9. Swagger UI is generated from OpenAPI.
10. Pydantic defines and validates data models.
11. `CaseCreate` is a schema, not one concrete case.
12. `case: CaseCreate` tells FastAPI how to parse the request body.
13. Invalid data can be rejected before business logic runs.
14. `constr` adds string constraints.
15. `Literal` restricts allowed values.
16. FastAPI converts Python return values into HTTP responses.
17. Understand the flow first; look up exact syntax when needed.

---

## 23. What I Should Be Able to Explain After Day 09

```text
What FastAPI is
What Uvicorn is
What an endpoint / route is
What @app.get("/") means
Difference between Path and Query Parameters
What Request Body means
Why POST uses Request Body
What /docs is
What Swagger UI is
What OpenAPI is
What Pydantic is
Why Pydantic uses class
What BaseModel does
How JSON becomes a CaseCreate object
Why invalid data is rejected
What constr does
What Literal does
How FastAPI creates a response
```

---

## Next: Day 10

```text
FastAPI + SQLite integration

POST /cases
→ validate request
→ insert into database

GET /cases
→ read from database

GET /cases/{case_id}
→ retrieve one record

Basic backend CRUD API
```

Architecture:

```text
Client
↓
HTTP API
↓
FastAPI
↓
Pydantic
↓
SQLite
```
