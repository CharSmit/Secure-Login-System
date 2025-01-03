import sqlite3

def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  
    return conn


def initialize_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        username TEXT UNIQUE PRIMARY KEY,
        email TEXT UNIQUE,
        password_hash TEXT

        );
        """)
        conn.commit()

def add_user(username, email, password_hash):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash),
        )
        conn.commit()


def get_user(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()


def update_user_password(username, new_password_hash):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (new_password_hash, username),
        )
        conn.commit()

def existing_user(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result is not None