-- ============================================================
-- Library Management System - Complete Database Schema
-- ============================================================



-- Users / Admins
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,   -- bcrypt hashed
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('admin','librarian','member') DEFAULT 'member',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Books
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    category VARCHAR(50),
    publisher VARCHAR(100),
    year INT,
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Members
CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    membership_date DATE,
    status ENUM('active','suspended','expired') DEFAULT 'active'
);

-- Issued Books
CREATE TABLE IF NOT EXISTS issued_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    issued_by INT NOT NULL,       -- user (librarian) id
    issue_date DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    status ENUM('issued','returned','overdue') DEFAULT 'issued',
    FOREIGN KEY (book_id)   REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (issued_by) REFERENCES users(id)
);

-- Reservations
CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending','fulfilled','cancelled') DEFAULT 'pending',
    FOREIGN KEY (book_id)   REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- Fines
CREATE TABLE IF NOT EXISTS fines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    amount DECIMAL(8,2) NOT NULL,
    paid BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issued_books(id)
);

-- ============================================================
-- Sample Data
-- ============================================================

-- Admin user (password: admin123)
INSERT IGNORE INTO users (username, password, full_name, email, role) VALUES
('admin', '$2b$12$KIXvPlVMpwIWm9Sd5o4pGOYoKpCX2J0P7mFMD1nV0.sSeIr1S8tOy', 'Admin User', 'admin@library.com', 'admin');

INSERT IGNORE INTO books (title, author, isbn, category, publisher, year, total_copies, available_copies) VALUES
('The Great Gatsby',      'F. Scott Fitzgerald', '9780743273565', 'Fiction',    'Scribner',          1925, 3, 3),
('To Kill a Mockingbird', 'Harper Lee',          '9780061935466', 'Fiction',    'HarperCollins',     1960, 2, 2),
('1984',                  'George Orwell',       '9780451524935', 'Dystopian',  'Signet Classic',    1949, 4, 4),
('Clean Code',            'Robert C. Martin',    '9780132350884', 'Technology', 'Prentice Hall',     2008, 2, 2),
('The Pragmatic Programmer','Andrew Hunt',       '9780135957059', 'Technology', 'Addison-Wesley',    1999, 2, 2);

INSERT IGNORE INTO members (full_name, email, phone, address) VALUES
('Alice Johnson', 'alice@example.com', '9876543210', '123 Main St'),
('Bob Smith',     'bob@example.com',   '9876543211', '456 Oak Ave'),
('Carol White',   'carol@example.com', '9876543212', '789 Pine Rd');
