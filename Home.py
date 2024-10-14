# Home.py
import streamlit as st
from auth import handle_authentication, handle_logout
from assistant import initialize_pinecone, get_assistant

st.set_page_config(
    page_title="TTRPG Buddy",
    page_icon="🎲",
)

@st.fragment
@st.fragment
def home_content():
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

def main():
    st.title("TTRPG Buddy")
    username = handle_authentication()

    if username:
        _pinecone_instance = initialize_pinecone()
        assistant = get_assistant(_pinecone_instance, username)
        # Proceed with using the assistant

        # Main content
        home_content()

        handle_logout()
    else:
        st.warning("Please log in to access TTRPG Buddy")

if __name__ == "__main__":
    main()
