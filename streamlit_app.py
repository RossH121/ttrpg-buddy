# streamlit_app.py
import streamlit as st

st.set_page_config(
    page_title="TTRPG Buddy",
    page_icon="🎲",
)

st.write("# Welcome to TTRPG Buddy! 👋")

st.sidebar.success("Select a page above.")

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
