from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import time
from datetime import datetime
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
        int: 1 if successful, 0 if failed.
    """
    existing_state = db.get_user_state(user_id)
    
    timestamp = {"$date": datetime.now().isoformat()}
    new_state = {
        "current": next_state,
        "previous": current_state,
        "updated_by": updated_by,
        "updated_at": timestamp
    }
    
    result = db.update_user_state(user_id, new_state)
    return result


@tool
def get_user_state(user_id: str) -> dict | None:
    """Retrieve the current state of a user.

    Args:
        user_id (str): The user ID to fetch the state for.

    Returns:
        dict: The state of the user if found, otherwise None.
    """
    state = db.get_user_state(user_id)
    return state if state else None


@tool
def get_user_state_history(user_id: str) -> list | None:
    """Retrieve the state history of a user.

    Args:
        user_id (str): The user ID to fetch the state history for.

    Returns:
        list: The state history of the user if found, otherwise None.
    """
    user = db.get_user(user_id)
    if user and "state_history" in user:
        return user["state_history"]
    return None


@tool
def create_initial_state(user_id: str, initial_state: str) -> int | None:
    """Create an initial state for a user if none exists.

    Args:
        user_id (str): The user ID to create initial state for.
        initial_state (str): The initial state to set.

    Returns:
        int: 1 if successful, 0 if failed.
    """
    timestamp = {"$date": datetime.now().isoformat()}
    state_data = {
        "current": initial_state,
        "updated_by": "System",
        "updated_at": timestamp
    }
    
    # This will create a state if it doesn't exist
    result = db.get_or_create_user_state(user_id, state_data)
    return 1 if result else 0