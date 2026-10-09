# Day 4 - 2026-10-04
# HTTP, REST API & Agent Tool Foundations

## 1. Client / Server / Request / Response

A basic HTTP interaction looks like:

```text
Client
↓ Request
Server
↓ Response
Client
```

In today's exercises:

```text
Python program = Client
JSONPlaceholder = Server
requests.get(...) = HTTP Request
response = HTTP Response
```

### Key idea
An API allows one software system to interact with another through defined interfaces.

---

## 2. HTTP GET

`GET` is mainly used to retrieve data.

```python
import requests

url = "https://jsonplaceholder.typicode.com/todos/1"
response = requests.get(url)
```

The returned `response` object contains:
- HTTP status
- response headers
- response body
- final request URL

---

## 3. HTTP Status Codes

Important codes learned today:

```text
200 = OK
201 = Created
400 = Bad Request
401 = Unauthorized
403 = Forbidden
404 = Not Found
500 = Server Error
```

### Important lesson

A `404` response is still an HTTP response.

```python
response = requests.get(url)
```

does not normally raise an exception just because the server returned `404`.

To turn HTTP 4xx / 5xx responses into Python exceptions:

```python
response.raise_for_status()
```

---

## 4. `requests.get()` vs `raise_for_status()`

### `requests.get()`

```python
response = requests.get(url, timeout=5)
```

Main responsibility:
- send HTTP request
- establish connection
- receive an HTTP response

It may raise exceptions for problems such as:
- connection failure
- DNS failure
- timeout
- SSL / network errors

### `response.raise_for_status()`

```python
response.raise_for_status()
```

Main responsibility:
- inspect HTTP status code
- raise `HTTPError` for 4xx / 5xx responses

### Mental model

```text
requests.get()
→ Did HTTP communication complete?

raise_for_status()
→ Was the HTTP result successful?
```

A response exists does **not** mean the business request succeeded.

---

## 5. API Error Handling

```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()

except requests.RequestException as error:
    print(f"API request failed: {error}")
```

### Execution flow

```text
requests.get()
↓
Network error?
├─ Yes → except
└─ No
   ↓
raise_for_status()
↓
4xx / 5xx?
├─ Yes → except
└─ No
   ↓
response.json()
↓
Continue
```

### Harness connection
Agent tools may fail because of:
- timeout
- API outage
- permission failure
- bad request
- unavailable resource

Reliable Agent runtimes must handle these failures explicitly.

---

## 6. JSON Response

An API often returns JSON.

```python
data = response.json()
```

This converts the response JSON into Python data structures.

Example:

```python
print(type(data))
```

may return:

```text
<class 'dict'>
```

Flow:

```text
API
↓ JSON
response.json()
↓
Python dict / list
```

This connects directly to Day 1–2 concepts.

---

## 7. Path Parameter

Example:

```text
/todos/1
```

Here `1` identifies a specific resource.

```python
todo_id = 1
url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
```

Typical enterprise patterns:

```text
/customers/123
/projects/456
/tasks/789
```

---

## 8. Query Parameter

Example:

```text
/todos?userId=1
```

This usually means:
> retrieve todos filtered by `userId = 1`

Recommended Python approach:

```python
params = {
    "userId": 1
}

response = requests.get(
    "https://jsonplaceholder.typicode.com/todos",
    params=params
)
```

`requests` automatically creates the URL query string.

For multiple parameters:

```python
params = {
    "userId": 1,
    "completed": "true"
}
```

becomes approximately:

```text
?userId=1&completed=true
```

### Difference

```text
/todos/1
→ identify one resource

/todos?userId=1
→ filter a collection
```

---

## 9. Headers

Headers carry metadata about the request.

Example:

```python
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}
```

Then:

```python
response = requests.get(
    url,
    headers=headers,
    timeout=5
)
```

Useful mental model:

```text
URL
→ Where am I calling?

params
→ What am I filtering/searching?

headers
→ Who am I / how are we communicating?

body
→ What data am I sending?
```

---

## 10. GET vs POST

### GET
Usually retrieves data.

```python
requests.get(...)
```

### POST
Usually submits or creates data.

```python
payload = {
    "title": "New Task",
    "completed": False,
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/todos",
    json=payload,
    timeout=5
)
```

`json=payload` sends the Python dict as a JSON request body.

---

## 11. Wrapping an API as a Function

```python
def get_todo(todo_id):
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"API request failed: {error}")
        return None
```

### Why this matters
The caller only needs:

```python
get_todo(1)
```

It does not need to know:
- URL construction
- timeout settings
- HTTP status handling
- exception handling

This is **encapsulation**.

---

## 12. Query API Function

```python
def get_user_todos(user_id):
    url = "https://jsonplaceholder.typicode.com/todos"

    params = {
        "userId": user_id
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"API request failed: {error}")
        return None
```

This combines:
- function parameters
- query parameters
- GET
- JSON
- status handling
- exceptions

---

## 13. Tool Registry

```python
tools = {
    "get_todo": get_todo,
    "get_user_todos": get_user_todos
}
```

Then:

```python
tool_name = "get_todo"
result = tools[tool_name](1)
```

This is equivalent to:

```python
result = get_todo(1)
```

### Why `(1)` works

`tools[tool_name]` returns the function itself:

```python
tools["get_todo"]
→ get_todo
```

Therefore:

```python
tools["get_todo"](1)
```

means:

```python
get_todo(1)
```

Python functions can be stored in variables, lists, or dictionaries and called later.

---

## 14. Function Parameter Types & Agent Calls

Python itself is dynamically typed.

```python
get_todo(1)
get_todo("1")
```

may both execute depending on the implementation.

For Agent tool calling, production systems usually define a schema such as:

```json
{
  "todo_id": {
    "type": "integer"
  }
}
```

The Agent should produce structured parameters matching the schema.

However:

> Never blindly trust model-generated tool arguments.

Production systems should still validate:
- type
- required fields
- allowed values
- permissions
- business rules

This introduces:

```text
Structured Input
+
Schema
+
Validation
```

which is fundamental to reliable Agent Engineering.

---

## 15. Connection to AI Agents

Today's complete chain:

```text
LLM / Agent
↓
Select Tool
↓
Tool Registry
↓
Python Function
↓
HTTP API
↓
External Enterprise System
↓
JSON Result
↓
Agent
```

Example future Agent decision:

```json
{
  "tool": "get_todo",
  "todo_id": 1
}
```

The runtime could:
1. Validate `todo_id`
2. Find `get_todo`
3. Execute `get_todo(1)`
4. Receive JSON result
5. Return result to the LLM

This is the foundation of Agent Tool Calling.

---

# Built Today

- Called an external HTTP API from Python.
- Parsed JSON responses.
- Tested successful and 404 responses.
- Used `raise_for_status()`.
- Combined API calls with `try / except`.
- Used path parameters.
- Used query parameters.
- Learned the role of headers.
- Learned GET vs POST.
- Wrapped APIs into reusable functions.
- Connected API functions to a Tool Registry.
- Understood how tool arguments need schema and validation.

---

# Key Engineering Takeaways

1. HTTP communication success and HTTP business success are different.
2. A 404 response is still a valid HTTP response.
3. `raise_for_status()` converts HTTP failure codes into exceptions.
4. APIs commonly exchange JSON.
5. Path and query parameters serve different purposes.
6. API logic should be encapsulated in functions.
7. External APIs are a common implementation of Agent tools.
8. Tool inputs must be structured and validated.
9. Network failures must be expected in production systems.
10. Reliable Agent systems combine LLM decisions with deterministic engineering controls.

---

# Next: Day 5 - 2026-10-05

Planned focus:

- API Authentication
- Bearer Token / API Key concepts
- Headers in more depth
- POST request bodies
- Request / response inspection
- Better API wrapper design
- Secrets and environment variables
- Why credentials must not be hard-coded
- Connection to enterprise Agent security
