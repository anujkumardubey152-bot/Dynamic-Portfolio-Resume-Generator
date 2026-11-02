
from pathlib import Path
import sys
from datetime import date
from copy import deepcopy

import pandas as pd
import streamlit as st


# =========================================================
# 1. APP CONFIGURATION
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

st.set_page_config(
    page_title="CareerForge AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. IMPORT EXISTING PROJECT MODULES
# =========================================================

try:
    from src.auth_ui import render_auth_page

    from src.user_data import (
        connect as connect_user_data,
        save_profile,
        load_profile,
        add_user_application,
        list_user_applications,
    )

    from src.resume_generator import generate_resume_pdf
    from src.portfolio_generator import generate_portfolio_html
    from src.job_matcher import analyze_job_match
    from src.validation import (
        validate_profile,
        validate_job_description,
    )
    from src.dashboard import build_dashboard_data
    from src.application_tracker import STATUSES

except ModuleNotFoundError as exc:
    st.error("A required project module or dependency is missing.")
    st.code(str(exc))
    st.info(
        "Check that your requirements.txt and src folder contain "
        "all the required project modules."
    )
    st.stop()


# =========================================================
# 3. PROFESSIONAL FRONTEND
# =========================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f5f7fc;
    }

    [data-testid="stSidebar"] {
        background: #111a35;
    }

    [data-testid="stSidebar"] * {
        color: #f5f7ff !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 8px 10px;
        border-radius: 9px;
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.8px;
        margin-bottom: 3px;
    }

    .brand-caption {
        font-size: 12px;
        color: #aab7d4;
        margin-bottom: 25px;
    }

    .hero {
        padding: 25px 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #18264b, #344b87);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 29px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .hero p {
        color: #dbe5ff;
        margin-bottom: 0;
    }

    .section-heading {
        color: #1d2b4d;
        font-size: 21px;
        font-weight: 750;
        margin-top: 12px;
        margin-bottom: 12px;
    }

    .small-muted {
        color: #73809b;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e7ebf4;
        padding: 17px;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(25, 42, 80, 0.04);
    }

    div[data-testid="stForm"] {
        background: white;
        padding: 20px;
        border: 1px solid #e7ebf4;
        border-radius: 14px;
    }

    div[data-testid="stExpander"] {
        background: white;
        border-radius: 12px;
        border: 1px solid #e7ebf4;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
    }

    .stTextInput input,
    .stTextArea textarea {
        border-radius: 9px;
    }

    hr {
        border-color: #e5eaf3;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 4. DEFAULT PROFILE AND SESSION STATE
# =========================================================

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

if "user" not in st.session_state:
    st.session_state.user = None

if "profile" not in st.session_state:
    st.session_state.profile = deepcopy(DEFAULT_PROFILE)

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "job_match_result" not in st.session_state:
    st.session_state.job_match_result = None

if "profile_edit_redirect" not in st.session_state:
    st.session_state.profile_edit_redirect = False


# =========================================================
# 5. HELPER FUNCTIONS
# =========================================================

def parse_lines(value):
    """Convert multiline text into a list of non-empty lines."""
    return [
        line.strip()
        for line in str(value or "").splitlines()
        if line.strip()
    ]


def parse_skills(value):
    """Convert comma-separated skills into a unique list."""
    return list(dict.fromkeys(
        skill.strip()
        for skill in str(value or "").replace("\n", ",").split(",")
        if skill.strip()
    ))


def current_profile():
    return st.session_state.profile


def load_current_user_data():
    """Load this signed-in user's profile and initialize user tables."""
    user = st.session_state.user

    if not user:
        return

    try:
        connect_user_data()
        stored_profile = load_profile(user["id"])

        if isinstance(stored_profile, dict):
            profile = deepcopy(DEFAULT_PROFILE)
            profile.update(stored_profile)

            # The account email is the verified login identifier,
            # not an email-verification claim.
            profile["email"] = user["email"]

            st.session_state.profile = profile
        else:
            profile = deepcopy(DEFAULT_PROFILE)
            profile["name"] = user.get("name", "")
            profile["email"] = user.get("email", "")
            st.session_state.profile = profile

    except Exception as exc:
        st.error("Could not load your saved profile.")
        st.caption(str(exc))


def get_applications():
    """Return only applications belonging to the signed-in user."""
    user = st.session_state.user

    if not user:
        return []

    try:
        return list_user_applications(user["id"]) or []
    except Exception as exc:
        st.error("Could not load your applications.")
        st.caption(str(exc))
        return []


def show_hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_empty_state(message):
    st.info(message)


# =========================================================
# 6. LOGIN PROTECTION
# =========================================================

# The authentication module manages registration and login.
# No application or profile page is shown before login.

if not st.session_state.user:
    render_auth_page()
    st.stop()


# Load the signed-in user's data once per session.
if st.session_state.get("loaded_user_id") != st.session_state.user["id"]:
    load_current_user_data()
    st.session_state.loaded_user_id = st.session_state.user["id"]


# =========================================================
# 7. SIDEBAR AND NAVIGATION
# =========================================================

user = st.session_state.user

with st.sidebar:
    st.markdown(
        '<div class="brand">CareerForge AI</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="brand-caption">Your personal career workspace</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Navigation")

    pages = [
        "Dashboard",
        "Profile & Resume",
        "Portfolio",
        "Job Match",
        "Application Tracker",
        "Settings & Privacy",
    ]

    if st.session_state.profile_edit_redirect:
        default_page = "Profile & Resume"
        st.session_state.profile_edit_redirect = False
    else:
        default_page = "Dashboard"

    if "selected_page" not in st.session_state:
        st.session_state.selected_page = default_page

    page = st.radio(
        "Choose a section",
        pages,
        key="selected_page",
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Signed in as")
    st.write(user.get("name", "User"))
    st.caption(user.get("email", ""))

    st.divider()

    st.caption("Your career. Your progress. Your future.")

    if st.button("Log out", use_container_width=True):
        for key in [
            "user",
            "profile",
            "job_description",
            "job_match_result",
            "loaded_user_id",
            "selected_page",
            "profile_edit_redirect",
        ]:
            st.session_state.pop(key, None)

        st.rerun()


# =========================================================
# 8. DASHBOARD
# =========================================================

if page == "Dashboard":

    show_hero(
        "Welcome back, " + user.get("name", "there") + "!",
        "Your career progress and job search activity at a glance.",
    )

    profile = current_profile()
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

        st.markdown(
            '<div class="section-heading">Application overview</div>',
            unsafe_allow_html=True,
        )

        status_counts = dashboard["status_counts"]

        if status_counts:
            chart_data = pd.DataFrame({
                "Status": list(status_counts.keys()),
                "Applications": list(status_counts.values()),
            }).set_index("Status")

            st.bar_chart(chart_data)
        else:
            show_empty_state(
                "Your application chart will appear after you add applications."
            )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<div class="section-heading">Upcoming follow-ups</div>',
                unsafe_allow_html=True,
            )

            followups = dashboard["upcoming_followups"]

            if followups:
                rows = [
                    {
                        "Company": app.get("company", ""),
                        "Position": app.get("job_title", ""),
                        "Date": app.get("follow_up_date", ""),
                        "Status": app.get("status", ""),
                    }
                    for app in followups
                ]

                st.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.caption("No upcoming follow-ups.")

        with col2:
            st.markdown(
                '<div class="section-heading">Recent applications</div>',
                unsafe_allow_html=True,
            )

            recent = dashboard["recent_applications"]

            if recent:
                rows = [
                    {
                        "Company": app.get("company", ""),
                        "Position": app.get("job_title", ""),
                        "Status": app.get("status", ""),
                        "Applied": app.get("applied_date", ""),
                    }
                    for app in recent
                ]

                st.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.caption("No recent applications.")

        st.metric(
            "Overdue follow-ups",
            dashboard["overdue_followups"],
        )

    except Exception as exc:
        st.error("Could not prepare your dashboard.")
        st.caption(str(exc))

    st.divider()

    st.markdown(
        '<div class="section-heading">Your career profile</div>',
        unsafe_allow_html=True,
    )

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:
        st.metric(
            "Profile skills",
            len(profile.get("skills", [])),
        )

    with profile_col2:
        st.metric(
            "Projects added",
            len(profile.get("projects", [])),
        )

    if not profile.get("name"):
        st.warning(
            "Your profile is not complete yet. "
            "Visit Profile & Resume to get started."
        )


# =========================================================
# 9. PROFILE AND RESUME
# =========================================================

elif page == "Profile & Resume":

    show_hero(
        "Profile & Resume",
        "Create and maintain the professional profile behind your career documents.",
    )

    profile = current_profile()

    st.markdown("### Personal information")

    with st.form("profile_form"):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Full name *",
                value=profile.get("name", ""),
            )

            email = st.text_input(
                "Email address",
                value=user.get("email", ""),
                disabled=True,
                help="Your account email is managed through your login.",
            )

            phone = st.text_input(
                "Phone number",
                value=profile.get("phone", ""),
            )

        with col2:
            location = st.text_input(
                "Location",
                value=profile.get("location", ""),
            )

            linkedin = st.text_input(
                "LinkedIn URL",
                value=profile.get("linkedin", ""),
            )

            website = st.text_input(
                "Personal website",
                value=profile.get("website", ""),
            )

        st.markdown("### Professional summary")

        summary = st.text_area(
            "Write a short professional introduction",
            value=profile.get("summary", ""),
            height=120,
            max_chars=3000,
        )

        st.markdown("### Skills")

        skills_text = st.text_area(
            "Skills (comma-separated)",
            value=", ".join(profile.get("skills", [])),
            placeholder="Python, SQL, Streamlit, Communication",
        )

        st.markdown("### Experience")

        experience_text = st.text_area(
            "Experience (one entry per line)",
            value="\n".join(profile.get("experience", [])),
            height=130,
        )

        st.markdown("### Education")

        education_text = st.text_area(
            "Education (one entry per line)",
            value="\n".join(profile.get("education", [])),
            height=100,
        )

        st.markdown("### Projects")

        projects_text = st.text_area(
            "Projects (one entry per line)",
            value="\n".join(profile.get("projects", [])),
            height=130,
        )

        submitted = st.form_submit_button(
            "Save My Profile",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        new_profile = {
            "name": name.strip(),
            "email": user["email"],
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
                save_profile(user["id"], new_profile)

                st.session_state.profile = new_profile

                st.success("Your profile has been saved.")
                st.rerun()

            except Exception as exc:
                st.error("Could not save your profile.")
                st.caption(str(exc))

    st.divider()

    st.markdown("### Download your resume")

    profile = current_profile()

    if not profile.get("name", "").strip():
        st.info("Save your profile before generating your resume.")

    else:
        try:
            pdf_bytes = generate_resume_pdf(profile)

            st.download_button(
                "Download Resume PDF",
                data=pdf_bytes,
                file_name="CareerForge_Resume.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )

        except Exception as exc:
            st.error("Resume generation failed.")
            st.caption(str(exc))


# =========================================================
# 10. PORTFOLIO GENERATOR
# =========================================================

elif page == "Portfolio":

    show_hero(
        "Portfolio Builder",
        "Turn your professional profile into a downloadable portfolio website.",
    )

    profile = current_profile()

    if not profile.get("name", "").strip():
        st.warning(
            "Complete your profile before creating your portfolio."
        )

    else:
        try:
            html_content = generate_portfolio_html(profile)

            st.success("Your portfolio is ready.")

            st.download_button(
                "Download Portfolio Website",
                data=html_content,
                file_name="CareerForge_Portfolio.html",
                mime="text/html",
                type="primary",
                use_container_width=True,
            )

            with st.expander("Preview generated HTML"):
                st.code(html_content, language="html")

        except Exception as exc:
            st.error("Could not generate your portfolio.")
            st.caption(str(exc))


# =========================================================
# 11. JOB MATCH
# =========================================================

elif page == "Job Match":

    show_hero(
        "Job Match Analyzer",
        "Compare your skills and experience with a job description.",
    )

    profile = current_profile()

    if not profile.get("name", "").strip():
        st.warning(
            "Please complete your profile before analyzing a job."
        )

    job_description = st.text_area(
        "Paste the job description",
        value=st.session_state.job_description,
        height=260,
        placeholder=(
            "Paste the job responsibilities, required skills, "
            "and qualifications here..."
        ),
    )

    if st.button("Analyze Job Match", type="primary"):

        st.session_state.job_description = job_description

        profile_errors = validate_profile(profile)
        description_error = validate_job_description(job_description)

        if not profile.get("name", "").strip():
            st.error("Please save your profile first.")

        elif description_error:
            st.error(description_error)

        elif profile_errors:
            for error in profile_errors:
                st.error(error)

        else:
            try:
                result = analyze_job_match(
                    profile,
                    job_description,
                )

                st.session_state.job_match_result = result

            except Exception as exc:
                st.error("Job matching failed.")
                st.caption(str(exc))

    result = st.session_state.job_match_result

    if result:

        st.divider()

        st.markdown("### Match results")

        score = result["match_percentage"]

        st.metric(
            "Keyword overlap",
            f"{score}%",
        )

        st.progress(
            max(0.0, min(float(score) / 100, 1.0))
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Matched keywords")

            matched = result["matched_keywords"]

            if matched:
                for keyword in matched:
                    st.success(keyword)
            else:
                st.info("No matching keywords found.")

        with col2:
            st.markdown("#### Missing keywords")

            missing = result["missing_keywords"]

            if missing:
                for keyword in missing:
                    st.warning(keyword)
            else:
                st.success("No missing keywords found.")

        st.markdown("### Improvement suggestions")

        for suggestion in result["suggestions"]:
            st.write(f"• {suggestion}")

        st.caption(
            "This is a keyword-overlap estimate. It is not an official "
            "ATS score or a prediction of hiring success."
        )


# =========================================================
# 12. APPLICATION TRACKER
# =========================================================

elif page == "Application Tracker":

    show_hero(
        "Application Tracker",
        "Keep track of the opportunities you are pursuing.",
    )

    st.markdown("### Add a new application")

    with st.form("add_application_form"):

        col1, col2 = st.columns(2)

        with col1:
            company = st.text_input("Company name *")
            job_title = st.text_input("Job title *")
            job_url = st.text_input("Job posting URL")

        with col2:
            status = st.selectbox(
                "Application status",
                options=list(STATUSES),
            )

            applied_date = st.date_input(
                "Applied date",
                value=date.today(),
            )

            has_followup = st.checkbox("Add a follow-up date")

            follow_up_date = None

            if has_followup:
                follow_up_date = st.date_input(
                    "Follow-up date",
                    value=date.today(),
                )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button(
            "Add Application",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        if not company.strip() or not job_title.strip():
            st.error("Company and job title are required.")

        else:
            try:
                add_user_application(
                    user["id"],
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

                st.success("Application added to your account.")
                st.rerun()

            except Exception as exc:
                st.error("Could not add the application.")
                st.caption(str(exc))

    st.divider()

    st.markdown("### Your saved applications")

    applications = get_applications()

    if applications:

        display_rows = [
            {
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

        st.caption(
            "These records are loaded using your signed-in account ID."
        )

    else:
        show_empty_state(
            "No applications yet. Add your first application above."
        )

    st.info(
        "This version supports secure per-user adding and viewing. "
        "Per-user editing and deletion require corresponding functions "
        "in src/user_data.py; the shared application database is not used."
    )


# =========================================================
# 13. SETTINGS AND PRIVACY
# =========================================================

elif page == "Settings & Privacy":

    show_hero(
        "Settings & Privacy",
        "Manage your account information and understand how your data is stored.",
    )

    profile = current_profile()

    st.markdown("### Account information")

    account_col1, account_col2 = st.columns(2)

    with account_col1:
        st.markdown("**Account name**")
        st.write(user.get("name", ""))

    with account_col2:
        st.markdown("**Login email**")
        st.write(user.get("email", ""))

    st.divider()

    st.markdown("### Profile information")

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:
        st.markdown("**Profile name**")
        st.write(profile.get("name") or "Not added")

        st.markdown("**Location**")
        st.write(profile.get("location") or "Not added")

    with profile_col2:
        st.markdown("**Skills added**")
        st.write(len(profile.get("skills", [])))

        st.markdown("**Projects added**")
        st.write(len(profile.get("projects", [])))

    if st.button("Edit My Profile", type="primary"):
        st.session_state.selected_page = "Profile & Resume"
        st.rerun()

    st.divider()

    st.markdown("### Privacy information")

    privacy_items = [
        (
            "Account authentication",
            "Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes "
            "by the authentication module, not as plain text."
        ),
        (
            "Account separation",
            "The profile and application functions in this app use "
            "the signed-in user's account ID."
        ),
        (
            "Profile data",
            "Your saved profile may contain contact information, "
            "skills, education, experience, and projects."
        ),
        (
            "Application data",
            "Your job application records may contain company names, "
            "job titles, dates, URLs, and notes."
        ),
        (
            "Database storage",
            "The current user-data module uses SQLite. Local SQLite "
            "files on Streamlit Community Cloud are not guaranteed "
            "to persist across environment replacement or redeployment."
        ),
    ]

    for heading, description in privacy_items:
        with st.expander(heading):
            st.write(description)

    st.warning(
        "For production use, configure persistent database storage, "
        "restrict database access, and use HTTPS. Do not commit users.db "
        "or .streamlit/secrets.toml to GitHub."
    )

    st.divider()

    st.markdown("### Security recommendations")

    st.write(
        "• Use a unique password that you do not use on other websites."
    )
    st.write(
        "• Never share your password or database credentials."
    )
    st.write(
        "• Rotate any database key that has accidentally been exposed."
    )
    st.write(
        "• Keep private configuration in Streamlit Secrets."
    )
    st.write(
        "• Use a persistent database before relying on this app "
        "for long-term account storage."
    )

    st.divider()

    st.markdown("### Sign out")

    st.write(
        "Sign out when using a shared or public computer."
    )

    if st.button("Sign Out", use_container_width=True):

        for key in [
            "user",
            "profile",
            "job_description",
            "job_match_result",
            "loaded_user_id",
            "selected_page",
            "profile_edit_redirect",
        ]:
            st.session_state.pop(key, None)

        st.rerun()


# =========================================================
# 14. FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#8490a8;
        font-size:12px;
        padding:12px 0;
    ">
        CareerForge AI · Your personal career workspace
    </div>
    """,
    unsafe_allow_html=True,
)
