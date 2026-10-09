# Day 3 - 2026-10-03
# Error Handling, Modularization & Tool Calling Basics

## 1. `try / except`

### What it is
`try / except` is used to handle errors without letting the entire program crash immediately.

### Basic pattern
```python
try:
    # code that may fail
except SomeError:
    # what to do if that error occurs
```

### Example: file not found
```python
try:
    with open("customer_cases.json", "r") as file:
        customer_cases = json.load(file)
except FileNotFoundError:
    print("File not found")
```

### Key point
A real system must not only design for the success path.

```text
Do something
↓
Success → continue
Failure → catch error → handle / retry / stop safely
```

This becomes very important later in Agent Harness engineering.

---

## 2. `FileNotFoundError`

The program tried to open a file that does not exist at the specified path.

```python
except FileNotFoundError:
    print(f"Error: {filename} was not found.")
    return []
```

### Engineering lesson
The program should fail safely instead of crashing without explanation.

---

## 3. `JSONDecodeError`

The file exists, but the content is not valid JSON.

```python
except json.JSONDecodeError:
    print(f"Error: {filename} is not valid JSON.")
    return []
```

### Important distinction
```text
FileNotFoundError
= the file cannot be found

JSONDecodeError
= the file exists, but its content cannot be parsed
```

---

## 4. Data Validation

Valid JSON does not mean valid business data.

### Risky approach
```python
priority = customer["priority"]
```

If `priority` is missing, Python raises `KeyError`.

### Safer approach
```python
priority = customer.get("priority")
```

or:

```python
priority = customer.get("priority", "unknown")
```

### Validation questions
- Does the field exist?
- Is the value the expected type?
- Is the value allowed?
- Should an unknown value be rejected or given a default?

The same idea later applies to API responses, LLM structured output, and Agent tool results.

---

## 5. Modularization

Day 3 structure:

```text
day03/
├── main.py
├── data_loader.py
├── sla.py
└── customer_case.json
```

### Responsibilities

`data_loader.py`
- Read JSON
- Handle file and JSON errors

`sla.py`
- Store SLA business rules

`main.py`
- Coordinate the workflow

### Engineering concept
This is **separation of concerns**: each module should ideally have one clear responsibility.

---

## 6. `import`

```python
from data_loader import load_customer_cases
from sla import get_sla
```

This means using functions defined in another Python module.

```text
Python file ≈ module
Function inside module ≈ reusable capability
```

---

## 7. `main()` and Program Entry Point

```python
def main():
    customer_cases = load_customer_cases("customer_case.json")

    for customer in customer_cases:
        priority = customer.get("priority", "unknown").lower()
        print(get_sla(priority))


if __name__ == "__main__":
    main()
```

### Key point
`main()` organizes the application's main execution flow.

For now, remember:

> `if __name__ == "__main__":` means run `main()` when this file is executed directly.

---

## 8. Tool Registry / Dispatcher

### Direct call
```python
get_sla("high")
```

### Tool registry
```python
tools = {
    "get_sla": get_sla
}
```

### Dynamic call
```python
tool_name = "get_sla"
result = tools[tool_name]("high")
```

This changes the flow from:

```text
hard-coded function call
```

to:

```text
tool name
↓
Tool Registry
↓
function
↓
result
```

This is an important bridge toward Agent Tool Calling.

---

## 9. Connection to AI Agents

A future LLM may output:

```json
{
  "tool": "get_sla",
  "priority": "high"
}
```

Then the application:

```text
LLM chooses tool
↓
Program finds tool
↓
Python function / API executes
↓
Result returns to LLM
```

A useful mental model:

```text
Agent Tool ≈ function or API that an LLM is allowed to select and call
```

---

## 10. Connection to Agent Harness

Today's error handling already connects to Harness engineering.

```text
Agent calls tool
↓
Tool fails
↓
What should the runtime do?
```

Possible decisions:
- Retry
- Stop
- Fallback
- Ask a human
- Log the error
- Return a safe failure response

So `try / except` is not only Python syntax. It introduces the idea of **reliable execution**.

---

## Built Today

- Split the project into multiple Python modules.
- Added JSON loading.
- Handled `FileNotFoundError`.
- Handled `JSONDecodeError`.
- Practiced safer field access with `.get()`.
- Used `import` across Python files.
- Learned the role of `main()`.
- Built a simple Tool Registry / Dispatcher concept.
- Connected Python functions to future Agent Tool Calling.

---

## Key Engineering Takeaways

1. Real systems must handle failure, not only success.
2. Valid file format does not guarantee valid business data.
3. Modules improve maintainability and reuse.
4. Functions become reusable capabilities.
5. A Tool Registry allows dynamic function selection.
6. Agent tools are usually ordinary functions or APIs underneath.
7. Error handling is foundational to reliable Agent Harness design.

---

## Next: Day 4 - 2026-10-04

- HTTP basics
- Client / Server
- Request / Response
- REST API
- GET / POST
- Headers
- JSON response
- Status codes
- Call an external API from Python
- Connect API calls to the Agent Tool concept
