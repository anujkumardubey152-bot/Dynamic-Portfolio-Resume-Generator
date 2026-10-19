import re
from urllib.parse import urlparse


def validate_email(email):
    """Return an error message, or None when the email looks valid."""
    email = str(email or "").strip()

    if not email:
        return None

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.fullmatch(pattern, email):
        return "Enter a valid email address, such as name@example.com."

    return None


def validate_url(url, field_name="Website"):
    """Allow empty URLs; otherwise require an HTTP or HTTPS URL."""
    url = str(url or "").strip()

    if not url:
        return None

    try:
        parsed = urlparse(url)
    except ValueError:
        return f"{field_name} must be a valid web address."

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return f"{field_name} must start with https:// or http://."

    if any(char.isspace() for char in url):
        return f"{field_name} must not contain spaces."

    return None


def validate_profile(profile):
    """
    Validate a profile dictionary.
    Returns a list of user-readable error messages.
    """
    profile = profile or {}
    errors = []

    name = str(profile.get("name") or "").strip()
    if not name:
        errors.append("Name is required.")
    elif len(name) > 100:
        errors.append("Name must be 100 characters or fewer.")

    email_error = validate_email(profile.get("email"))
    if email_error:
        errors.append(email_error)

    for field, label in (
        ("linkedin", "LinkedIn URL"),
        ("website", "Website URL"),
    ):
        url_error = validate_url(profile.get(field), label)
        if url_error:
            errors.append(url_error)

    summary = str(profile.get("summary") or "")
    if len(summary) > 3000:
        errors.append("Summary must be 3,000 characters or fewer.")

    return errors


def validate_job_description(description):
    """Validate the text supplied for job matching."""
    description = str(description or "").strip()

    if not description:
        return "Paste a job description before running the match."

    if len(description) < 30:
        return "Please enter a more complete job description (at least 30 characters)."

    if len(description) > 30000:
        return "Job description is too long. Limit it to 30,000 characters."

    return None
