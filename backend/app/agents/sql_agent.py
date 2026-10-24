import re

from app.core.database import get_schema
from app.core.llm import ask_llm


def _schema_text() -> str:
    lines = []
    for table, cols in get_schema().items():
        col_text = ", ".join(f"{c['column']} ({c['type']})" for c in cols)
        lines.append(f"Table {table}: {col_text}")
    return "\n".join(lines)


SYSTEM_PROMPT = """You are a SQL expert for DuckDB.
Write exactly ONE read-only SELECT query that answers the user's question.

Rules:
- Use ONLY the tables and columns listed in the schema below. Never invent a column.
- Revenue means quantity * unit_price (there is no revenue column).
- Output ONLY the SQL. No explanation, no markdown, no comments.
- If the question cannot be answered with the schema, output exactly: CANNOT_ANSWER

Schema:
{schema}
"""


def _clean(text: str) -> str:
    """Remove markdown code fences if the model added them."""
    text = text.strip()
    text = re.sub(r"^```(?:sql)?", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text).strip()
    return text


def generate_sql(question: str, previous_sql: str | None = None, error: str | None = None) -> str:
    prompt = SYSTEM_PROMPT.format(schema=_schema_text())
    user_message = question
    if previous_sql and error:
        user_message += (
            f"\n\nYour previous SQL failed.\nPrevious SQL: {previous_sql}\n"
            f"Error: {error}\nFix it. Use only columns from the schema."
        )
    return _clean(ask_llm(prompt, user_message))