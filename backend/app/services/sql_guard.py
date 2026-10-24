import re

import sqlglot
from sqlglot import exp

BLOCKED_WORDS = {
    "drop", "delete", "update", "insert", "alter", "create", "truncate",
    "attach", "detach", "copy", "export", "import", "install", "load",
    "pragma", "call", "set",
    "read_csv", "read_csv_auto", "read_parquet", "read_json", "read_text", "glob",
}


def _strip_strings(sql: str) -> str:
    """Replace 'text values' with '' so a word inside a value isn't flagged."""
    return re.sub(r"'(?:[^']|'')*'", "''", sql)


def check_sql(sql: str) -> tuple[bool, str]:
    if not sql or not sql.strip():
        return False, "Empty query"

    cleaned = _strip_strings(sql)

    if "--" in cleaned or "/*" in cleaned:
        return False, "SQL comments are not allowed"

    words = set(re.findall(r"[a-z_]+", cleaned.lower()))
    bad = words & BLOCKED_WORDS
    if bad:
        return False, f"Blocked keyword: {sorted(bad)[0]}"

    try:
        statements = sqlglot.parse(sql, read="duckdb")
    except sqlglot.errors.ParseError:
        return False, "Could not parse SQL"

    statements = [s for s in statements if s is not None]
    if len(statements) != 1:
        return False, "Only one statement is allowed"

    if not isinstance(statements[0], (exp.Select, exp.Union)):
        return False, "Only SELECT queries are allowed"

    return True, "ok"