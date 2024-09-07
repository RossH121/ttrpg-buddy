from openai import OpenAI
import os
import streamlit as st

@st.cache_resource
def initialize_openai():
    api_key = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Please set it in your environment variables or Streamlit secrets.")
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        # Test the API key with a simple request
        client.models.list()
        return client
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return None

def generate_optimized_prompt(prompt):
    client = initialize_openai()
    if not client:
        return None

    try:
        prompt_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at creating perfect prompts for text-to-image AI. Your task is to create a detailed, vivid prompt for generating a top-down view image. Focus on describing the scene, layout, objects, colors, and atmosphere. Do not mention 'battle map' or 'RPG' explicitly. Aim for a 50-75 word description."},
                {"role": "user", "content": f"Create an optimal text-to-image prompt for a top-down view based on this description: {prompt}"}
            ]
        )
        return prompt_response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating optimized prompt: {str(e)}")
        return None

def generate_images_from_prompt(optimized_prompt):
    client = initialize_openai()
    if not client:
        return None

    try:
        image_urls = []
        for i in range(4):
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=f"{optimized_prompt}",
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_urls.append(image_response.data[0].url)
        return image_urls
    except Exception as e:
        st.error(f"Error generating images: {str(e)}")
        return None
