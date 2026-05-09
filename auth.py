import streamlit as st
import hashlib
import json
import os

USERS_FILE = "users.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def is_logged_in():
    return st.session_state.get("logged_in", False)


def logout():
    for key in ["logged_in", "username", "fullname", "complaint", "result"]:
        st.session_state.pop(key, None)


def show_auth_page():
    st.markdown("""
    <style>
        .block-container {
            max-width: 440px;
            padding-top: 60px;
        }

        .stTextInput > div > div > input {
            background-color: #ffffff !important;
            color: #111827 !important;
            border: 1px solid #374151 !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-size: 14px !important;
        }
        .stTextInput > div > div > input::placeholder {
            color: #9ca3af !important;
            opacity: 1 !important;
        }
        .stTextInput > label {
            font-size: 11px !important;
            font-weight: 600 !important;
            letter-spacing: 0.07em !important;
            text-transform: uppercase !important;
            color: #9aa6b2 !important;
        }

        .stButton > button {
            background-color: #ffffff !important;
            color: #111827 !important;
            border: 1px solid #d1d5db !important;
            border-radius: 8px !important;
            width: 100% !important;
            margin-top: 6px !important;
            font-size: 14px !important;
            padding: 10px !important;
        }
        .stButton > button:hover {
            border-color: #2563eb !important;
            color: #2563eb !important;
            background-color: #ffffff !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style='font-size:26px; font-weight:700; color:#f1f5f9; margin-bottom:4px;'>VaniSeva</h2>
    <p style='color:#475569; font-size:13px; margin-bottom:28px;'>
       Type, speak or write in your native language — we'll handle the rest
    </p>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        username = st.text_input("Username", key="li_user", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="li_pass", placeholder="Enter your password")

        if st.button("Login", key="btn_login"):
            if not username.strip() or not password.strip():
                st.error("Please fill in both fields.")
            else:
                users = load_users()
                if username in users and users[username]["password"] == hash_password(password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"]  = username
                    st.session_state["fullname"]  = users[username]["fullname"]
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
                users = load_users()
                if username_r in users:
                    st.error("This username is already taken.")
                else:
                    users[username_r] = {
                        "fullname": fullname.strip(),
                        "password": hash_password(password_r),
                    }
                    save_users(users)
                    st.success("Account created. Go to the Login tab to sign in.")
