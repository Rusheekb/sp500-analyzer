import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from auth import register_user, login_user, init_auth_db
from styles import load_css

st.set_page_config(page_title="Login", layout="wide", page_icon="🔐")
st.markdown(load_css(), unsafe_allow_html=True)

init_auth_db()

st.title("🔐 Login")

if "user_id" in st.session_state and st.session_state.user_id:
    st.success(f"Already logged in as **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()
else:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.markdown("#### 👤 Sign In")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", key="login_btn"):
            if login_username and login_password:
                success, user_id, message = login_user(login_username, login_password)
                if success:
                    st.session_state.user_id = user_id
                    st.session_state.username = login_username
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please enter both username and password.")

    with tab2:
        st.markdown("#### ✨ Create Account")
        reg_username = st.text_input("Choose a username", key="reg_user")
        reg_password = st.text_input("Choose a password", type="password", key="reg_pass")
        reg_confirm = st.text_input("Confirm password", type="password", key="reg_confirm")

        if st.button("Create Account", key="reg_btn"):
            if reg_username and reg_password and reg_confirm:
                if reg_password != reg_confirm:
                    st.error("Passwords don't match.")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    success, message = register_user(reg_username, reg_password)
                    if success:
                        st.success(message + " Please log in.")
                    else:
                        st.error(message)
            else:
                st.warning("Please fill in all fields.")