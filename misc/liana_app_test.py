import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load your secret password from .env
load_dotenv()

# Database connection details
user = "root"
password = os.getenv("MYSQL_PASSWORD")
host = "localhost"
port = 3306
schema = "sample_library"

# Build connection and engine
connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema}"
engine = create_engine(connection_string)

# Pull the genres table into Python
genres_df = pd.read_sql("genres", con=engine)

print("Boom! Connected successfully. Here are your genres:")
print(genres_df)


# Create a new genre (try changing the name if you run it again)
new_genre = pd.DataFrame({"name": ["Fantasy"], "description": ["Magical worlds and epic quests"]})

# Push it into MySQL safely using try-except
try:
    new_genre.to_sql("genres", con=engine, if_exists="append", index=False)
    print("Successfully inserted a new genre!")
except Exception as e:
    print("Note: This genre already exists in the database.")

# Pull and print the full genres table to see everything
genres_df = pd.read_sql("genres", con=engine)
print("\nUpdated Genres List:")
print(genres_df)

# Create a new book DataFrame with a shorter ISBN to fit the column limit
new_book = pd.DataFrame({
    "isbn": ["1234567890"],
    "title": ["Dune"],
    "publisher": ["Chilton Books"],
    "published_year": [1965]
})

# try except block to view if  errors occured 
try:
    new_book.to_sql("books", con=engine, if_exists="append", index=False)
    print("\nSuccessfully inserted a new book!")
except Exception as e:
    print(f"\nNote on book insertion: {e}")

# Pull and print the full books table
books_df = pd.read_sql("books", con=engine)
print("\nCurrent Books in Library:")
print(books_df)


#trying to input new book 
my_book = pd.DataFrame({
    "isbn": ["9999999999999"],
    "title": ["the great day of the man"],
    "publisher": ["Gramedia"],
    "published_year": [2023],
    "is_lendable": [False]
})

# try except block to handle potential errors during insertion
try:
    my_book.to_sql("books", con=engine, if_exists="append", index=False)
    print("\nSuccessfully inserted 'the great day of the man' into the books table!")
except Exception as e:
    print(f"\nError adding book: {e}")

books_df = pd.read_sql("books", con=engine)
print("\nCurrent Books in Library:")
print(books_df)


#pulling the entire table from SQL to Python
books_df = pd.read_sql("books", con=engine)
print(books_df)


# as wee can see there is duplicaate. TO  handle :
from sqlalchemy import text

# Open a safe connection block and delete the duplicate row by its ISBN
with engine.begin() as connection:
    connection.execute(
        text("DELETE FROM books WHERE isbn = '9999999999999';")
    )

print("Duplicate book removed from SQL!")

# Verify by pulling the table again
books_df = pd.read_sql("books", con=engine)
print(books_df)


pd.read_sql("SELECT * FROM books", con=engine)
