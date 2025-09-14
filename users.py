from storage import load_data, save_data

USERS_FILE = "users.json"
users_cache = load_data(USERS_FILE, default=[])

def add_user(user_id=None, name=None, email=None, phone=None):
    if not user_id:
        user_id = f"U{len(users_cache)+1:03}"
    if not name:
        name = input("Enter user name: ")
    new_user = {
        "user_id": user_id,
        "name": name,
        "email": email or "",
        "phone": phone or "",
        "issued_books": []
    }
    users_cache.append(new_user)
    return True, f"User '{name}' added successfully with ID {user_id}."

def view_users():
    return users_cache

def save_users():
    save_data(USERS_FILE, users_cache)

