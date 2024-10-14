# database.py
import os 
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

@st.cache_resource                                                                                                                                                                                       
def init_connection():                                                                                                                                                                                                                                                                                             
     uri = os.environ.get("MONGO_URI") or st.secrets.get("MONGO_URI")                                                                                                                  
     if not uri:                                                                                                                                                                                          
         raise ValueError("MongoDB URI not found in environment variables or Streamlit secrets")                                                                                                          
     return MongoClient(uri, server_api=ServerApi('1'))

def init_connection_no_cache():
    uri = os.environ.get("MONGO_URI")
    if not uri:
        raise ValueError("MongoDB URI not found in environment variables")
    return MongoClient(uri, server_api=ServerApi('1'))

def get_database():
    client = init_connection_no_cache()
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

def get_users_collection():
    db = get_database()
    return db["users"]

def create_user(username, email, name, password_hash):
    users = get_users_collection()
    user = {
        "username": username,
        "email": email,
        "name": name,
        "password": password_hash,
        "failed_login_attempts": 0,
        "logged_in": False,
        "created_at": datetime.utcnow()
    }
    result = users.insert_one(user)
    return result.inserted_id

def get_user(username):
    users = get_users_collection()
    return users.find_one({"username": username})

def get_user_by_email(email):
    users = get_users_collection()
    return users.find_one({"email": email})

def update_user(username, update_data):
    users = get_users_collection()
    result = users.update_one({"username": username}, {"$set": update_data})
    return result.modified_count > 0

def delete_user(username):
    users = get_users_collection()
    result = users.delete_one({"username": username})
    return result.deleted_count > 0

def get_all_users():
    users = get_users_collection()
    return list(users.find({}, {"password": 0}))

def increment_failed_login_attempts(username):
    users = get_users_collection()
    result = users.update_one(
        {"username": username},
        {"$inc": {"failed_login_attempts": 1}}
    )
    return result.modified_count > 0

def reset_failed_login_attempts(username):
    users = get_users_collection()
    result = users.update_one(
        {"username": username},
        {"$set": {"failed_login_attempts": 0}}
    )
    return result.modified_count > 0

def set_user_logged_in(username, logged_in):
    users = get_users_collection()
    result = users.update_one(
        {"username": username},
        {"$set": {"logged_in": logged_in}}
    )
    return result.modified_count > 0
