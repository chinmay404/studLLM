import time
from main import MongoCRUD  # Import your class

mongo = MongoCRUD()

# user_state_data = {
#     "user_id": "123",
#     "state": {"logged_in": True, "last_active": time.time()}
# }
# chat_history_data = {
#     "user_id": "123",
#     "messages": [{"text": "Hello!", "timestamp": time.time()}]
# }

# user_id = mongo.create_user_state(user_state_data)
# chat_id = mongo.create_chat_history(chat_history_data)
# print(f"Inserted User State ID: {user_id}")
# print(f"Inserted Chat History ID: {chat_id}")


# print("\n🔍 Current User State (Before Update):")
# user_states = mongo.read_user_state({"user_id": "123"})
# print(user_states)

# print("\n🔍 Current Chat History (Before Update):")
# chat_histories = mongo.read_chat_history({"user_id": "123"})
# print(chat_histories)


# mongo.update_user_state({"user_id": "123"}, {"state": {"logged_in": False, "last_active": time.time()}})
# mongo.update_chat_history({"user_id": "123"}, {"messages": [{"text": "Updated!", "timestamp": time.time()}]})


# print("\n🔍 Updated User State:")
# updated_user_states = mongo.read_user_state({"user_id": "123"})
# print(updated_user_states)

# print("\n🔍 Updated Chat History:")
# updated_chat_histories = mongo.read_chat_history({"user_id": "123"})
# print(updated_chat_histories)

# delete_user_count = mongo.delete_user_state({"user_id": "123"})
# delete_chat_count = mongo.delete_chat_history({"user_id": "123"})
# print(f"\n🗑 Deleted User State Count: {delete_user_count}")
# print(f"🗑 Deleted Chat History Count: {delete_chat_count}")

# print("\n🔍 Final User State (After Delete):")
final_user_states = mongo.read_user_state({"user_id": "123"})
print(final_user_states)

# print("\n🔍 Final Chat History (After Delete):")
# final_chat_histories = mongo.read_chat_history({"user_id": "123"})
# print(final_chat_histories)

# user_id = "123"
# user_chats = mongo.read_chat_history({"user_id": user_id})

# print(f"\n🔍 All Chats for User {user_id}:")
# for chat in user_chats:
#     print(chat)
def update_state(user_id: str,
                 current_state: str, 
                 updated_by: str, 
                 next_state: str) -> int | None:
    """Append a new state update to a user's state history.

    Args:
        user_id (str): The user ID whose state needs to be updated.
        current_state (str): The current state of the user.
        updated_by (str): The entity that updated the state (e.g., "LLM").
        next_state (str): The next state of the user.

    Returns:
        int: The number of documents updated (should be 1 if successful, 0 if no user found).
    """
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
        update_data,
        upsert=True  
    )
    
    return result.modified_count if result.modified_count else None
print(update_state("123", "Done With Visa", "LLM", "Book Flight Ticket"))
update_state("123", "Book Flight Ticket", "LLM", "Do Packing")
update_state("123", "Do Packing", "LLM", "Departure")
update_state("123", "Departure", "LLM", "Arrival")
update_state("123", "Arrival", "LLM", "Landed Germnay")

mongo.close_connection()
