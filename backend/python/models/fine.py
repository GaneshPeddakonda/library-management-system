# models/fine.py
from utils.db_connection import execute_query

class Fine:
    @staticmethod
    def get_all():
        return execute_query("""
            SELECT f.*, m.full_name AS member_name, b.title
            FROM fines f
            JOIN issued_books ib ON f.issue_id=ib.id
            JOIN members m ON ib.member_id=m.id
            JOIN books b ON ib.book_id=b.id
            ORDER BY f.created_at DESC
        """)

    @staticmethod
    def create(issue_id, amount):
        return execute_query(
            "INSERT INTO fines (issue_id, amount) VALUES (%s,%s)",
            (issue_id, amount),
            fetch=False
        )

    @staticmethod
    def pay(fine_id):
        return execute_query(
            "UPDATE fines SET paid=TRUE WHERE id=%s",
            (fine_id,),
            fetch=False
        )
