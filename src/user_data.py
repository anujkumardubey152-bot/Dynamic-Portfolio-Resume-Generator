
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "users.db"


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER PRIMARY KEY,
            profile_data TEXT NOT NULL DEFAULT '{}',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company TEXT NOT NULL,
            job_title TEXT NOT NULL,
            job_url TEXT DEFAULT '',
            status TEXT DEFAULT '',
            applied_date TEXT DEFAULT '',
            follow_up_date TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    return conn


def save_profile(user_id, profile):
    conn = connect()
    try:
        conn.execute("""
            INSERT INTO user_profiles (user_id, profile_data)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET profile_data = excluded.profile_data
        """, (user_id, json.dumps(profile)))
        conn.commit()
    finally:
        conn.close()


def load_profile(user_id):
    conn = connect()
    try:
        row = conn.execute(
            "SELECT profile_data FROM user_profiles WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        return json.loads(row["profile_data"]) if row else {}
    finally:
        conn.close()


def add_user_application(user_id, company, job_title, job_url="",
                         status="", applied_date="", follow_up_date="",
                         notes=""):
    conn = connect()
    try:
        conn.execute("""
            INSERT INTO user_applications
            (user_id, company, job_title, job_url, status,
             applied_date, follow_up_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, company, job_title, job_url, status,
            applied_date, follow_up_date, notes
        ))
        conn.commit()
    finally:
        conn.close()


def list_user_applications(user_id):
    conn = connect()
    try:
        rows = conn.execute("""
            SELECT * FROM user_applications
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,)).fetchall()

        return [dict(row) for row in rows]
    finally:
        conn.close()
