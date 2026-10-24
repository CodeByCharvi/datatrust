from datetime import date, datetime
from decimal import Decimal

from app.core.database import get_connection
from app.core.llm import ask_llm

MAX_ROWS = 100

SUMMARY_PROMPT = """You write short answers for business users.
Using ONLY the data below, answer the question in 1-2 plain sentences.
Do not use any number that is not in the data. Do not mention SQL.
Do not add currency symbols or units unless they appear in the data.

Question: {question}
Columns: {columns}
Rows: {rows}"""


def _clean_value(v):
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


def _pick_chart(columns, rows):
    if len(rows) == 1 and len(columns) == 1:
        return "number"
    if len(columns) == 2 and rows:
        first, second = rows[0][0], rows[0][1]
        second_is_number = isinstance(second, (int, float))
        if isinstance(first, str) and len(first) == 10 and first[4] == "-" and second_is_number:
            return "line"
        if isinstance(first, str) and second_is_number:
            return "bar"
    return "table"


def synthesize(question: str, sql: str) -> dict:
    cursor = get_connection().execute(sql)
    columns = [d[0] for d in cursor.description]
    rows = [[_clean_value(v) for v in row] for row in cursor.fetchmany(MAX_ROWS)]

    answer = ask_llm(
        "You are a careful data analyst.",
        SUMMARY_PROMPT.format(question=question, columns=columns, rows=rows[:20]),
    ).strip()

    return {
        "columns": columns,
        "rows": rows,
        "chart": _pick_chart(columns, rows),
        "answer": answer,
    }