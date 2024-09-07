import streamlit as st
import yaml
from yaml.loader import SafeLoader
from auth import initialize_auth, handle_authentication, handle_account_settings

def main():
    st.title("TTRPG Buddy")

    # Load authentication configuration
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize authentication
    authenticator = initialize_auth(config)

    # Handle authentication
    username = handle_authentication(authenticator)
    if not username:
        return

    # Main content
    st.header("Welcome to TTRPG Buddy")
    st.write("This application helps you manage your tabletop role-playing games.")
    
    st.subheader("Instructions")
    st.write("1. Use the 'Chat' page to have conversations with your AI assistant.")
    st.write("2. Use the 'File Management' page to upload and manage your game files.")
    st.write("3. Navigate between pages using the sidebar on the left.")

    # Account settings
    handle_account_settings(authenticator)

    # Saving config file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

if __name__ == "__main__":
    main()
