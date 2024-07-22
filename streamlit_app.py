import os
import streamlit as st
import pinecone
from pinecone_plugins.assistant.models.chat import Message

# Utility Functions

def get_api_key():
    """Retrieve the API key from environment variables or Streamlit secrets."""
    return os.environ.get("PINECONE_API_KEY") or st.secrets.get("PINECONE_API_KEY")

@st.cache_resource
def initialize_pinecone():
    """Initialize the Pinecone client."""
    api_key = get_api_key()
    if not api_key:
        st.error("Pinecone API key not found. Please set it in your environment variables or Streamlit secrets.")
        return None

    try:
        pinecone_instance = pinecone.Pinecone(
            api_key=api_key,
            environment="prod-1-data.ke.pinecone.io"
        )
        return pinecone_instance
    except Exception as e:
        st.error(f"Error initializing Pinecone: {e}")
        st.error("Make sure you've set your Pinecone API key correctly.")
        return None

def get_assistant(_pinecone_instance):
    """Get the Pinecone assistant instance."""
    try:
        return _pinecone_instance.assistant.Assistant("dnd5e-assistant")
    except Exception as e:
        st.error(f"Error connecting to assistant: {e}")
        return None

# Initialize Pinecone and get the assistant
pinecone_instance = initialize_pinecone()
assistant = get_assistant(pinecone_instance) if pinecone_instance else None

# Assistant Query Function
def query_assistant(query, chat_history):
    """Query the assistant with the given prompt and chat history and return a stream."""
    try:
        chat_context = chat_history + [Message(content=query, role="user")]
        return assistant.chat_completions(messages=chat_context, stream=True)
    except Exception as e:
        return f"Error querying assistant: {str(e)}"

def clear_chat_history():
    st.session_state.messages = []

# File Management Functions

def list_files():
    """List all files associated with the assistant."""
    try:
        files = assistant.list_files()
        return files
    except Exception as e:
        return f"Error listing files: {str(e)}"

def upload_file(file):
    """Upload a file to the assistant."""
    try:
        # Check file size (assuming 10MB limit, adjust as needed)
        max_size = 200 * 1024 * 1024  # 10MB in bytes
        if file.size > max_size:
            st.error(f"File is too large. Maximum size is {max_size/1024/1024:.2f}MB. Your file is {file.size/1024/1024:.2f}MB.")
            return False

        with st.spinner("Uploading file..."):
            temp_file_path = f"temp_{file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(file.getbuffer())
            response = assistant.upload_file(file_path=temp_file_path)
            os.remove(temp_file_path)
        st.success(f"File uploaded successfully: {response.get('name', 'Unknown')}")
        return True
    except pinecone.PineconeApiException as e:
        if e.status_code == 413:
            st.error(f"File is too large for the server to handle. Please try a smaller file or contact support for assistance.")
        else:
            st.error(f"Error uploading file: {str(e)}")
        return False
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return False
    
def delete_file(file_id):
    """Delete a file from the assistant."""
    try:
        assistant.delete_file(file_id=file_id)
        return True
    except Exception as e:
        st.error(f"Error deleting file: {str(e)}")
        return False

# Main Application

def main():
    st.title("TTRPG Buddy")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Clear chat button on main page
    if st.button("Clear Chat", on_click=clear_chat_history):
        st.empty()  # This will clear the previous messages visually

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
                response_stream = query_assistant(prompt, [Message(content=m["content"], role=m["role"]) for m in st.session_state.messages])
                
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

    # Debug information
    api_key = get_api_key()
    if assistant:
        st.sidebar.success("Connected to Assistant.")
    else:
        st.sidebar.error("Failed to connect to Assistant.")

    # Instructions for users
    with st.sidebar.expander("Instructions", expanded=False):
        st.write("Welcome to the TTRPG Buddy!")
        st.write("Chat with your TTRPG Rulebooks and Guides")
        st.write("Use the file management section to add or remove files from the assistant.")
        st.write("For example, try asking 'What are the steps for character creation?'")

    # File management in sidebar
    with st.sidebar:
        st.title("File Management")

        # File upload
        uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "pdf"])
        if uploaded_file is not None:
            if st.button("Upload"):
                if upload_file(uploaded_file):
                    st.rerun()

        # Display file list
        st.subheader("Uploaded Files")
        files = list_files()
        if isinstance(files, list):
            for file in files:
                col1, col2 = st.columns([3, 1])
                col1.write(f"{file.get('name', 'Unknown')}")
                if col2.button("Delete", key=file.get('id')):
                    if delete_file(file.get('id')):
                        st.success(f"Deleted {file.get('name', 'Unknown')}")
                        st.rerun()
        else:
            st.error(files)  # This will be the error message if listing failed

if __name__ == "__main__":
    main()