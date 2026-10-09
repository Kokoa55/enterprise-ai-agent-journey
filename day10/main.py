from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from typing import Literal

from database import(
    create_database,
    insert_case,
    get_all_cases,
    get_case_by_id,
    get_cases_by_priority
)

app = FastAPI()

class CaseCreate(BaseModel):
    customer: constr(strip_whitespace=True, min_length=1)
    issue: constr(strip_whitespace=True,min_length=1)
    priority: Literal["high","medium","low"]

create_database()

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


@app.get("/cases")
def list_cases(priority:str = None):
    if priority is None:
        return get_all_cases()
        #查全部
    return get_cases_by_priority(priority)
        #只查high

@app.get("/cases/{case_id}")
def get_case(case_id: int):
    row = get_case_by_id(case_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return row