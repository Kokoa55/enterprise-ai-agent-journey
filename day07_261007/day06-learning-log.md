# Day 06 - 2026-10-07
# Customer Support Workflow v1

## 1. Day 06 Goal

Day 06 was the first day where the previous lessons were integrated into one small workflow.

The project combined:

```text
Python basics
+ JSON
+ file loading
+ validation
+ business rules
+ API calls
+ POST
+ environment variables
+ secret handling
+ module separation
```

The workflow:

```text
customer_cases.json
        ↓
data_loader.py
        ↓
validator.py
        ↓
business_rules.py
        ↓
main.py
        ↓
api_tools.py
        ↓
External API
```

The important learning goal was not memorizing syntax. It was understanding how different pieces work together.

---

## 2. Project Structure

```text
day06/
├── main.py
├── data_loader.py
├── validator.py
├── business_rules.py
├── api_tools.py
├── customer_cases.json
├── README.md
└── learning-log.md
```

Each file has one main responsibility.

This is called:

```text
Separation of Concerns
```

Instead of putting everything into `main.py`, the system is split into smaller modules.

---

## 3. data_loader.py

Purpose:

```text
Read JSON file
↓
Convert JSON into Python data
↓
Handle file / JSON errors
```

Example:

```python
import json

def load_customer_cases(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON format: {filename}")
        return []
```

Key concepts reviewed:

```text
import
def
open()
with
json.load()
return
try / except
```

---

## 4. validator.py

Purpose:

```text
Check whether input data is structurally valid
```

Example:

```python
def validate_case(case):
    customer = case.get("customer")
    issue = case.get("issue")
    priority = case.get("priority")

    if not isinstance(customer, str) or not customer.strip():
        return False

    if not isinstance(issue, str) or not issue.strip():
        return False

    if not isinstance(priority, str) or not priority.strip():
        return False

    return True
```

Important concepts:

- `.get()` avoids `KeyError` when a field is missing.
- `isinstance(value, str)` checks type.
- `.strip()` removes surrounding whitespace.
- Empty strings are falsy in Python.

---

## 5. Important Bug: Function Object vs Function Call

A major bug during Day 06:

Wrong:

```python
if not validate_case:
```

Correct:

```python
if not validate_case(case):
```

Difference:

```text
validate_case
= function object

validate_case(case)
= execute the function
```

This same concept also appeared with:

```python
requests.post
```

vs:

```python
requests.post(...)
```

---

## 6. business_rules.py

Purpose:

```text
Apply deterministic business rules
```

Example:

```python
def normalize_priority(priority):
    return priority.strip().lower()
```

This converts values such as:

```text
HIGH
High
 high
```

into:

```text
high
```

Supported priority check:

```python
def is_supported_priority(priority):
    priority = normalize_priority(priority)
    supported_priorities = ["high", "medium", "low"]
    return priority in supported_priorities
```

SLA mapping:

```python
def get_sla(priority):
    priority = normalize_priority(priority)

    sla_map = {
        "high": "4 hours",
        "medium": "8 hours",
        "low": "24 hours"
    }

    return sla_map.get(priority, "Unknown SLA")
```

---

## 7. Validation vs Business Rule

This distinction was one of the most important concepts today.

Example:

```text
priority = "urgent"
```

Structurally:

```text
It is a non-empty string
→ valid format
```

Business-wise:

```text
It is not in high / medium / low
→ unsupported value
```

Therefore:

```text
Validation
≠
Business Rule
```

Validator asks:

```text
Is the data structurally valid?
```

Business rules ask:

```text
Is the value allowed by our business logic?
```

---

## 8. continue

Example:

```python
if not validate_case(case):
    print("Invalid case")
    continue
```

`continue` means:

```text
Stop processing the current item
↓
Go directly to the next loop iteration
```

This is useful because invalid data should not continue to later steps.

---

## 9. api_tools.py

Purpose:

```text
Execute an external API action
```

Main responsibilities:

```text
Load token
Validate token
Validate input
Build headers
Build payload
POST request
Handle HTTP errors
Return response data
```

The `.env` file is loaded from the project root.

Example:

```python
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
```

---

## 10. Environment Variable and Secret Validation

Example `.env`:

```text
API_TOKEN=abc123
```

Python:

```python
token = os.getenv("API_TOKEN")
```

If missing:

```python
if not token:
    raise ValueError("API_TOKEN is missing")
```

This is a simple example of:

```text
Fail Fast
```

The program stops before sending a bad API request.

---

## 11. `.env` and `.gitignore`

Secrets should not be committed to GitHub.

Root `.gitignore`:

```text
.env
__pycache__/
*.pyc
```

Useful checks:

```bash
git status
git check-ignore -v .env
git ls-files .env
```

If `.env` was already tracked:

```bash
git rm --cached .env
```

---

## 12. HTTP POST

The workflow creates a task with:

```python
response = requests.post(
    "https://jsonplaceholder.typicode.com/todos",
    headers=headers,
    json=payload,
    timeout=5
)
```

Important difference:

```python
requests.post
```

is only the function object.

```python
requests.post(...)
```

actually executes the request.

---

## 13. Why return response.json()?

A POST request sends data, but the server can still return a response.

```python
response.json()
```

converts returned JSON into Python data.

```python
return response.json()
```

passes that data back to the caller.

Flow:

```text
POST request
↓
Server processes request
↓
HTTP response
↓
response.json()
↓
Python dict
↓
return
```

---

## 14. HTTP 201 vs `"id": 201`

These are different.

HTTP status:

```text
201 Created
```

means the resource was created successfully.

Returned JSON:

```json
{
  "id": 201
}
```

means the created object was assigned an ID.

In a real API, that ID might later be used for:

```text
GET /tasks/201
PATCH /tasks/201
DELETE /tasks/201
```

JSONPlaceholder is a mock API, so returned IDs are simulated.

---

## 15. Fixed userId = 1

Current code uses:

```python
user_id = 1
```

This is fine for the learning project.

In a real system, user ID could come from:

```text
authenticated user
task owner
workflow context
customer account
upstream system
```

---

## 16. main.py as Orchestrator

`main.py` coordinates the workflow:

```text
Load
↓
Validate
↓
Check business rule
↓
Calculate SLA
↓
Call API tool
```

It does not need to know the internal details of every module.

For example:

```python
task = create_task(...)
```

`main.py` only needs to know that it wants to create a task.

The API module handles:

```text
requests.post()
headers
token
timeout
HTTP errors
```

---

## 17. Orchestration and Separation of Concerns

Day 06 introduced:

```text
Orchestration
```

Current orchestration:

```text
data_loader
↓
validator
↓
business_rules
↓
api_tools
```

This idea will later evolve into:

```text
Agent Harness
Workflow Engine
LangGraph
Tool Runtime
```

---

## 18. Side Effects

Calculating SLA is local and deterministic.

Calling:

```python
requests.post(...)
```

can change an external system.

That is a:

```text
Side Effect
```

Before a side effect, the program should check:

```text
input validity
business rules
credentials
permissions
```

Current Day 06 pattern:

```text
Invalid input
→ stop

Unsupported priority
→ stop

Missing token
→ stop

Valid input
→ POST
```

This is an early Agent Security pattern.

---

## 19. Errors Encountered Today

### SyntaxError

Example:

```python
def validate_case(case)
```

Missing `:`.

Correct:

```python
def validate_case(case):
```

### ImportError

Example:

```text
cannot import name 'is_supported_priority'
```

Possible causes:

```text
function not written
name misspelled
file not saved
```

### IndentationError

Example:

```text
unexpected indent
```

Meaning:

```text
Indentation does not match Python's block structure.
```

### API_TOKEN is missing

Example:

```text
ValueError: API_TOKEN is missing
```

This confirmed secret validation was working correctly.

### NotOpenSSLWarning

The Mac environment showed a LibreSSL / urllib3 warning.

This was only a warning and not the cause of workflow failure.

---

## 20. Final Workflow Result

Successful cases:

```text
Toyota
→ high
→ 4 hours
→ task created

Honda
→ medium
→ 8 hours
→ task created

Nissan
→ low
→ 24 hours
→ task created
```

Unsupported case:

```text
Mazda
→ urgent
→ Unsupported priority
→ no API call
```

---

## 21. Key Engineering Takeaways

1. Do not try to memorize every line immediately.
2. Understand responsibilities and flow first.
3. A function object is different from calling a function.
4. Validation and business rules are separate concerns.
5. `continue` stops invalid items from reaching later steps.
6. `main.py` should orchestrate rather than implement everything.
7. External API calls are side effects.
8. Validate before side effects.
9. Secrets belong outside source code.
10. Modules improve maintainability.
11. Deterministic rules should remain deterministic where possible.
12. This architecture is an early foundation for Agent Harness design.

---

## 22. What I Should Be Able to Explain After Day 06

```text
What data_loader does
What validator does
What business_rules does
What api_tools does
Why main.py is an orchestrator
Why validation happens before POST
Why .env should not be committed
Why validate_case differs from validate_case(case)
What response.json() does
Why POST can still return data
```

---

## Next: Day 07

Day 07 will focus on consolidation:

```text
Review Day 01–06
Clean the Git repository
Improve project structure
Refactor main.py
Introduce main() and __name__
Review debugging patterns
Prepare for later FastAPI / Agent upgrades
```
