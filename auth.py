#auth.py
import sqlite3
import hashlib

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Step 1: Create a table to store user credentials
def create_user_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()

# Step 2: Add a new user to the database
def add_user(username, password):
    try:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception("Username already exists.")

# Step 3: Verify login by checking if user and hashed password match
def verify_user(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
    return c.fetchone()
