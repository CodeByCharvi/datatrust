from app.services.sql_guard import check_sql


def test_allows_normal_select():
    ok, _ = check_sql("SELECT product, SUM(quantity) FROM sales GROUP BY product")
    assert ok


def test_allows_trailing_semicolon():
    ok, _ = check_sql("SELECT * FROM sales LIMIT 5;")
    assert ok


def test_allows_blocked_word_inside_a_value():
    ok, _ = check_sql("SELECT * FROM sales WHERE product = 'drop'")
    assert ok


def test_blocks_drop_table():
    ok, _ = check_sql("DROP TABLE sales")
    assert not ok


def test_blocks_second_statement():
    ok, _ = check_sql("SELECT 1; SELECT 2")
    assert not ok


def test_blocks_file_read():
    ok, _ = check_sql("SELECT * FROM read_csv('C:/secret.csv')")
    assert not ok


def test_blocks_comment_trick():
    ok, _ = check_sql("SELECT * FROM sales WHERE region = 'North' -- ' OR 1=1")
    assert not ok