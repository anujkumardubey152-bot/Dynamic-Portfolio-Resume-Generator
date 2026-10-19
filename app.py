import re
import sys
from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from src.resume_generator import generate_resume_pdf
from src.portfolio_generator import generate_portfolio_html
from src.application_tracker import (
    STATUSES,
    add_application,
    list_applications,
    update_application,
    delete_application,
)

st.set_page_config(
    page_title="Dynamic Portfolio and Resume Generator",
    page_icon="📄",
    layout="wide",
)

st.title("Dynamic Portfolio and Resume Generator")
st.caption(
    "Create a resume, preview a portfolio, compare job keywords, "
    "and track applications."
)

PAGES = [
    "Profile & Resume",
    "Portfolio Preview",
    "Job Description Match",
    "Application Tracker",
]

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a feature", PAGES)
    st.divider()
    st.caption("Use sample information while developing. Avoid sensitive data.")

st.session_state.setdefault("profile", {})

# ---------------------------------------------------------
# PROFILE AND RESUME
# ---------------------------------------------------------
if page == "Profile & Resume":
    st.header("Your professional profile")
    saved = st.session_state.profile

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full name *", value=saved.get("name", ""))
            email = st.text_input("Email", value=saved.get("email", ""))
            phone = st.text_input("Phone", value=saved.get("phone", ""))
            location = st.text_input("Location", value=saved.get("location", ""))

        with col2:
            linkedin = st.text_input("LinkedIn URL", value=saved.get("linkedin", ""))
            website = st.text_input(
                "Website or GitHub URL", value=saved.get("website", "")
            )
            target_role = st.text_input(
                "Target role", value=saved.get("target_role", "")
            )

        summary = st.text_area(
            "Professional summary", value=saved.get("summary", "")
        )
        skills = st.text_area(
            "Skills",
            value=saved.get("skills", ""),
            help="Enter skills separated by commas or on separate lines.",
        )
        experience = st.text_area(
            "Experience", value=saved.get("experience", ""), height=130
        )
        education = st.text_area(
            "Education", value=saved.get("education", "")
        )
        projects = st.text_area(
            "Projects", value=saved.get("projects", ""), height=110
        )

        save_profile = st.form_submit_button("Save profile", type="primary")

    if save_profile:
        if not name.strip():
            st.error("Please enter your name.")
        else:
            st.session_state.profile = {
                "name": name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "location": location.strip(),
                "linkedin": linkedin.strip(),
                "website": website.strip(),
                "target_role": target_role.strip(),
                "summary": summary.strip(),
                "skills": skills.strip(),
                "experience": experience.strip(),
                "education": education.strip(),
                "projects": projects.strip(),
            }
            st.success("Profile saved for this session.")
            st.rerun()

    profile = st.session_state.profile
    if profile.get("name"):
        st.subheader("Resume PDF")
        try:
            pdf_data = generate_resume_pdf(profile)
            st.download_button(
                "Download resume PDF",
                data=pdf_data,
                file_name="resume.pdf",
                mime="application/pdf",
                type="primary",
            )
        except Exception as exc:
            st.error(f"Could not generate the resume: {exc}")

# ---------------------------------------------------------
# PORTFOLIO PREVIEW AND DOWNLOAD
# ---------------------------------------------------------
elif page == "Portfolio Preview":
    profile = st.session_state.profile
    st.header("Portfolio preview")

    if not profile.get("name"):
        st.info("Save your profile first in Profile & Resume.")
    else:
        st.title(profile["name"])
        if profile.get("target_role"):
            st.subheader(profile["target_role"])
        if profile.get("location"):
            st.caption(profile["location"])

        if profile.get("summary"):
            st.markdown("### About Me")
            st.write(profile["summary"])

        if profile.get("skills"):
            st.markdown("### Skills")
            skill_items = [
                item.strip()
                for item in re.split(r"[,\n]", profile["skills"])
                if item.strip()
            ]
            st.write(" · ".join(skill_items))

        for heading, key in [
            ("Experience", "experience"),
            ("Projects", "projects"),
            ("Education", "education"),
        ]:
            if profile.get(key):
                st.markdown(f"### {heading}")
                st.write(profile[key])

        links = []
        if profile.get("linkedin"):
            links.append(f"[LinkedIn]({profile['linkedin']})")
        if profile.get("website"):
            links.append(f"[Website / GitHub]({profile['website']})")
        if links:
            st.markdown(" · ".join(links))

        try:
            html_data = generate_portfolio_html(profile)
            st.download_button(
                "Download portfolio HTML",
                data=html_data,
                file_name="portfolio.html",
                mime="text/html",
            )
        except Exception as exc:
            st.error(f"Could not generate the portfolio: {exc}")

# ---------------------------------------------------------
# JOB DESCRIPTION MATCH
# ---------------------------------------------------------
elif page == "Job Description Match":
    st.header("Job description keyword match")
    profile = st.session_state.profile

    if not profile.get("name"):
        st.info("Save your profile first. You can still paste a job description below.")

    job_description = st.text_area(
        "Paste the job description",
        height=230,
        placeholder="Paste the responsibilities and required skills here.",
    )

    if st.button("Analyze keyword match", type="primary"):
        if not profile.get("name"):
            st.warning("Please save your profile first.")
        elif not job_description.strip():
            st.warning("Please paste a job description.")
        else:
            profile_text = " ".join(
                str(profile.get(key, ""))
                for key in [
                    "target_role", "summary", "skills",
                    "experience", "education", "projects",
                ]
            ).lower()

            stop_words = {
                "and", "the", "with", "for", "you", "your", "are",
                "our", "will", "from", "that", "this", "have", "has",
                "job", "role", "work", "team", "years", "year",
                "ability", "including", "using", "required", "preferred",
                "strong", "knowledge", "must", "should",
            }

            def get_keywords(text):
                words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", text.lower())
                return {
                    word for word in words
                    if len(word) > 2 and word not in stop_words
                }

            job_terms = get_keywords(job_description)
            profile_terms = get_keywords(profile_text)

            if not job_terms:
                st.warning("Not enough recognizable keywords were found.")
            else:
                matched = sorted(job_terms & profile_terms)
                missing = sorted(job_terms - profile_terms)
                score = round(100 * len(matched) / len(job_terms))

                st.metric("Keyword overlap estimate", f"{score}%")
                st.caption(
                    "This is a simple keyword estimate, not an actual ATS score "
                    "or a prediction of hiring success."
                )

                left, right = st.columns(2)
                with left:
                    st.markdown("#### Matching keywords")
                    st.write(", ".join(matched) if matched else "No matches found.")
                with right:
                    st.markdown("#### Keywords to review")
                    st.write(", ".join(missing[:60]) if missing else "No unmatched keywords.")

                st.info(
                    "Only add skills or keywords that accurately represent your experience."
                )

# ---------------------------------------------------------
# APPLICATION TRACKER: ADD, EDIT, DELETE
# ---------------------------------------------------------
elif page == "Application Tracker":
    st.header("Job Application Tracker")
    st.write("Record applications, update progress, and manage follow-ups.")

    with st.form("add_application_form", clear_on_submit=True):
        company = st.text_input("Company name *")
        job_title = st.text_input("Job title *")
        job_url = st.text_input("Job posting URL")
        status = st.selectbox("Status", STATUSES, key="new_application_status")
        applied_date = st.date_input("Application date", value=date.today())
        follow_up_date = st.date_input("Follow-up date", value=None)
        notes = st.text_area("Notes")
        add_clicked = st.form_submit_button("Add application", type="primary")

    if add_clicked:
        if not company.strip() or not job_title.strip():
            st.error("Company name and job title are required.")
        else:
            try:
                add_application(
                    company=company,
                    job_title=job_title,
                    job_url=job_url,
                    status=status,
                    applied_date=applied_date.isoformat(),
                    follow_up_date=(
                        follow_up_date.isoformat() if follow_up_date else ""
                    ),
                    notes=notes,
                )
                st.success("Application added.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not add application: {exc}")

    st.divider()
    st.subheader("Saved applications")

    filter_status = st.selectbox(
        "Filter applications by status",
        ["All"] + STATUSES,
        key="filter_application_status",
    )

    try:
        applications = list_applications(
            status=None if filter_status == "All" else filter_status
        )
    except Exception as exc:
        applications = []
        st.error(f"Could not load applications: {exc}")

    if not applications:
        st.info("No applications found. Add your first application above.")
    else:
        table_columns = [
            "id", "company", "job_title", "status",
            "applied_date", "follow_up_date", "job_url", "notes",
        ]
        st.dataframe(
            pd.DataFrame(applications)[table_columns],
            use_container_width=True,
            hide_index=True,
        )

        ids = [row["id"] for row in applications]
        selected_id = st.selectbox(
            "Select an application to manage",
            ids,
            format_func=lambda item_id: next(
                f"#{row['id']} — {row['company']} — {row['job_title']}"
                for row in applications if row["id"] == item_id
            ),
        )
        selected = next(row for row in applications if row["id"] == selected_id)

        with st.expander("Edit selected application"):
            with st.form("edit_application_form"):
                edit_company = st.text_input(
                    "Company name", value=selected["company"]
                )
                edit_title = st.text_input(
                    "Job title", value=selected["job_title"]
                )
                edit_url = st.text_input(
                    "Job posting URL", value=selected.get("job_url") or ""
                )
                edit_status = st.selectbox(
                    "Application status",
                    STATUSES,
                    index=STATUSES.index(selected["status"]),
                )
                edit_applied = st.text_input(
                    "Application date (YYYY-MM-DD)",
                    value=selected.get("applied_date") or "",
                )
                edit_follow_up = st.text_input(
                    "Follow-up date (YYYY-MM-DD)",
                    value=selected.get("follow_up_date") or "",
                )
                edit_notes = st.text_area(
                    "Notes", value=selected.get("notes") or ""
                )
                save_changes = st.form_submit_button("Save changes")

            if save_changes:
                try:
                    changed = update_application(
                        selected_id,
                        company=edit_company,
                        job_title=edit_title,
                        job_url=edit_url,
                        status=edit_status,
                        applied_date=edit_applied,
                        follow_up_date=edit_follow_up,
                        notes=edit_notes,
                    )
                    if changed:
                        st.success("Application updated.")
                        st.rerun()
                    else:
                        st.warning("No changes were saved.")
                except Exception as exc:
                    st.error(f"Could not update application: {exc}")

        st.divider()
        st.subheader("Remove an application")
        st.warning("Deleting an application permanently removes that record from the local database.")

        confirm_delete = st.checkbox(
            f"I want to permanently delete #{selected_id}: "
            f"{selected['company']} — {selected['job_title']}",
            key=f"confirm_delete_{selected_id}",
        )

        if st.button(
            "Delete selected application",
            type="secondary",
            disabled=not confirm_delete,
        ):
            try:
                deleted = delete_application(selected_id)
                if deleted:
                    st.success("Application deleted.")
                    st.rerun()
                else:
                    st.warning("Application was not found.")
            except Exception as exc:
                st.error(f"Could not delete application: {exc}")
