from fastapi import FastAPI
from pydantic import BaseModel

from core import run_llm

app = FastAPI(title="Servicenow Assistant AI API")


class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
def ask_question(request: QueryRequest):

    result = run_llm(
        query=request.query,
        chat_history=None,
    )

    return {
        "answer": result.get("result", "")
    }
