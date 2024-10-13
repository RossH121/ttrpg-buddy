# Home.py
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from auth import initialize_auth, handle_authentication, handle_account_settings
from assistant import initialize_pinecone, get_assistant

st.set_page_config(
    page_title="TTRPG Buddy",
    page_icon="🎲",
)

def main():
    st.title("TTRPG Buddy")

    # Load authentication configuration
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize authentication
    authenticator = initialize_auth(config)

    # Handle authentication
    username = handle_authentication(authenticator, config)
    if not username:
        return

    # Sidebar content (only shown when logged in)
    with st.sidebar:
        st.title("⚙️ Account Settings")
        st.write(f'Logged in as: *{st.session_state["name"]}*')
        if authenticator.logout("Logout", "sidebar"):
            st.rerun()

    # Use session state to manage navigation
    if "redirect_to_home" not in st.session_state:
        st.session_state.redirect_to_home = True

    if st.session_state.redirect_to_home:
        st.session_state.redirect_to_home = False
        st.rerun()

    # Main content
    st.header("Welcome to TTRPG Buddy")
    st.write("This application helps you manage your tabletop role-playing games.")

    st.markdown(
        """
        TTRPG Buddy is an AI-powered assistant for tabletop role-playing games.

        **👈 Select a page from the sidebar** to get started!

        ### What you can do:
        - Chat with the AI assistant about your game
        - Manage your game files
        - And more!

        ### How to use:
        1. Use the 'Chat' page to have conversations with your AI assistant.
        2. Use the 'File Management' page to upload and manage your game files.
        3. Navigate between pages using the sidebar on the left.

        Enjoy your adventure!
        """
    )

    # Saving config file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

if __name__ == "__main__":
    main()
