/**********************************************************************
 Liana's Library

 Run order: 01_ddl -> 02_seed_data -> 03_functions -> 04_views -> 05_procedures -> 06_tests
 **********************************************************************/

DROP DATABASE IF EXISTS sample_library;

CREATE DATABASE sample_library
	CHARACTER SET utf8mb4
	COLLATE utf8mb4_0900_ai_ci;

USE sample_library;

/******************
 Friends
 ******************/
DROP TABLE IF EXISTS friends;
DROP TABLE IF EXISTS friends;
CREATE TABLE friends (
    friend_id   INT AUTO_INCREMENT PRIMARY KEY,
    full_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(255) NULL,
    phone       VARCHAR(20) NULL,
    notes       TEXT NULL,

    UNIQUE KEY uq_friends_email (email),
    KEY ix_friends_name (full_name)
) ENGINE = InnoDB;


/******************
 Authors
 ******************/
DROP TABLE IF EXISTS authors;
CREATE TABLE authors (
    author_id   INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(150) NOT NULL,

    KEY ix_authors_name (author_name)
) ENGINE = InnoDB;

DROP TABLE IF EXISTS genres;
CREATE TABLE genres (
    genre_id   INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL,

    UNIQUE KEY uq_genre_name (genre_name)
) ENGINE = InnoDB;


DROP TABLE IF EXISTS books;
CREATE TABLE books (
    isbn               VARCHAR(20) PRIMARY KEY,
    title              VARCHAR(255) NOT NULL,
    publisher          VARCHAR(100) NULL,
    published_year     INT NULL,

    KEY ix_books_title (title),

    -- Allows 13-digit ISBNs (with or without hyphens) or 10-digit ISBNs (with or without hyphens ending in a digit or X)
    CONSTRAINT chk_books_isbn CHECK (
        isbn REGEXP '^(97[89]-)?[0-9]{1,5}-[0-9]{1,7}-[0-9]{1,7}-[0-9X]$' 
        OR isbn REGEXP '^[0-9]{13}$' 
        OR isbn REGEXP '^[0-9]{9}[0-9X]$'
    ),
    CONSTRAINT chk_books_year CHECK (published_year IS NULL OR published_year BETWEEN 1400 AND 2100)
) ENGINE = InnoDB;



DROP TABLE IF EXISTS book_authors;
CREATE TABLE book_authors (
    isbn          VARCHAR(20) NOT NULL,
    author_id     INT NOT NULL,
    author_order  TINYINT NOT NULL DEFAULT 1,  -- 1 = first-billed author

    PRIMARY KEY (isbn, author_id),
    KEY ix_book_authors_author (author_id),

    CONSTRAINT fk_book_authors_book
        FOREIGN KEY (isbn) REFERENCES books (isbn)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_book_authors_author
        FOREIGN KEY (author_id) REFERENCES authors (author_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;



DROP TABLE IF EXISTS book_genres;
CREATE TABLE book_genres (
    isbn      VARCHAR(20) NOT NULL,
    genre_id  INT NOT NULL,

    PRIMARY KEY (isbn, genre_id),
    KEY ix_book_genres_genre (genre_id),

    CONSTRAINT fk_book_genres_book
        FOREIGN KEY (isbn) REFERENCES books (isbn)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_book_genres_genre
        FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;


/******************
 Lending
 ******************/


DROP TABLE IF EXISTS loans;
CREATE TABLE loans (
	loan_id         INT AUTO_INCREMENT PRIMARY KEY,
	isbn            VARCHAR(20) NOT NULL,
	friend_id       INT NOT NULL,
	loan_date       DATE NOT NULL,
	due_date        DATE NOT NULL,
	return_date     DATE NULL,
	condition_out   ENUM('new', 'good', 'fair', 'poor', 'damaged') NOT NULL,
	condition_in    ENUM('new', 'good', 'fair', 'poor', 'damaged') NULL,
	status          ENUM('out', 'returned', 'lost') NOT NULL DEFAULT 'out',
	notes           VARCHAR(255) NULL,

	-- Same generated-column trick as friends.owner_flag: this is the isbn
	-- while the loan is out and NULL once it is closed, so the UNIQUE key
	-- allows only one open loan per book but any number of closed ones.
	-- With a single copy of everything, that is the whole story: two people
	-- cannot hold the same book at the same time.
	active_isbn     VARCHAR(20) GENERATED ALWAYS AS (IF(status = 'out', isbn, NULL)) STORED,

	UNIQUE KEY uq_loans_one_active_per_book (active_isbn),
	KEY ix_loans_friend (friend_id, loan_date),
	KEY ix_loans_book_status (isbn, status),

	-- RESTRICT on both, and not by preference: MySQL forbids CASCADE / SET NULL
	-- on a foreign key whose column feeds a generated column, and isbn feeds
	-- active_isbn above. (Get this wrong and the DDL fails with ERROR 1215,
	-- 'Cannot add foreign key constraint', which does not explain itself.)
	-- Books are never deleted anyway — they get retired — so nothing is lost.
	CONSTRAINT fk_loans_book
		FOREIGN KEY (isbn) REFERENCES books (isbn)
		ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT fk_loans_friend
		FOREIGN KEY (friend_id) REFERENCES friends (friend_id)
		ON DELETE RESTRICT ON UPDATE CASCADE,

	CONSTRAINT chk_loans_due_after_loan
		CHECK (due_date >= loan_date),
	CONSTRAINT chk_loans_return_after_loan
		CHECK (return_date IS NULL OR return_date >= loan_date),
	-- a returned loan must say when, and an open loan must not
	CONSTRAINT chk_loans_returned_has_date
		CHECK ((status = 'returned' AND return_date IS NOT NULL)
			OR (status <> 'returned' AND (status = 'lost' OR return_date IS NULL)))
) ENGINE = InnoDB;


/*
 Check
 */

SHOW TABLES;

select *
from loans;

select *
from friends;

select * from loans;
