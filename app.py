from pathlib import Path
import sys
import json
from datetime import date

import streamlit as st
import pandas as pd

# --------------------------------------------------
# 1. APP CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

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

    from src.privacy_settings import PRIVACY_GUIDANCE

    from src.privacy_store import (
        render_admin_page,
        save_submission,
    )

except ModuleNotFoundError as exc:
    st.error("A required project module or dependency is missing.")
    st.code(str(exc))
    st.info(
        "Check that your src folder contains all required Python "
        "modules and that requirements.txt includes their dependencies."
    )
    st.stop()

# --------------------------------------------------
# 3. OWNER ADMIN DASHBOARD
# Open the app URL with ?admin=1
# --------------------------------------------------

if st.query_params.get("admin") == "1":
    render_admin_page()
    st.stop()

# --------------------------------------------------
# 4. SESSION STATE
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

if "profile" not in st.session_state:
    st.session_state.profile = DEFAULT_PROFILE.copy()

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# --------------------------------------------------
# 5. HELPER FUNCTIONS
# --------------------------------------------------

def parse_lines(value):
    """Convert multiline text into a list of non-empty lines."""
    return [
        line.strip()
        for line in str(value or "").splitlines()
        if line.strip()
    ]


def parse_skills(value):
    """Convert comma-separated skills into a unique list."""
    skills = [
        skill.strip()
        for skill in str(value or "").replace("\n", ",").split(",")
        if skill.strip()
    ]
    return list(dict.fromkeys(skills))


def current_profile():
    return st.session_state.profile


def get_application_id(application):
    """Support common application ID field names."""
    for key in ("id", "application_id"):
        if application.get(key) is not None:
            return application[key]
    return None


def get_applications():
    """Load application records safely."""
    try:
        return list_applications() or []
    except Exception as exc:
        st.error(f"Could not load applications: {exc}")
        return []


# --------------------------------------------------
# 6. SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("CareerForge AI")
st.sidebar.caption("Your personal career toolkit")

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

st.sidebar.divider()
st.sidebar.caption(
    "Build your profile. Prepare your resume. Track your career."
)
