import streamlit as st
import streamlit_authenticator as stauth
import yaml

def initialize_auth(config):
    return stauth.Authenticate(
        credentials=config['credentials'],
        cookie_name=config['cookie']['name'],
        key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days']
    )

def handle_authentication(authenticator, config):
    if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
        return st.session_state["username"]

    tabs = st.tabs(["Login", "Register"])

    with tabs[0]:
        # Login tab
        if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
            st.warning('Please enter your username and password')
        
        login_result = authenticator.login(location="main")
        
        if login_result is not None:
            name, authentication_status, username = login_result
            
            if authentication_status is False:
                st.error('Username/password is incorrect')
            elif authentication_status is None:
                st.warning('Please enter your username and password')
            else:
                st.session_state["authentication_status"] = authentication_status
                st.session_state["name"] = name
                st.session_state["username"] = username
                st.experimental_set_query_params(page="Home")
                return username

    with tabs[1]:
        # Registration tab
        st.title("Register New User")
        try:

            # Capture the default return values from the register_user function
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                pre_authorized=config.get('pre-authorized', {}).get('emails', []),
                captcha=False,
                fields={
                    'Form name': 'Register user',
                    'Email': 'Email',
                    'Username': 'Username',
                    'Password': 'Password',
                    'Repeat password': 'Repeat password',
                    'Register': 'Register'
                }
            )
            if email_of_registered_user:
                # Update config with new user details
                config['credentials']['usernames'][username_of_registered_user] = {
                    "email": email_of_registered_user,
                    "name": name_of_registered_user,
                    "password": config['credentials']['usernames'][username_of_registered_user]['password'],
                    "failed_login_attempts": 0, 
                    "logged_in": False
                }

                # Save updated config
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)

                # Automatically log in the user
                st.session_state["authentication_status"] = True
                st.session_state["name"] = name_of_registered_user
                st.session_state["username"] = username_of_registered_user
                st.success("Registration successful! You are now logged in.")
                st.rerun()  # Refresh the app to reflect the logged-in state
        except Exception as e:
            st.error(f"Registration failed: {e}")

    # Ensure the correct tab is active
    if 'active_tab' in st.session_state:
        tabs[1 if st.session_state['active_tab'] == 'Register' else 0].active = True

    return None

def handle_account_settings(authenticator):
    if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
        with st.sidebar:
            st.title("⚙️ Account Settings")
            st.write(f'Logged in as: *{st.session_state["name"]}*')
            if authenticator.logout("Logout", "sidebar"):
                st.rerun()
