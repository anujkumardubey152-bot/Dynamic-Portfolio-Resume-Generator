from pathlib import Path
import sys
from datetime import date
import json

import streamlit as st
import pandas as pd

# --------------------------------------------------
# 1. APP CONFIGURATION AND IMPORT PATH
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"

# Ensure Python can find the src package on Streamlit Cloud.
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

st.set_page_config(
    page_title="CareerForge AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# 2. IMPORT PROJECT MODULES
# --------------------------------------------------

try:
    from src.resume_generator import generate_resume_pdf
    from src.portfolio_generator import generate_portfolio_html
    from src.application_tracker import (
        STATUSES,
        add_application,
        list_applications,
        update_application,
        delete_application,
    )
    from src.job_matcher import analyze_job_match
    from src.validation import (
        validate_profile,
        validate_job_description,
    )
    from src.dashboard import build_dashboard_data
    from src.privacy_settings import (
        get_database_info,
        reset_application_database,
        PRIVACY_GUIDANCE,
    )
    from src.privacy_store import render_admin_page, save_submission
    from src.auth_ui import render_auth_page
    from src.user_data import (
        load_profile,
        save_profile as save_user_profile,
        add_user_application,
        list_user_applications,
        connect as connect_user_data,
    )

except ModuleNotFoundError as exc:
    st.error("A required project module or dependency is missing.")
    st.code(str(exc))

    st.markdown(
        """
        **Check your GitHub repository structure:**

        ```text
        Dynamic-Portfolio-Resume-Generator/
        ├── app.py
        ├── requirements.txt
        └── src/
            ├── __init__.py
            ├── resume_generator.py
            ├── portfolio_generator.py
            ├── application_tracker.py
            ├── job_matcher.py
            ├── validation.py
            ├── dashboard.py
            └── privacy_settings.py
        ```

        Commit the missing files and redeploy the app.
        """
    )
    st.stop()

# --------------------------------------------------
# OWNER-ONLY ADMIN DASHBOARD
# Open your app URL with ?admin=1, then enter the owner password.
# --------------------------------------------------
if st.query_params.get("admin") == "1":
    render_admin_page()
    st.stop()

# --------------------------------------------------
# USER LOGIN: every user must sign in before using the app.
# The owner admin page above remains a separate route.
# --------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    render_auth_page()
    st.stop()

# --------------------------------------------------
# 3. SESSION STATE
# --------------------------------------------------

DEFAULT_PROFILE = {
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "website": "",
    "summary": "",
    "skills": [],
    "experience": [],
    "education": [],
    "projects": [],
}

# Load the signed-in user's saved profile once per account.
active_user_id = st.session_state.user["id"]
if st.session_state.get("active_user_id") != active_user_id:
    try:
        saved_profile = load_profile(active_user_id) or {}
    except Exception as exc:
        st.error(f"Could not load your saved profile: {exc}")
        saved_profile = {}
    st.session_state.profile = {**DEFAULT_PROFILE, **saved_profile}
    st.session_state.active_user_id = active_user_id
    st.session_state.job_description = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# --------------------------------------------------
# 4. HELPER FUNCTIONS
# --------------------------------------------------

def parse_lines(value):
    """Convert multiline text into a list of non-empty lines."""
    return [
        line.strip()
        for line in str(value or "").splitlines()
        if line.strip()
    ]


def parse_skills(value):
    """Convert comma-separated skills into a clean list."""
    return list(dict.fromkeys(
        skill.strip()
        for skill in str(value or "").replace("\n", ",").split(",")
        if skill.strip()
    ))


def current_profile():
    return st.session_state.profile


def get_application_id(application):
    """Support common database ID field names."""
    for key in ("id", "application_id"):
        if application.get(key) is not None:
            return application[key]
    return None


def get_applications():
    """Load only the signed-in user's application records."""
    try:
        return list_user_applications(st.session_state.user["id"]) or []
    except Exception as exc:
        st.error(f"Could not load the application tracker: {exc}")
        return []


def update_owned_application(application_id, **fields):
    """Update an application only when it belongs to the signed-in user."""
    allowed = {
        "company", "job_title", "job_url", "status",
        "applied_date", "follow_up_date", "notes",
    }
    values = {key: value for key, value in fields.items() if key in allowed}
    if not values:
        return False
    assignments = ", ".join(f"{key} = ?" for key in values)
    with connect_user_data() as connection:
        cursor = connection.execute(
            f"UPDATE user_applications SET {assignments} "
            "WHERE id = ? AND user_id = ?",
            (*values.values(), application_id, st.session_state.user["id"]),
        )
        connection.commit()
        return cursor.rowcount > 0


def delete_owned_application(application_id):
    """Delete an application only when it belongs to the signed-in user."""
    with connect_user_data() as connection:
        cursor = connection.execute(
            "DELETE FROM user_applications WHERE id = ? AND user_id = ?",
            (application_id, st.session_state.user["id"]),
        )
        connection.commit()
        return cursor.rowcount > 0


# --------------------------------------------------
# 5. SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("CareerForge AI")
st.sidebar.caption("Your career toolkit")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Profile & Resume",
        "Portfolio",
        "Job Match",
        "Application Tracker",
        "Settings & Privacy",
    ],
)

st.sidebar.caption(f"Signed in as: {st.session_state.user.get('name', '')}")
if st.sidebar.button("Logout", use_container_width=True):
    for key in ("user", "profile", "active_user_id", "job_description"):
        st.session_state.pop(key, None)
    st.rerun()

st.sidebar.divider()
st.sidebar.caption("Build your profile. Prepare your resume. Track your career.")

# Always render a visible main-area header so a page-routing problem is obvious.
st.title("CareerForge AI")
st.caption(f"Current section: {page}")

# --------------------------------------------------
# 6. DASHBOARD
# --------------------------------------------------

if page == "Dashboard":
    st.title("Career Dashboard")
    st.write("An overview of your job search activity.")

    applications = get_applications()

    try:
        dashboard = build_dashboard_data(applications)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total applications",
            dashboard["total_applications"],
        )
        col2.metric(
            "Active applications",
            dashboard["active_applications"],
        )
        col3.metric(
            "Interviews",
            dashboard["interviews"],
        )
        col4.metric(
            "Offers",
            dashboard["offers"],
        )

        st.subheader("Applications by status")

        status_counts = dashboard["status_counts"]

        if status_counts:
            chart_data = pd.DataFrame({
                "Status": list(status_counts.keys()),
                "Applications": list(status_counts.values()),
            }).set_index("Status")

            st.bar_chart(chart_data)
        else:
            st.info("Add an application to see your statistics.")

        st.subheader("Upcoming follow-ups")

        followups = dashboard["upcoming_followups"]

        if followups:
            followup_rows = [
                {
                    "Company": app.get("company", ""),
                    "Job title": app.get("job_title", ""),
                    "Follow-up date": app.get("follow_up_date", ""),
                    "Status": app.get("status", ""),
                }
                for app in followups
            ]
            st.dataframe(
                pd.DataFrame(followup_rows),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No upcoming follow-ups recorded.")

        st.metric(
            "Overdue follow-ups",
            dashboard["overdue_followups"],
        )

        st.subheader("Recent applications")

        recent = dashboard["recent_applications"]

        if recent:
            recent_rows = [
                {
                    "Company": app.get("company", ""),
                    "Job title": app.get("job_title", ""),
                    "Status": app.get("status", ""),
                    "Applied date": app.get("applied_date", ""),
                }
                for app in recent
            ]

            st.dataframe(
                pd.DataFrame(recent_rows),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Your recent applications will appear here.")

    except Exception as exc:
        st.error(f"Could not build the dashboard: {exc}")

# --------------------------------------------------
# 7. PROFILE AND RESUME
# --------------------------------------------------

elif page == "Profile & Resume":
    st.title("Profile & Resume")
    st.write("Enter your details to prepare your resume.")

    profile = current_profile()

    with st.form("profile_form"):
        name = st.text_input(
            "Full name *",
            value=profile.get("name", ""),
        )
        email = st.text_input(
            "Email",
            value=profile.get("email", ""),
        )
        phone = st.text_input(
            "Phone",
            value=profile.get("phone", ""),
        )
        location = st.text_input(
            "Location",
            value=profile.get("location", ""),
        )
        linkedin = st.text_input(
            "LinkedIn URL",
            value=profile.get("linkedin", ""),
        )
        website = st.text_input(
            "Personal website URL",
            value=profile.get("website", ""),
        )

        summary = st.text_area(
            "Professional summary",
            value=profile.get("summary", ""),
            height=120,
            max_chars=3000,
        )

        skills_text = st.text_area(
            "Skills (separate with commas)",
            value=", ".join(profile.get("skills", [])),
            help="Example: Python, SQL, Streamlit, Data Analysis",
        )

        experience_text = st.text_area(
            "Experience",
            value="\n".join(profile.get("experience", [])),
            height=130,
            help="Enter one experience entry per line.",
        )

        education_text = st.text_area(
            "Education",
            value="\n".join(profile.get("education", [])),
            height=100,
            help="Enter one education entry per line.",
        )

        projects_text = st.text_area(
            "Projects",
            value="\n".join(profile.get("projects", [])),
            height=130,
            help="Enter one project entry per line.",
        )

        save_profile = st.form_submit_button(
            "Save Profile",
            type="primary",
        )

    if save_profile:
        new_profile = {
            "name": name.strip(),
            "email": email.strip(),
            "phone": phone.strip(),
            "location": location.strip(),
            "linkedin": linkedin.strip(),
            "website": website.strip(),
            "summary": summary.strip(),
            "skills": parse_skills(skills_text),
            "experience": parse_lines(experience_text),
            "education": parse_lines(education_text),
            "projects": parse_lines(projects_text),
        }

        errors = validate_profile(new_profile)

        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                save_user_profile(st.session_state.user["id"], new_profile)
                st.session_state.profile = new_profile
                st.success("Your profile has been saved to your account.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not save your profile: {exc}")

    st.divider()
    st.subheader("Download your resume")

    profile = current_profile()

    if not profile.get("name", "").strip():
        st.info("Enter and save your name before generating a resume.")
    else:
        try:
            pdf_bytes = generate_resume_pdf(profile)

            st.download_button(
                "Download Resume PDF",
                data=pdf_bytes,
                file_name="resume.pdf",
                mime="application/pdf",
            )
        except Exception as exc:
            st.error(f"Could not generate the resume: {exc}")

# --------------------------------------------------
# 8. PORTFOLIO
# --------------------------------------------------

elif page == "Portfolio":
    st.title("Portfolio Generator")
    st.write("Create a downloadable HTML portfolio from your profile.")

    profile = current_profile()

    if not profile.get("name", "").strip():
        st.info(
            "First complete and save your profile in the Profile & Resume page."
        )
    else:
        try:
            html_content = generate_portfolio_html(profile)

            st.success("Your portfolio is ready.")

            st.download_button(
                "Download Portfolio HTML",
                data=html_content,
                file_name="portfolio.html",
                mime="text/html",
            )

            with st.expander("Preview portfolio HTML"):
                st.code(html_content, language="html")

        except Exception as exc:
            st.error(f"Could not generate your portfolio: {exc}")

# --------------------------------------------------
# 9. JOB DESCRIPTION MATCH
# --------------------------------------------------

elif page == "Job Match":
    st.title("Job Description Match")
    st.write(
        "Compare the keywords in your saved profile with a job description."
    )

    profile = current_profile()

    job_description = st.text_area(
        "Paste job description",
        value=st.session_state.job_description,
        height=240,
        placeholder="Paste the job responsibilities and qualifications here...",
    )

    st.session_state.job_description = job_description

    if st.button("Analyze Match", type="primary"):
        errors = validate_profile(profile)
        description_error = validate_job_description(job_description)

        if not profile.get("name", "").strip():
            st.warning(
                "Please save your profile first. A name is required."
            )
        elif description_error:
            st.warning(description_error)
        else:
            try:
                result = analyze_job_match(profile, job_description)

                st.metric(
                    "Keyword overlap",
                    f"{result['match_percentage']}%",
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Matched keywords")
                    if result["matched_keywords"]:
                        st.write(
                            ", ".join(result["matched_keywords"])
                        )
                    else:
                        st.info("No matching keywords found.")

                with col2:
                    st.subheader("Missing keywords")
                    if result["missing_keywords"]:
                        st.write(
                            ", ".join(result["missing_keywords"])
                        )
                    else:
                        st.success(
                            "All extracted job keywords were found."
                        )

                st.subheader("Suggestions")
                for suggestion in result["suggestions"]:
                    st.write(f"- {suggestion}")

                st.caption(
                    "This is a simple keyword-overlap estimate, "
                    "not an official ATS score or a hiring prediction."
                )

            except Exception as exc:
                st.error(f"Could not analyze the job description: {exc}")

    st.divider()
    st.subheader("Optionally submit your information for owner review")
    st.write(
        "Only submit if you want the CareerForge AI owner to review your "
        "information. If you consent, your name, email, saved profile/resume "
        "text, and job description will be stored in a private database. "
        "The owner will receive an email notification containing your name "
        "and email, but not your resume or job description. You may request "
        "deletion by contacting the app owner."
    )

    with st.form("owner_submission_form"):
        consent_to_store = st.checkbox(
            "I have read the notice and consent to storing my name, email, "
            "resume/profile text, and job description, and to the owner "
            "receiving an email notification."
        )
        submit_for_owner = st.form_submit_button(
            "Submit information to app owner",
            type="primary",
        )

    if submit_for_owner:
        # Use the saved profile as the resume/profile text. No submission is
        # stored unless the user explicitly checks the consent box.
        resume_text = json.dumps(
            current_profile(), ensure_ascii=False, indent=2
        )
        saved, message = save_submission(
            name=current_profile().get("name", ""),
            email=current_profile().get("email", ""),
            resume_text=resume_text,
            job_description=st.session_state.get("job_description", ""),
            consent=consent_to_store,
        )
        if saved:
            st.success(message)
        else:
            st.warning(message)

# --------------------------------------------------
# 10. APPLICATION TRACKER
# --------------------------------------------------

elif page == "Application Tracker":
    st.title("Job Application Tracker")
    st.write("Save and manage the jobs you are applying for.")

    with st.expander("Add a new application", expanded=True):
        with st.form("add_application_form"):
            company = st.text_input("Company *")
            job_title = st.text_input("Job title *")
            job_url = st.text_input("Job URL")
            status = st.selectbox(
                "Status",
                options=list(STATUSES),
                index=0,
            )
            applied_date = st.date_input(
                "Applied date",
                value=date.today(),
            )
            has_followup = st.checkbox("Set a follow-up date")
            follow_up_date = None

            if has_followup:
                follow_up_date = st.date_input(
                    "Follow-up date",
                    value=date.today(),
                )

            notes = st.text_area("Notes")

            add_submitted = st.form_submit_button(
                "Add Application",
                type="primary",
            )

        if add_submitted:
            if not company.strip() or not job_title.strip():
                st.error("Company and job title are required.")
            else:
                try:
                    add_user_application(
                        user_id=st.session_state.user["id"],
                        company=company.strip(),
                        job_title=job_title.strip(),
                        job_url=job_url.strip(),
                        status=status,
                        applied_date=applied_date.isoformat(),
                        follow_up_date=(
                            follow_up_date.isoformat()
                            if follow_up_date else ""
                        ),
                        notes=notes.strip(),
                    )
                    st.success("Application added.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not add the application: {exc}")

    st.divider()
    st.subheader("Saved applications")

    applications = get_applications()

    if not applications:
        st.info("No applications saved yet.")
    else:
        display_rows = [
            {
                "ID": get_application_id(app),
                "Company": app.get("company", ""),
                "Job title": app.get("job_title", ""),
                "Status": app.get("status", ""),
                "Applied date": app.get("applied_date", ""),
                "Follow-up date": app.get("follow_up_date", ""),
            }
            for app in applications
        ]

        st.dataframe(
            pd.DataFrame(display_rows),
            use_container_width=True,
            hide_index=True,
        )

        editable_apps = [
            app for app in applications
            if get_application_id(app) is not None
        ]

        if editable_apps:
            st.subheader("Edit or delete an application")

            selected_id = st.selectbox(
                "Select application",
                options=[
                    get_application_id(app)
                    for app in editable_apps
                ],
                format_func=lambda app_id: next(
                    (
                        f"{app.get('company', '')} — "
                        f"{app.get('job_title', '')} (ID {app_id})"
                        for app in editable_apps
                        if get_application_id(app) == app_id
                    ),
                    str(app_id),
                ),
            )

            selected_app = next(
                app for app in editable_apps
                if get_application_id(app) == selected_id
            )

            with st.form("edit_application_form"):
                edit_company = st.text_input(
                    "Company",
                    value=selected_app.get("company", ""),
                )
                edit_title = st.text_input(
                    "Job title",
                    value=selected_app.get("job_title", ""),
                )
                edit_url = st.text_input(
                    "Job URL",
                    value=selected_app.get("job_url", ""),
                )

                current_status = selected_app.get("status", STATUSES[0])
                status_index = (
                    list(STATUSES).index(current_status)
                    if current_status in STATUSES else 0
                )

                edit_status = st.selectbox(
                    "Status",
                    options=list(STATUSES),
                    index=status_index,
                )

                edit_applied_date = st.text_input(
                    "Applied date (YYYY-MM-DD)",
                    value=selected_app.get("applied_date", ""),
                )
                edit_follow_up = st.text_input(
                    "Follow-up date (YYYY-MM-DD, optional)",
                    value=selected_app.get("follow_up_date", ""),
                )
                edit_notes = st.text_area(
                    "Notes",
                    value=selected_app.get("notes", ""),
                )

                update_submitted = st.form_submit_button(
                    "Save Changes"
                )

            if update_submitted:
                if not edit_company.strip() or not edit_title.strip():
                    st.error("Company and job title are required.")
                else:
                    try:
                        update_owned_application(
                            selected_id,
                            company=edit_company.strip(),
                            job_title=edit_title.strip(),
                            job_url=edit_url.strip(),
                            status=edit_status,
                            applied_date=edit_applied_date.strip(),
                            follow_up_date=edit_follow_up.strip(),
                            notes=edit_notes.strip(),
                        )
                        st.success("Application updated.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not update the application: {exc}")

            st.divider()
            st.subheader("Delete an application")

            confirm_delete = st.checkbox(
                f"I confirm that I want to delete application ID {selected_id}."
            )

            if st.button("Delete Selected Application"):
                if not confirm_delete:
                    st.warning("Please confirm before deleting.")
                else:
                    try:
                        deleted = delete_owned_application(selected_id)
                        if not deleted:
                            st.warning("That application was not found in your account.")
                            st.stop()
                        st.success("Application deleted.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not delete the application: {exc}")

# --------------------------------------------------
# 11. SETTINGS & PRIVACY
# --------------------------------------------------

elif page == "Settings & Privacy":
    st.title("Settings & Privacy")
    st.write(PRIVACY_GUIDANCE)
    st.info(
        "Owner-submitted records are stored separately in the private "
        "Supabase submissions table. Use the owner dashboard (your app URL "
        "followed by ?admin=1) to review or delete those submissions."
    )
