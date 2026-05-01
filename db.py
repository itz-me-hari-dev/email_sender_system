import sqlite3
from datetime import datetime

DB_NAME = "emails.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        status TEXT,
        attempts INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_result(result):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO email_logs (email, status, attempts, timestamp)
    VALUES (?, ?, ?, ?)
    """, (
        result["email"],
        result["status"],
        result["attempts"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def clear_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM email_logs")

    conn.commit()
    conn.close()