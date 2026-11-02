
import sqlite3
import hashlib
import hmac
import secrets
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "users.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    return conn


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_hash):
    try:
        salt, expected_hash = stored_hash.split("$", 1)
        actual_hash = hash_password(password, salt).split("$", 1)[1]
        return hmac.compare_digest(actual_hash, expected_hash)
    except (ValueError, AttributeError):
        return False


def register_user(name, email, password):
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or len(password) < 8:
        return False, "Enter your name, valid email and password of at least 8 characters."

    conn = get_connection()

    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, hash_password(password))
        )
        conn.commit()
        return True, "Account created successfully. Please log in."

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

    finally:
        conn.close()


def login_user(email, password):
    conn = get_connection()

    try:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.strip().lower(),)
        ).fetchone()

        if user and verify_password(password, user["password_hash"]):
            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }

        return None

    finally:
        conn.close()
