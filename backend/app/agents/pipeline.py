from app.agents.planner import plan_question
from app.agents.router import route_question
from app.agents.synthesizer import synthesize
from app.agents.verifier import generate_verified_sql
from app.services.anomaly import find_anomalies
from app.services.rag import ask_document
from app.services.semantic_cache import cache


def ask_datatrust(question: str) -> dict:
    hit = cache.get(question)
    if hit:
        return {
            **hit["result"],
            "cache": {
                "hit": True,
                "cached_from": hit["cached_from"],
                "similarity": hit["similarity"],
            },
        }

    result = _run_pipeline(question)
    result["cache"] = {"hit": False}

    if result["status"] == "ok":
        cache.add(question, result)

    return result


def _run_pipeline(question: str) -> dict:
    route = route_question(question)

    if route == "document":
        doc = ask_document(question)
        return {
            "route": route,
            "status": "ok",
            "answer": doc["answer"],
            "sources": doc["sources"],
        }

    if route == "anomaly":
        found = find_anomalies()
        return {
            "route": route,
            "status": "ok",
            "chart": "table",
            "columns": list(found[0].keys()) if found else [],
            "rows": [list(a.values()) for a in found],
            "answer": (
                f"Found {len(found)} unusual orders, each far above the normal quantity for its product."
                if found else "No unusual orders found."
            ),
        }

    plan = plan_question(question)
    if not plan["answerable"]:
        return {
            "route": route,
            "status": "cannot_answer",
            "message": "This data does not contain: " + ", ".join(plan["missing_columns"] or ["the needed columns"]),
            "plan": plan,
        }

    verified = generate_verified_sql(question)
    if verified["status"] != "ok":
        return {
            "route": route,
            "status": verified["status"],
            "message": "Could not produce a safe, valid query for this question.",
            "plan": plan,
            "attempts": verified["attempts"],
        }

    result = synthesize(question, verified["sql"])
    return {
        "route": route,
        "status": "ok",
        "plan": plan,
        "sql": verified["sql"],
        "attempts": len(verified["attempts"]),
        **result,
    }