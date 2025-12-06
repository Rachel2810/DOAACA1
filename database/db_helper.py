# database/db_helper.py
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "history.db"

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        cur = conn.cursor()

        # Prediction table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                area REAL,
                beds REAL,
                baths REAL,
                prediction TEXT,
                model_name TEXT,
                created_at TEXT
            )
        """)

        # Simple user table (optional)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT
            )
        """)

        conn.commit()


def insert_prediction(username, area, beds, baths, prediction, model_name="random_forest"):
    now = datetime.utcnow().isoformat()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO predictions (username, area, beds, baths, prediction, model_name, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, area, beds, baths, str(prediction), model_name, now))
        conn.commit()


def fetch_predictions(limit=500):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM predictions ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
    return rows


def add_user(username, password_hash):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))
        conn.commit()


def get_user(username):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()
