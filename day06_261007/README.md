# Day 06 - Customer Support Workflow v1

## Project Goal

This project integrates the concepts learned in Day 1–5 into one small workflow.

The workflow reads customer support cases from a JSON file, validates the input, applies business rules, calculates SLA, and creates a task through an external API.

The goal is not only to make the code run, but also to practice separating responsibilities between different modules.

---

## Workflow

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

Project Structure
day06/
├── main.py
├── data_loader.py
├── validator.py
├── business_rules.py
├── api_tools.py
├── customer_cases.json
└── README.md

Module Responsibilities

data_loader.py
Reads customer case data from a JSON file.
Main responsibilities:
- Open JSON file
- Convert JSON into Python data
- Handle FileNotFoundError
- Handle JSONDecodeError

validator.py
Checks whether the input data structure is valid.
Validation rules:
- customer must be a non-empty string
- issue must be a non-empty string
- priority must be a non-empty string
Example:
if not isinstance(customer, str) or not customer.strip():
return False


business_rules.py
Contains deterministic business logic.
Main responsibilities:
- Normalize priority
- Check whether priority is supported
- Calculate SLA
Supported priorities: high，medium，low

SLA rules:
high   → 4 hours
medium → 8 hours
low    → 24 hours

Unsupported priorities such as: urgent
will not continue to the API execution step.

api_tools.py
Contains the external API tool.
Main responsibilities:
- Load API token from environment variables
- Validate required credentials
- Build HTTP headers
- Build POST payload
- Send POST request
- Handle HTTP errors
- Return API response data
The tool uses: requests.post() to create a task.


main.py
Acts as the workflow orchestrator.
It does not contain all business logic itself.
Instead, it coordinates other modules:
Load data
↓
Validate case
↓
Check business rules
↓
Calculate SLA
↓
Create task

This separation makes the code easier to maintain and extend.
Example Input
{
  "customer": "Toyota",
  "issue": "Cannot login to production system",
  "priority": "HIGH"
}

Example Output
Customer: Toyota
SLA: 4 hours

Created task:
{
  "title": "[Toyota-Cannot login to production system]",
  "completed": false,
  "userId": 1,
  "id": 201
}

Validation Example
If the customer field is empty:
{
  "customer": "   ",
  "issue": "Dashboard is loading slowly",
  "priority": "low"
}

the workflow stops before API execution:
Invalid case

Business Rule Example
If priority is unsupported:
{
  "customer": "Mazda",
  "issue": "Production service is unavailable",
  "priority": "urgent"
}

the workflow returns:
Unsupported priority: urgent

and does not create a task.
Environment Variable
The API token is stored outside the source code.
Example .env:
API_TOKEN=abc123

The .env file must not be committed to GitHub.
Example .gitignore:
.env
__pycache__/
*.pyc


Agent / Harness Connection
This project is still deterministic and does not use an LLM yet.
However, the architecture already resembles an Agent runtime:
Input
↓
Validation
↓
Business Rules
↓
Orchestration
↓
Tool Execution
↓
External System

Later, an LLM can be inserted into this workflow to handle fuzzy tasks such as:
- understanding customer intent
- classifying issues
- selecting tools
- generating structured arguments
Deterministic logic such as validation, permissions, SLA rules, and API execution should remain controlled by code.
Security Considerations
Before executing an external tool, the workflow checks:
- Is the input valid?
- Is the business value supported?
- Is the API credential available?
This reduces the risk of invalid or unauthorized tool execution.
Future versions can add:
- authorization
- RBAC
- human approval
- audit logging
- tool permission scopes
- input schema validation
Current Limitation
This project uses JSONPlaceholder as a test API.
The API does not permanently store created tasks, and returned IDs are simulated.
The current userId is also fixed as:
user_id = 1


In a real enterprise system, the user ID would usually come from authentication context, ownership rules, or an upstream system.
Next Step
The next version can introduce:
- cleaner orchestration
- workflow state
- structured output
- real API integration
- FastAPI
- database storage
- LLM-based classification
- Agent tool calling

