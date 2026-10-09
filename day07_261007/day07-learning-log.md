# Day 07 - 2026-10-07
# Refactoring, Entry Points & Debugging Mental Model

## 1. Day 07 Goal

Day 07 focused on consolidation and refactoring rather than learning many new concepts.

Main goals:

- Refactor Day 06 into a cleaner program structure
- Understand `if __name__ == "__main__":`
- Separate orchestration from per-case processing
- Review common Python / data / config / API errors
- Build a reusable debugging mental model
- Practice testing failure paths deliberately

---

## 2. Standard Python Entry Point

We refactored `main.py` into:

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

### Meaning

When running:

```bash
python3 main.py
```

Python sets:

```python
__name__ = "__main__"
```

so this condition becomes true:

```python
if __name__ == "__main__":
```

and `main()` executes.

But when another file does:

```python
import main
```

then inside `main.py`:

```python
__name__ = "main"
```

so the workflow does not execute automatically.

---

## 3. Small Experiment: Run vs Import

We created:

```python
import main

print("import_test.py finished")
```

### Direct run

```bash
python3 main.py
```

Result:

```text
__name__ = __main__
```

The workflow runs.

### Import

```bash
python3 import_test.py
```

Result:

```text
__name__ = main
import_test.py finished
```

The workflow does not run automatically.

### Why this matters

A Python file can be used in two ways:

```text
Directly executed
or
Imported as a module
```

The `__main__` guard lets us control that behavior.

---

## 4. Refactoring main.py

Instead of putting all logic into one `main()` function, we introduced:

```python
def process_case(case):
    ...
```

Then `main()` became simpler:

```python
def main():
    cases = load_customer_cases("customer_cases.json")

    for case in cases:
        print("---------------")
        print(case)
        process_case(case)
```

### Responsibility split

```text
main()
→ overall workflow

process_case(case)
→ handle one customer case
```

This is another example of:

```text
Separation of Concerns
```

---

## 5. `continue` vs `return`

In Day 06 we used:

```python
continue
```

inside the `for` loop.

In Day 07, after moving case logic into:

```python
process_case(case)
```

we used:

```python
return
```

Example:

```python
if not validate_case(case):
    print("Invalid case")
    return
```

### Difference

```text
continue
→ skip current loop iteration

return
→ exit current function
```

Because `process_case()` handles only one case, `return` ends that case and control goes back to `main()`.

Then the `for` loop continues with the next case.

---

# 6. Debugging Mental Model

One of the most important Day 07 outcomes was building a layered model for debugging.

Instead of thinking:

```text
"The program is broken"
```

we classify the problem by layer.

```text
Program Problem
├── Python code problem
├── Input data problem
├── Configuration problem
└── External system problem
```

This makes debugging faster and more systematic.

---

# 7. Layer 1: Python Code Problems

These are errors in the code itself.

Typical examples:

```text
SyntaxError
IndentationError
ImportError
```

---

## 7.1 SyntaxError

### Example problem

Wrong:

```python
def validate_case(case)
```

Missing:

```text
:
```

Correct:

```python
def validate_case(case):
```

Another possible example:

```python
if customer == "Toyota"
```

Correct:

```python
if customer == "Toyota":
```

### Who detects it?

Python itself.

The interpreter cannot parse the code.

### Typical things to inspect

```text
:
()
[]
{}
quotes
spelling
unfinished expressions
```

### Mental model

```text
Python cannot understand the grammar of my code.
```

---

## 7.2 IndentationError

### Example problem

```python
def create_task(...):
    token = ...

        try:
            ...
```

The `try:` has an unexpected extra indentation level.

Correct:

```python
def create_task(...):
    token = ...

    try:
        ...
```

### Who detects it?

Python interpreter.

### Typical places to inspect

```text
def
if
for
while
try
except
```

Check whether blocks are aligned correctly.

### Mental model

```text
Python understands the words,
but the block structure is wrong.
```

---

## 7.3 ImportError

### Example

```python
from business_rules import is_supported_priority
```

But `business_rules.py` does not contain:

```python
def is_supported_priority(...):
```

Possible causes:

```text
Function was not created
Function name is misspelled
File was not saved
Wrong module version
```

### Simple checks

Check the source file:

```python
def is_supported_priority(priority):
    ...
```

Or inspect the module:

```python
import business_rules
print(dir(business_rules))
```

Then look for:

```text
is_supported_priority
```

### Mental model

```text
Python found the module,
but could not find the name I asked for.
```

---

# 8. Layer 2: Input Data Problems

Here the Python program itself can run.

The problem is the data.

Two important categories from Day 06/07:

```text
Invalid case
Unsupported priority
```

---

## 8.1 Invalid Case

### Example data

```json
{
  "customer": "   ",
  "issue": "Dashboard is loading slowly",
  "priority": "low"
}
```

The structure contains the field, but the customer value is effectively empty.

### Validation code

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

### Main workflow check

```python
if not validate_case(case):
    print("Invalid case")
    return
```

### What this checks

```text
Field exists
Value is a string
Value is not empty
Value is not whitespace-only
```

### Mental model

```text
The data format / structure is not acceptable.
```

---

## 8.2 Unsupported Priority

### Example

```json
{
  "priority": "urgent"
}
```

This is a valid non-empty string.

So structural validation passes.

But the business rule only accepts:

```text
high
medium
low
```

### Business rule check

```python
def is_supported_priority(priority):
    priority = priority.strip().lower()

    supported_priorities = [
        "high",
        "medium",
        "low"
    ]

    return priority in supported_priorities
```

### Main workflow check

```python
if not is_supported_priority(case["priority"]):
    print(f"Unsupported priority: {case['priority']}")
    return
```

### Mental model

```text
The data is structurally valid,
but not allowed by business rules.
```

---

# 9. Validation vs Business Rule

This distinction is critical.

Example:

```text
priority = "urgent"
```

Validation asks:

```text
Is this a valid string?
```

Result:

```text
Yes
```

Business rules ask:

```text
Is this an allowed priority?
```

Result:

```text
No
```

Therefore:

```text
Validation
≠
Business Rule
```

---

# 10. Layer 3: Configuration Problems

These happen when the program needs environment setup or credentials.

Day 07 example:

```text
API_TOKEN missing
```

---

## 10.1 Missing API Token

### `.env`

Wrong / empty:

```text
API_TOKEN=
```

or the key is missing entirely.

### Read configuration

```python
token = os.getenv("API_TOKEN")
```

### Check configuration

```python
if not token:
    raise ValueError("API_TOKEN is missing")
```

### Debug check

```python
print("Token loaded:", bool(token))
```

Possible output:

```text
Token loaded: False
```

### Mental model

```text
The code is fine.
The input may be fine.
But the runtime environment is missing required configuration.
```

---

## 10.2 Why Fail Fast?

Instead of sending:

```text
Authorization: Bearer None
```

we stop early:

```python
raise ValueError("API_TOKEN is missing")
```

This is called:

```text
Fail Fast
```

It makes the real root cause easier to find.

---

# 11. Layer 4: External System Problems

These happen after the program actually attempts to call another system.

Examples:

```text
Network failure
Timeout
DNS failure
Connection error
HTTP 4xx
HTTP 5xx
```

---

## 11.1 requests.RequestException

Example:

```python
try:
    response = requests.post(
        url,
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

### What each part does

```python
requests.post(...)
```

tries to send the request.

```python
timeout=5
```

prevents waiting forever.

```python
response.raise_for_status()
```

turns HTTP 4xx / 5xx into exceptions.

```python
except requests.RequestException
```

catches common request/network/HTTP failures.

### Mental model

```text
My program reached the external system call,
but communication or the server response failed.
```

---

# 12. Full Debugging Decision Tree

A practical sequence:

```text
Program fails
↓
1. Is Python unable to run the code?
   ↓
   SyntaxError / IndentationError / ImportError
↓
2. Does the program run, but reject a case?
   ↓
   Validator / Business Rule
↓
3. Does it stop before the API call?
   ↓
   Configuration / API_TOKEN
↓
4. Does it fail while calling the API?
   ↓
   requests / network / HTTP
```

---

# 13. Four Gatekeepers

A useful way to remember Day 07:

```python
# 1. Structural validation
validate_case(case)

# 2. Business rule validation
is_supported_priority(priority)

# 3. Configuration validation
if not token:
    raise ValueError(...)

# 4. External call protection
try:
    requests.post(...)
except requests.RequestException:
    ...
```

These four layers protect the workflow before and during side effects.

---

# 14. Failure Path Testing

We deliberately created failures instead of only testing success.

### Test 1: Invalid customer

```json
{
  "customer": "   "
}
```

Expected:

```text
Invalid case
```

### Test 2: Unsupported priority

```json
{
  "priority": "urgent"
}
```

Expected:

```text
Unsupported priority: urgent
```

### Test 3: Missing API token

```text
API_TOKEN=
```

Expected:

```text
ValueError: API_TOKEN is missing
```

### Test 4: Broken JSON

```json
{
  "customer": "Toyota"
  "issue": "Cannot login"
}
```

Expected:

```text
Invalid JSON format: customer_cases.json
```

The loader then returns:

```python
[]
```

and the loop has nothing to process.

---

# 15. Why Testing Failure Paths Matters

A program is not reliable just because:

```text
Happy path works.
```

Real enterprise software must also behave predictably when:

```text
Input is invalid
Configuration is missing
Business value is unsupported
External API fails
```

This principle will later become even more important in:

```text
Agent Harness
Tool Calling
MCP
RAG pipelines
LLM APIs
Agent Security
```

---

# 16. Agent / Harness Connection

The Day 07 debugging model maps naturally to future Agent systems.

```text
Agent Input
↓
Input Validation
↓
Business / Policy Rules
↓
Credential / Permission Check
↓
Tool Execution
↓
External System
```

Possible future failure layers:

```text
Bad tool arguments
Unsupported action
Missing credential
Insufficient permission
Tool timeout
API 500
LLM malformed output
```

The same layered debugging mindset still applies.

---

# 17. Key Engineering Takeaways

1. `if __name__ == "__main__":` separates direct execution from import behavior.
2. `main()` should coordinate the workflow.
3. `process_case()` should handle one case.
4. `continue` and `return` solve different control-flow problems.
5. Debugging should start by identifying the failure layer.
6. Syntax, data, configuration, and external system problems are different categories.
7. Validation and business rules are not the same.
8. Fail fast when required configuration is missing.
9. Test failure paths deliberately.
10. A reliable system is defined by both success behavior and failure behavior.

---

# 18. What I Should Be Able to Explain After Day 07

```text
Why use if __name__ == "__main__"
Difference between direct run and import
Difference between continue and return
Difference between validation and business rules
What SyntaxError means
What IndentationError means
What ImportError means
How to detect invalid data
How to detect unsupported business values
How to detect missing configuration
How to handle external API failures
How to classify an error before debugging it
```

---

# 19. Day 07 Mental Model Summary

```text
Program Problem
├── Python Code
│   ├── SyntaxError
│   ├── IndentationError
│   └── ImportError
│
├── Input Data
│   ├── Invalid case
│   └── Unsupported priority
│
├── Configuration
│   └── API_TOKEN missing
│
└── External System
    └── requests.RequestException
```

The most important habit:

> Do not immediately change random code when something fails.

First ask:

```text
Which layer failed?
```

Then inspect the corresponding code.

---

# Next: Day 08

Planned focus:

```text
SQL fundamentals
tables / rows / columns
SELECT
WHERE
INSERT
UPDATE
basic SQLite
connect Python workflow to persistent data
```

This will begin moving the project from file-based data toward a small backend-style system.
