# assistant.py
import os
import streamlit as st
import pinecone
from pinecone_plugins.assistant.models.chat import Message
from database import save_conversation, get_conversation, get_all_conversations, create_new_conversation, rename_conversation, delete_conversation
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import re
from image_generator import generate_optimized_prompt, generate_images_from_prompt

@st.cache_resource
def initialize_pinecone(max_retries=3, retry_delay=5):
    api_key = get_api_key()
    if not api_key:
        st.error("Pinecone API key not found. Please set it in your environment variables or Streamlit secrets.")
        return None

    for attempt in range(max_retries):
        try:
            return pinecone.Pinecone(api_key=api_key)
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Error initializing Pinecone (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                st.error(f"Failed to initialize Pinecone after {max_retries} attempts: {e}")
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

def query_assistant(assistant, query, chat_history, max_retries=3, retry_delay=5, timeout=90):
    def execute_query():
        chat_context = chat_history + [Message(content=query, role="user")]
        return assistant.chat_completions(messages=chat_context, stream=True)

    for attempt in range(max_retries):
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(execute_query)
                try:
                    return future.result(timeout=timeout)
                except TimeoutError:
                    raise Exception(f"Query timed out after {timeout} seconds")
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Error querying assistant (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                return f"Error querying assistant after {max_retries} attempts: {str(e)}"

def get_or_create_initial_conversation(username):
    conversations = get_all_conversations(username)
    if conversations:
        return conversations[0]["conversation_id"]
    else:
        return create_new_conversation(username)

def cleanup_response(response):
    # Remove empty numbered lines
    cleaned = re.sub(r'\n\d+\.\s*$', '', response, flags=re.MULTILINE)
    
    # Remove trailing empty lines
    cleaned = cleaned.rstrip()
    
    # If the last non-empty line is a question about what to do next, remove empty numbers after it
    last_line = cleaned.split('\n')[-1]
    if "what would you like to do" in last_line.lower() or "what do you want to do" in last_line.lower():
        cleaned = re.sub(r'\n\d+\.?\s*$', '', cleaned, flags=re.MULTILINE)
    
    return cleaned

def generate_topdown_image_from_context(messages):
    context = " ".join([m["content"] for m in messages[-5:]])  # Use the last 5 messages for context
    prompt = f"Based on this context, create a detailed top-down view image: {context}"
    return generate_optimized_prompt(prompt)

def generate_character_image_from_context(messages):
    context = " ".join([m["content"] for m in messages[-5:]])  # Use the last 5 messages for context
    prompt = f"""Based on the following context, create a detailed prompt for generating a character portrait image:

Context: {context}

Your prompt should include:
1. Character's race and class (if applicable)
2. Physical appearance (face, body type, hair, eyes, skin)
3. Clothing and armor
4. Weapons or magical items they might be holding
5. Character's expression and pose
6. Any distinctive features or accessories
7. Background or environment hints (if relevant)

Aim for a vivid, detailed description in about 75-100 words, focusing on visual elements that would make for an interesting and unique character portrait."""

    return generate_optimized_prompt(prompt, is_character=True)

def chat_interface(assistant, username):
    # Initialize session state variables
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = get_or_create_initial_conversation(username)
    if "renaming_conversation" not in st.session_state:
        st.session_state.renaming_conversation = None
    if "deleting_conversation" not in st.session_state:
        st.session_state.deleting_conversation = None
    if "editing_message_index" not in st.session_state:
        st.session_state.editing_message_index = None
    if "original_message_content" not in st.session_state:
        st.session_state.original_message_content = None
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}

    # Get all conversations for the sidebar
    conversations = get_all_conversations(username)

    # Sidebar for conversation management
    with st.sidebar:
        st.title("Conversations")
        if st.button("New Conversation"):
            new_id = create_new_conversation(username)
            st.session_state.current_conversation_id = new_id
            st.session_state.messages = []
            st.session_state.conversations[new_id] = {"optimized_prompt": None}
            st.rerun()

        for conv in conversations:
            conv_id = conv["conversation_id"]
            conv_name = conv.get("name", f"Conversation {conv['created_at'].strftime('%Y-%m-%d %H:%M')}")
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            if col1.button(conv_name, key=f"conv_{conv_id}"):
                st.session_state.current_conversation_id = conv_id
                st.session_state.messages = get_conversation(username, conv_id)
                if conv_id not in st.session_state.conversations:
                    st.session_state.conversations[conv_id] = {"optimized_prompt": None}
                st.rerun()
            
            if col2.button("✏️ Rename", key=f"rename_{conv_id}"):
                st.session_state.renaming_conversation = conv_id
            
            if col3.button("🗑️ Delete", key=f"delete_{conv_id}"):
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
    display_chat_messages(username)

    current_conv_state = st.session_state.conversations[st.session_state.current_conversation_id]

    # Add an expander for image generation features
    with st.expander("Image Generation", expanded=current_conv_state.get("optimized_prompt") is not None or current_conv_state.get("character_prompt") is not None):
        col1, col2 = st.columns(2)
        
        if col1.button("Generate Top-Down View Prompt"):
            with st.spinner("Generating optimized prompt for map..."):
                optimized_prompt = generate_topdown_image_from_context(st.session_state.messages)
                if optimized_prompt:
                    current_conv_state["optimized_prompt"] = optimized_prompt
                    current_conv_state["prompt_type"] = "map"
                    st.success("Optimized prompt for map generated!")
                else:
                    st.error("Failed to generate optimized prompt for map.")

        if col2.button("Generate Character Prompt"):
            with st.spinner("Generating optimized prompt for character..."):
                character_prompt = generate_character_image_from_context(st.session_state.messages)
                if character_prompt:
                    current_conv_state["character_prompt"] = character_prompt
                    current_conv_state["prompt_type"] = "character"
                    st.success("Optimized prompt for character generated!")
                else:
                    st.error("Failed to generate optimized prompt for character.")

        # Display and allow editing of the optimized prompt
        if current_conv_state.get("optimized_prompt") or current_conv_state.get("character_prompt"):
            prompt_type = current_conv_state.get("prompt_type", "map")
            prompt_key = "optimized_prompt" if prompt_type == "map" else "character_prompt"
            prompt_title = "Edit the optimized prompt for map:" if prompt_type == "map" else "Edit the optimized prompt for character:"
            
            col1, col2 = st.columns([5, 1])
            edited_prompt = col1.text_area(prompt_title, value=current_conv_state[prompt_key], height=100)
            if col2.button("Close"):
                current_conv_state[prompt_key] = None
                current_conv_state["prompt_type"] = None
                st.rerun()
            
            if st.button(f"Generate {prompt_type.capitalize()} Images"):
                with st.spinner(f"Generating {prompt_type} images..."):
                    image_urls = generate_images_from_prompt(edited_prompt)
                    if image_urls:
                        for i, url in enumerate(image_urls, 1):
                            st.image(url, caption=f"Generated {prompt_type.capitalize()} {i}")
                            st.markdown(f"[Download {prompt_type.capitalize()} Image {i}]({url})")
                    else:
                        st.error(f"Failed to generate {prompt_type} images.")

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
                # Clear the conversation state
                if st.session_state.deleting_conversation in st.session_state.conversations:
                    del st.session_state.conversations[st.session_state.deleting_conversation]
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

def display_chat_messages(username):
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if st.session_state.editing_message_index == idx:
                edit_message(username, idx, message)
            else:
                display_message(username, idx, message)

def display_message(username, idx, message):
    st.markdown(message["content"])
    if message["role"] == "assistant":
        if st.button("Edit", key=f"edit_{idx}"):
            st.session_state.editing_message_index = idx
            st.session_state.original_message_content = message["content"]
            st.rerun()

def edit_message(username, idx, message):
    edited_content = st.text_area("Edit message", value=message["content"], key=f"edit_area_{idx}", height=400)
    col1, col2 = st.columns(2)
    if col1.button("Save", key=f"save_{idx}"):
        st.session_state.messages[idx]["content"] = edited_content
        st.session_state.messages[idx]["edited"] = True
        save_conversation(username, st.session_state.current_conversation_id, st.session_state.messages)
        st.session_state.editing_message_index = None
        st.rerun()
    if col2.button("Cancel", key=f"cancel_{idx}"):
        st.session_state.editing_message_index = None
        st.rerun()

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
            
            if isinstance(response_stream, str):  # Error occurred
                st.error(response_stream)
                return

            message_placeholder = st.empty()
            full_response = ""
            
            try:
                for chunk in response_stream:
                    if chunk.choices:
                        content = chunk.choices[0].delta.content
                        if content:
                            full_response += content
                            cleaned_response = cleanup_response(full_response)
                            message_placeholder.markdown(cleaned_response + "▌")
            except Exception as e:
                st.error(f"Error while streaming response: {str(e)}")
                return
            
            final_cleaned_response = cleanup_response(full_response)
            message_placeholder.markdown(final_cleaned_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": final_cleaned_response})

        # Save the updated conversation
        save_conversation(username, st.session_state.current_conversation_id, st.session_state.messages)

# Debug function to display assistant information
def debug_assistant_info(assistant):
    if assistant:
        st.sidebar.write("Assistant Information:")
        st.sidebar.write(f"Name: {assistant.name}")
        st.sidebar.write(f"ID: {assistant.id}")
    else:
        st.sidebar.write("Assistant not initialized")

# You can uncomment the following line in chat_interface to use the debug function
# debug_assistant_info(assistant)
