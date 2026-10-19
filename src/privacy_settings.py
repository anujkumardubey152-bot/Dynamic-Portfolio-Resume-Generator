import sqlite3
from pathlib import Path

from src.application_tracker import initialize_database


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE = PROJECT_DIR / "applications.db"


def get_database_path(db_path=None):
    """Return the configured local SQLite database path."""
    return Path(db_path) if db_path else DEFAULT_DATABASE


def get_database_info(db_path=None):
    """Return basic information about the local application database."""
    path = get_database_path(db_path)

    return {
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else 0,
    }


def clear_application_database(db_path=None, confirm=False):
    """
    Delete all application records by removing the SQLite database file.

    The caller must explicitly pass confirm=True.
    """
    if not confirm:
        raise ValueError(
            "Confirmation is required before deleting application data."
        )

    path = get_database_path(db_path)

    if not path.exists():
        return False

    # Ensure the database is not being used by an active connection.
    with sqlite3.connect(str(path)) as connection:
        connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")

    # Remove SQLite sidecar files if present.
    for suffix in ("-wal", "-shm"):
        sidecar = Path(str(path) + suffix)
        if sidecar.exists():
            sidecar.unlink()

    path.unlink()
    return True


def reset_application_database(db_path=None, confirm=False):
    """Clear saved applications and initialize an empty database."""
    if not confirm:
        raise ValueError(
            "Confirmation is required before resetting application data."
        )

    path = get_database_path(db_path)

    if path.exists():
        clear_application_database(path, confirm=True)

    initialize_database(db_path=path)
    return path


PRIVACY_GUIDANCE = [
    "Do not commit personal resumes, .env files, or application databases to GitHub.",
    "Keep applications.db excluded through .gitignore.",
    "Review PDF resumes and portfolio HTML before sharing them publicly.",
    "Use only contact information you intend to publish.",
    "Keep backups before deleting application records.",
]
