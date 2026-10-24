from app.core.llm import ask_llm

ROUTES = {"data", "document", "anomaly"}

SYSTEM_PROMPT = """You are a router. Classify the user's question into exactly one label.

The sales table has ONLY these columns: order_id, order_date, product, category, region, quantity, unit_price.

Labels:
- data: a number computed from those sales columns (totals, rankings, counts, trends, comparisons by product, category, region or date)
- anomaly: unusual, suspicious, outlier or abnormal orders or records
- document: anything else. This includes policies, rules, fees, costs, prices of services, time limits, refunds, returns, shipping, warranty, gift cards, loyalty points, discounts, support hours or contacts. These answers are written in text documents, not in the sales table.

If the question needs information that is not one of the sales columns, choose document.

Examples:
Q: Total revenue by category -> data
Q: Which region sold the most units? -> data
Q: Top 3 products by quantity -> data
Q: Are there any unusual orders? -> anomaly
Q: Show suspicious orders -> anomaly
Q: How many points do I need for a 5 dollar discount? -> document
Q: What is the express shipping cost? -> document
Q: When do gift cards expire? -> document
Q: How long is the laptop warranty? -> document
Q: What is the refund window? -> document

Reply with ONLY the label: data, document, or anomaly."""


def route_question(question: str) -> str:
    answer = ask_llm(SYSTEM_PROMPT, question).strip().lower()
    for route in ROUTES:
        if route in answer:
            return route
    return "data"
