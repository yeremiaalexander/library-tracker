# Liana's Library 📚

A small Streamlit app for tracking a personal book collection and the books
lent out to friends. Built with Python, Streamlit, SQLAlchemy and MySQL.

## Features
- Browse and search the collection (available / currently lent)
- Add and retire books
- Add, edit and remove friends
- Record loans and returns, with overdue highlighting

## Setup

1. **Create the environment**
   ```bash
   conda env create -f environment.yml
   conda activate lianes-lib-env
   ```
2. **Create the database** (MySQL 8+). Run these scripts in order:
   ```
   sql_files/01_ddl.sql
   sql_files/02_seed_data.sql
   ```
   Warning: `01_ddl.sql` starts with `DROP DATABASE IF EXISTS sample_library`,
   so it will erase any existing database with that name.
3. **Add your database password.** In the project root, create the file
   `.streamlit/secrets.toml` with:
   ```toml
   [mysql]
   password = "your_mysql_password"
   ```
   This file is git-ignored. Never commit it.
4. **Run the app** (from the project root)
   ```bash
   streamlit run src/app.py
   ```

The app connects to MySQL as `root` at `127.0.0.1:3306`, database `sample_library`.

## Project layout
| Path | Purpose |
|------|---------|
| `src/app.py` | Streamlit UI |
| `src/db.py` | Shared database engine |
| `src/create.py`, `read.py`, `update.py`, `delete.py` | Database operations (CRUD) |
| `src/validate.py` | Input validation helpers |
| `sql_files/01_ddl.sql` | Database schema |
| `sql_files/02_seed_data.sql` | Sample data |
