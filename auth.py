import streamlit as st
from database import (
    get_user, create_user,
    increment_failed_login_attempts, reset_failed_login_attempts,
    set_user_logged_in
)
import bcrypt
from bson.binary import Binary


def initialize_auth():
    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None
    if "name" not in st.session_state:
        st.session_state.name = None
    if "username" not in st.session_state:
        st.session_state.username = None

def hash_password(password):
    return Binary(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def login(username, password):
    user = get_user(username)
    if user and verify_password(password, user['password']):
        reset_failed_login_attempts(username)
        set_user_logged_in(username, True)
        return user['name'], True, username
    else:
        if user:
            increment_failed_login_attempts(username)
        return None, False, None

def logout():
    for key in ['authentication_status', 'name', 'username']:
        if key in st.session_state:
            del st.session_state[key]

def register_user(username, email, name, password):
    if get_user(username):
        raise ValueError("Username already exists")
    hashed_password = hash_password(password)
    create_user(username, email, name, hashed_password)
    # Automatically log in the user after registration
    return login(username, password)

def handle_authentication():
    initialize_auth()

    if st.session_state.authentication_status:
        return st.session_state.username

    tabs = st.tabs(["Login", "Register"])

    with tabs[0]:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            name, authentication_status, username = login(username, password)
            if authentication_status:
                st.session_state.authentication_status = True
                st.session_state.name = name
                st.session_state.username = username
                st.rerun()
            else:
                st.error('Username/password is incorrect')

    with tabs[1]:
        st.subheader("Register New User")
        email = st.text_input("Email", key="register_email")
        username = st.text_input("Username", key="register_username")
        name = st.text_input("Name", key="register_name")
        password = st.text_input("Password", type="password", key="register_password")
        repeat_password = st.text_input("Repeat password", type="password", key="register_repeat_password")

        if st.button("Register"):
            if password != repeat_password:
                st.error("Passwords do not match")
            else:
                try:
                    name, authentication_status, username = register_user(username, email, name, password)
                    if authentication_status:
                        st.session_state.authentication_status = True
                        st.session_state.name = name
                        st.session_state.username = username
                        st.success("Registration successful! You are now logged in.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Registration failed: {e}")

    return None

def handle_logout():
    if st.session_state.authentication_status:
        with st.sidebar:
            st.divider()
            st.write(f'Logged in as: *{st.session_state["name"]}*')
            if st.button("Logout"):
                logout()
                st.rerun()
