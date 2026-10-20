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
                        update_application(
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
                        delete_application(selected_id)
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

