from storage import load_data, save_data
from datetime import datetime, timedelta

BOOKS_FILE = "library.json"
USERS_FILE = "users.json"
TRANS_FILE = "transactions.json"

books_cache = load_data(BOOKS_FILE, default=[])
users_cache = load_data(USERS_FILE, default=[])
trans_cache = load_data(TRANS_FILE, default=[])

FINE_PER_DAY = 10

def issue_book(user_id, book_id):
    if not user_id or not book_id:
        return False, "Provide user_id and book_id."
    user = next((u for u in users_cache if u.get("user_id") == user_id), None)
    if not user:
        return False, "User not found."
    book = next((b for b in books_cache if b.get("book_id") == book_id), None)
    if not book:
        return False, "Book not found."
    if not book.get("available", True):
        return False, "Book already issued."

    issue_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    book["available"] = False
    book["issued_to"] = user_id
    book["issue_date"] = issue_date

    user.setdefault("issued_books", []).append({
        "book_id": book_id,
        "issue_date": issue_date,
        "due_date": due_date
    })

    trans_cache.append({
        "user_id": user_id,
        "book_id": book_id,
        "issue_date": issue_date,
        "due_date": due_date,
        "status": "issued"
    })

    return True, f"Book {book_id} issued to {user_id} until {due_date}."

def return_book(user_id, book_id):
    user = next((u for u in users_cache if u.get("user_id") == user_id), None)
    if not user:
        return False, "User not found."
    issued = next((rec for rec in user.get("issued_books", []) if rec.get("book_id") == book_id), None)
    if not issued:
        return False, "This book was not issued to this user."

    book = next((b for b in books_cache if b.get("book_id") == book_id), None)
    if book:
        book["available"] = True
        book["issued_to"] = ""
        book["issue_date"] = ""

    due_date = datetime.strptime(issued["due_date"], "%Y-%m-%d")
    today = datetime.now()
    fine = 0
    if today > due_date:
        fine = (today - due_date).days * FINE_PER_DAY

    user["issued_books"].remove(issued)

    trans_cache.append({
        "user_id": user_id,
        "book_id": book_id,
        "return_date": today.strftime("%Y-%m-%d"),
        "fine": fine,
        "status": "returned"
    })

    msg = f"Book {book_id} returned successfully."
    if fine > 0:
        msg += f" Late fine: ₹{fine}"

    return True, msg

def save_transactions():
    # save transactions and also ensure books/users persisted (transactions depend on both)
    save_data(TRANS_FILE, trans_cache)
    save_data(BOOKS_FILE, books_cache)
    save_data(USERS_FILE, users_cache)

