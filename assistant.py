import os
import streamlit as st
import pinecone
from pinecone_plugins.assistant.models.chat import Message

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

def get_assistant(_pinecone_instance):
    try:
        return _pinecone_instance.assistant.Assistant("dnd5e-assistant")
    except Exception as e:
        st.error(f"Error connecting to assistant: {e}")
        return None

def query_assistant(assistant, query, chat_history):
    try:
        chat_context = chat_history + [Message(content=query, role="user")]
        return assistant.chat_completions(messages=chat_context, stream=True)
    except Exception as e:
        return f"Error querying assistant: {str(e)}"

def chat_interface(assistant):
    # Initialize chat history in session state if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Create a container for chat messages
    chat_container = st.container()

    # Display chat messages
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know about?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # Generate assistant response
        with chat_container:
            with st.chat_message("assistant"):
                response_stream = query_assistant(assistant, prompt, [Message(content=m["content"], role=m["role"]) for m in st.session_state.messages])
                
                # Create a placeholder for the streaming effect
                message_placeholder = st.empty()
                full_response = ""
                
                # Stream the response
                for chunk in response_stream:
                    if chunk.choices:
                        content = chunk.choices[0].delta.content
                        if content:
                            full_response += content
                            message_placeholder.markdown(full_response + "▌")
                
                # Display the final response without the cursor
                message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})