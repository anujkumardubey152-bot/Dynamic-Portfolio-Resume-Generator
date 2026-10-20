```python
import smtplib
import streamlit as st
from email.message import EmailMessage
from supabase import create_client


def _get_supabase():
    database = st.secrets.get("database", {})
    url = database.get("url", "").strip()
    key = database.get("service_role_key", "").strip()

    if not url or not key:
        raise ValueError(
            "Missing database URL or service-role key in Streamlit Secrets."
        )

    return create_client(url, key)


def save_submission(name, email, resume_text, job_description, consent):
    if not consent:
        return False

    client = _get_supabase()
    client.table("submissions").insert({
        "name": name.strip(),
        "email": email.strip(),
        "resume_text": resume_text,
        "job_description": job_description,
        "consent": True,
    }).execute()

    return True


def _send_owner_notification(subject, body):
    settings = st.secrets.get("email", {})
    host = settings.get("smtp_server", "")
    port = int(settings.get("smtp_port", 587))
    username = settings.get("sender_email", "")
    password = settings.get("sender_password", "")
    recipient = settings.get("owner_email", "")

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
    st.title("Admin Dashboard")

    admin_password = st.secrets.get("admin", {}).get("password", "")

    if not admin_password:
        st.error(
            "Admin password is missing. Configure [admin] password "
            "in Streamlit Cloud Secrets."
        )
        return

    if not st.session_state.get("owner_authenticated", False):
        entered_password = st.text_input(
            "Admin password",
            type="password",
            key="admin_password_input",
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
                "id, created_at, name, email, "
                "resume_text, job_description, consent"
            )
            .order("created_at", desc=True)
            .limit(500)
            .execute()
        )
        records = response.data or []

    except Exception as exc:
        st.error("Could not load submissions from Supabase.")

        # Display diagnostic details without exposing the configured key.
        message = str(exc)
        key = st.secrets.get("database", {}).get("service_role_key", "")
        if key:
            message = message.replace(key, "[REDACTED]")

        st.code(f"{type(exc).__name__}: {message}")
        st.info(
            "Verify the Supabase Project URL, service-role key, "
            "and public.submissions table."
        )
        return

    if not records:
        st.info("No submissions have been saved yet.")
        return

    st.success(f"Loaded {len(records)} submission(s).")

    for index, record in enumerate(records):
        name = record.get("name") or "Unnamed"
        created_at = record.get("created_at") or "Unknown date"

        with st.expander(f"{name} — {created_at}"):
            st.write("**Email:**", record.get("email", ""))
            st.write("**Consent:**", record.get("consent", False))

            st.write("**Resume text**")
            st.text_area(
                "Resume",
                value=record.get("resume_text", ""),
                height=180,
                key=f"resume_{index}",
            )

            st.write("**Job description**")
            st.text_area(
                "Job description",
                value=record.get("job_description", ""),
                height=180,
                key=f"job_{index}",
            )
```
