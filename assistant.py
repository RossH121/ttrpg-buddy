# assistant.py
import os
import streamlit as st
import pinecone
from pinecone_plugins.assistant.models.chat import Message
from database import save_conversation, get_conversation, get_all_conversations, create_new_conversation, rename_conversation, delete_conversation

@st.cache_resource
def initialize_pinecone():
    api_key = get_api_key()
    if not api_key:
        st.error("Pinecone API key not found. Please set it in your environment variables or Streamlit secrets.")
        return None

    try:
        return pinecone.Pinecone(api_key=api_key, environment="prod-1-data.ke.pinecone.io")
    except Exception as e:
        st.error(f"Error initializing Pinecone: {e}")
        return None

def get_api_key():
    return os.environ.get("PINECONE_API_KEY") or st.secrets.get("PINECONE_API_KEY")

def get_assistant(_pinecone_instance, config, username):
    try:
        assistant_name = config['credentials']['usernames'][username]['assistant']
        return _pinecone_instance.assistant.Assistant(assistant_name)
    except Exception as e:
        st.error(f"Error connecting to assistant: {e}")
        return None

def query_assistant(assistant, query, chat_history):
    try:
        chat_context = chat_history + [Message(content=query, role="user")]
        return assistant.chat_completions(messages=chat_context, stream=True)
    except Exception as e:
        return f"Error querying assistant: {str(e)}"
    
def get_or_create_initial_conversation(username):
    conversations = get_all_conversations(username)
    if conversations:
        return conversations[0]["conversation_id"]
    else:
        return create_new_conversation(username)

def chat_interface(assistant, username):
    # Initialize session state variables
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = get_or_create_initial_conversation(username)
    if "renaming_conversation" not in st.session_state:
        st.session_state.renaming_conversation = None
    if "deleting_conversation" not in st.session_state:
        st.session_state.deleting_conversation = None

    # Get all conversations for the sidebar
    conversations = get_all_conversations(username)

    # Sidebar for conversation management
    with st.sidebar:
        st.title("Conversations")
        if st.button("New Conversation"):
            new_id = create_new_conversation(username)
            st.session_state.current_conversation_id = new_id
            st.session_state.messages = []
            st.rerun()

        for conv in conversations:
            conv_id = conv["conversation_id"]
            conv_name = conv.get("name", f"Conversation {conv['created_at'].strftime('%Y-%m-%d %H:%M')}")
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            if col1.button(conv_name, key=f"conv_{conv_id}"):
                st.session_state.current_conversation_id = conv_id
                st.session_state.messages = get_conversation(username, conv_id)
                st.rerun()
            
            if col2.button("Rename", key=f"rename_{conv_id}"):
                st.session_state.renaming_conversation = conv_id
            
            if col3.button("Delete", key=f"delete_{conv_id}"):
                st.session_state.deleting_conversation = conv_id

        # Handle renaming
        if st.session_state.renaming_conversation:
            handle_rename(username, conversations)

        # Handle deleting
        if st.session_state.deleting_conversation:
            handle_delete(username, conversations)

    # Initialize chat history from database
    if "messages" not in st.session_state:
        st.session_state.messages = get_conversation(username, st.session_state.current_conversation_id)

    # Display current conversation name
    display_current_conversation(conversations)

    # Display chat messages
    display_chat_messages()

    # Chat input
    handle_chat_input(assistant, username)

def handle_rename(username, conversations):
    conv_to_rename = next((c for c in conversations if c["conversation_id"] == st.session_state.renaming_conversation), None)
    if conv_to_rename:
        new_name = st.text_input("New name", value=conv_to_rename.get("name", ""))
        col1, col2 = st.columns(2)
        if col1.button("Confirm Rename"):
            if rename_conversation(username, st.session_state.renaming_conversation, new_name):
                st.success("Conversation renamed successfully!")
                st.session_state.renaming_conversation = None
                st.rerun()
            else:
                st.error("Failed to rename conversation.")
        if col2.button("Cancel Rename"):
            st.session_state.renaming_conversation = None
            st.rerun()

def handle_delete(username, conversations):
    conv_to_delete = next((c for c in conversations if c["conversation_id"] == st.session_state.deleting_conversation), None)
    if conv_to_delete:
        st.warning(f"Are you sure you want to delete '{conv_to_delete.get('name', 'this conversation')}'?")
        col1, col2 = st.columns(2)
        if col1.button("Confirm Delete"):
            if delete_conversation(username, st.session_state.deleting_conversation):
                st.success("Conversation deleted successfully!")
                if st.session_state.current_conversation_id == st.session_state.deleting_conversation:
                    st.session_state.current_conversation_id = create_new_conversation(username)
                    st.session_state.messages = []
                st.session_state.deleting_conversation = None
                st.rerun()
            else:
                st.error("Failed to delete conversation.")
        if col2.button("Cancel Delete"):
            st.session_state.deleting_conversation = None
            st.rerun()

def display_current_conversation(conversations):
    current_conv = next((conv for conv in conversations if conv["conversation_id"] == st.session_state.current_conversation_id), None)
    if current_conv:
        st.header(current_conv.get("name", f"Conversation {current_conv['created_at'].strftime('%Y-%m-%d %H:%M')}"))

def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_chat_input(assistant, username):
    if prompt := st.chat_input("What would you like to know about?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            response_stream = query_assistant(assistant, prompt, [Message(content=m["content"], role=m["role"]) for m in st.session_state.messages])
            
            message_placeholder = st.empty()
            full_response = ""
            
            for chunk in response_stream:
                if chunk.choices:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Save the updated conversation
        save_conversation(username, st.session_state.current_conversation_id, st.session_state.messages)