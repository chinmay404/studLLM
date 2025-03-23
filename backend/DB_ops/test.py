import time
from main import MongoCRUD
import pprint

# Create pretty printer for better output formatting
pp = pprint.PrettyPrinter(indent=2)
print("🔄 Starting MongoDB CRUD Tests...\n")

try:
    # Initialize MongoDB connection
    mongo = MongoCRUD()
    
    # Test user ID for all operations
    test_user_id = "test_user_" + str(int(time.time()))
    print(f"🧪 Using test user ID: {test_user_id}")
    
    # ========== CREATE OPERATIONS ==========
    print("\n===== CREATE OPERATIONS =====")
    
    # Create user state
    user_state_data = {
        "user_id": test_user_id,
        "name": "Test User",
        "email": "test@example.com",
        "state": {"logged_in": True, "last_active": time.time()},
        "state_history": []
    }
    
    user_id = mongo.create_user_state(user_state_data)
    print(f"✅ Created user state with ID: {user_id}")
    
    # Create chat history
    chat_history_data = {
        "user_id": test_user_id,
        "conversation_id": "conv_" + str(int(time.time())),
        "messages": [
            {"role": "user", "content": "Hello!", "timestamp": time.time()},
            {"role": "assistant", "content": "Hi there! How can I help you?", "timestamp": time.time()}
        ]
    }
    
    chat_id = mongo.create_chat_history(chat_history_data)
    print(f"✅ Created chat history with ID: {chat_id}")
    
    # ========== READ OPERATIONS ==========
    print("\n===== READ OPERATIONS =====")
    
    # Read user state
    user_states = mongo.read_user_state({"user_id": test_user_id})
    print(f"✅ Found {len(user_states)} user state(s):")
    pp.pprint(user_states)
    
    # Read chat history
    chat_histories = mongo.read_chat_history({"user_id": test_user_id})
    print(f"✅ Found {len(chat_histories)} chat history(s):")
    pp.pprint(chat_histories)
    
    # ========== UPDATE OPERATIONS ==========
    print("\n===== UPDATE OPERATIONS =====")
    
    # Update user state
    update_count = mongo.update_user_state(
        {"user_id": test_user_id},
        {"state": {"logged_in": False, "last_active": time.time()}}
    )
    print(f"✅ Updated {update_count} user state(s)")
    
    # Test state history update function
    def update_state(user_id, current_state, updated_by, next_state):
        update_data = {
            "$push": {
                "state_history": {
                    "current": current_state,
                    "updated_by": updated_by,
                    "updated_at": time.time(),
                    "next_state": next_state
                }
            }
        }
        result = mongo.user_state_collection.update_one(
            {"user_id": user_id}, 
            update_data
        )
        return result.modified_count
    
    # Add state history entries
    update_state(test_user_id, "Initial", "System", "Application Started")
    update_state(test_user_id, "Application Started", "LLM", "Form Completed")
    print("✅ Added state history entries")
    
    # Update chat history
    new_message = {
        "role": "user", 
        "content": "Can you help me with my assignment?", 
        "timestamp": time.time()
    }
    
    update_count = mongo.update_chat_history(
        {"user_id": test_user_id},
        {"$push": {"messages": new_message}}
    )
    print(f"✅ Updated {update_count} chat history(s)")
    
    # ========== READ AFTER UPDATE ==========
    print("\n===== READ AFTER UPDATE =====")
    
    # Read updated user state
    updated_user_states = mongo.read_user_state({"user_id": test_user_id})
    print("✅ Updated user state:")
    pp.pprint(updated_user_states)
    
    # Read updated chat history
    updated_chat_histories = mongo.read_chat_history({"user_id": test_user_id})
    print("✅ Updated chat history:")
    pp.pprint(updated_chat_histories)
    
    # ========== DELETE OPERATIONS ==========
    print("\n===== DELETE OPERATIONS =====")
    
    # Delete user state
    delete_user_count = mongo.delete_user_state({"user_id": test_user_id})
    print(f"✅ Deleted {delete_user_count} user state(s)")
    
    # Delete chat history
    delete_chat_count = mongo.delete_chat_history({"user_id": test_user_id})
    print(f"✅ Deleted {delete_chat_count} chat history(s)")
    
    # ========== VERIFY DELETION ==========
    print("\n===== VERIFY DELETION =====")
    
    # Verify user state deletion
    final_user_states = mongo.read_user_state({"user_id": test_user_id})
    print(f"✅ Found {len(final_user_states)} user state(s) after deletion:")
    pp.pprint(final_user_states)
    
    # Verify chat history deletion
    final_chat_histories = mongo.read_chat_history({"user_id": test_user_id})
    print(f"✅ Found {len(final_chat_histories)} chat history(s) after deletion:")
    pp.pprint(final_chat_histories)

except Exception as e:
    print(f"❌ Error during testing: {str(e)}")
    
finally:
    # Close MongoDB connection
    print("\n🔄 Closing MongoDB connection...")
    mongo.close_connection()
    print("✅ Tests completed!")