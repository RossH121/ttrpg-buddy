import openai
import os
import streamlit as st

@st.cache_resource
def initialize_openai():
    api_key = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Please set it in your environment variables or Streamlit secrets.")
        return None
    openai.api_key = api_key
    return openai

def generate_battlemap(prompt):
    openai_instance = initialize_openai()
    if not openai_instance:
        return None

    try:
        response = openai_instance.Image.create(
            model="dall-e-3",
            prompt=f"I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: Create a top-down view battlemap for a tabletop RPG based on this description: {prompt}",
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response['data'][0]['url']
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None
