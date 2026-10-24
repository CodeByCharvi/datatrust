from app.core.database import get_connection

Z_THRESHOLD = 3.0


def find_anomalies(z_threshold: float = Z_THRESHOLD) -> list[dict]:
    sql = """
        WITH scored AS (
            SELECT
                order_id, order_date, product, region, quantity, unit_price,
                AVG(quantity) OVER (PARTITION BY product) AS avg_qty,
                STDDEV_SAMP(quantity) OVER (PARTITION BY product) AS std_qty
            FROM sales
        )
        SELECT
            order_id, order_date, product, region, quantity,
            ROUND(avg_qty, 1) AS typical_quantity,
            ROUND((quantity - avg_qty) / std_qty, 1) AS z_score
        FROM scored
        WHERE std_qty > 0
          AND ABS((quantity - avg_qty) / std_qty) > ?
        ORDER BY ABS((quantity - avg_qty) / std_qty) DESC
    """
    cursor = get_connection().execute(sql, [z_threshold])
    columns = [d[0] for d in cursor.description]
    rows = []
    for row in cursor.fetchall():
        item = dict(zip(columns, row))
        item["order_date"] = item["order_date"].isoformat()
        rows.append(item)
    return rows