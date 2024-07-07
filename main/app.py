import streamlit as st
import sqlite3
from datetime import datetime

# Function to create or get database connection
def get_connection():
    conn = sqlite3.connect('complaints.db')
    return conn

# Function to create user account
def create_user(name, email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()

# Function to authenticate user
def authenticate_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    return user

# Function to fetch all complaints
def fetch_complaints():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT users.name, users.email, complaints.* FROM complaints INNER JOIN users ON complaints.user_id = users.id")
    complaints = c.fetchall()
    conn.close()
    return complaints

# Function to insert complaint
def insert_complaint(user_id, department, description, lodging_date, location, file_attachment, suggestion):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO complaints (user_id, department, description, lodging_date, location, file_attachment, suggestion) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (user_id, department, description, lodging_date, location, file_attachment, suggestion))
    conn.commit()
    conn.close()

# Streamlit interface
def main():
    st.title('Complaint Management System')

    menu = ['Login', 'Register']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Login':
        st.subheader('Login')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            user = authenticate_user(email, password)
            if user:
                st.success(f'Logged in as {user[1]}')
                user_id = user[0]
                st.write('Fill New Complaint Form:')
                department = st.selectbox('Department Name', [1, 2, 3, 4])
                description = st.text_area('Description')
                lodging_date = st.date_input('Date of Lodging', datetime.today())
                location = st.text_input('Address/Location')
                file_attachment = st.file_uploader('File Attachment')
                suggestion = st.text_area('Suggestion (Optional)')
                if st.button('Submit'):
                    insert_complaint(user_id, department, description, lodging_date, location, file_attachment, suggestion)
                    st.success('Complaint submitted successfully!')

            else:
                st.error('Invalid credentials')

    elif choice == 'Register':
        st.subheader('Create a new account')
        name = st.text_input('Name')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        if st.button('Register'):
            create_user(name, email, password)
            st.success('Account created successfully! Please login.')

if __name__ == '__main__':
    main()
