from datetime import date, timedelta

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

import db
from create import create_book, create_friend, create_loan_by_name
from delete import delete_friend
from read import read_books, read_friends, read_lent_books, read_loans
from update import retire_book, return_loan, update_friend


st.set_page_config(page_title="Liana's Library", page_icon="📚", layout="wide")

st.markdown(
    """
    <style>
    .block-container { max-width: 1200px; padding-top: 2rem; }
    .library-hero {
        background: linear-gradient(135deg, #173f35 0%, #285b4d 100%);
        border-radius: 12px;
        padding: 2rem 2.25rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 12px 30px rgba(23, 63, 53, 0.22);
    }
    .library-eyebrow {
        color: #e8b75d;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .library-hero h1 { color: #fffaf0; margin: 0; font-size: 2.35rem; }
    .library-hero p { color: #d8e7df; margin: 0.5rem 0 0; font-size: 1rem; }
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.25rem 0 1.75rem;
    }
    .summary-card {
        display: block;
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
        border-top: 5px solid;
        background: #f6f1e7;
        text-decoration: none !important;
        transition: transform 160ms ease, box-shadow 160ms ease;
    }
    .summary-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 22px rgba(23, 63, 53, 0.16);
    }
    .summary-card .label { color: #52645e; font-size: 0.9rem; font-weight: 600; }
    .summary-card .value { color: #1d2926; font-size: 2rem; font-weight: 800; line-height: 1.2; }
    .summary-card .detail { color: #6d7a74; font-size: 0.78rem; margin-top: 0.35rem; }
    .callout-label { color: #dce7e2; font-size: 0.95rem; font-weight: 700; }
    .callout-value { color: #fffaf0; font-size: 1.55rem; font-weight: 800; line-height: 1.2; }
    .callout-detail { color: #9fb5ad; font-size: 0.82rem; margin-bottom: 0.7rem; }
    .view-kicker {
        color: #e8b75d;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    .view-description { color: #9fb5ad; margin-top: -0.5rem; }
    .collection-pulse {
        color: #dce7e2;
        background: #172d2a;
        border-left: 4px solid #4e8b72;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0 1rem;
    }
    .circulation-pulse {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin: 0.75rem 0 1rem;
    }
    .circulation-stat {
        background: #172d2a;
        border-radius: 8px;
        padding: 0.7rem 0.9rem;
        border-left: 4px solid #4e8b72;
    }
    .circulation-stat.warning { border-left-color: #e87561; }
    .circulation-stat .number { color: #fffaf0; font-size: 1.35rem; font-weight: 800; }
    .circulation-stat .label { color: #9fb5ad; font-size: 0.75rem; }
    @media (max-width: 760px) {
        .circulation-pulse { grid-template-columns: 1fr; }
    }
    .section-kicker {
        color: #e8b75d;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    div[data-testid="stForm"] {
        border: 1px solid #38434b;
        border-radius: 10px;
        padding: 1rem 1.1rem;
        background: #11161d;
    }
    div[data-testid="stForm"] label { color: #dce7e2 !important; }
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
        background: #e87561 !important;
        border-color: #e87561 !important;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #38434b;
        border-radius: 10px;
        overflow: hidden;
    }
    .summary-books { border-color: #4e8b72; }
    .summary-friends { border-color: #6c8fc7; }
    .summary-out { border-color: #e87561; }
    .summary-available { border-color: #e8b75d; }
    div[data-testid="stButton"] > button[aria-label^="Books"] {
        background: #f6f1e7 !important; border-top: 5px solid #4e8b72 !important;
    }
    div[data-testid="stButton"] > button[aria-label^="Friends"] {
        background: #f6f1e7 !important; border-top: 5px solid #6c8fc7 !important;
    }
    div[data-testid="stButton"] > button[aria-label^="Currently out"] {
        background: #f6f1e7 !important; border-top: 5px solid #e87561 !important;
    }
    div[data-testid="stButton"] > button[aria-label^="Available"] {
        background: #f6f1e7 !important; border-top: 5px solid #e8b75d !important;
    }
    div[data-testid="stButton"] > button[aria-label^="Books"],
    div[data-testid="stButton"] > button[aria-label^="Friends"],
    div[data-testid="stButton"] > button[aria-label^="Currently out"],
    div[data-testid="stButton"] > button[aria-label^="Available"] {
        color: #1d2926 !important;
        min-height: 132px;
        white-space: pre-line;
        text-align: left;
        border-radius: 10px;
        box-shadow: 0 5px 16px rgba(23, 63, 53, 0.12);
    }
    div[data-testid="stButton"] > button[aria-label^="Books"]:hover,
    div[data-testid="stButton"] > button[aria-label^="Friends"]:hover,
    div[data-testid="stButton"] > button[aria-label^="Currently out"]:hover,
    div[data-testid="stButton"] > button[aria-label^="Available"]:hover {
        color: #173f35 !important;
        transform: translateY(-3px);
    }
    @media (max-width: 760px) {
        .summary-grid { grid-template-columns: repeat(2, 1fr); }
        .library-hero h1 { font-size: 1.8rem; }
    }
    h2, h3 { color: #dce7e2; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_engine():
    password = st.secrets["mysql"]["password"]
    connection_string = (
        f"mysql+pymysql://root:{password}@127.0.0.1:3306/sample_library"
    )
    return create_engine(connection_string, pool_pre_ping=True)


def load_data(loader):
    try:
        return loader()
    except SQLAlchemyError as error:
        st.error(f"Could not load the database: {error}")
        return None


def humanize_columns(dataframe):
    display = dataframe.copy()
    display.columns = [
        "ISBN" if column == "isbn" else column.replace("_", " ").capitalize()
        for column in display.columns
    ]
    return display


def style_collection(dataframe, active_isbns):
    display = dataframe.copy()
    if "status" not in display.columns:
        display["availability"] = display["isbn"].astype(str).map(
            lambda isbn: "Lent" if isbn in active_isbns else "Available"
        )
    else:
        display["availability"] = display["status"].map(
            {"out": "Lent", "returned": "Available", "lost": "Lost"}
        ).fillna(display["status"])

    display = display.drop(
        columns=["is_lendable", "retired_on", "owner_flag", "status"],
        errors="ignore",
    )
    display = humanize_columns(display)

    def color_availability(value):
        colors = {
            "Available": "color: #2f795c; font-weight: 700",
            "Lent": "color: #c65545; font-weight: 700",
            "Lost": "color: #9b3d3d; font-weight: 700",
        }
        return colors.get(value, "")

    return display.style.map(color_availability, subset=["Availability"])


def style_loan_table(dataframe):
    display = dataframe.copy()
    today = pd.Timestamp(date.today())
    due_dates = pd.to_datetime(display["due_date"], errors="coerce")
    display["loan_status"] = display["status"].map(
        {"out": "Lent", "returned": "Returned", "lost": "Lost"}
    ).fillna(display["status"])
    overdue = (display["status"] == "out") & (due_dates < today)
    display.loc[overdue, "loan_status"] = "Overdue"
    display = display.drop(
        columns=["friend_id", "active_isbn", "status"],
        errors="ignore",
    )
    display = humanize_columns(display)

    def color_status(value):
        colors = {
            "Lent": "color: #c65545; font-weight: 700",
            "Overdue": "color: #a13d35; background-color: #f8d8d0; font-weight: 800",
            "Returned": "color: #2f795c; font-weight: 700",
            "Lost": "color: #9b3d3d; font-weight: 800",
        }
        return colors.get(value, "")

    return display.style.map(color_status, subset=["Loan status"])


try:
    db.set_engine(get_engine())
    db.ensure_book_management_columns()
except KeyError:
    st.error("Missing [mysql] password in .streamlit/secrets.toml.")
    st.stop()
except SQLAlchemyError as error:
    st.error(f"Could not create the database connection: {error}")
    st.stop()


st.markdown(
    """
    <section class="library-hero">
        <div class="library-eyebrow">Liana's personal collection</div>
        <h1>Welcome to the library</h1>
        <p>Keep every book, borrower, and lending moment in one thoughtful place.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

friends = load_data(read_friends)
books = load_data(read_books)
loans = load_data(read_loans)

if friends is None or books is None or loans is None:
    st.stop()

active_loans = loans[loans["status"] == "out"] if "status" in loans else loans

available_count = max(len(books) - len(active_loans), 0)
summary_columns = st.columns(4)
summary_cards = [
    (summary_columns[0], "Books", f"Total books: {len(books)}", "titles", "books"),
    (summary_columns[1], "Friends", f"Total friends: {len(friends)}", "registered borrowers", "friends"),
    (summary_columns[2], "Number of loans", f"{len(active_loans)}", "active loans", "out"),
    (summary_columns[3], "Available to lend", f"{available_count}", "books", "available"),
]
for column, label, value, detail, destination in summary_cards:
    with column:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="callout-label">{label}</div>
                <div class="callout-value">{value}</div>
                <div class="callout-detail">{detail}</div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Open", key=f"summary_{destination}", use_container_width=True):
                st.query_params["page"] = destination
                st.rerun()

page = st.query_params.get("page", "home")
if page not in {"home", "books", "friends", "out", "available"}:
    page = "home"

if page in {"books", "available"}:
    st.markdown('<div class="view-kicker">The collection</div>', unsafe_allow_html=True)
    st.subheader("Browse the collection")
    st.markdown(
        '<div class="view-description">Find a title quickly and see what is ready to lend.</div>',
        unsafe_allow_html=True,
    )
    book_controls = st.columns([1.5, 1])
    with book_controls[0]:
        search = st.text_input(
            "Search books",
            placeholder="Title, ISBN, or publisher",
        )
    with book_controls[1]:
        collection_view = st.radio(
            "View",
            ["All books", "Available", "Currently lent"],
            index=["All books", "Available", "Currently lent"].index(
                "Available" if page == "available" else "All books"
            ),
            horizontal=True,
        )
    if collection_view == "Available":
        visible_books = read_books(available_only=True)
    elif collection_view == "Currently lent":
        visible_books = read_lent_books()
    else:
        visible_books = books
    if search:
        search_term = search.lower()
        visible_books = visible_books[
            visible_books.astype(str)
            .apply(lambda column: column.str.lower().str.contains(search_term, na=False))
            .any(axis=1)
        ]
    active_isbns = set(active_loans["isbn"].astype(str))
    st.markdown(
        f'<div class="collection-pulse">{len(visible_books)} titles shown · '
        f'{available_count} ready to lend · {len(active_loans)} currently out</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Showing {len(visible_books)} book(s) · {collection_view}")
    st.dataframe(
        style_collection(visible_books, active_isbns),
        use_container_width=True,
        height=380,
        hide_index=True,
    )

    if page == "books":
        add_book_tab, retire_book_tab = st.tabs(["Add book", "Retire book"])
        with add_book_tab:
            st.markdown('<div class="section-kicker">New arrival</div>', unsafe_allow_html=True)
            st.caption("Add a title to the collection and make it ready for circulation.")
            with st.form("create_book_form", clear_on_submit=True):
                identity_column, title_column = st.columns([0.8, 1.8])
                with identity_column:
                    isbn = st.text_input("ISBN", placeholder="9780441013593")
                with title_column:
                    title = st.text_input("Title")
                publisher_column, year_column = st.columns([1.8, 0.8])
                with publisher_column:
                    publisher = st.text_input("Publisher")
                with year_column:
                    published_year = st.number_input(
                        "Published year", min_value=1400, max_value=2100, value=2026
                    )
                condition_column, shelf_column = st.columns(2)
                with condition_column:
                    book_condition = st.selectbox(
                        "Condition", ["new", "good", "fair", "poor", "damaged"], index=1
                    )
                with shelf_column:
                    shelf_location = st.text_input("Shelf location")
                book_notes = st.text_area("Notes")
                submitted = st.form_submit_button("Add book", type="primary")
            if submitted:
                clean_isbn = isbn.strip()
                if not clean_isbn or not title.strip():
                    st.warning("ISBN and title are required.")
                elif len(clean_isbn) not in (10, 13) or not clean_isbn.isdigit():
                    st.warning("ISBN must contain 10 or 13 digits.")
                else:
                    try:
                        create_book(
                            clean_isbn,
                            title,
                            publisher or None,
                            published_year,
                            book_condition,
                            shelf_location or None,
                            book_notes or None,
                        )
                        st.success(f"Added {title}.")
                        st.rerun()
                    except SQLAlchemyError as error:
                        st.error(f"Could not add book: {error}")

        with retire_book_tab:
            st.markdown('<div class="section-kicker">Collection maintenance</div>', unsafe_allow_html=True)
            st.caption("Retire a title without deleting its lending history.")
            retire_options = books[books["is_lendable"] == True].to_dict("records")
            if retire_options:
                book_to_retire = st.selectbox(
                    "Book to retire",
                    retire_options,
                    format_func=lambda book: f"{book['title']} ({book['isbn']})",
                )
                st.warning("A lent book must be returned before it can be retired.")
                if st.button("Retire book", type="secondary"):
                    try:
                        retired, retire_message = retire_book(book_to_retire["isbn"])
                        if retired:
                            st.success(retire_message)
                            st.rerun()
                        else:
                            st.warning(retire_message)
                    except SQLAlchemyError as error:
                        st.error(f"Could not retire book: {error}")
            else:
                st.info("There are no active books to retire.")

elif page == "friends":
    st.subheader("People in your library")
    st.info(f"There are currently {len(active_loans)} active loans across the collection.")
    if not active_loans.empty:
        st.subheader("Currently out")
        st.dataframe(
            style_loan_table(active_loans),
            use_container_width=True,
            hide_index=True,
        )
    create_tab, update_tab, delete_tab = st.tabs(["Add friend", "Edit friend", "Remove friend"])
    with create_tab:
        with st.form("create_friend_form", clear_on_submit=True):
            name = st.text_input("Full name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Add friend", type="primary")
        if submitted:
            if not name.strip():
                st.warning("A name is required.")
            else:
                try:
                    create_friend(name.strip(), email or None, phone or None, notes or None)
                    st.success(f"Added {name}.")
                    st.rerun()
                except SQLAlchemyError as error:
                    st.error(f"Could not add friend: {error}")

    with update_tab:
        friend_options = friends.to_dict("records")
        if friend_options:
            selected_friend = st.selectbox(
                "Friend",
                friend_options,
                format_func=lambda friend: f"{friend['friend_id']} - {friend['full_name']}",
            )
            with st.form("update_friend_form"):
                updated_name = st.text_input("Full name", value=selected_friend["full_name"])
                updated_email = st.text_input("Email", value=selected_friend.get("email") or "")
                updated_phone = st.text_input("Phone", value=selected_friend.get("phone") or "")
                updated_notes = st.text_area("Notes", value=selected_friend.get("notes") or "")
                submitted = st.form_submit_button("Save changes", type="primary")
            if submitted:
                try:
                    update_friend(
                        selected_friend["friend_id"],
                        updated_name.strip(),
                        updated_email or None,
                        updated_phone or None,
                        updated_notes or None,
                    )
                    st.success("Friend updated.")
                    st.rerun()
                except SQLAlchemyError as error:
                    st.error(f"Could not update friend: {error}")
        else:
            st.info("Add a friend to enable editing.")

    with delete_tab:
        if friend_options:
            friend_to_delete = st.selectbox(
                "Friend to remove",
                friend_options,
                format_func=lambda friend: f"{friend['friend_id']} - {friend['full_name']}",
                key="delete_friend",
            )
            if st.button("Remove friend", type="secondary"):
                try:
                    delete_friend(friend_to_delete["full_name"])
                    st.success("Friend removed.")
                    st.rerun()
                except SQLAlchemyError as error:
                    st.error(f"Could not remove friend: {error}")

    st.divider()
    st.subheader("Friend directory")
    friend_search = st.text_input(
        "Search friends",
        placeholder="Search by name, email, or phone",
    )
    visible_friends = friends
    if friend_search:
        search_term = friend_search.lower()
        visible_friends = friends[
            friends.astype(str)
            .apply(lambda column: column.str.lower().str.contains(search_term, na=False))
            .any(axis=1)
        ]
    st.caption(f"Showing {len(visible_friends)} of {len(friends)} friends")
    st.dataframe(
        humanize_columns(visible_friends),
        use_container_width=True,
        height=380,
        hide_index=True,
    )

elif page == "out":
    st.markdown('<div class="section-kicker">Library circulation</div>', unsafe_allow_html=True)
    st.subheader("Lending desk")
    st.caption(f"Showing {len(active_loans)} book(s) currently out.")
    overdue_count = (
        (pd.to_datetime(active_loans["due_date"], errors="coerce") < pd.Timestamp(date.today()))
    ).sum()
    st.markdown(
        f"""
        <div class="circulation-pulse">
            <div class="circulation-stat">
                <div class="number">{len(active_loans)}</div><div class="label">Active loans</div>
            </div>
            <div class="circulation-stat warning">
                <div class="number">{overdue_count}</div><div class="label">Overdue</div>
            </div>
            <div class="circulation-stat">
                <div class="number">{available_count}</div><div class="label">Books ready to lend</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(
        style_loan_table(active_loans),
        use_container_width=True,
        height=300,
        hide_index=True,
    )

    available_books = read_books(available_only=True)
    book_options = available_books.to_dict("records")
    friend_options = friends.to_dict("records")
    if book_options and friend_options:
        st.markdown('<div class="section-kicker">Check out a book</div>', unsafe_allow_html=True)
        with st.form("create_loan_form"):
            selected_book = st.selectbox(
                "Book",
                book_options,
                format_func=lambda book: f"{book['title']} ({book['isbn']})",
            )
            selected_borrower = st.selectbox(
                "Borrower",
                friend_options,
                format_func=lambda friend: friend["full_name"],
            )
            due_date_column, condition_column = st.columns(2)
            with due_date_column:
                due_date = st.date_input("Due date", value=date.today() + timedelta(days=14))
            with condition_column:
                condition = st.selectbox(
                    "Condition", ["new", "good", "fair", "poor", "damaged"], index=1
                )
            loan_notes = st.text_area("Notes")
            submitted = st.form_submit_button("Record loan", type="primary")
        if submitted:
            try:
                loan_created, loan_message = create_loan_by_name(
                    selected_book["isbn"],
                    selected_borrower["full_name"],
                    due_date,
                    condition,
                    loan_notes or None,
                )
                if loan_created:
                    st.success(loan_message)
                    st.rerun()
                else:
                    st.warning(loan_message)
            except SQLAlchemyError as error:
                st.error(f"Could not record loan: {error}")
    else:
        st.info("You need at least one book and one friend before recording a loan.")

    st.divider()
    st.markdown('<div class="section-kicker">Close a loan</div>', unsafe_allow_html=True)
    st.subheader("Return a book")
    active_loan_options = loans[loans["status"] == "out"].to_dict("records")
    if active_loan_options:
        with st.form("return_loan_form"):
            selected_loan = st.selectbox(
                "Active loan",
                active_loan_options,
                format_func=lambda loan: (
                    f"{loan['isbn']} - {loan['friend_name']} "
                    f"(due {str(loan['due_date'])[:10]})"
                ),
            )
            return_date_column, returned_condition_column = st.columns(2)
            with return_date_column:
                st.date_input("Return date", value=date.today(), disabled=True)
            with returned_condition_column:
                returned_condition = st.selectbox(
                    "Condition on return",
                    ["new", "good", "fair", "poor", "damaged"],
                    index=1,
                )
            return_notes = st.text_area("Return notes")
            returned = st.form_submit_button("Record return", type="primary")
        if returned:
            try:
                return_created, return_message = return_loan(
                    selected_loan["loan_id"],
                    returned_condition,
                    notes=return_notes or None,
                )
                if return_created:
                    st.success(return_message)
                    st.rerun()
                else:
                    st.warning(return_message)
            except SQLAlchemyError as error:
                st.error(f"Could not record return: {error}")
    else:
        st.info("There are no books currently out.")