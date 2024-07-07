import streamlit as st
import sqlite3
from database import init_db, add_user, authenticate_user, add_query, get_user_queries, get_all_queries
import datetime

# Initialize database
init_db()

# Utility functions
def login(email, password):
    user = authenticate_user(email, password)
    return user

def register(name, email, password):
    add_user(name, email, password)
    st.success("You have successfully registered. Please login.")

# Streamlit UI
st.title("Query Management System")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

def handle_login(email, password):
    user = login(email, password)
    if user:
        st.session_state.logged_in = True
        st.session_state.user_info = user
    else:
        st.warning("Incorrect Email/Password")

menu = ["Home", "Login", "Register", "Admin"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Welcome to the Query Management System")

elif choice == "Login":
    st.subheader("Login Section")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        handle_login(email, password)

elif choice == "Register":
    st.subheader("Register Section")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Register"):
        register(name, email, password)

elif choice == "Admin":
    st.subheader("Admin Login")
    admin_user = st.text_input("Username")
    admin_password = st.text_input("Password", type='password')
    if st.button("Login as Admin"):
        if admin_user == "Amit" and admin_password == "12345":
            st.session_state.logged_in = True
            st.session_state.user_info = {"name": "Amit", "email": "admin@example.com", "role": "admin"}
            st.success("Logged in as Admin")
        else:
            st.warning("Incorrect Admin Username/Password")

if st.session_state.logged_in:
    if st.session_state.user_info[1] == 'Amit' and st.session_state.user_info[3] == '12345':
        st.subheader("Admin Section")
        queries = get_all_queries()
        for query in queries:
            st.write(f"Name: {query[0]}, Email: {query[1]}, Password: {query[2]}, Time: {query[9]}")
            st.write(f"Department: {query[4]}, Description: {query[5]}, Date: {query[6]}, Address: {query[7]}, Suggestion: {query[8]}")
            st.write("---")
    else:
        st.subheader("User Section")

        if st.button("+ Add New Query"):
            st.session_state.show_form = not st.session_state.show_form

        if st.session_state.show_form:
            st.subheader("New Query Form")
            department = st.selectbox("Department Name", [1, 2, 3, 4])
            description = st.text_area("Description")
            date_of_lodging = st.date_input("Date of Lodging", datetime.date.today())
            address = st.text_input("Address/Location")
            file_attachment = st.file_uploader("File Attachment")
            suggestion = st.text_area("Suggestion (Optional)")
            if st.button("Submit"):
                add_query(st.session_state.user_info[0], department, description, date_of_lodging, address, file_attachment.name if file_attachment else None, suggestion)
                st.success("Query Submitted Successfully")
                st.session_state.show_form = False

        st.subheader("Your Queries")
        queries = get_user_queries(st.session_state.user_info[0])
        for query in queries:
            st.write(f"Department: {query[2]}, Description: {query[3]}, Date: {query[4]}, Address: {query[5]}, Suggestion: {query[7]}, Time: {query[8]}")
            st.write("---")
