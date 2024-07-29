import streamlit as st
import streamlit_authenticator as stauth

def initialize_auth(config):
    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config.get('pre-authorized')
    )

def handle_authentication(authenticator):
    if not st.session_state.get("authentication_status"):
        name, authentication_status, username = authenticator.login()
        if authentication_status is False:
            st.error('Username/password is incorrect')
        elif authentication_status is None:
            st.warning('Please enter your username and password')
        else:
            return username
    else:
        return st.session_state.get("username")
    return None

def handle_account_settings(authenticator):
    with st.sidebar:
        st.title("⚙️ Account Settings")
        st.write(f'Logged in as: *{st.session_state["name"]}*')
        if authenticator.logout("Logout", "sidebar"):
            st.rerun()