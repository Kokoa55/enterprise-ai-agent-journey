# Day 5 - 2026-10-05
# API Authentication, Secrets & Agent Security Basics

## 1. API Authentication

Authentication answers:

> Who are you?

Real enterprise APIs often require credentials.

Common methods:

```text
API Key
Bearer Token
OAuth
```

Day 5 focused on API Key and Bearer Token concepts.

---

## 2. HTTP Headers

Headers carry metadata about a request.

```python
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
```

### Meaning

```text
Authorization
→ authentication information

Bearer <token>
→ send a token as the credential

Content-Type: application/json
→ request body is JSON
```

Useful mental model:

```text
URL
→ Where am I calling?

params
→ What am I filtering?

headers
→ Who am I / how am I communicating?

body
→ What data am I sending?
```

---

## 3. Bearer Token

```python
token = "abc123"

headers = {
    "Authorization": f"Bearer {token}"
}
```

This produces:

```text
Authorization: Bearer abc123
```

The token is a credential.

Do not hard-code real tokens in source code.

Bad:

```python
API_TOKEN = "real-secret-token"
```

Better:

```python
token = os.getenv("API_TOKEN")
```

---

## 4. API Key

Another common credential format:

```python
headers = {
    "X-API-Key": "abc123"
}
```

Some APIs use query parameters for API keys, but sensitive credentials should generally not be exposed unnecessarily in URLs.

---

## 5. POST Requests

`GET` usually retrieves data.

`POST` usually submits or creates data.

```python
payload = {
    "title": "Prepare customer meeting",
    "completed": False,
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/todos",
    json=payload,
    timeout=5
)
```

`json=payload` converts a Python dict into JSON and places it in the HTTP request body.

---

## 6. API Wrapper Function

```python
def create_task(title, user_id):
    token = os.getenv("API_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "title": title,
        "completed": False,
        "userId": user_id
    }

    try:
        response = requests.post(
            "https://jsonplaceholder.typicode.com/todos",
            headers=headers,
            json=payload,
            timeout=5
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"Create task failed: {error}")
        return None
```

The caller only needs business inputs:

```python
create_task("Prepare customer meeting", 1)
```

The function handles:
- token loading
- headers
- payload
- POST
- timeout
- HTTP errors

This is close to a real enterprise Agent Tool.

---

## 7. Environment Variables

Instead of putting secrets directly in code:

```python
API_TOKEN = "abc123"
```

store them outside source code.

Terminal:

```bash
export API_TOKEN="abc123"
```

Python:

```python
import os

token = os.getenv("API_TOKEN")
```

`os.getenv("API_TOKEN")` reads the environment variable named `API_TOKEN`.

---

## 8. `.env`

A local `.env` file can store environment variables:

```text
API_TOKEN=abc123
```

Using `python-dotenv`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("API_TOKEN")
```

### Error encountered

```text
python-dotenv could not parse statement starting at line 1
```

and:

```text
Authorization: Bearer None
```

This meant the `.env` file could not be parsed, so `os.getenv("API_TOKEN")` returned `None`.

Correct syntax:

```text
API_TOKEN=abc123
```

---

## 9. `.gitignore`

Secrets should not be committed to GitHub.

Project-level `.gitignore`:

```text
.env
__pycache__/
*.pyc
```

Important rule:

```text
.env
```

should not appear in `git status` as a file to be committed.

If a real secret has already been committed, revoke / rotate the secret. Removing it from the current file alone is not enough.

---

## 10. Secret Validation

Do not continue with:

```text
Authorization: Bearer None
```

Instead:

```python
token = os.getenv("API_TOKEN")

if not token:
    raise ValueError("API_TOKEN is missing")
```

If a required credential is missing, fail early and clearly.

---

## 11. Input Validation

```python
if not isinstance(title, str) or not title.strip():
    raise ValueError("Task title must be a non-empty string")
```

### `isinstance()`

```python
isinstance(title, str)
```

checks whether `title` is a string.

### `not`

Reverses a boolean result.

### `.strip()`

Removes leading and trailing spaces.

```python
"   ".strip()
→ ""
```

### `or`

The condition is true if either side is true.

Full meaning:

> If `title` is not a string OR becomes empty after removing spaces, reject it.

---

## 12. Authentication vs Authorization

### Authentication

```text
Who are you?
```

Examples:
- API Token
- Login
- Service identity

### Authorization

```text
What are you allowed to do?
```

Examples:
- Can this user read salary data?
- Can this Agent create tasks?
- Can this Agent delete records?

A valid token does not imply unlimited permission.

---

## 13. Approval

Authorization and approval are different.

Example:

```text
Agent prepares action
↓
Human approves
↓
Tool executes action
```

This becomes important in enterprise Agent design.

---

## 14. Connection to Agent Security

An Agent becomes operationally risky when it can use real credentials.

```text
Agent
↓
create_task()
↓
API Token
↓
POST /tasks
↓
Real enterprise system
```

The problem is no longer only:

```text
Did the LLM answer correctly?
```

It becomes:

```text
Was the Agent allowed to perform this action?
```

Key risks:
- Credential leakage
- Excessive permissions
- Invalid tool inputs
- Unauthorized actions
- Unapproved execution

---

## 15. Connection to Agent Harness

A future runtime may need:

```text
Tool Schema
↓
Input Validation
↓
Authentication
↓
Authorization
↓
Human Approval
↓
Execution
↓
Audit Log
```

This is where Harness and Security begin to overlap.

---

# Built / Practiced Today

- Learned Bearer Token and API Key concepts.
- Used HTTP headers.
- Sent POST requests.
- Used JSON request bodies.
- Loaded secrets from environment variables.
- Used `.env`.
- Added project-level `.gitignore`.
- Prevented `.env` from being committed.
- Validated missing secrets.
- Practiced input validation.
- Understood Authentication vs Authorization.
- Connected API credentials to Agent execution risk.

---

# Key Engineering Takeaways

1. Credentials must not be hard-coded into source code.
2. `.env` is convenient for local development, but must be ignored by Git.
3. Missing secrets should fail clearly and early.
4. Valid credentials do not imply unlimited authorization.
5. Agent tool inputs must be validated before execution.
6. POST introduces real write/action capability.
7. Once an Agent can use enterprise credentials, security becomes part of runtime design.
8. Harness engineering and Agent Security overlap around permissions, validation, approvals, and auditability.

---

# Next: Day 6 - 2026-10-06

Planned focus:
- Consolidate Day 1–5 into one mini project
- Build a simple Customer Support Workflow v1
- Separate business logic, API tools, and orchestration
- Add structured input and validation
- Add deterministic rules
- Add one external API tool
- Introduce a simple workflow state
- Draw the first architecture diagram
- Start README for the first portfolio-style project
