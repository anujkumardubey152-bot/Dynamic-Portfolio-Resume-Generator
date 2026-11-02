import re
import sqlite3
import hashlib
import secrets
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "users.db"

PBKDF2_ITERATIONS = 200_000


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    return connection


def normalize_email(email):
    return str(email or "").strip().lower()


def validate_email(email):
    email = normalize_email(email)

    if not email:
        return False, "Email address is required."

    if len(email) > 254:
        return False, "Email address is too long."

    pattern = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"

    if not re.fullmatch(pattern, email):
        return False, "Enter a valid email address, such as name@example.com."

    if ".." in email or email.startswith(".") or email.endswith("."):
        return False, "Please enter a valid email address."

    local_part = email.split("@")[0]

    if local_part.startswith(".") or local_part.endswith("."):
        return False, "Please enter a valid email address."

    return True, ""


def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PBKDF2_ITERATIONS,
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_hash):
    try:
        salt, saved_hash = stored_hash.split("$", 1)

        check_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            PBKDF2_ITERATIONS,
        ).hex()

        return secrets.compare_digest(check_hash, saved_hash)

    except (ValueError, AttributeError):
        return False


def register_user(name, email, password):
    name = str(name or "").strip()
    email = normalize_email(email)

    if not name:
        return False, "Please enter your full name."

    valid, message = validate_email(email)

    if not valid:
        return False, message

    if not password or len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if len(password) > 128:
        return False, "Password must be 128 characters or fewer."

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (name, email, hash_password(password)),
        )

        connection.commit()
        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

    finally:
        connection.close()


def login_user(email, password):
    email = normalize_email(email)

    valid, _ = validate_email(email)

    if not valid or not password:
        return None

    connection = get_connection()

    try:
        user = connection.execute(
            """
            SELECT id, name, email, password_hash
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

        if user is None:
            return None

        if not verify_password(password, user["password_hash"]):
            return None

        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        }

    finally:
        connection.close()
