from app.agents.pipeline import ask_datatrust

questions = [
    "Total revenue by category",
    "What is the profit by region?",
    "What does the uploaded report say about refunds?",
    "Which region sold the most units?",
]

for q in questions:
    out = ask_datatrust(q)
    print("-" * 60)
    print("Q:", q)
    print("Route:", out["route"], "| Status:", out["status"])
    if out["status"] == "ok":
        print("Chart:", out["chart"], "| Attempts:", out["attempts"])
        print("Answer:", out["answer"])
    else:
        print("Message:", out.get("message"))