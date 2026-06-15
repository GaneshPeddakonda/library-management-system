# services/report_service.py
from utils.db_connection import execute_query

class ReportService:
    @staticmethod
    def dashboard_stats():
        books     = execute_query("SELECT COUNT(*) AS c FROM books")[0]['c']
        members   = execute_query("SELECT COUNT(*) AS c FROM members")[0]['c']
        issued    = execute_query("SELECT COUNT(*) AS c FROM issued_books WHERE status='issued'")[0]['c']
        overdue   = execute_query(
            "SELECT COUNT(*) AS c FROM issued_books WHERE status='issued' AND due_date<CURDATE()"
        )[0]['c']
        fines_due = execute_query(
            "SELECT COALESCE(SUM(amount),0) AS s FROM fines WHERE paid=FALSE"
        )[0]['s']
        return {
            "total_books": books,
            "total_members": members,
            "active_issues": issued,
            "overdue_books": overdue,
            "fines_due": float(fines_due)
        }

    @staticmethod
    def popular_books(limit=10):
        return execute_query("""
            SELECT b.title, b.author, COUNT(ib.id) AS times_issued
            FROM issued_books ib
            JOIN books b ON ib.book_id=b.id
            GROUP BY b.id
            ORDER BY times_issued DESC
            LIMIT %s
        """, (limit,))

    @staticmethod
    def active_members(limit=10):
        return execute_query("""
            SELECT m.full_name, m.email, COUNT(ib.id) AS books_borrowed
            FROM issued_books ib
            JOIN members m ON ib.member_id=m.id
            GROUP BY m.id
            ORDER BY books_borrowed DESC
            LIMIT %s
        """, (limit,))
