# models/book.py
from utils.db_connection import execute_query

class Book:
    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM books ORDER BY title")

    @staticmethod
    def get_by_id(book_id):
        rows = execute_query("SELECT * FROM books WHERE id=%s", (book_id,))
        return rows[0] if rows else None

    @staticmethod
    def search(keyword):
        kw = f"%{keyword}%"
        return execute_query(
            "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s",
            (kw, kw, kw)
        )

    @staticmethod
    def create(title, author, isbn, category, publisher, year, copies):
        return execute_query(
            "INSERT INTO books (title,author,isbn,category,publisher,year,total_copies,available_copies) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (title, author, isbn, category, publisher, year, copies, copies),
            fetch=False
        )

    @staticmethod
    def update(book_id, **fields):
        set_clause = ", ".join(f"{k}=%s" for k in fields)
        values = list(fields.values()) + [book_id]
        return execute_query(f"UPDATE books SET {set_clause} WHERE id=%s", values, fetch=False)

    @staticmethod
    def delete(book_id):
        return execute_query("DELETE FROM books WHERE id=%s", (book_id,), fetch=False)
