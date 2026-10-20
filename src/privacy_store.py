```python
import smtplib
import streamlit as st
from email.message import EmailMessage
from supabase import create_client


def _get_supabase():
    """Connect to Supabase using Streamlit secrets."""
    database = st.secrets.get("database", {})

    url = database.get("url", "").strip()
    service_role_key = database.get("service_role_key", "").strip()

    if not url or not service_role_key:
        raise ValueError(
            "Missing database.url or database.service_role_key "
            "in Streamlit Cloud Secrets."
        )

    return create_client(url, service_role_key)


def save_submission(
    name,
    email,
    resume_text,
    job_description,
    consent,
):
    """Save a submission only when consent is provided."""
    if not consent:
        return False

    client = _get_supabase()

    record = {
        "name": name.strip(),
        "email": email.strip(),
        "resume_text": resume_text,
        "job_description": job_description,
        "consent": True,
    }

    client.table("submissions").insert(record).execute()
    return True


def _send_owner_notification(subject, body):
    """Send an optional email notification to the owner."""
    email_settings = st.secrets.get("email", {})

    host = email_settings.get("smtp_server", "")
    port = int(email_settings.get("smtp_port", 587))
    username = email_settings.get("sender_email", "")
    password = email_settings.get("sender_password", "")
    recipient = email_settings.get("owner_email", "")

    if not all([host, username, password, recipient]):
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = username
    message["To"] = recipient
    message.set_content(body)

    with smtplib.SMTP(host, port, timeout=15) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(message)

    return True


def render_admin_page():
    """Show stored submissions to an authenticated administrator."""
    st.title("Admin Dashboard")

    admin_settings = st.secrets.get("admin", {})
    admin_password = admin_settings.get("password", "")

    if not admin_password:
        st.error(
            "
