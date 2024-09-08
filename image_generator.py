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

def generate_optimized_prompt(prompt, is_character=False):
    client = initialize_openai()
    if not client:
        return None

    try:
        system_content = "You are an expert at creating perfect prompts for text-to-image AI. Your task is to create a detailed, vivid prompt for generating a top-down view image. Focus on describing the scene, layout, objects, colors, and atmosphere. Do not mention 'battle map' or 'RPG' explicitly. Aim for a 50-75 word description." if not is_character else "You are an expert at creating perfect prompts for text-to-image AI. Your task is to create a detailed, vivid prompt for generating a character or monster portrait. Focus on describing the character's appearance, clothing, pose, expression, and any notable features or items. Aim for a 75-100 word description."
        
        prompt_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"Create an optimal text-to-image prompt based on this description: {prompt}"}
            ]
        )
        return prompt_response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating optimized prompt: {str(e)}")
        return None

def generate_single_image(optimized_prompt):
    client = initialize_openai()
    if not client:
        return None

    try:
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"{optimized_prompt}",
            size="1024x1024",
            quality="standard",
            n=1
        )
        return image_response.data[0].url
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def generate_topdown_image_from_context(messages):
    context = " ".join([m["content"] for m in messages[-5:]])  # Use the last 5 messages for context
    prompt = f"Based on this context, create a detailed top-down view image: {context}"
    return generate_optimized_prompt(prompt)

def generate_character_image_from_context(messages):
    context = " ".join([m["content"] for m in messages[-5:]])  # Use the last 5 messages for context
    prompt = f"""Based on the following context, create a detailed prompt for generating a character/monster portrait image:

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
