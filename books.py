from storage import load_data, save_data

BOOKS_FILE = "library.json"
books_cache = load_data(BOOKS_FILE, default=[])

def add_book(book_id=None, title=None, author=None, genre="General"):
    if not book_id:
        book_id = f"B{len(books_cache)+1:03}"
    if not title:
        title = input("Enter book title: ")
    if not author:
        author = input("Enter book author: ")
    new_book = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "genre": genre,
        "available": True,
        "issued_to": "",
        "issue_date": ""
    }
    books_cache.append(new_book)
    return True, f"Book '{title}' added successfully with ID {book_id}."

def view_books():
    return books_cache

def search_book(keyword=None):
    if not keyword:
        keyword = input("Enter title or author to search: ")
    q = (keyword or "").lower()
    return [b for b in books_cache if q in b.get("title","").lower() or q in b.get("author","").lower()]

def save_books():
    save_data(BOOKS_FILE, books_cache)
