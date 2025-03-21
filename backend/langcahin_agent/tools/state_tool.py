from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import time
import yaml
import sys
sys.path.append("..")
from DB_ops.main import MongoCRUD

db = MongoCRUD()


@tool
def update_state(user_id: str,
                current_state: str, 
                updated_by: str, 
                next_state: str) -> int | None:
    """Update the state of a user.

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
            "state": {
                "current": current_state,
                "updated_by": "LLM",
                "updated_at": time.time(),
                "next_state": next_state
            }
        }
    }

    result = db.update_user_state({"user_id": user_id}, update_data ,upsert=True)
    return result if result else None


@tool
def get_user_state(user_id :str) -> dict | None:
    """Retrieve the current state of a user.

    Args:
        user_id (str): The user ID to fetch the state for.

    Returns:
        dict: The state of the user if found, otherwise None.
    """
    user_data = db.read_user_state({"user_id": user_id})

    if user_data:
        return user_data[0].get("state", {})
    return None




def get_user_state_(user_id :str) -> dict | None:
    """Retrieve the current state of a user.

    Args:
        user_id (str): The user ID to fetch the state for.

    Returns:
        dict: The state of the user if found, otherwise None.
    """
    user_data = db.read_user_state({"user_id": user_id})
    print("user_data : ", user_data)    
    if user_data:
        return user_data[0].get("state_history", [])
    return None