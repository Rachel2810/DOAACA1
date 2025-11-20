import sqlite3
import os

DB_PATH = "database/history.db"

def init_db():
    if not os.path.exists("database"):
        os.makedirs("database")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feature1 REAL,
        feature2 REAL,
        feature3 REAL,
        prediction REAL,
        username TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()


def insert_history(f1, f2, f3, pred, user):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO history(feature1, feature2, feature3, prediction, username)
        VALUES (?, ?, ?, ?, ?)
    """, (f1, f2, f3, pred, user))
    conn.commit()
    conn.close()


def fetch_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows
