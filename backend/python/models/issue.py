# models/issue.py
from utils.db_connection import execute_query

class Issue:
    @staticmethod
    def get_all():
        return execute_query("""
            SELECT ib.*, b.title, b.author, m.full_name AS member_name
            FROM issued_books ib
            JOIN books b ON ib.book_id=b.id
            JOIN members m ON ib.member_id=m.id
            ORDER BY ib.issue_date DESC
        """)

    @staticmethod
    def get_active():
        return execute_query("""
            SELECT ib.*, b.title, b.author, m.full_name AS member_name
            FROM issued_books ib
            JOIN books b ON ib.book_id=b.id
            JOIN members m ON ib.member_id=m.id
            WHERE ib.status='issued'
            ORDER BY ib.due_date
        """)

    @staticmethod
    def get_overdue():
        return execute_query("""
            SELECT ib.*, b.title, m.full_name AS member_name, m.email,
                   DATEDIFF(CURDATE(), ib.due_date) AS days_overdue
            FROM issued_books ib
            JOIN books b ON ib.book_id=b.id
            JOIN members m ON ib.member_id=m.id
            WHERE ib.status='issued' AND ib.due_date < CURDATE()
        """)

    @staticmethod
    def issue_book(book_id, member_id, issued_by, due_date):
        return execute_query(
            "INSERT INTO issued_books (book_id,member_id,issued_by,due_date) VALUES (%s,%s,%s,%s)",
            (book_id, member_id, issued_by, due_date),
            fetch=False
        )

    @staticmethod
    def return_book(issue_id):
        return execute_query(
            "UPDATE issued_books SET return_date=CURDATE(), status='returned' WHERE id=%s",
            (issue_id,),
            fetch=False
        )
