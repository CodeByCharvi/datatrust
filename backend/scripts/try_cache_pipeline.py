import time

from app.agents.pipeline import ask_datatrust

questions = [
    "Total revenue by category",
    "Total revenue per category",
    "Total revenue by region",
]

for q in questions:
    start = time.time()
    out = ask_datatrust(q)
    seconds = time.time() - start
    print(f"{seconds:5.1f}s | cache hit: {out['cache']['hit']} | status: {out['status']} | {q}")