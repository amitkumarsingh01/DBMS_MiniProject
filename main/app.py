import streamlit as st
import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

# Functions for database operations
def create_user_table():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    
def create_complaints_table():
    c.execute('''CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    department INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    location TEXT NOT NULL,
                    attachment TEXT,
                    suggestion TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')

def add_complaint(user_id, department, description, date, location, attachment, suggestion):
    c.execute('''INSERT INTO complaints (user_id, department, description, date, location, attachment, suggestion)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (user_id, department, description, date, location, attachment, suggestion))
    conn.commit()
    st.success('Complaint added successfully!')

def fetch_user(email):
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    return c.fetchone()

def fetch_all_complaints():
    c.execute("SELECT * FROM complaints")
    return c.fetchall()

# Initialize tables
create_user_table()
create_complaints_table()

# Streamlit app
def main():
    st.title("Complaint Management System")

    menu = ["Home", "Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to Complaint Management System")

    elif choice == "Login":
        st.subheader("Login Section")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            user = fetch_user(email)
            if user:
                if password == user[3]:  # Check password
                    st.success(f"Logged in as {user[1]}")
                    # Display user's complaints or add new complaint based on user role
                else:
                    st.error("Incorrect email or password")
            else:
                st.error("User not found")

    elif choice == "Register":
        st.subheader("Create New Account")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        if st.button("Register"):
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            st.success(f"Account created for {name}!")

    # Admin Section
    if st.sidebar.checkbox("Admin Login"):
        admin_username = "dbms"
        admin_password = "12345"
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')
        if username == admin_username and password == admin_password:
            st.subheader("Admin Dashboard")
            complaints = fetch_all_complaints()
            if complaints:
                st.write("All Complaints:")
                for complaint in complaints:
                    st.write(f"User: {complaint[1]}, Email: {complaint[2]}, Timestamp: {complaint[9]}")
                    st.write(f"Department: {complaint[3]}")
                    st.write(f"Description: {complaint[4]}")
                    st.write(f"Date: {complaint[5]}")
                    st.write(f"Location: {complaint[6]}")
                    st.write(f"Suggestion: {complaint[8]}")
                    st.write("-----")
            else:
                st.write("No complaints yet.")

if __name__ == '__main__':
    main()
