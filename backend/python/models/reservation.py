# models/reservation.py
from utils.db_connection import execute_query

class Reservation:
    @staticmethod
    def get_all():
        return execute_query("""
            SELECT r.*, b.title, b.author, m.full_name AS member_name
            FROM reservations r
            JOIN books b ON r.book_id=b.id
            JOIN members m ON r.member_id=m.id
            ORDER BY r.reserved_at DESC
        """)

    @staticmethod
    def create(book_id, member_id):
        return execute_query(
            "INSERT INTO reservations (book_id, member_id) VALUES (%s,%s)",
            (book_id, member_id),
            fetch=False
        )

    @staticmethod
    def cancel(reservation_id):
        return execute_query(
            "UPDATE reservations SET status='cancelled' WHERE id=%s",
            (reservation_id,),
            fetch=False
        )
