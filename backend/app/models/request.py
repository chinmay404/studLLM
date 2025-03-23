from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str
    user_id: str = Field(..., title="User ID", description="Unique identifier for the user")
    thread_id: str = Field(..., title="Thread ID", description="Unique identifier for the thread")
    