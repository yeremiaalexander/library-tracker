import pandas as pd
from sqlalchemy import text
import db


def create_book(
    isbn,
    title,
    publisher=None,
    published_year=None,
    current_condition="good",
    shelf_location=None,
    notes=None,
):
    engine = db.get_engine()
    query = """
        INSERT INTO books (
            isbn, title, publisher, published_year, current_condition,
            shelf_location, is_lendable, notes
        )
        VALUES (
            :isbn, :title, :publisher, :published_year, :current_condition,
            :shelf_location, TRUE, :notes
        )
    """

    with engine.begin() as connection:
        connection.execute(text(query), {
            "isbn": str(isbn).strip(),
            "title": title.strip(),
            "publisher": publisher,
            "published_year": published_year,
            "current_condition": current_condition,
            "shelf_location": shelf_location,
            "notes": notes,
        })

    return True, f"Added {title.strip()} to the library."


# Corrected versions
def create_friend(name, email=None, phone=None, notes=None):
    engine = db.get_engine()
    query = """
        INSERT INTO friends (full_name, email, phone, notes)
        VALUES (:name, :email, :phone, :notes)
    """

    with engine.begin() as connection:
        connection.execute(text(query), {
            "name": name,
            "email": email,
            "phone": phone,
            "notes": notes,
        })

    print(f"Human name : {name} successfully added!")


def create_loan_by_name(
    isbn,
    friend_name,
    due_date,
    condition_on_out="good",
    notes=None,
):
    engine = db.get_engine()
    friend_query = """
        SELECT friend_id
        FROM friends
        WHERE full_name = :friend_name
    """
    friend_df = pd.read_sql(
        text(friend_query),
        con=engine,
        params={"friend_name": friend_name},
    )

    if friend_df.empty:
        return False, f"'{friend_name}' is not in your friends list."

    book_query = "SELECT title FROM books WHERE isbn = :isbn"
    book_df = pd.read_sql(
        text(book_query),
        con=engine,
        params={"isbn": str(isbn)},
    )

    if book_df.empty:
        return False, f"No book found with ISBN {isbn}."

    active_loan_query = """
        SELECT loan_id
        FROM loans
        WHERE isbn = :isbn AND status = 'out'
    """
    active_loan_df = pd.read_sql(
        text(active_loan_query),
        con=engine,
        params={"isbn": str(isbn)},
    )

    if not active_loan_df.empty:
        return False, f"{book_df['title'].iloc[0]} is already checked out."

    insert_query = """
        INSERT INTO loans (
            isbn, friend_id, loan_date, due_date,
            condition_out, status, notes
        )
        VALUES (
            :isbn, :friend_id, CURRENT_DATE, :due_date,
            :condition_out, 'out', :notes
        )
    """

    with engine.begin() as connection:
        connection.execute(text(insert_query), {
            "isbn": str(isbn),
            "friend_id": int(friend_df["friend_id"].iloc[0]),
            "due_date": due_date,
            "condition_out": condition_on_out,
            "notes": notes,
        })

    return True, f"Loan successfully recorded for {friend_name}."
