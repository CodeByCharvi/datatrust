import json
import sys

from app.agents.verifier import generate_verified_sql

question = " ".join(sys.argv[1:]) or "Which region sold the most units?"
print(json.dumps(generate_verified_sql(question), indent=2))