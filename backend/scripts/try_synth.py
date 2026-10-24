import json
import sys

from app.agents.synthesizer import synthesize
from app.agents.verifier import generate_verified_sql

question = " ".join(sys.argv[1:]) or "Total revenue by category"
verified = generate_verified_sql(question)

if verified["status"] != "ok":
    print("Could not produce a safe query:", verified["status"])
else:
    print("SQL:", verified["sql"])
    print(json.dumps(synthesize(question, verified["sql"]), indent=2))