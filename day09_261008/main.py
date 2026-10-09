from fastapi import FastAPI
from pydantic import BaseModel, constr
from typing import Literal

class CaseCreate(BaseModel):
    customer:constr(strip_whitespace=True, min_length=1)
    # constr就是带规则的String，去掉前后空格 -> 长度至少是1
    issue:constr(strip_whitespace=True, min_length=1)
    priority:Literal["high", "medium", "low"]
#class代表定义数据结构，BaseModel 就是 Pydantic 提供的“模板能力”

app = FastAPI()
#创建一个FastAPI的Application

@app.post("/cases")
def create_case(case: CaseCreate):
#case = 一个符合 CaseCreate 结构的 Python 对象
    return{
        "message": "Case received",
        "case": case
    }

@app.get("/")
#这里的 / 是网站最根部的路径。
def root():
    return{
        "message": "Hello FastAPI"
    }

@app.get("/cases/{case_id}")
def get_case(case_id: int):
    return{
        "case_id": case_id
    }

@app.get("/cases")
def get_case(priority: str = None):
    return{
        "priority": priority
    }
