import os
from pymongo import MongoClient

class MongoCRUD:
    def __init__(self):
        uri = "mongodb://localhost:27017/"
        db_name = "user"
        
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.user_state_collection = self.db["user_state"]
        self.chat_history_collection = self.db["chat_history"]
    
    def create_user_state(self, data: dict):
        """Insert a new document into the user_state collection"""
        result = self.user_state_collection.insert_one(data)
        return str(result.inserted_id)
    
    def read_user_state(self, query: dict = {}):
        """Read documents from the user_state collection"""
        return list(self.user_state_collection.find(query))
    
    def update_user_state(self, query: dict, new_values: dict):
        """Update documents in the user_state collection"""
        result = self.user_state_collection.update_many(query, {"$set": new_values})
        return result.modified_count
    
    def delete_user_state(self, query: dict):
        """Delete documents from the user_state collection"""
        result = self.user_state_collection.delete_many(query)
        return result.deleted_count
    
    def create_chat_history(self, data: dict):
        """Insert a new document into the chat_history collection"""
        result = self.chat_history_collection.insert_one(data)
        return str(result.inserted_id)
    
    def read_chat_history(self, query: dict = {}):
        """Read documents from the chat_history collection"""
        return list(self.chat_history_collection.find(query))
    
    def update_chat_history(self, query: dict, new_values: dict):
        """Update documents in the chat_history collection"""
        result = self.chat_history_collection.update_many(query, {"$set": new_values})
        return result.modified_count
    
    def delete_chat_history(self, query: dict):
        """Delete documents from the chat_history collection"""
        result = self.chat_history_collection.delete_many(query)
        return result.deleted_count
    
    def close_connection(self):
        """Close the MongoDB connection"""
        self.client.close()
