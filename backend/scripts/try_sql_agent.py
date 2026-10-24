import sys

from app.agents.sql_agent import generate_sql
from app.core.database import get_connection
from app.services.sql_guard import check_sql

question = " ".join(sys.argv[1:]) or "Which product has the highest total revenue?"
print("Question:", question)

sql = generate_sql(question)
print("SQL:", sql)

ok, reason = check_sql(sql)
print("Guard:", "PASSED" if ok else f"BLOCKED ({reason})")

if ok:
    print("Result:", get_connection().execute(sql).fetchall())