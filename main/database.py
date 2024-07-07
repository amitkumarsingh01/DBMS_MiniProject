import sqlite3

def init_db():
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        department INTEGER,
        description TEXT,
        date_of_lodging TEXT,
        address TEXT,
        file_attachment TEXT,
        suggestion TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    conn.commit()
    conn.close()

def add_user(name, email, password):
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user

def add_query(user_id, department, description, date_of_lodging, address, file_attachment, suggestion):
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute("INSERT INTO queries (user_id, department, description, date_of_lodging, address, file_attachment, suggestion) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (user_id, department, description, date_of_lodging, address, file_attachment, suggestion))
    conn.commit()
    conn.close()

def get_user_queries(user_id):
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute("SELECT * FROM queries WHERE user_id = ?", (user_id,))
    queries = c.fetchall()
    conn.close()
    return queries

def get_all_queries():
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute('''
    SELECT users.name, users.email, users.password, queries.*
    FROM queries
    JOIN users ON queries.user_id = users.id
    ''')
    queries = c.fetchall()
    conn.close()
    return queries
