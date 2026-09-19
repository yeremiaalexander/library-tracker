import pandas as pd
from sqlalchemy import text
import db


def delete_friend(friend_name):
    engine = db.get_engine()
    friend_query = """
        SELECT friend_id
        FROM friends
        WHERE full_name = :friend_name
    """
    friend_df = pd.read_sql(
        text(friend_query),
        con=engine,
        params={"friend_name": friend_name}
    )

    if friend_df.empty:
        print(f"Error: '{friend_name}' was not found.")
        return

    friend_id = int(friend_df["friend_id"].iloc[0])

    loan_count_query = """
        SELECT COUNT(*) AS loan_count
        FROM loans
        WHERE friend_id = :friend_id
    """
    loan_count_df = pd.read_sql(
        text(loan_count_query),
        con=engine,
        params={"friend_id": friend_id}
    )

    if loan_count_df["loan_count"].iloc[0] > 0:
        print(
            f"Deletion denied: {friend_name} has loan history. "
            "Keep the friend record for history."
        )
        return

    with engine.begin() as connection:
        result = connection.execute(
            text("DELETE FROM friends WHERE friend_id = :friend_id"),
            {"friend_id": friend_id}
        )

    if result.rowcount == 1:
        print(f"Successfully removed {friend_name} from your friends list.")
    else:
        print(f"No friend record was removed for {friend_name}.")


def delete_loan(loan_id):
    engine = db.get_engine()
    loan_query = """
        SELECT status
        FROM loans
        WHERE loan_id = :loan_id
    """
    loan_df = pd.read_sql(
        text(loan_query),
        con=engine,
        params={"loan_id": loan_id}
    )

    if loan_df.empty:
        print(f"Error: Loan ID {loan_id} was not found.")
        return

    current_status = loan_df["status"].iloc[0]

    if current_status == "out":
        print(
            f"Deletion denied: Loan ID {loan_id} is still out. "
            "Return the book first."
        )
        return

    delete_query = "DELETE FROM loans WHERE loan_id = :loan_id"

    with engine.begin() as connection:
        result = connection.execute(
            text(delete_query),
            {"loan_id": loan_id}
        )

    if result.rowcount == 1:
        print(f"Successfully deleted loan record {loan_id}.")
    else:
        print(f"No loan record was deleted for ID {loan_id}.")
