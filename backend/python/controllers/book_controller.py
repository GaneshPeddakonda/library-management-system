# controllers/book_controller.py
from flask import Blueprint, request
from services.book_service import BookService
from utils.helper import success, error
from controllers.auth_middleware import token_required

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    keyword = request.args.get('q')
    data = BookService.search(keyword) if keyword else BookService.get_all()
    return success(data)

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    from models.book import Book
    book = Book.get_by_id(book_id)
    return success(book) if book else error("Book not found", 404)

@books_bp.route('/', methods=['POST'])
@token_required
def add_book(current_user):
    data = request.get_json() or {}
    bid, err = BookService.add_book(data)
    if err:
        return error(err)
    return success({"id": bid}, "Book added successfully", 201)

@books_bp.route('/<int:book_id>', methods=['PUT'])
@token_required
def update_book(current_user, book_id):
    data = request.get_json() or {}
    ok, err = BookService.update_book(book_id, data)
    if err:
        return error(err)
    return success(None, "Book updated")

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user, book_id):
    ok, err = BookService.delete_book(book_id)
    if err:
        return error(err)
    return success(None, "Book deleted")
