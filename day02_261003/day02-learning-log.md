# Day 2 - JSON & File I/O

## 1. JSON

### What it is
JSON is a text format used to store and exchange structured data between systems.

### Key points
- JSON is text, not Python code.
- Objects use `{}`.
- Arrays use `[]`.
- Keys and string values use double quotes.
- JSON is commonly used by APIs, LLM structured output, and MCP-based tools.

### Example
```json
[
  {
    "customer": "Toyota",
    "priority": "HIGH"
  }
]
```

---

## 2. Python dict / list vs JSON

### Python
```python
customer_cases = [
    {
        "customer": "Toyota",
        "priority": "HIGH"
    }
]
```

### JSON
```json
[
  {
    "customer": "Toyota",
    "priority": "HIGH"
  }
]
```

### Key difference
- Python `dict` / `list` are runtime data structures.
- JSON is a text representation used for storage or data exchange.

---

## 3. Reading JSON in Python

```python
import json

with open("customer_cases.json", "r") as file:
    customer_cases = json.load(file)
```

### Key points
- `import json` loads Python's built-in JSON module.
- `open(..., "r")` opens a file for reading.
- `json.load(file)` converts JSON file content into Python data structures.

Typical flow:

```text
JSON file
↓
json.load()
↓
Python list / dict
↓
Business logic
```

---

## 4. Writing JSON in Python

```python
summary = {
    "total_cases": len(customer_cases),
    "status": "processed"
}

with open("summary.json", "w") as file:
    json.dump(summary, file, indent=4)
```

### Key points
- `"w"` means write mode.
- `json.dump()` converts Python data into JSON and writes it to a file.
- `indent=4` makes the JSON easier to read.

---

## 5. String normalization

```python
priority = customer["priority"].lower()
```

### Why it matters
Different users or systems may provide:

```text
HIGH
High
high
```

Using `.lower()` normalizes them to:

```text
high
```

This reduces unnecessary branching and data inconsistency.

---

## 6. Useful string / list / dict methods

### String
```python
.lower()
.upper()
.strip()
```

- `.lower()` → lowercase
- `.upper()` → uppercase
- `.strip()` → remove leading/trailing spaces

### List
```python
.append()
.remove()
len()
```

### Dict
```python
.get()
.keys()
.values()
.items()
```

`.get()` is useful when a key may not exist:

```python
owner = customer.get("owner", "Not assigned")
```

---

## 7. JSONDecodeError

### Error encountered
```text
json.decoder.JSONDecodeError:
Expecting value: line 1 column 1 (char 0)
```

### Meaning
Python found the file, but could not parse its content as valid JSON.

### Common causes
- File is empty.
- Invalid JSON syntax.
- Missing double quotes.
- Extra commas.
- Python code such as `customer_cases =` was written inside the JSON file.

### Debugging approach
Check the file content:

```bash
cat customer_cases.json
```

The important distinction:

```text
FileNotFoundError
= file cannot be found

JSONDecodeError
= file exists, but its content cannot be parsed as JSON
```

---

## 8. Engineering Takeaways

1. Enterprise systems frequently exchange data in JSON.
2. Python programs often convert JSON into `list` and `dict` before processing it.
3. Data should be normalized before applying business rules.
4. Input data can be malformed, so parsing and validation matter.
5. Error messages are useful debugging information, not just failures.

---

## 9. Connection to AI Agents

Agent systems frequently use JSON for:

- Tool input/output
- API responses
- Structured LLM output
- MCP messages
- Workflow state

Typical pattern:

```text
LLM / Agent
↓
Structured JSON
↓
Python
↓
Business logic / Tool execution
```

This is why understanding JSON and basic file I/O is foundational for Agent Engineering.

---

## Built Today

- Read structured customer data from a JSON file.
- Converted JSON into Python list/dict data.
- Normalized priority values with `.lower()`.
- Processed business rules using existing Python logic.
- Learned how to write Python data back to JSON.
- Debugged a `JSONDecodeError`.

---

## Next: Day 3

- `try / except`
- Error handling
- Splitting code into modules
- `import` between Python files
- Understanding functions as the foundation of Agent tools
