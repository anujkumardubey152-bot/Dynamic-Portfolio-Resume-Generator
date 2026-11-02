
import streamlit as st
from src.auth import register_user, login_user


def render_auth_page():
    st.markdown(
        "<h1 style='text-align:center;'>CareerForge AI</h1>"
        "<p style='text-align:center;'>Build your career. Showcase your talent.</p>",
        unsafe_allow_html=True
    )

    _, center, _ = st.columns([1, 2, 1])

    with center:
        tab_login, tab_signup = st.tabs(["Login", "Create Account"])

        with tab_login:
            st.subheader("Welcome Back")

            email = st.text_input("Email Address", key="login_email")
            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button("Login", use_container_width=True):
                user = login_user(email, password)

                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Incorrect email or password.")

        with tab_signup:
            st.subheader("Create Your Account")

            name = st.text_input("Full Name", key="signup_name")
            email = st.text_input("Email Address", key="signup_email")
            password = st.text_input(
                "Password (minimum 8 characters)",
                type="password",
                key="signup_password"
            )
            confirm = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm"
            )

            if st.button("Create Account", use_container_width=True):
                if password != confirm:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_user(
                        name, email, password
                    )

                    if success:
                        st.success(message)
                    else:
                        st.error(message)
