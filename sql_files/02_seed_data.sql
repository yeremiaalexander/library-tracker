/**********************************************************************
 Liana's Library — seed data (Updated for Minimalist Schema)
 Run this AFTER your DDL script, against a freshly created database.
 **********************************************************************/

USE sample_library;

/******************
 1. friends
 ******************/
INSERT INTO friends (full_name, email, phone) VALUES
('Liana Cruz',    'liana@email.com',         '555-0101'),
('Maya Chen',     'maya.chen@email.com',     '555-0102'),
('Diego Alvarez', 'diego.alvarez@email.com', '555-0103'),
('Priya Nair',    'priya.nair@email.com',    '555-0104'),
('Sam O''Brien',  'sam.obrien@email.com',    '555-0105'),
('Yusuf Demir',   'yusuf.demir@email.com',   '555-0106'),
('Ana Kowalski',  'ana.kowalski@email.com',  '555-0107');


/******************
 2. authors
 ******************/
INSERT INTO authors (author_name) VALUES
('Frank Herbert'),
('George Orwell'),
('Toni Morrison'),
('Haruki Murakami'),
('Agatha Christie'),
('Yuval Noah Harari');


/******************
 3. genres
 ******************/
INSERT INTO genres (genre_name) VALUES
('Science Fiction'),
('Dystopian'),
('Literary Fiction'),
('Mystery'),
('Non-fiction'),
('Fantasy');


/******************
 4. books
 ******************/
INSERT INTO books (isbn, title, publisher, published_year) VALUES
('9780441013593', 'Dune',                     'Ace Books',      1965),
('9780451524935', '1984',                     'Signet Classic', 1949),
('9781400033416', 'Beloved',                  'Vintage',        1987),
('9780099448822', 'Norwegian Wood',           'Vintage',        1987),
('9780062073488', 'And Then There Were None', 'William Morrow', 1939),
('9780062316097', 'Sapiens',                  'Harper',         2011);


/******************
 5. book_authors (pairing sheet: book <-> author)
 ******************/
INSERT INTO book_authors (isbn, author_id, author_order) VALUES
('9780441013593', 1, 1),  -- Dune / Frank Herbert
('9780451524935', 2, 1),  -- 1984 / George Orwell
('9781400033416', 3, 1),  -- Beloved / Toni Morrison
('9780099448822', 4, 1),  -- Norwegian Wood / Haruki Murakami
('9780062073488', 5, 1),  -- And Then There Were None / Agatha Christie
('9780062316097', 6, 1);  -- Sapiens / Yuval Noah Harari


/******************
 6. book_genres (pairing sheet: book <-> genre)
 ******************/
INSERT INTO book_genres (isbn, genre_id) VALUES
('9780441013593', 1),  -- Dune / Science Fiction
('9780441013593', 6),  -- Dune / Fantasy
('9780451524935', 2),  -- 1984 / Dystopian
('9781400033416', 3),  -- Beloved / Literary Fiction
('9780099448822', 3),  -- Norwegian Wood / Literary Fiction
('9780062073488', 4),  -- And Then There Were None / Mystery
('9780062316097', 5);  -- Sapiens / Non-fiction


/******************
 7. loans (heavy-duty tracking with conditions and statuses)
 ******************/
INSERT INTO loans (isbn, friend_id, loan_date, due_date, return_date, condition_out, condition_in, status, notes) VALUES
('9780441013593', 2, '2026-06-01', '2026-06-15', NULL,         'good', NULL,   'out',      'Lent for summer reading'),
('9780451524935', 3, '2026-05-01', '2026-05-15', '2026-05-14', 'good', 'good', 'returned', NULL),
('9781400033416', 4, '2026-04-10', '2026-04-24', '2026-04-20', 'fair', 'fair', 'returned', NULL),
('9780099448822', 5, '2026-07-01', '2026-07-15', NULL,         'good', NULL,   'out',      NULL),
('9780062316097', 6, '2026-03-01', '2026-03-15', '2026-03-10', 'new',  'good', 'returned', NULL),
('9780062073488', 7, '2026-01-01', '2026-01-15', NULL,         'good', NULL,   'lost',     'Lost during move');


-- Quick Verification Queries
SELECT * FROM friends;
SELECT * FROM authors;
SELECT * FROM books;
SELECT * FROM loans;