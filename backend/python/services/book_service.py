# services/book_service.py
from models.book import Book
from utils.db_connection import execute_query

class BookService:
    @staticmethod
    def get_all():
        return Book.get_all()

    @staticmethod
    def search(keyword):
        return Book.search(keyword)

    @staticmethod
    def add_book(data):
        required = ['title', 'author']
        for f in required:
            if not data.get(f):
                return None, f"'{f}' is required"
        bid = Book.create(
            data['title'], data['author'],
            data.get('isbn',''), data.get('category',''),
            data.get('publisher',''), data.get('year', 0),
            data.get('copies', 1)
        )
        return bid, None

    @staticmethod
    def update_book(book_id, data):
        allowed = ['title','author','isbn','category','publisher','year','total_copies','available_copies']
        fields = {k: v for k, v in data.items() if k in allowed}
        if not fields:
            return False, "No valid fields to update"
        Book.update(book_id, **fields)
        return True, None

    @staticmethod
    def delete_book(book_id):
        # Check if book is currently issued
        active = execute_query(
            "SELECT id FROM issued_books WHERE book_id=%s AND status='issued'", (book_id,)
        )
        if active:
            return False, "Cannot delete: book has active issues"
        Book.delete(book_id)
        return True, None
