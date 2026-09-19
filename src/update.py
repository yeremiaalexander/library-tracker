from datetime import date

from sqlalchemy import inspect, text
import db


def sanitize_text(new_data):
    if isinstance(new_data, str):
        new_data = new_data.replace("'", "\\'")
    return new_data

def format_field(field):
    if field == "dates":
        return "Contact dates"
    elif field == "isbn":
        return "ISBN"
    else:
        return field.replace("_", " ").capitalize()




def update_friend(friend_id, full_name, email=None, phone=None, notes=None):
    """Update a friend's details (like fixing a name typo, email, or phone) by their friend_id."""
    engine = db.get_engine()

    update_query = """
        UPDATE friends 
        SET 
            full_name = COALESCE(:full_name, full_name),
            email = COALESCE(:email, email), 
            phone = COALESCE(:phone, phone), 
            notes = COALESCE(:notes, notes)
        WHERE friend_id = :friend_id
    """

    with engine.begin() as connection:
        connection.execute(text(update_query), {
            "friend_id": friend_id,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "notes": notes
        })
        
    print(f"Successfully updated information for Friend ID {friend_id}!")

def update_active_loan(isbn, condition_on_out=None, notes=None):
    engine = db.get_engine()
    update_query = """
        UPDATE loans
        SET
            condition_out = COALESCE(:condition_on_out, condition_out),
            notes = COALESCE(:notes, notes)
        WHERE isbn = :isbn AND status = 'out'
    """

    with engine.begin() as connection:
        result = connection.execute(
            text(update_query),
            {
                "isbn": isbn,
                "condition_on_out": condition_on_out,
                "notes": notes,
            },
        )

    if result.rowcount == 1:
        print(f"Successfully updated active loan for ISBN {isbn}.")
    else:
        print(f"No active loan found for ISBN {isbn}.")


def return_loan(loan_id, condition_in, return_date=None, notes=None):
    engine = db.get_engine()
    return_date = return_date or date.today()
    update_query = """
        UPDATE loans
        SET
            return_date = :return_date,
            condition_in = :condition_in,
            status = 'returned',
            notes = COALESCE(:notes, notes)
        WHERE loan_id = :loan_id AND status = 'out'
    """

    with engine.begin() as connection:
        result = connection.execute(
            text(update_query),
            {
                "loan_id": loan_id,
                "return_date": return_date,
                "condition_in": condition_in,
                "notes": notes,
            },
        )

    if result.rowcount == 1:
        return True, "Book returned successfully."
    return False, "This loan is not currently active."


def retire_book(isbn):
    engine = db.get_engine()
    book_columns = {
        column["name"] for column in inspect(engine).get_columns("books")
    }
    retirement_fields = "is_lendable = FALSE"
    if "retired_on" in book_columns:
        retirement_fields += ", retired_on = CURRENT_DATE"

    with engine.begin() as connection:
        active_loan = connection.execute(
            text("""
                SELECT loan_id FROM loans
                WHERE isbn = :isbn AND status = 'out'
            """),
            {"isbn": str(isbn)},
        ).first()
        if active_loan:
            return False, "This book is currently lent and must be returned first."

        result = connection.execute(
            text(f"""
                UPDATE books
                SET {retirement_fields}
                WHERE isbn = :isbn AND is_lendable = TRUE
            """),
            {"isbn": str(isbn)},
        )

    if result.rowcount == 1:
        return True, "Book retired from the library."
    return False, "Book was not found or is already retired."