from sqlalchemy import inspect, text


engine = None

def set_engine(e):
    global engine
    engine = e

def get_engine():
    return engine


def ensure_book_management_columns():
    book_columns = {
        column["name"] for column in inspect(engine).get_columns("books")
    }

    with engine.begin() as connection:
        if "is_lendable" not in book_columns:
            connection.execute(text(
                "ALTER TABLE books ADD COLUMN is_lendable BOOLEAN NOT NULL DEFAULT TRUE"
            ))
        if "retired_on" not in book_columns:
            connection.execute(text(
                "ALTER TABLE books ADD COLUMN retired_on DATE NULL"
            ))