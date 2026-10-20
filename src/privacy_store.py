import smtplib
from email.message import EmailMessage

import streamlit as st
from supabase import create_client


def _get_supabase():
    """Create a Supabase client using Streamlit secrets."""
    database = st.secrets.get("database", {})
    url = str(database.get("url", "")).strip()
    service_role_key = str(database.get("service_role_key", "")).strip()

    if not url or not service_role_key:
        raise ValueError(
            "Missing database.url or database.service_role_key in Streamlit Secrets."
        )

    return create_client(url, service_role_key)


def save_submission(name, email, resume_text, job_description, consent):
    """Save a submission to Supabase only when consent is true."""
    if not consent:
        return False

    client = _get_supabase()
    record = {
        "name": str(name).strip(),
        "email": str(email).strip(),
        "resume_text": str(resume_text),
        "job_description": str(job_description),
        "consent": True,
    }
    client.table("submissions").insert(record).execute()
    return True


def _send_owner_notification(subject, body):
    """Send an optional owner email when SMTP settings are configured."""
    settings = st.secrets.get("email", {})
    host = str(settings.get("smtp_server", "")).strip()
    username = str(settings.get("sender_email", "")).strip()
    password = str(settings.get("sender_password", "")).strip()
    recipient = str(settings.get("owner_email", "")).strip()

    try:
        port = int(settings.get("smtp_port", 587))
    except (TypeError, ValueError):
        port = 587

    if not all((host, username, password, recipient)):
        return False

    message = EmailMessage()
    message["Subject"] = str(subject)
    message["From"] = username
    message["To"] = recipient
    message.set_content(str(body))

    with smtplib.SMTP(host, port, timeout=15) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(message)

    return True


def render_admin_page():
    """Authenticate the owner and display saved submissions."""
    st.title("Admin Dashboard")

    admin_password = str(st.secrets.get("admin", {}).get("password", ""))
    if not admin_password:
        st.error(
            "Admin password is missing. Add a password under [admin] "
            "in Streamlit Cloud Secrets."
        )
        return

    if not st.session_state.get("owner_authenticated", False):
        entered_password = st.text_input(
            "Admin password", type="password", key="admin_password_input"
        )
        if st.button("Log in", key="admin_login_button"):
            if entered_password and entered_password == admin_password:
                st.session_state["owner_authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        return

    if st.button("Log out", key="admin_logout_button"):
        st.session_state["owner_authenticated"] = False
        st.rerun()

    st.subheader("Stored Submissions")
    try:
        client = _get_supabase()
        response = (
            client.table("submissions")
            .select(
                "id, created_at, name, email, resume_text, "
                "job_description, consent"
            )
            .order("created_at", desc=True)
            .limit(500)
            .execute()
        )
        records = response.data or []
    except Exception as exc:
        st.error("Could not load submissions from Supabase.")
        message = str(exc)
        secret_key = str(
            st.secrets.get("database", {}).get("service_role_key", "")
        )
        if secret_key:
            message = message.replace(secret_key, "[REDACTED]")
        st.code(f"{type(exc).__name__}: {message}")
        st.info(
            "Check that the Supabase URL and service-role key belong to the "
            "same project and that public.submissions exists with the expected columns."
        )
        return

    if not records:
        st.info("No submissions have been saved yet.")
        return

    st.success(f"Loaded {len(records)} submission(s).")
    for index, record in enumerate(records):
        display_name = record.get("name") or "Unnamed"
        created_at = record.get("created_at") or "Unknown date"
        with st.expander(f"{display_name} — {created_at}"):
            st.write("**Email:**", record.get("email", ""))
            st.write("**Consent:**", record.get("consent", False))
            st.text_area(
                "Resume text",
                value=record.get("resume_text", ""),
                height=180,
                key=f"admin_resume_{index}",
            )
            st.text_area(
                "Job description",
                value=record.get("job_description", ""),
                height=180,
                key=f"admin_job_description_{index}",
            )
