import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator import ResetError

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

def handle_account_settings(authenticator, config):
    with st.sidebar:
        st.title("⚙️ Account Settings")
        st.write(f'Logged in as: *{st.session_state["name"]}*')
        if authenticator.logout("Logout", "sidebar"):
            st.rerun()
        
        reset_password_expander = st.expander("Reset Password")
        reset_success_placeholder = st.empty()

        with reset_password_expander:
            reset_successful, message = handle_password_reset(authenticator, config)
            if reset_successful:
                reset_password_expander.empty()
                reset_success_placeholder.success(message)
                st.rerun()
            elif message != "Password reset cancelled":
                st.error(message)

def handle_password_reset(authenticator, config):
    st.write("Password must:")
    st.write("- Be at least 8 characters long")
    st.write("- Contain at least one number")
    st.write("- Contain at least one lowercase letter")
    st.write("- Contain at least one uppercase letter")
    st.write("- Contain at least one special character (!@#$%^&*()_+-=[]{};\':\"\\|,.<>/?)")
    try:
        if authenticator.reset_password(st.session_state["username"]):
            return True, "Password modified successfully"
        else:
            return False, "Password reset cancelled"
    except ResetError as e:
        return False, f"ResetError: {str(e)}"
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"