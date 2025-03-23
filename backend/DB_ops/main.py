from fastapi import FastAPI, Depends
from pymongo import MongoClient
from typing import Dict, List
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId

# MongoDB CRUD class
class MongoCRUD:
    def __init__(self):
        uri = "mongodb://localhost:27017/studLLM_main"
        
        self.client = MongoClient(uri)
        self.db = self.client.get_database()
        self.users_collection = self.db["users"]
        self.user_state_collection = self.db["user_state"]
        self.chat_history_collection = self.db["chat_history"]
    
    # === USER OPERATIONS ===
    def get_user(self, user_id: str):
        """Get a user document by ID"""
        return self.users_collection.find_one({"_id": user_id})
    
    # === STATE MANAGEMENT ===
    def update_user_state(self, user_id: str, state_data: dict):
        """Update user state within the user document"""
        timestamp = {"$date": datetime.now().isoformat()}
        current_user = self.users_collection.find_one({"_id": user_id})
        current_state = current_user.get("state", {}) if current_user else {}
        state_data["last_updated"] = timestamp
        
        update_operation = {
            "$set": {
                "state": state_data
            }
        }
        
        if current_state:
            update_operation["$push"] = {
                "state_history": {
                    "previous_state": current_state,
                    "updated_at": timestamp
                }
            }
        
        result = self.users_collection.update_one(
            {"_id": user_id},
            update_operation,
            upsert=True
        )
        return result.modified_count or (1 if result.upserted_id else 0)
    
    def get_user_state(self, user_id: str):
        """Get user state from the user document"""
        user = self.users_collection.find_one(
            {"_id": user_id},
            {"state": 1}
        )
        return user.get("state", {}) if user else {}
    
    def get_or_create_user_state(self, user_id: str, default_state: dict = None):
        """Get user state or create it if it doesn't exist"""
        if default_state is None:
            default_state = {"initialized": True}
        
        user = self.users_collection.find_one({"_id": user_id}, {"state": 1})
        
        if not user or "state" not in user:
            self.update_user_state(user_id, default_state)
            return default_state
        
        return user.get("state", {})
    
    # === THINGS ABOUT USER ===
    def set_user_things(self, user_id: str, things: dict):
        """Set things about user"""
        timestamp = {"$date": datetime.now().isoformat()}
        
        result = self.users_collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "things_about_user": things,
                    "things_about_user.updated_at": timestamp
                }
            },
            upsert=True
        )
        return result.modified_count or (1 if result.upserted_id else 0)
    
    def get_user_things(self, user_id: str):
        """Get things about user"""
        user = self.users_collection.find_one(
            {"_id": user_id},
            {"things_about_user": 1}
        )
        return user.get("things_about_user", {}) if user else {}
    
    def update_user_things(self, user_id: str, things_to_update: dict):
        """Update specific things about user"""
        timestamp = {"$date": datetime.now().isoformat()}
        prefixed_things = {}
        for key, value in things_to_update.items():
            prefixed_things[f"things_about_user.{key}"] = value
        prefixed_things["things_about_user.updated_at"] = timestamp
        
        result = self.users_collection.update_one(
            {"_id": user_id},
            {"$set": prefixed_things},
            upsert=True
        )
        return result.modified_count or (1 if result.upserted_id else 0)
    
    def remove_user_things(self, user_id: str, keys: List[str]):
        """Remove specific things about user"""
        prefixed_keys = {}
        for key in keys:
            prefixed_keys[f"things_about_user.{key}"] = ""
        
        result = self.users_collection.update_one(
            {"_id": user_id},
            {"$unset": prefixed_keys}
        )
        return result.modified_count
    
    # === CHAT HISTORY ===
    def create_conversation(self, user_id: str, metadata: dict = None):
        """Create a new conversation for a user"""
        conversation_id = f"conv_{int(datetime.now().timestamp())}"
        timestamp = {"$date": datetime.now().isoformat()} 
        if metadata is None:
            metadata = {}    
        result = self.users_collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    f"chat_history.{conversation_id}": {
                        "messages": [],
                        "metadata": metadata,
                        "created_at": timestamp,
                        "updated_at": timestamp
                    }
                }
            },
            upsert=True
        )    
        return conversation_id if (result.modified_count > 0 or result.upserted_id) else None
    
    def add_message(self, user_id: str, conversation_id: str, message: dict):
        """Add a message to a conversation"""
        if "timestamp" not in message:
            message["timestamp"] = {"$date": datetime.now().isoformat()}
        timestamp = {"$date": datetime.now().isoformat()}
        result = self.users_collection.update_one(
            {"_id": user_id, f"chat_history.{conversation_id}": {"$exists": True}},
            {
                "$push": {
                    f"chat_history.{conversation_id}.messages": message
                },
                "$set": {
                    f"chat_history.{conversation_id}.updated_at": timestamp
                }
            }
        )
        
        if result.modified_count == 0:
            result = self.users_collection.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        f"chat_history.{conversation_id}": {
                            "messages": [message],
                            "metadata": {},
                            "created_at": timestamp,
                            "updated_at": timestamp
                        }
                    }
                },
                upsert=True
            )
        
        return result.modified_count or (1 if result.upserted_id else 0)
    
    def get_conversations(self, user_id: str, limit: int = 10):
        """Get a list of conversations for a user"""
        user = self.users_collection.find_one(
            {"_id": user_id},
            {"chat_history": 1}
        )
        
        if not user or "chat_history" not in user:
            return []
        
        conversations = []
        for conv_id, conv_data in user["chat_history"].items():
            conv_data["conversation_id"] = conv_id
            conversations.append(conv_data)

        conversations.sort(
            key=lambda c: c.get("updated_at", {"$date": "1970-01-01T00:00:00Z"}),
            reverse=True
        )
        
        return conversations[:limit]
    
    def get_conversation(self, user_id: str, conversation_id: str):
        """Get a specific conversation"""
        user = self.users_collection.find_one(
            {"_id": user_id},
            {f"chat_history.{conversation_id}": 1}
        )
        
        if not user or "chat_history" not in user or conversation_id not in user["chat_history"]:
            return None
            
        conversation = user["chat_history"][conversation_id]
        conversation["conversation_id"] = conversation_id
        return conversation
