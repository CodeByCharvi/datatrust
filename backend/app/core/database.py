from pathlib import Path

import duckdb

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

_conn = None


def get_connection():
    """Create the DuckDB connection once and load sales.csv into a table."""
    global _conn
    if _conn is None:
        _conn = duckdb.connect(database=":memory:")
        csv_path = (DATA_DIR / "sales.csv").as_posix()
        _conn.execute(
            f"CREATE TABLE sales AS SELECT * FROM read_csv_auto('{csv_path}')"
        )
    return _conn


def get_schema():
    """Return the real tables and columns, the 'label list' for the AI."""
    conn = get_connection()
    rows = conn.execute("DESCRIBE sales").fetchall()
    return {"sales": [{"column": r[0], "type": r[1]} for r in rows]}