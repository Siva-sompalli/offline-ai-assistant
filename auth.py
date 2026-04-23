import sqlite3
from database import get_connection

def register_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user
