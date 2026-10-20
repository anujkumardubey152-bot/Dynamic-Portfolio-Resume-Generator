
import smtplib
from email.message import EmailMessage

import streamlit as st


def _get_supabase():
    """Connect to Supabase using private Streamlit secrets."""
    from supabase import create_client

    url = st.secrets["database"]["url"]
    key = st.secrets["database"]["service_role_key"]

    return create_client(url, key)


def _send_owner_notification(name, email):
    """Notify the owner without emailing resume contents."""
    settings = st.secrets.get("email", {})

    host = settings.get("smtp_host")
    username = settings.get("smtp_username")
    password = settings.get("smtp_app_password")
    recipient = settings.get("notification_to")

    if not all([host, username, password, recipient]):
        return False

    message = EmailMessage()
    message["Subject"] = "New CareerForge AI submission"
    message["From"] = username
    message["To"] = recipient
    message.set_content(
        f"A user submitted information with consent.\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        "Sign in to the private admin dashboard to review it."
    )

    port = int(settings.get("smtp_port", 587))

    with smtplib.SMTP(host, port, timeout=20) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(message)

    return True


def save_submission(
    name,
    email,
    resume_text,
    job_description,
    consent,
):
    """Save user data only after explicit consent."""
    if not consent:
        return False, "Please provide consent before submitting."

    if not str(name).strip() or not str(email).strip():
        return False, "A name and email address are required."

    if not str(resume_text).strip():
        return False, "There is no profile information to submit."

    try:
        client = _get_supabase()

        client.table("submissions").insert({
            "name": str(name).strip(),
            "email": str(email).strip(),
            "resume_text": str(resume_text),
            "job_description": str(job_description or ""),
            "consent": True,
        }).execute()

    except Exception:
        return (
            False,
            "Could not save your submission. Check the database "
            "configuration and try again.",
        )

    notification_sent = False

    try:
        notification_sent = _send_owner_notification(
            str(name).strip(),
            str(email).strip(),
        )
    except Exception:
        # The database record is already saved.
        pass

    if notification_sent:
        return True, "Submission saved. The owner has been notified."

    return (
        True,
        "Submission saved successfully. Email notification could not "
        "be sent, so the owner should check the admin dashboard.",
    )


def render_admin_page():
    """Display a password-protected owner dashboard."""
    st.title("CareerForge AI — Owner Dashboard")

    try:
        expected_password = st.secrets["admin"]["password"]
    except Exception:
        st.error("The admin password is not configured in app secrets.")
        st.stop()

    if not st.session_state.get("owner_authenticated", False):
        password = st.text_input(
            "Owner password",
            type="password",
        )

        if st.button("Sign in", type="primary"):
            if password and password == expected_password:
                st.session_state.owner_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")

        st.caption("This page is for the app owner only.")
        return

    if st.button("Sign out"):
        st.session_state.owner_authenticated = False
        st.rerun()

    try:
        client = _get_supabase()

        response = (
            client.table("submissions")
            .select("*")
            .order("created_at", desc=True)
            .limit(500)
            .execute()
        )

        records = response.data or []

    except Exception:
        st.error(
            "Could not load submissions. Check the Supabase secrets "
            "and table permissions."
        )
        return

    st.subheader("User submissions")
    st.write(f"Total records loaded: {len(records)}")

    if not records:
        st.info("No submissions found.")
        return

    for record in records:
        record_id = record.get("id")

        with st.expander(
            f"{record.get('name', 'Unknown')} — "
            f"{record.get('created_at', '')}"
        ):
            st.write("**Email:**", record.get("email", ""))
            st.write("**Consent:**", record.get("consent", False))

            st.subheader("Submitted profile / resume")
            st.text_area(
                "Resume text",
                value=record.get("resume_text", ""),
                height=200,
                key=f"resume_{record_id}",
                disabled=True,
            )

            st.subheader("Job description")
            st.text_area(
                "Job description text",
                value=record.get("job_description", ""),
                height=160,
                key=f"job_{record_id}",
                disabled=True,
            )

            confirm = st.checkbox(
                "Confirm deletion of this record",
                key=f"confirm_delete_{record_id}",
            )

            if st.button(
                "Delete record",
                key=f"delete_{record_id}",
            ):
                if not confirm:
                    st.warning("Confirm deletion first.")
                else:
                    try:
                        (
                            client.table("submissions")
                            .delete()
                            .eq("id", record_id)
                            .execute()
                        )
                        st.success("Record deleted.")
                        st.rerun()
                    except Exception:
                        st.error("Could not delete this record.")
