import streamlit as st
import yaml
from yaml.loader import SafeLoader
from auth import handle_authentication, handle_account_settings
from assistant import initialize_pinecone, get_assistant
from file_management import file_management_sidebar

def main():
    st.title("File Management")

    # Handle authentication
    username = handle_authentication()
    if not username:
        return

    if username:
        # Initialize Pinecone and get the assistant
        pinecone_instance = initialize_pinecone()
        assistant = get_assistant(pinecone_instance, username) if pinecone_instance else None

        # Main file management interface
        if assistant:
            file_management_sidebar(assistant)
        else:
            st.error("Assistant not initialized. File management is unavailable.")

    # Account settings
    handle_account_settings()

if __name__ == "__main__":
    main()
