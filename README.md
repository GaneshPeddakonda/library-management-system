# 📚 Library Management System (LMS)

A full-stack Library Management System built with **Python / Flask** (REST API backend) and plain **HTML + CSS + JavaScript** (frontend). No frontend framework required — open the HTML files directly in a browser or serve with any static server.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Run](#setup--run)
- [Default Login](#default-login)
- [API Reference](#api-reference)
- [Business Rules](#business-rules)
- [Bug Fixes Applied](#bug-fixes-applied)
- [Troubleshooting](#troubleshooting)

---

## Features

- JWT-based authentication (login / register)
- Book management — add, edit, delete, search
- Member management — add, edit, delete
- Book issuing and returns with automatic fine calculation
- Fine tracking and payment
- Dashboard with live statistics
- Reports: most popular books and most active members

---

## Project Structure

```
LMS/
├── backend/
│   └── python/
│       ├── app.py                    ← Flask entry point; all routes registered here
│       ├── config.py                 ← DB credentials, JWT secret, fine/loan constants
│       ├── requirements.txt          ← pip dependencies
│       ├── controllers/
│       │   ├── auth_middleware.py    ← JWT token decorator (@token_required)
│       │   ├── book_controller.py    ← /api/books routes
│       │   ├── member_controller.py  ← /api/members routes
│       │   ├── issue_controller.py   ← /api/issues routes
│       │   ├── fine_controller.py    ← /api/fines routes
│       │   └── report_controller.py  ← /api/reports routes
│       ├── models/
│       │   ├── book.py               ← SQL queries for books table
│       │   ├── member.py             ← SQL queries for members table
│       │   ├── issue.py              ← SQL queries for issued_books table
│       │   ├── fine.py               ← SQL queries for fines table
│       │   └── reservation.py        ← SQL queries for reservations table
│       ├── services/
│       │   ├── auth_service.py       ← Login / register + JWT generation
│       │   ├── book_service.py       ← Business logic for books
│       │   ├── issue_service.py      ← Issue/return flow + fine calculation
│       │   └── report_service.py     ← Dashboard stats and report queries
│       └── utils/
│           ├── db_connection.py      ← MySQL connection pool + execute_query()
│           └── helper.py             ← success() / error() JSON response helpers
├── frontend/
│   ├── index.html                    ← Landing page (auto-redirects if already logged in)
│   ├── login.html                    ← Login form
│   ├── register.html                 ← Registration form
│   ├── dashboard.html                ← Stats overview
│   ├── books.html                    ← Book list with Add / Edit / Delete
│   ├── members.html                  ← Member list with Add / Edit / Delete
│   ├── issue-book.html               ← Issue & return books
│   ├── fines.html                    ← View & pay fines
│   ├── reports.html                  ← Popular books & active members
│   ├── css/
│   │   ├── style.css                 ← Global styles (nav, cards, tables, forms, modals)
│   │   └── login.css                 ← Login / register page styles
│   └── js/
│       ├── api.js                    ← API base URL, fetch wrapper, auth helpers
│       ├── login.js                  ← Login form submission
│       ├── dashboard.js              ← Loads and displays stats
│       ├── books.js                  ← CRUD for books
│       ├── members.js                ← CRUD for members
│       ├── issue.js                  ← Issue / return + active issues table
│       └── fines.js                  ← Fines list + pay action
└── database/
    └── library_management.sql        ← Complete schema + sample data
```

---

## Prerequisites

| Tool   | Minimum Version |
|--------|----------------|
| Python | 3.9+           |
| MySQL  | 8.0+           |
| pip    | latest         |

No Node.js or build tools are needed.

---

## Setup & Run

### 1. Database

Import the schema into MySQL:

```bash
mysql -u root -p < database/library_management.sql
```

Or from inside the MySQL shell:

```sql
source database/library_management.sql;
```

This creates the `library_management` database with all tables and inserts sample data (1 admin user, 5 books, 3 members).

---

### 2. Backend

```bash
cd backend/python

# Install Python dependencies
pip install -r requirements.txt

# Configure database credentials (optional — these are the defaults)
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=
export DB_NAME=library_management

# (Optional) Override the JWT secret in production
export SECRET_KEY=your-very-secret-key

# Start the Flask API server
python app.py
```

The API will be available at **http://localhost:5000**.

To verify it is running:

```bash
curl http://localhost:5000/api/health
# {"message":"Library Management System API","status":"ok"}
```

---

### 3. Frontend

No build step is needed. You can open the files directly:

```
frontend/index.html   ← double-click in your file manager
```

Or serve them with Python's built-in HTTP server to avoid any browser CORS/file restrictions:

```bash
cd frontend
python -m http.server 3000
# Open http://localhost:3000 in your browser
```

---

## Default Login

| Username | Password  | Role  |
|----------|-----------|-------|
| `admin`  | `admin123`| admin |

---

## API Reference

All endpoints except `/api/auth/*` and `GET /api/books/` require a JWT token in the `Authorization: Bearer <token>` header.

### Auth

| Method | Endpoint            | Body fields                              | Description              |
|--------|---------------------|------------------------------------------|--------------------------|
| POST   | /api/auth/login     | `username`, `password`                   | Returns JWT token + user |
| POST   | /api/auth/register  | `username`, `password`, `full_name`, `email` | Creates new account  |

### Books

| Method | Endpoint           | Description                   |
|--------|--------------------|-------------------------------|
| GET    | /api/books/        | List all books                |
| GET    | /api/books/?q=term | Search by title / author / ISBN |
| GET    | /api/books/:id     | Get a single book             |
| POST   | /api/books/        | Add a book (auth required)    |
| PUT    | /api/books/:id     | Update a book (auth required) |
| DELETE | /api/books/:id     | Delete a book (auth required) |

### Members

| Method | Endpoint          | Description                     |
|--------|-------------------|---------------------------------|
| GET    | /api/members/     | List all members (auth required)|
| GET    | /api/members/:id  | Get a single member             |
| POST   | /api/members/     | Add a member                    |
| PUT    | /api/members/:id  | Update a member                 |
| DELETE | /api/members/:id  | Delete a member                 |

### Issues

| Method | Endpoint                  | Description                              |
|--------|---------------------------|------------------------------------------|
| GET    | /api/issues/              | All active (unreturned) issues           |
| GET    | /api/issues/overdue       | Issues past their due date               |
| POST   | /api/issues/              | Issue a book (`book_id`, `member_id`)    |
| POST   | /api/issues/return/:id    | Return a book; auto-calculates fine      |

### Fines

| Method | Endpoint           | Description             |
|--------|--------------------|-------------------------|
| GET    | /api/fines/        | All fines               |
| POST   | /api/fines/pay/:id | Mark a fine as paid     |

### Reports

| Method | Endpoint                    | Description                     |
|--------|-----------------------------|---------------------------------|
| GET    | /api/reports/stats          | Dashboard summary statistics    |
| GET    | /api/reports/popular-books  | Top 10 most borrowed books      |
| GET    | /api/reports/active-members | Top 10 most active members      |

---

## Business Rules

| Rule                  | Value / Behaviour                                                        |
|-----------------------|--------------------------------------------------------------------------|
| Loan period           | 14 days (change `LOAN_DAYS` in `config.py`)                              |
| Overdue fine          | ₹2.00 per day (change `FINE_PER_DAY` in `config.py`)                    |
| Fine calculation      | Calculated automatically on book return if `return_date > due_date`      |
| Book deletion guard   | A book cannot be deleted while it has an active (unreturned) issue       |
| JWT expiry            | 8 hours (change `JWT_EXPIRY_HOURS` in `config.py`)                       |
| Password storage      | bcrypt-hashed; plaintext is never stored                                  |

---

## Bug Fixes Applied

| File | Bug | Fix |
|------|-----|-----|
| `utils/db_connection.py` | `cursor.close()` was inside the `try` block and never called when an exception occurred, leaking database cursor objects | Moved `cursor.close()` into the `finally` block so it always runs |
| `frontend/js/issue.js` | Overdue check used `new Date(due_date) < new Date()`. Date strings like `"2026-06-11"` are parsed as **UTC midnight**, but `new Date()` is **local time** — causing books to appear overdue on their actual due day in timezones east of UTC | Replaced with a locale-safe string comparison using `toLocaleDateString('en-CA')` to get the local `YYYY-MM-DD` date |
| `frontend/register.html` | The password field stated "Min 6 characters" but had no `minlength` attribute and no JS length check, so a 1-character password was accepted by the browser | Added `minlength="6"` to the `<input>` and an explicit JS guard before form submission |

---

## Troubleshooting

**`mysql.connector.errors.DatabaseError: Access denied`**
Check that `DB_USER` and `DB_PASSWORD` in `config.py` (or environment variables) match your MySQL installation.

**`mysql.connector.errors.ProgrammingError: Table doesn't exist`**
Run the SQL schema file first: `mysql -u root -p < database/library_management.sql`

**`401 Unauthorized` on every API call**
Your JWT token has expired (default: 8 hours). Log out and log in again.

**CORS errors in the browser console**
Make sure the Flask backend is running and that `flask-cors` is installed (`pip install flask-cors`). The `CORS(app)` call in `app.py` allows all origins by default.

**`ModuleNotFoundError: No module named 'flask'`**
You are not in the right directory or virtual environment. Run `pip install -r requirements.txt` from inside `backend/python/`.

**Books or members not loading (empty table)**
Open the browser developer console (F12). A `401` means the token is missing or expired — log out and back in. A `500` usually means a database connection issue.
