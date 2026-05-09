import streamlit as st
import hashlib
from datetime import datetime
from db import get_db


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def is_logged_in():
    return st.session_state.get("logged_in", False)


def logout():
    for key in ["logged_in", "username", "fullname", "complaint", "result"]:
        st.session_state.pop(key, None)


def show_auth_page():
    st.markdown("""
    <style>
        .block-container { max-width: 440px; padding-top: 60px; }
        .stTextInput > label {
            font-size: 11px;
            color: #9aa6b2;
            font-weight: 600;
            letter-spacing: 0.07em;
            text-transform: uppercase;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff !important;
            color: #111827 !important;
            border: 1px solid #d1d5db !important;
            border-radius: 8px !important;
            font-size: 14px !important;
        }
        .stTextInput > div > div > input::placeholder {
            color: #9ca3af !important;
        }
        .stButton > button {
            width: 100%;
            margin-top: 6px;
            background-color: #ffffff !important;
            color: #111827 !important;
            border: 1px solid #d1d5db !important;
            border-radius: 8px !important;
            font-size: 14px !important;
        }
        .stButton > button:hover {
            border-color: #2563eb !important;
            color: #2563eb !important;
        }
        .stTabs [data-baseweb="tab-list"] { margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style='font-size:26px; font-weight:700; margin-bottom:4px;'>VaniSeva</h2>
    <p style='font-size:13px; margin-bottom:28px;'>
        Type, speak or write in your native language — we'll handle the rest
    </p>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["Login", "Register"])

    users_col = get_db()["users"]

    with tab_login:
        username = st.text_input("Username", key="li_user", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="li_pass", placeholder="Enter your password")

        if st.button("Login", key="btn_login"):
            if not username.strip() or not password.strip():
                st.error("Please fill in both fields.")
            else:
                user = users_col.find_one({"username": username})
                if user and user["password"] == hash_password(password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"]  = username
                    st.session_state["fullname"]  = user["fullname"]
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

    with tab_register:
        fullname   = st.text_input("Full Name",        key="rg_name", placeholder="Your full name")
        username_r = st.text_input("Username",         key="rg_user", placeholder="Choose a username")
        password_r = st.text_input("Password",         type="password", key="rg_pass", placeholder="At least 6 characters")
        confirm    = st.text_input("Confirm Password", type="password", key="rg_conf", placeholder="Re-enter password")

        if st.button("Create Account", key="btn_register"):
            if not all([fullname.strip(), username_r.strip(), password_r, confirm]):
                st.error("Please fill in all fields.")
            elif password_r != confirm:
                st.error("Passwords do not match.")
            elif len(password_r) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                if users_col.find_one({"username": username_r}):
                    st.error("This username is already taken.")
                else:
                    users_col.insert_one({
                        "username":   username_r,
                        "fullname":   fullname.strip(),
                        "password":   hash_password(password_r),
                        "created_at": datetime.now().isoformat(),
                    })
                    st.success("Account created. Go to the Login tab to sign in.")
