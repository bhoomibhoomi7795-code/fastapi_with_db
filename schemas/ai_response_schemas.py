from pydantic import BaseModel
from datetime import datetime

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."

class AIResponse(BaseModel):
    response: str

class ChatResponse(BaseModel):
    id: int
    user_id: int
    role: str
    content: str
    timestamp: datetime



    class Config:
        from_attributes = True
