import streamlit as st
import yaml
from yaml.loader import SafeLoader
from auth import handle_authentication, handle_account_settings
from assistant import initialize_pinecone, get_assistant, chat_interface
from image_generator import initialize_openai

def main():
    st.title("Chat with TTRPG Buddy")


    # Handle authentication
    username = handle_authentication()
    if not username:
        return

    if username:
        # Initialize Pinecone and get the assistant
        pinecone_instance = initialize_pinecone()
        assistant = get_assistant(pinecone_instance, username) if pinecone_instance else None

        # Main chat interface
        if assistant:
            chat_interface(assistant, username)
        else:
            st.error("Assistant not initialized. Chat functionality is unavailable.")

    # Account settings
    handle_account_settings()

if __name__ == "__main__":
    main()
