from app.services.semantic_cache import cache

cache.add("Total revenue by category", {"fake": "result"})

tests = [
    "Total revenue by category",
    "Total revenue per category",
    "What is the revenue for each category?",
    "Total revenue by region",
    "Which region sold the most units?",
]

for q in tests:
    score, _ = cache.best_match(q)
    status = "HIT " if cache.get(q) else "MISS"
    print(f"{score:.2f} | {status} | {q}")