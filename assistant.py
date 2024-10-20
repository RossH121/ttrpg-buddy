# assistant.py
import os
from dotenv import load_dotenv
import streamlit as st
import pinecone
from pinecone_plugins.assistant.models.chat import Message
from database import save_conversation, get_conversation, get_all_conversations, create_new_conversation, rename_conversation, delete_conversation, get_user
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from image_generator import generate_single_image, generate_topdown_image_from_context, generate_character_image_from_context
from roll20_integration import generate_npc_json, parse_npc_json, generate_roll20_command

@st.cache_resource
def initialize_pinecone(max_retries=3, retry_delay=5):
    api_key = get_api_key()
    if not api_key:
        st.error("Pinecone API key not found. Please set it in your environment variables, .env file, or Streamlit secrets.")
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
    
    # Check environment variables (including those loaded from .env)
    api_key = os.getenv("PINECONE_API_KEY")
    
    # If not found in environment variables, check Streamlit secrets
    if not api_key:
        api_key = st.secrets.get("PINECONE_API_KEY")
    
    if not api_key:
        st.error("Pinecone API key not found in environment variables, .env file, or Streamlit secrets.")
    
    return api_key

from database import get_user

def get_assistant(_pinecone_instance, username):
    try:
        # Fetch user data from MongoDB
        user = get_user(username)
        if not user or 'assistant' not in user:
            raise KeyError("Assistant information not found for the user")

        assistant_name = user['assistant']
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
                    result = future.result(timeout=timeout)
                    return result  # This is now a generator
                except TimeoutError:
                    raise Exception(f"Query timed out after {timeout} seconds")
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Error querying assistant (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                return f"Error querying assistant after {max_retries} attempts: {str(e)}"

def response_stream_processor(stream):
    full_response = ""
    for chunk in stream:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                yield content
    return full_response

def get_or_create_initial_conversation(username):
    conversations = get_all_conversations(username)
    if conversations:
        return conversations[0]["conversation_id"]
    else:
        return create_new_conversation(username)

@st.fragment
def conversation_management(username):
    conversations = get_all_conversations(username)
    
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
            st.session_state.cancel_rename = False
            st.rerun()

        if col3.button("🗑️ Delete", key=f"delete_{conv_id}"):
            st.session_state.deleting_conversation = conv_id
            st.session_state.cancel_delete = False
            st.rerun()

        # Handle renaming
        if st.session_state.renaming_conversation == conv_id and not st.session_state.cancel_rename:
            new_name = st.text_input("New name", value=conv_name, key=f"new_name_{conv_id}")
            col1, col2 = st.columns(2)
            if col1.button("Confirm Rename", key=f"confirm_rename_{conv_id}"):
                if rename_conversation(username, conv_id, new_name):
                    st.success("Conversation renamed successfully!")
                    st.session_state.renaming_conversation = None
                    st.rerun()
                else:
                    st.error("Failed to rename conversation.")
            if col2.button("Cancel Rename", key=f"cancel_rename_{conv_id}"):
                st.session_state.renaming_conversation = None
                st.session_state.cancel_rename = True
                st.rerun()

        # Handle deleting
        if st.session_state.deleting_conversation == conv_id and not st.session_state.cancel_delete:
            st.warning(f"Are you sure you want to delete '{conv_name}'?")
            col1, col2 = st.columns(2)
            if col1.button("Confirm Delete", key=f"confirm_delete_{conv_id}"):
                if delete_conversation(username, conv_id):
                    st.success("Conversation deleted successfully!")
                    if st.session_state.current_conversation_id == conv_id:
                        st.session_state.current_conversation_id = create_new_conversation(username)
                        st.session_state.messages = []
                    if conv_id in st.session_state.conversations:
                        del st.session_state.conversations[conv_id]
                    st.session_state.deleting_conversation = None
                    st.rerun()
                else:
                    st.error("Failed to delete conversation.")
            if col2.button("Cancel Delete", key=f"cancel_delete_{conv_id}"):
                st.session_state.deleting_conversation = None
                st.session_state.cancel_delete = True
                st.rerun()

@st.fragment
def image_generation_section(messages, current_conv_state):
    if messages:
        with st.expander("Image Generation", expanded=current_conv_state.get("optimized_prompt") is not None or current_conv_state.get("character_prompt") is not None):
            col1, col2 = st.columns(2)
            
            if col1.button("Generate Top-Down View Prompt"):
                with st.spinner("Generating optimized prompt for map..."):
                    optimized_prompt = generate_topdown_image_from_context(messages)
                    if optimized_prompt:
                        current_conv_state["optimized_prompt"] = optimized_prompt
                        current_conv_state["prompt_type"] = "map"
                        st.success("Optimized prompt for map generated!")
                    else:
                        st.error("Failed to generate optimized prompt for map. Please ensure there's enough context in the chat.")

            if col2.button("Generate Character Prompt"):
                with st.spinner("Generating optimized prompt for character..."):
                    character_prompt = generate_character_image_from_context(messages)
                    if character_prompt:
                        current_conv_state["character_prompt"] = character_prompt
                        current_conv_state["prompt_type"] = "character"
                        st.success("Optimized prompt for character generated!")
                    else:
                        st.error("Failed to generate optimized prompt for character. Please ensure there's enough context in the chat.")

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
                    progress_bar = st.progress(0)
                    for i in range(4):
                        with st.spinner(f"Generating {prompt_type} image {i+1}/4..."):
                            image_url = generate_single_image(edited_prompt)
                            if image_url:
                                st.image(image_url, caption=f"Generated {prompt_type.capitalize()} {i+1}")
                                st.markdown(f"[Download {prompt_type.capitalize()} Image {i+1}]({image_url})")
                            else:
                                st.error(f"Failed to generate {prompt_type} image {i+1}.")
                        progress_bar.progress((i + 1) / 4)
                    st.success(f"All {prompt_type} images generated!")
    else:
        st.info("Start a conversation to enable image generation features.")

@st.fragment
def roll20_npc_command_section(messages):
    if messages:
        with st.expander("Roll20 NPC Command Generation", expanded=False):
            if st.button("Generate Roll20 NPC Command"):
                with st.spinner("Generating NPC data..."):
                    try:
                        npc_json = generate_npc_json(messages)
                        npc_data = parse_npc_json(npc_json)
                        roll20_command = generate_roll20_command(npc_data)
                        st.code(roll20_command, language="text")
                        st.info("Copy this command and paste it into your Roll20 chat to create the NPC.")
                    except ValueError as e:
                        st.error(f"Error generating NPC data: {str(e)}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")

def chat_interface(assistant, username):
    #Initialize session state variables
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
    if "messages" not in st.session_state:
        st.session_state.messages = get_conversation(username, st.session_state.current_conversation_id)
    if "cancel_rename" not in st.session_state:
        st.session_state.cancel_rename = False
    if "cancel_delete" not in st.session_state:
        st.session_state.cancel_delete = False

    # Sidebar for conversation management
    with st.sidebar:
        conversation_management(username)

    # Display current conversation name
    display_current_conversation(get_all_conversations(username))

    # Display chat messages
    display_chat_messages(username)

    # Chat input
    handle_chat_input(assistant, username)

    # Image Generation Section
    current_conv_state = st.session_state.conversations.get(st.session_state.current_conversation_id, {"optimized_prompt": None})
    image_generation_section(st.session_state.messages, current_conv_state)

    # Roll20 NPC Command Generation Section
    roll20_npc_command_section(st.session_state.messages)

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
            st.rerun()  # Trigger a rerun to immediately show the edit form

def edit_message(username, idx, message):
    edited_content = st.text_area("Edit message", value=message["content"], key=f"edit_area_{idx}", height=400)
    col1, col2 = st.columns(2)
    if col1.button("Save", key=f"save_{idx}"):
        st.session_state.messages[idx]["content"] = edited_content
        st.session_state.messages[idx]["edited"] = True
        save_conversation(username, st.session_state.current_conversation_id, st.session_state.messages)
        st.session_state.editing_message_index = None
        st.rerun()  # Trigger a rerun to update the UI after saving
    if col2.button("Cancel", key=f"cancel_{idx}"):
        st.session_state.editing_message_index = None
        st.rerun()  # Trigger a rerun to update the UI after canceling

def handle_chat_input(assistant, username):
    if prompt := st.chat_input("What would you like to know about?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        user = get_user(username)
        message_history_limit = user.get('message_history_limit', 10)

        with st.chat_message("assistant"):
            limited_history = st.session_state.messages[-message_history_limit:]
            response_stream = query_assistant(assistant, prompt, [Message(content=m["content"], role=m["role"]) for m in limited_history])
            
            if isinstance(response_stream, str):
                st.error(response_stream)
                return

            full_response = st.write_stream(response_stream_processor(response_stream))
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_conversation(username, st.session_state.current_conversation_id, st.session_state.messages)
