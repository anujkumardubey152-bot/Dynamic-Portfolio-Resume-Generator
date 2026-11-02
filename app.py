
from pathlib import Path
import sys
from datetime import date
import json

import streamlit as st
import pandas as pd

# ==========================================================
# 1. APP CONFIGURATION
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

st.set_page_config(
    page_title="CareerForge AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# 2. MODERN FRONTEND DESIGN
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f5f7fc;
}

[data-testid="stHeader"] {
    background: rgba(245,247,252,0.9);
}

[data-testid="stSidebar"] {
    background: #101a2c;
    border-right: 1px solid #243149;
}

[data-testid="stSidebar"] * {
    color: #e7edf8;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #aab8ce;
}

[data-testid="stSidebar"] .stRadio label {
    padding: 8px 10px;
    border-radius: 9px;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: #243550;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #15233b;
    font-weight: 800;
    letter-spacing: -0.5px;
}

p, label {
    color: #56647a;
}

.hero {
    background: linear-gradient(120deg, #14233d, #244c83);
    padding: 30px 34px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 34px;
    margin-bottom: 8px;
}

.hero p {
    color: #d6e4fa;
    margin-bottom: 0;
}

.section-card {
    background: white;
    padding: 22px;
    border: 1px solid #e7ebf2;
    border-radius: 16px;
    margin-bottom: 18px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border: 1px solid #e7ebf2;
    border-radius: 15px;
    box-shadow: 0 3px 12px rgba(20,35,60,0.04);
}

div[data-testid="stMetricLabel"] {
    color: #68768c;
}

div[data-testid="stMetricValue"] {
    color: #1c3760;
    font-weight: 800;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
    border: 0;
    background: #2563eb;
    color: white;
    font-weight: 700;
    padding: 10px 18px;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #174bb8;
    color: white;
    border: 0;
    transform: translateY(-1px);
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

div[data-testid="stForm"] {
    background: white;
    border: 1px solid #e7ebf2;
    border-radius: 15px;
    padding: 22px;
}

div[data-testid="stExpander"] {
    background: white;
    border: 1px solid #e7ebf2;
    border-radius: 12px;
}

hr {
    border-color: #e4e9f1;
}

.small-muted {
    color: #8290a5;
    font-size: 13px;
}

.brand {
    font-size: 23px;
    font-weight: 800;
    color: white;
    padding: 8px 0 2px 0;
}

.sidebar-tagline {
    color: #91a5c2;
    font-size: 12px;
    margin-bottom: 22px;
}

div[data-testid="stTabs"] button {
    font-weight: 600;
}

@media (max-width: 768px) {
    .hero {
        padding: 22px;
    }
    .hero h1 {
        font-size: 27px;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. BACKEND IMPORTS
# ==========================================================

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

    from src.privacy_store import (
        render_admin_page,
        save_submission,
    )

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
    st.info("Check that your requirements.txt and src folder are committed to GitHub.")
    st.stop()

# ==========================================================
# 4. ADMIN ROUTE AND LOGIN
# ==========================================================

if st.query_params.get("admin") == "1":
    render_admin_page()
    st.stop()

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    render_auth_page()
    st.stop()

# ==========================================================
# 5. PROFILE AND SESSION STATE
# ==========================================================

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

active_user_id = st.session_state.user["id"]

if st.session_state.get("active_user_id") != active_user_id:
    try:
        saved_profile = load_profile(active_user_id) or {}
    except Exception as exc:
        st.error(f"Could not load your saved profile: {exc}")
        saved_profile = {}

    st.session_state.profile = {
        **DEFAULT_PROFILE,
        **saved_profile,
    }

    st.session_state.active_user_id = active_user_id
    st.session_state.job_description = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# ==========================================================
# 6. HELPER FUNCTIONS
# ==========================================================

def parse_lines(value):
    return [
        line.strip()
        for line in str(value or "").splitlines()
        if line.strip()
    ]


def parse_skills(value):
    return list(dict.fromkeys(
        skill.strip()
        for skill in str(value or "").replace("\n", ",").split(",")
        if skill.strip()
    ))


def current_profile():
    return st.session_state.profile


def get_application_id(application):
    for key in ("id", "application_id"):
        if application.get(key) is not None:
            return application[key]
    return None


def get_applications():
    try:
        return list_user_applications(
            st.session_state.user["id"]
        ) or []
    except Exception as exc:
        st.error(f"Could not load applications: {exc}")
        return []


def update_owned_application(application_id, **fields):
    allowed = {
        "company",
        "job_title",
        "job_url",
        "status",
        "applied_date",
        "follow_up_date",
        "notes",
    }

    values = {
        key: value
        for key, value in fields.items()
        if key in allowed
    }

    if not values:
        return False

    assignments = ", ".join(
        f"{key} = ?" for key in values
    )

    with connect_user_data() as connection:
        cursor = connection.execute(
            f"UPDATE user_applications SET {assignments} "
            "WHERE id = ? AND user_id = ?",
            (
                *values.values(),
                application_id,
                st.session_state.user["id"],
            ),
        )
        connection.commit()
        return cursor.rowcount > 0


def delete_owned_application(application_id):
    with connect_user_data() as connection:
        cursor = connection.execute(
            "DELETE FROM user_applications "
            "WHERE id = ? AND user_id = ?",
            (
                application_id,
                st.session_state.user["id"],
            ),
        )
        connection.commit()
        return cursor.rowcount > 0


def page_header(title, subtitle, icon="✨"):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# 7. SIDEBAR NAVIGATION
# ==========================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">🚀 CareerForge AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-tagline">YOUR PERSONAL CAREER WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Dashboard",
            "Profile & Resume",
            "Portfolio",
            "Job Match",
            "Application Tracker",
            "Settings & Privacy",
        ],
        label_visibility="visible",
    )

    st.divider()

    st.markdown("### Account")
    st.write(f"👤 {st.session_state.user.get('name', 'User')}")
    st.caption(st.session_state.user.get("email", ""))

    if st.button("↪ Log Out", use_container_width=True):
        for key in (
            "user",
            "profile",
            "active_user_id",
            "job_description",
        ):
            st.session_state.pop(key, None)

        st.rerun()

    st.divider()

    st.caption("Build your profile. Prepare your resume. Track your career.")
    st.caption("CareerForge AI · Version 1.0")

# ==========================================================
# 8. DASHBOARD
# ==========================================================

if page == "Dashboard":

    page_header(
        "Your Career Dashboard",
        "Welcome back! Here's an overview of your career journey.",
        "📊",
    )

    applications = get_applications()

    try:
        dashboard = build_dashboard_data(applications)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Applications",
            dashboard["total_applications"],
            help="All jobs saved in your tracker.",
        )

        col2.metric(
            "Active Applications",
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

        st.write("")

        left, right = st.columns([1.3, 1])

        with left:
            with st.container(border=True):
                st.subheader("📈 Applications by Status")

                status_counts = dashboard["status_counts"]

                if status_counts:
                    chart_data = pd.DataFrame({
                        "Status": list(status_counts.keys()),
                        "Applications": list(status_counts.values()),
                    }).set_index("Status")

                    st.bar_chart(chart_data)
                else:
                    st.info("Add an application to see your statistics.")

        with right:
            with st.container(border=True):
                st.subheader("🎯 Career Snapshot")

                total = dashboard["total_applications"]
                interviews = dashboard["interviews"]
                offers = dashboard["offers"]

                if total:
                    interview_rate = round(
                        interviews / total * 100
                    )
                    offer_rate = round(
                        offers / total * 100
                    )
                else:
                    interview_rate = 0
                    offer_rate = 0

                st.metric("Interview rate", f"{interview_rate}%")
                st.progress(interview_rate / 100)

                st.metric("Offer rate", f"{offer_rate}%")
                st.progress(offer_rate / 100)

                st.caption("Rates are based on your saved application records.")

        st.write("")

        left, right = st.columns(2)

        with left:
            with st.container(border=True):
                st.subheader("📅 Upcoming Follow-ups")

                followups = dashboard["upcoming_followups"]

                if followups:
                    followup_rows = [
                        {
                            "Company": app.get("company", ""),
                            "Job": app.get("job_title", ""),
                            "Follow-up": app.get("follow_up_date", ""),
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
                    "Overdue Follow-ups",
                    dashboard["overdue_followups"],
                )

        with right:
            with st.container(border=True):
                st.subheader("🕒 Recent Applications")

                recent = dashboard["recent_applications"]

                if recent:
                    recent_rows = [
                        {
                            "Company": app.get("company", ""),
                            "Job": app.get("job_title", ""),
                            "Status": app.get("status", ""),
                            "Applied": app.get("applied_date", ""),
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

# ==========================================================
# 9. PROFILE AND RESUME
# ==========================================================

elif page == "Profile & Resume":

    page_header(
        "Profile & Resume",
        "Build your professional profile and create a polished resume.",
        "👤",
    )

    profile = current_profile()

    st.info("Complete your details below, then save your profile.")

    with st.form("profile_form"):

        st.subheader("👤 Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Full Name *",
                value=profile.get("name", ""),
                placeholder="Your full name",
            )

            email = st.text_input(
                "Email",
                value=profile.get("email", ""),
                placeholder="you@example.com",
            )

            phone = st.text_input(
                "Phone",
                value=profile.get("phone", ""),
                placeholder="+91 9876543210",
            )

        with col2:
            location = st.text_input(
                "Location",
                value=profile.get("location", ""),
                placeholder="City, Country",
            )

            linkedin = st.text_input(
                "LinkedIn URL",
                value=profile.get("linkedin", ""),
                placeholder="https://linkedin.com/in/...",
            )

            website = st.text_input(
                "Personal Website",
                value=profile.get("website", ""),
                placeholder="https://yourwebsite.com",
            )

        st.divider()

        st.subheader("✍️ Professional Summary")

        summary = st.text_area(
            "About you",
            value=profile.get("summary", ""),
            height=130,
            max_chars=3000,
            placeholder="Write a short professional introduction...",
        )

        st.divider()

        st.subheader("⚡ Skills")

        skills_text = st.text_area(
            "Add your skills",
            value=", ".join(profile.get("skills", [])),
            placeholder="Python, SQL, Streamlit, HTML, CSS",
            height=90,
        )

        st.divider()

        st.subheader("💼 Experience")

        experience_text = st.text_area(
            "Work experience",
            value="\n".join(profile.get("experience", [])),
            height=130,
            placeholder=(
                "Python Developer Intern – ABC Company\n"
                "Developed Python applications and dashboards."
            ),
        )

        st.divider()

        st.subheader("🎓 Education")

        education_text = st.text_area(
            "Education details",
            value="\n".join(profile.get("education", [])),
            height=110,
            placeholder="Degree – University – Year",
        )

        st.divider()

        st.subheader("🚀 Projects")

        projects_text = st.text_area(
            "Your projects",
            value="\n".join(profile.get("projects", [])),
            height=140,
            placeholder=(
                "CareerForge AI – Resume and portfolio generator\n"
                "Student Management System – Student record application"
            ),
            help="Enter one project per line.",
        )

        save_profile = st.form_submit_button(
            "💾 Save My Profile",
            type="primary",
            use_container_width=True,
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
                save_user_profile(
                    st.session_state.user["id"],
                    new_profile,
                )

                st.session_state.profile = new_profile

                st.success("Your profile has been saved successfully!")
                st.rerun()

            except Exception as exc:
                st.error(f"Could not save your profile: {exc}")

    st.divider()

    st.subheader("📄 Resume Generator")

    profile = current_profile()

    if not profile.get("name", "").strip():
        st.info("Save your name and profile before generating your resume.")

    else:
        try:
            pdf_bytes = generate_resume_pdf(profile)

            st.success("Your resume is ready!")

            st.download_button(
                "⬇️ Download Resume PDF",
                data=pdf_bytes,
                file_name="careerforge_resume.pdf",
                mime="application/pdf",
                type="primary",
            )

        except Exception as exc:
            st.error(f"Could not generate the resume: {exc}")

# ==========================================================
# 10. PORTFOLIO
# ==========================================================

elif page == "Portfolio":

    page_header(
        "Portfolio Generator",
        "Turn your professional profile into a personal portfolio website.",
        "🌐",
    )

    profile = current_profile()

    if not profile.get("name", "").strip():

        st.warning(
            "Please complete and save your profile before generating your portfolio."
        )

        st.button(
            "Go to Profile & Resume",
            on_click=lambda: st.session_state.update(
                {"_unused_navigation_hint": True}
            ),
        )

    else:

        with st.container(border=True):
            st.subheader("Your Portfolio")

            st.write(
                "Your portfolio is generated from your saved profile, "
                "including your skills, experience, education, and projects."
            )

            try:
                html_content = generate_portfolio_html(profile)

                st.success("Your portfolio is ready!")

                st.download_button(
                    "⬇️ Download Portfolio HTML",
                    data=html_content,
                    file_name="careerforge_portfolio.html",
                    mime="text/html",
                    type="primary",
                )

                with st.expander("View HTML source"):
                    st.code(html_content, language="html")

            except Exception as exc:
                st.error(f"Could not generate your portfolio: {exc}")

# ==========================================================
# 11. JOB MATCH
# ==========================================================

elif page == "Job Match":

    page_header(
        "AI Job Match",
        "Compare your profile skills with a job description.",
        "🎯",
    )

    profile = current_profile()

    with st.container(border=True):

        st.subheader("Paste a Job Description")

        job_description = st.text_area(
            "Job description",
            value=st.session_state.job_description,
            height=240,
            placeholder="Paste the job responsibilities and qualifications here...",
        )

        st.session_state.job_description = job_description

        analyze_clicked = st.button(
            "🔍 Analyze Job Match",
            type="primary",
            use_container_width=True,
        )

    if analyze_clicked:

        errors = validate_profile(profile)
        description_error = validate_job_description(job_description)

        if not profile.get("name", "").strip():

            st.warning("Please save your profile first.")

        elif description_error:

            st.warning(description_error)

        else:

            try:
                result = analyze_job_match(
                    profile,
                    job_description,
                )

                score = result["match_percentage"]

                st.divider()
                st.subheader("Your Match Results")

                score_col, details_col = st.columns([1, 2])

                with score_col:
                    st.metric(
                        "Keyword Match",
                        f"{score}%",
                    )

                    st.progress(
                        max(0, min(100, score)) / 100
                    )

                with details_col:
                    if score >= 75:
                        st.success("Strong keyword match!")
                    elif score >= 45:
                        st.info("Moderate keyword match. You can improve your profile.")
                    else:
                        st.warning("Low keyword match. Review the missing skills.")

                    st.caption(
                        "This is a keyword-overlap estimate, not an official ATS score."
                    )

                matched_col, missing_col = st.columns(2)

                with matched_col:
                    with st.container(border=True):
                        st.subheader("✅ Matched Keywords")

                        if result["matched_keywords"]:
                            for keyword in result["matched_keywords"]:
                                st.write(f"• {keyword}")
                        else:
                            st.info("No matching keywords found.")

                with missing_col:
                    with st.container(border=True):
                        st.subheader("📌 Missing Keywords")

                        if result["missing_keywords"]:
                            for keyword in result["missing_keywords"]:
                                st.write(f"• {keyword}")
                        else:
                            st.success("All extracted job keywords were found.")

                st.subheader("💡 Suggestions")

                for suggestion in result["suggestions"]:
                    st.write(f"• {suggestion}")

            except Exception as exc:
                st.error(f"Could not analyze the job description: {exc}")

    # Optional owner submission remains available.
    st.divider()

    with st.expander("Optional: Submit information for owner review"):

        st.write(
            "Only submit if you want the app owner to review your information. "
            "If you consent, your name, email, saved profile text, and job "
            "description will be stored in a private database. The owner will "
            "receive an email notification containing your name and email, "
            "but not your resume or job description. You may request deletion "
            "by contacting the app owner."
        )

        with st.form("owner_submission_form"):

            consent_to_store = st.checkbox(
                "I have read the notice and consent to storing my name, email, "
                "profile text, and job description, and to the owner receiving "
                "an email notification."
            )

            submit_for_owner = st.form_submit_button(
                "Submit Information to App Owner",
            )

        if submit_for_owner:

            resume_text = json.dumps(
                current_profile(),
                ensure_ascii=False,
                indent=2,
            )

            saved, message = save_submission(
                name=current_profile().get("name", ""),
                email=current_profile().get("email", ""),
                resume_text=resume_text,
                job_description=st.session_state.get(
                    "job_description", ""
                ),
                consent=consent_to_store,
            )

            if saved:
                st.success(message)
            else:
                st.warning(message)

# ==========================================================
# 12. APPLICATION TRACKER
# ==========================================================

elif page == "Application Tracker":

    page_header(
        "Application Tracker",
        "Organize your job search and keep track of every opportunity.",
        "📋",
    )

    applications = get_applications()

    total_apps = len(applications)

    interview_count = sum(
        1 for app in applications
        if "interview" in str(app.get("status", "")).lower()
    )

    offer_count = sum(
        1 for app in applications
        if "offer" in str(app.get("status", "")).lower()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Applications", total_apps)
    col2.metric("Interviews", interview_count)
    col3.metric("Offers", offer_count)

    st.write("")

    with st.expander("➕ Add a New Application", expanded=True):

        with st.form("add_application_form"):

            col1, col2 = st.columns(2)

            with col1:
                company = st.text_input(
                    "Company *",
                    placeholder="Company name",
                )

                job_title = st.text_input(
                    "Job Title *",
                    placeholder="Python Developer",
                )

                job_url = st.text_input(
                    "Job URL",
                    placeholder="https://...",
                )

            with col2:
                status = st.selectbox(
                    "Application Status",
                    options=list(STATUSES),
                    index=0,
                )

                applied_date = st.date_input(
                    "Applied Date",
                    value=date.today(),
                )

                has_followup = st.checkbox(
                    "Add a follow-up date"
                )

                follow_up_date = None

                if has_followup:
                    follow_up_date = st.date_input(
                        "Follow-up Date",
                        value=date.today(),
                    )

            notes = st.text_area(
                "Notes",
                placeholder="Add interview details, reminders, or notes...",
            )

            add_submitted = st.form_submit_button(
                "➕ Add Application",
                type="primary",
                use_container_width=True,
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

                    st.success("Application added successfully!")
                    st.rerun()

                except Exception as exc:
                    st.error(f"Could not add the application: {exc}")

    st.divider()

    st.subheader("Your Saved Applications")

    applications = get_applications()

    if not applications:

        st.info("No applications saved yet. Add your first application above.")

    else:

        search_text = st.text_input(
            "🔎 Search applications",
            placeholder="Search by company or job title...",
        )

        filtered_apps = [
            app for app in applications
            if (
                search_text.strip().lower()
                in str(app.get("company", "")).lower()
                or search_text.strip().lower()
                in str(app.get("job_title", "")).lower()
            )
        ]

        display_rows = [
            {
                "ID": get_application_id(app),
                "Company": app.get("company", ""),
                "Job Title": app.get("job_title", ""),
                "Status": app.get("status", ""),
                "Applied Date": app.get("applied_date", ""),
                "Follow-up Date": app.get("follow_up_date", ""),
            }
            for app in filtered_apps
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

            st.divider()
            st.subheader("✏️ Edit or Delete an Application")

            selected_id = st.selectbox(
                "Select an application",
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

                col1, col2 = st.columns(2)

                with col1:
                    edit_company = st.text_input(
                        "Company",
                        value=selected_app.get("company", ""),
                    )

                    edit_title = st.text_input(
                        "Job Title",
                        value=selected_app.get("job_title", ""),
                    )

                    edit_url = st.text_input(
                        "Job URL",
                        value=selected_app.get("job_url", ""),
                    )

                with col2:
                    current_status = selected_app.get(
                        "status", STATUSES[0]
                    )

                    status_index = (
                        list(STATUSES).index(current_status)
                        if current_status in STATUSES
                        else 0
                    )

                    edit_status = st.selectbox(
                        "Status",
                        options=list(STATUSES),
                        index=status_index,
                    )

                    edit_applied_date = st.text_input(
                        "Applied Date (YYYY-MM-DD)",
                        value=selected_app.get("applied_date", ""),
                    )

                    edit_follow_up = st.text_input(
                        "Follow-up Date (YYYY-MM-DD)",
                        value=selected_app.get("follow_up_date", ""),
                    )

                edit_notes = st.text_area(
                    "Notes",
                    value=selected_app.get("notes", ""),
                )

                update_submitted = st.form_submit_button(
                    "💾 Save Changes",
                    type="primary",
                )

            if update_submitted:

                if not edit_company.strip() or not edit_title.strip():

                    st.error("Company and job title are required.")

                else:

                    try:
                        updated = update_owned_application(
                            selected_id,
                            company=edit_company.strip(),
                            job_title=edit_title.strip(),
                            job_url=edit_url.strip(),
                            status=edit_status,
                            applied_date=edit_applied_date.strip(),
                            follow_up_date=edit_follow_up.strip(),
                            notes=edit_notes.strip(),
                        )

                        if updated:
                            st.success("Application updated!")
                            st.rerun()
                        else:
                            st.warning("Application was not found in your account.")

                    except Exception as exc:
                        st.error(f"Could not update the application: {exc}")

            with st.expander("🗑️ Delete an Application"):

                confirm_delete = st.checkbox(
                    f"I confirm that I want to delete application ID {selected_id}."
                )

                if st.button(
                    "Delete Selected Application",
                    type="primary",
                ):

                    if not confirm_delete:

                        st.warning("Please confirm before deleting.")

                    else:

                        try:
                            deleted = delete_owned_application(selected_id)

                            if deleted:
                                st.success("Application deleted.")
                                st.rerun()
                            else:
                                st.warning(
                                    "That application was not found in your account."
                                )

                        except Exception as exc:
                            st.error(f"Could not delete the application: {exc}")

# ==========================================================
# 13. SETTINGS AND PRIVACY
# ==========================================================

elif page == "Settings & Privacy":

    page_header(
        "Settings & Privacy",
        "Manage your account and understand how your information is handled.",
        "🔒",
    )

    user = st.session_state.user

    account_tab, privacy_tab, data_tab, about_tab = st.tabs([
        "👤 Account",
        "🔐 Privacy",
        "💾 Data Management",
        "ℹ️ About",
    ])

    with account_tab:

        with st.container(border=True):

            st.subheader("Account Information")

            st.text_input(
                "Name",
                value=user.get("name", ""),
                disabled=True,
            )

            st.text_input(
                "Email",
                value=user.get("email", ""),
                disabled=True,
            )

            st.success("Your account is active.")

            st.caption(
                "Account information is managed through your CareerForge AI login."
            )

    with privacy_tab:

        with st.container(border=True):

            st.subheader("Your Privacy Matters")

            st.markdown("""
            - Your profile and applications are associated with your account.
            - Your personal details are not automatically published.
            - Your portfolio can be shared when you choose to share its file or link.
            - Keep your password private.
            - Log out when using a shared computer.
            """)

        with st.expander("More about privacy"):

            st.write(PRIVACY_GUIDANCE)

        st.info(
            "Information submitted for owner review is stored separately "
            "in the private submissions database."
        )

    with data_tab:

        with st.container(border=True):

            st.subheader("Download Your Data")

            st.write(
                "Download a copy of your saved profile and job applications."
            )

            if st.button("Prepare My Data", use_container_width=True):

                try:
                    profile_data = load_profile(active_user_id) or {}
                    application_data = list_user_applications(
                        active_user_id
                    ) or []

                    export_data = {
                        "profile": profile_data,
                        "applications": application_data,
                    }

                    st.session_state["careerforge_export"] = json.dumps(
                        export_data,
                        indent=4,
                        ensure_ascii=False,
                        default=str,
                    )

                except Exception as exc:
                    st.error(f"Could not prepare your data: {exc}")

            if st.session_state.get("careerforge_export"):

                st.download_button(
                    "⬇️ Download My Data",
                    data=st.session_state["careerforge_export"],
                    file_name="careerforge_my_data.json",
                    mime="application/json",
                    use_container_width=True,
                )

        with st.container(border=True):

            st.subheader("Delete Your Data")

            st.warning(
                "This permanently deletes your saved profile and job "
                "applications. It does not delete your login account or "
                "separately stored owner submissions."
            )

            confirm_delete_data = st.checkbox(
                "I understand that deleting my profile and applications cannot be undone.",
                key="confirm_delete_data",
            )

            if st.button(
                "🗑️ Delete My Profile and Applications",
                type="primary",
                use_container_width=True,
            ):

                if not confirm_delete_data:

                    st.warning("Please confirm before deleting your data.")

                else:

                    try:
                        with connect_user_data() as connection:

                            connection.execute(
                                "DELETE FROM user_applications WHERE user_id = ?",
                                (active_user_id,),
                            )

                            connection.execute(
                                "DELETE FROM user_profiles WHERE user_id = ?",
                                (active_user_id,),
                            )

                            connection.commit()

                        st.session_state.profile = DEFAULT_PROFILE.copy()
                        st.session_state.pop("careerforge_export", None)
                        st.session_state.confirm_delete_data = False

                        st.success(
                            "Your profile and application records have been deleted."
                        )

                        st.rerun()

                    except Exception as exc:
                        st.error(f"Could not delete your data: {exc}")

    with about_tab:

        with st.container(border=True):

            st.subheader("CareerForge AI")

            st.write(
                "Your personal career workspace for creating resumes, "
                "building portfolios, matching job descriptions, and "
                "tracking applications."
            )

            st.markdown("""
            **Version:** 1.0

            **Built with:** Python and Streamlit

            **Main features:**
            - Resume generation
            - Portfolio generation
            - Job description matching
            - Application tracking
            - Personal dashboard
            """)

            st.caption("Build your profile. Showcase your skills. Grow your career.")

    st.divider()

    st.subheader("Sign Out")

    st.write("Sign out of your CareerForge AI account on this device.")

    if st.button("↪ Log Out", use_container_width=True):

        for key in (
            "user",
            "profile",
            "active_user_id",
            "job_description",
            "careerforge_export",
        ):
            st.session_state.pop(key, None)

        st.rerun()

