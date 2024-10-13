import streamlit as st
import yaml
from yaml.loader import SafeLoader
from auth import initialize_auth, handle_authentication, handle_account_settings
from assistant import initialize_pinecone, get_assistant, chat_interface
from image_generator import initialize_openai

def main():
    st.title("Chat with TTRPG Buddy")

    # Load authentication configuration
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize authentication
    authenticator = initialize_auth(config)

    # Handle authentication
    username = handle_authentication(authenticator, config)
    if not username:
        return

    if username:
        # Initialize Pinecone and get the assistant
        pinecone_instance = initialize_pinecone()
        assistant = get_assistant(pinecone_instance, config, username) if pinecone_instance else None

        # Main chat interface
        if assistant:
            chat_interface(assistant, username)
        else:
            st.error("Assistant not initialized. Chat functionality is unavailable.")

    # Account settings
    handle_account_settings(authenticator)

    # Saving config file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

if __name__ == "__main__":
    main()
