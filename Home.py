# Home.py
import streamlit as st
from auth import handle_authentication, handle_logout
from assistant import initialize_pinecone, get_assistant
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="TTRPG Buddy",
    page_icon="🎲",
)

def main():
    logger.debug("Starting main function")
    st.title("TTRPG Buddy")

    logger.debug("Calling handle_authentication")
    username = handle_authentication()
    logger.debug(f"Returned username: {username}")

    if username:
        logger.info(f"User authenticated: {username}")
        _pinecone_instance = initialize_pinecone()
        assistant = get_assistant(_pinecone_instance, username)
        # Proceed with using the assistant

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

        handle_logout()
    else:
        st.warning("Please log in to access TTRPG Buddy")

    logger.debug("Main function completed")

if __name__ == "__main__":
    main()
