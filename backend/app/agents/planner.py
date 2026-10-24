import json
import re

from app.agents.sql_agent import _schema_text
from app.core.database import get_schema
from app.core.llm import ask_llm

SYSTEM_PROMPT = """You are a query planner for a sales database.
Decide which columns are needed to answer the question, and describe the approach in one or two sentences.
Revenue means quantity * unit_price (there is no revenue column).

Schema:
{schema}

Reply with ONLY JSON in this shape:
{{"columns": ["col1", "col2"], "approach": "short plan"}}

If the question needs data that is not in the schema (for example profit, cost, or customer names), still list the columns you think it needs."""


def plan_question(question: str) -> dict:
    raw = ask_llm(SYSTEM_PROMPT.format(schema=_schema_text()), question)

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        plan = json.loads(match.group(0)) if match else {}
    except json.JSONDecodeError:
        plan = {}

    wanted = [str(c) for c in plan.get("columns", [])]
    real = {c["column"] for c in get_schema()["sales"]}
    missing = [c for c in wanted if c not in real]

    return {
        "columns": [c for c in wanted if c in real],
        "missing_columns": missing,
        "approach": plan.get("approach", ""),
        "answerable": len(missing) == 0 and len(wanted) > 0,
    }