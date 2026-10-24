from app.agents.sql_agent import generate_sql
from app.core.database import get_connection
from app.services.sql_guard import check_sql

MAX_RETRIES = 2


def verify_sql(sql: str) -> tuple[bool, str]:
    if sql.strip() == "CANNOT_ANSWER":
        return False, "CANNOT_ANSWER"

    ok, reason = check_sql(sql)
    if not ok:
        return False, reason

    try:
        get_connection().execute(f"EXPLAIN {sql}")
    except Exception as e:
        return False, f"Database rejected the query: {e}"

    return True, "ok"


def generate_verified_sql(question: str) -> dict:
    sql, feedback = None, None
    attempts = []

    for attempt in range(1, MAX_RETRIES + 2):
        sql = generate_sql(question, previous_sql=sql, error=feedback)
        ok, reason = verify_sql(sql)
        attempts.append({"attempt": attempt, "sql": sql, "ok": ok, "reason": reason})

        if ok:
            return {"status": "ok", "sql": sql, "attempts": attempts}
        if reason == "CANNOT_ANSWER":
            return {"status": "cannot_answer", "sql": None, "attempts": attempts}
        feedback = reason

    return {"status": "failed", "sql": None, "attempts": attempts}