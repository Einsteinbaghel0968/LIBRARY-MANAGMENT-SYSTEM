import streamlit as st
from books import add_book, view_books, search_book, save_books
from users import add_user, view_users, save_users
from transactions import issue_book, return_book, save_transactions

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# Sidebar menu
menu = [
    "Home", 
    "Add Book", "View Books", "Search Book", "Edit Book",
    "Add User", "View Users", "Edit User",
    "Issue Book", "Return Book"
]
choice = st.sidebar.selectbox("Menu", menu)

# 🔹 Home Page
if choice == "Home":
    st.markdown("<h1 style='text-align: center; color: #4B0082;'>📚 Welcome to the Library Management System</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #6A5ACD;'>Manage books, users, and transactions efficiently</h4>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Books", len(view_books()))
    col2.metric("Total Users", len(view_users()))
    col3.metric("Books Issued", "Check Reports")

    st.image("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=800&q=80", use_container_width=True)

    st.markdown("""
    <div style='text-align: center;'>
    <p>➡ Use the sidebar to navigate between functionalities.</p>
    <p>➡ Add, edit, view, issue and return books easily.</p>
    </div>
    """, unsafe_allow_html=True)

# 🔹 Add Book
elif choice == "Add Book":
    st.subheader("Add a New Book")
    book_title = st.text_input("Book Title")
    book_author = st.text_input("Author")
    book_id = st.text_input("Book ID (Leave blank for auto)")
    if st.button("Add Book"):
        success, msg = add_book(book_id, book_title, book_author)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# 🔹 View Books
elif choice == "View Books":
    st.subheader("All Books")
    books = view_books()
    if books:
        st.table(books)
    else:
        st.warning("No books available.")

# 🔹 Search Book
elif choice == "Search Book":
    st.subheader("Search a Book")
    query = st.text_input("Enter book title or author")
    if st.button("Search"):
        results = search_book(query)
        if results:
            st.table(results)
        else:
            st.warning("No book found matching the query!")

# 🔹 Edit Book
elif choice == "Edit Book":
    st.subheader("Edit Book Details")
    books = view_books()
    if books:
        book_ids = [b["book_id"] for b in books]
        selected_book = st.selectbox("Select Book ID", book_ids)
        book = next((b for b in books if b["book_id"] == selected_book), None)

        if book:
            new_title = st.text_input("Book Title", book["title"])
            new_author = st.text_input("Author", book["author"])

            if st.button("Update Book"):
                book["title"] = new_title
                book["author"] = new_author
                st.success(f"Book '{selected_book}' updated successfully!")
    else:
        st.warning("No books available.")

# 🔹 Add User
elif choice == "Add User":
    st.subheader("Add a New User")
    user_name = st.text_input("User Name")
    user_email = st.text_input("Email")
    user_phone = st.text_input("Phone")
    user_id = st.text_input("User ID (Leave blank for auto)")
    if st.button("Add User"):
        success, msg = add_user(user_id, user_name, user_email, user_phone)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# 🔹 View Users
elif choice == "View Users":
    st.subheader("All Users")
    users = view_users()
    if users:
        st.table(users)
    else:
        st.warning("No users available.")

# 🔹 Edit User
elif choice == "Edit User":
    st.subheader("Edit User Details")
    users = view_users()
    if users:
        user_ids = [u["user_id"] for u in users]
        selected_user = st.selectbox("Select User ID", user_ids)
        user = next((u for u in users if u["user_id"] == selected_user), None)

        if user:
            new_name = st.text_input("User Name", user["name"])
            new_email = st.text_input("Email", user.get("email", ""))
            new_phone = st.text_input("Phone", user.get("phone", ""))

            if st.button("Update User"):
                user["name"] = new_name
                user["email"] = new_email
                user["phone"] = new_phone
                st.success(f"User '{selected_user}' updated successfully!")
    else:
        st.warning("No users available.")

# 🔹 Issue Book
elif choice == "Issue Book":
    st.subheader("Issue a Book")
    user_id = st.text_input("User ID")
    book_id = st.text_input("Book ID")
    if st.button("Issue Book"):
        success, msg = issue_book(user_id, book_id)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# 🔹 Return Book
elif choice == "Return Book":
    st.subheader("Return a Book")
    user_id = st.text_input("User ID (Return)")
    book_id = st.text_input("Book ID (Return)")
    if st.button("Return Book"):
        success, msg = return_book(user_id, book_id)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# 🔹 Save All Changes Button
st.sidebar.markdown("---")
if st.sidebar.button("💾 Save All Changes"):
    save_users()
    save_books()
    save_transactions()
    st.sidebar.success("All changes saved to disk!")
   