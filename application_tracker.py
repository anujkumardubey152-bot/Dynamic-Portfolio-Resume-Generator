import sqlite3
from pathlib import Path


DEFAULT_DB = Path(__file__).resolve().parent.parent / "applications.db"

STATUSES = [
    "Interested",
    "Applied",
    "Assessment",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
]


def _connect(db_path=None):
    path = Path(db_path) if db_path else DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path=None):
    """Create the application table if it does not already exist."""
    with _connect(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                job_title TEXT NOT NULL,
                job_url TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'Interested',
                applied_date TEXT DEFAULT '',
                follow_up_date TEXT DEFAULT '',
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_application(
    company,
    job_title,
    job_url="",
    status="Interested",
    applied_date="",
    follow_up_date="",
    notes="",
    db_path=None,
):
    """Add one application and return its new database ID."""
    company = str(company or "").strip()
    job_title = str(job_title or "").strip()

    if not company:
        raise ValueError("Company name is required.")
    if not job_title:
        raise ValueError("Job title is required.")
    if status not in STATUSES:
        raise ValueError("Choose a valid application status.")

    initialize_database(db_path)

    with _connect(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO applications
            (company, job_title, job_url, status, applied_date, follow_up_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company,
                job_title,
                str(job_url or "").strip(),
                status,
                str(applied_date or ""),
                str(follow_up_date or ""),
                str(notes or "").strip(),
            ),
        )
        return cursor.lastrowid


def list_applications(status=None, db_path=None):
    """Return application records as dictionaries, newest first."""
    initialize_database(db_path)

    with _connect(db_path) as connection:
        if status and status != "All":
            rows = connection.execute(
                """
                SELECT * FROM applications
                WHERE status = ?
                ORDER BY created_at DESC, id DESC
                """,
                (status,),
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT * FROM applications
                ORDER BY created_at DESC, id DESC
                """
            ).fetchall()

    return [dict(row) for row in rows]


def update_application(application_id, db_path=None, **fields):
    """Update supported fields for an existing application."""
    allowed_fields = {
        "company",
        "job_title",
        "job_url",
        "status",
        "applied_date",
        "follow_up_date",
        "notes",
    }

    updates = {key: value for key, value in fields.items() if key in allowed_fields}
    if not updates:
        return False

    if "status" in updates and updates["status"] not in STATUSES:
        raise ValueError("Choose a valid application status.")

    for key in ("company", "job_title"):
        if key in updates:
            updates[key] = str(updates[key] or "").strip()
            if not updates[key]:
                raise ValueError(f"{key.replace('_', ' ').title()} is required.")

    initialize_database(db_path)
    columns = list(updates)
    assignments = ", ".join(f"{column} = ?" for column in columns)
    values = [updates[column] for column in columns]
    values.append(int(application_id))

    with _connect(db_path) as connection:
        cursor = connection.execute(
            f"UPDATE applications SET {assignments} WHERE id = ?",
            values,
        )
        return cursor.rowcount > 0


def delete_application(application_id, db_path=None):
    """Delete one application by its ID."""
    initialize_database(db_path)

    with _connect(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM applications WHERE id = ?",
            (int(application_id),),
        )
        return cursor.rowcount > 0
