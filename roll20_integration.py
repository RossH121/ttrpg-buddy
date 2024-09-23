import json
from openai import OpenAI
import os
import streamlit as st
from image_generator import generate_character_image_from_context, generate_single_image

@st.cache_resource
def initialize_openai():
    api_key = os.getenv("OPENAI_API_KEY")
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

def generate_npc_prompt(chat_context):
    return """Based on the conversation above, create a JSON object representing an NPC with the following fields:
    name, race, class, level, strength, dexterity, constitution, intelligence, wisdom, charisma,
    actions, background, personality_traits, equipment, skills, languages, appearance.
    If any information is missing, use reasonable defaults. Ensure all ability scores are between 3 and 20.
    For actions, include 2-4 notable abilities or attack actions appropriate for the NPC's class and level.
    Each action should have a name and description.
    The background should be a brief summary of the NPC's history.
    Personality traits should be a list of 2-3 distinct characteristics.
    Equipment should be a list of items the NPC carries.
    Skills should be a list of proficient skills.
    Languages should be a list of languages the NPC speaks.
    Appearance should be a brief description of the NPC's physical characteristics.
    Only return the JSON object, no other text."""

def generate_npc_json(chat_context):
    client = initialize_openai()
    if not client:
        return None

    prompt = generate_npc_prompt(chat_context)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates JSON data for NPCs based on chat context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        npc_data = json.loads(response.choices[0].message.content)
        
        # Generate character image
        image_prompt = generate_character_image_from_context(chat_context)
        if image_prompt:
            image_url = generate_single_image(image_prompt)
            if image_url:
                npc_data['image_url'] = image_url
        
        return json.dumps(npc_data)
    except Exception as e:
        st.error(f"Error generating NPC JSON: {str(e)}")
        return None

def parse_npc_json(json_str):
    try:
        npc_data = json.loads(json_str)
        required_fields = ["name", "race", "class", "level", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma",
                           "actions", "background", "personality_traits", "equipment", "skills", "languages", "appearance"]
        for field in required_fields:
            if field not in npc_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate actions
        if not isinstance(npc_data["actions"], list) or len(npc_data["actions"]) == 0:
            raise ValueError("Actions must be a non-empty list")
        for action in npc_data["actions"]:
            if not all(key in action for key in ["name", "description"]):
                raise ValueError("Each action must have a name and description")
        
        return npc_data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")

def generate_roll20_command(npc_data):
    command = "!create-npc "
    command += json.dumps(npc_data)
    return command
