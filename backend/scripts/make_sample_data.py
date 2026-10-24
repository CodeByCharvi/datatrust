import csv
import random
from datetime import date, timedelta

random.seed(42)

products = {
    "Laptop": ("Electronics", 55000),
    "Phone": ("Electronics", 30000),
    "Headphones": ("Electronics", 2500),
    "Desk": ("Furniture", 8000),
    "Chair": ("Furniture", 5000),
    "Notebook": ("Stationery", 120),
    "Pen Pack": ("Stationery", 80),
}
regions = ["North", "South", "East", "West"]

start = date(2026, 1, 1)
rows = []
for i in range(1, 501):
    product = random.choice(list(products))
    category, price = products[product]
    qty = random.randint(1, 5)
    if i in (123, 287, 411):  # planted anomalies for later
        qty = random.randint(80, 120)
    rows.append({
        "order_id": i,
        "order_date": (start + timedelta(days=random.randint(0, 270))).isoformat(),
        "product": product,
        "category": category,
        "region": random.choice(regions),
        "quantity": qty,
        "unit_price": price,
    })

with open("data/sales.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to data/sales.csv")