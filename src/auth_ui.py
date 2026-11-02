import streamlit as st

from src.auth import register_user, login_user, validate_email


def render_auth_page():

    st.markdown(
        """
        <style>
        .auth-heading {
            text-align: center;
            font-size: 34px;
            font-weight: 800;
            color: #26345f;
            margin-bottom: 5px;
        }

        .auth-subheading {
            text-align: center;
            color: #64748b;
            margin-bottom: 25px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="auth-heading">CareerForge AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="auth-subheading">Build your career. Create your future.</div>',
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.5, 1])

    with center:
        login_tab, signup_tab = st.tabs(
            ["Login", "Create Account"]
        )

        with login_tab:
            st.subheader("Welcome back")

            with st.form("login_form"):
                email = st.text_input(
                    "Email address",
                    placeholder="name@example.com",
                )

                password = st.text_input(
                    "Password",
                    type="password",
                )

                submitted = st.form_submit_button(
                    "Login",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                valid, message = validate_email(email)

                if not valid:
                    st.error(message)

                elif not password:
                    st.error("Please enter your password.")

                else:
                    user = login_user(email, password)

                    if user:
                        st.session_state.user = user
                        st.session_state.profile_edit_redirect = False
                        st.success("Login successful.")
                        st.rerun()
                    else:
                        st.error("Incorrect email address or password.")

        with signup_tab:
            st.subheader("Create your account")

            with st.form("signup_form"):
                name = st.text_input(
                    "Full name",
                    placeholder="Your full name",
                )

                email = st.text_input(
                    "Email address",
                    placeholder="name@example.com",
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    help="Use at least 8 characters.",
                )

                confirm_password = st.text_input(
                    "Confirm password",
                    type="password",
                )

                submitted = st.form_submit_button(
                    "Create Account",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                valid, message = validate_email(email)

                if not name.strip():
                    st.error("Please enter your full name.")

                elif not valid:
                    st.error(message)

                elif len(password) < 8:
                    st.error("Password must contain at least 8 characters.")

                elif len(password) > 128:
                    st.error("Password must be 128 characters or fewer.")

                elif password != confirm_password:
                    st.error("Passwords do not match.")

                else:
                    success, result = register_user(
                        name,
                        email,
                        password,
                    )

                    if success:
                        st.success(result + " Please log in.")
                    else:
                        st.error(result)
