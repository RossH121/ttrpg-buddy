# database.py
import os 
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

@st.cache_resource                                                                                                                                                                                       
def init_connection():                                                                                                                                                                                   
     # Try to get the URI from environment variables first, then fall back to Streamlit secrets                                                                                                           
     uri = os.environ.get("MONGODB_URI")                                                                                                                      
     if not uri:                                                                                                                                                                                          
         raise ValueError("MongoDB URI not found in environment variables or Streamlit secrets")                                                                                                          
     return MongoClient(uri, server_api=ServerApi('1'))

def get_database():
    client = init_connection()
    return client.get_database("ttrpg-buddy-db")

def get_chat_history_collection():
    db = get_database()
    return db["chat-history"]

def save_conversation(username, conversation_id, messages):
    if not messages:
        return  # Don't save empty conversations
    
    collection = get_chat_history_collection()
    collection.update_one(
        {"username": username, "conversation_id": conversation_id},
        {
            "$set": {
                "messages": messages,
                "last_updated": datetime.utcnow()
            },
            "$setOnInsert": {"created_at": datetime.utcnow()}
        },
        upsert=True
    )

def update_message(username, conversation_id, message_index, new_content):
    collection = get_chat_history_collection()
    result = collection.update_one(
        {"username": username, "conversation_id": conversation_id},
        {
            "$set": {
                f"messages.{message_index}.content": new_content,
                f"messages.{message_index}.edited": True,
                "last_updated": datetime.utcnow()
            }
        }
    )
    return result.modified_count > 0

def get_conversation(username, conversation_id):
    collection = get_chat_history_collection()
    result = collection.find_one({"username": username, "conversation_id": conversation_id})
    return result["messages"] if result else []

def get_all_conversations(username):
    collection = get_chat_history_collection()
    conversations = collection.find(
        {"username": username},
        {"conversation_id": 1, "name": 1, "last_updated": 1, "created_at": 1}
    ).sort("last_updated", -1)
    return list(conversations)

def create_new_conversation(username):
    return str(datetime.utcnow().timestamp())

def rename_conversation(username, conversation_id, new_name):
    collection = get_chat_history_collection()
    result = collection.update_one(
        {"username": username, "conversation_id": conversation_id},
        {"$set": {"name": new_name, "last_updated": datetime.utcnow()}}
    )
    return result.modified_count > 0

def delete_conversation(username, conversation_id):
    collection = get_chat_history_collection()
    result = collection.delete_one({"username": username, "conversation_id": conversation_id})
    return result.deleted_count > 0
