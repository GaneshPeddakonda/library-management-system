# services/issue_service.py
from datetime import date, timedelta
from models.issue import Issue
from models.fine import Fine
from utils.db_connection import execute_query
from config import FINE_PER_DAY, LOAN_DAYS

class IssueService:
    @staticmethod
    def issue_book(book_id, member_id, issued_by):
        # Check availability
        rows = execute_query(
            "SELECT available_copies FROM books WHERE id=%s", (book_id,)
        )
        if not rows or rows[0]['available_copies'] < 1:
            return None, "Book not available"
        due = date.today() + timedelta(days=LOAN_DAYS)
        issue_id = Issue.issue_book(book_id, member_id, issued_by, due)
        execute_query(
            "UPDATE books SET available_copies=available_copies-1 WHERE id=%s",
            (book_id,), fetch=False
        )
        return {"issue_id": issue_id, "due_date": str(due)}, None

    @staticmethod
    def return_book(issue_id):
        rows = execute_query(
            "SELECT * FROM issued_books WHERE id=%s", (issue_id,)
        )
        if not rows:
            return None, "Issue record not found"
        record = rows[0]
        if record['status'] == 'returned':
            return None, "Book already returned"
        Issue.return_book(issue_id)
        execute_query(
            "UPDATE books SET available_copies=available_copies+1 WHERE id=%s",
            (record['book_id'],), fetch=False
        )
        # Calculate fine
        fine_amount = 0.0
        today = date.today()
        due = record['due_date']
        if isinstance(due, str):
            from datetime import datetime
            due = datetime.strptime(due, "%Y-%m-%d").date()
        if today > due:
            overdue_days = (today - due).days
            fine_amount = round(overdue_days * FINE_PER_DAY, 2)
            Fine.create(issue_id, fine_amount)
        return {"fine": fine_amount}, None

    @staticmethod
    def get_active_issues():
        return Issue.get_active()

    @staticmethod
    def get_overdue():
        return Issue.get_overdue()
