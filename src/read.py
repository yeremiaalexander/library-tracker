import pandas as pd
from sqlalchemy import text
import db


def prettify_df(df):
    df.columns = [c.upper() if c == "isbn" else c.replace("_", " ").capitalize() for c in df.columns]
    return df.fillna("")


def read_friends():
    engine = db.get_engine()
    query = "SELECT * FROM friends"
    return pd.read_sql(query, con=engine)


def read_books(available_only=False):
    engine = db.get_engine()
    if available_only:
        query = """
            SELECT b.*
            FROM books AS b
            LEFT JOIN loans AS l
                ON b.isbn = l.isbn
                AND l.status = 'out'
            WHERE l.loan_id IS NULL
                AND b.is_lendable = TRUE
        """
    else:
        query = "SELECT * FROM books"

    return pd.read_sql(query, con=engine)


def read_lent_books():
    engine = db.get_engine()
    query = """
        SELECT
            b.isbn,
            b.title,
            b.publisher,
            b.published_year,
            l.loan_date,
            l.due_date,
            f.full_name AS borrower,
            l.status
        FROM books AS b
        JOIN loans AS l ON l.isbn = b.isbn
        JOIN friends AS f ON f.friend_id = l.friend_id
        WHERE l.status = 'out'
        ORDER BY l.due_date
    """
    return pd.read_sql(query, con=engine)


def read_loans():
    engine = db.get_engine()
    query = """
        SELECT
            l.loan_id,
            l.isbn,
            f.full_name AS friend_name,
            l.friend_id,
            l.loan_date,
            l.due_date,
            l.return_date,
            l.condition_out,
            l.condition_in,
            l.status,
            l.notes,
            l.active_isbn
        FROM loans AS l
        JOIN friends AS f ON f.friend_id = l.friend_id
        ORDER BY l.loan_id
    """
    return pd.read_sql(query, con=engine)



