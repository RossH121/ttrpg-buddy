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
        authenticator.login()
        if st.session_state.get("authentication_status") is False:
            st.error('Username/password is incorrect')
        elif st.session_state.get("authentication_status") is None:
            st.warning('Please enter your username and password')
        return False
    return True

def handle_account_settings(authenticator):
    with st.sidebar:
        st.title("⚙️ Account Settings")
        st.write(f'Logged in as: *{st.session_state["name"]}*')
        if authenticator.logout("Logout", "sidebar"):
            st.rerun()