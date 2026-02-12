from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import Chat
from utils.ai_response import get_completion
from schemas.ai_response_schemas import AIRequest, AIResponse, ChatResponse
from utils.jwt_handler import verify_token

router = APIRouter()

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get response from AI model and store chat in chat_messages."""
    try:
        user_id = int(current_user.get("sub"))
        response = get_completion(request.message, request.system_prompt)
        
        # 1. Store User Message
        user_chat_entry = Chat(
            user_id=user_id,
            role="user",
            content=request.message
        )
        db.add(user_chat_entry)
        
        # 2. Store Assistant Response
        assistant_chat_entry = Chat(
            user_id=user_id,
            role="assistant",
            content=response
        )
        db.add(assistant_chat_entry)
        
        db.commit()
        
        return AIResponse(response=response)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/chats", response_model=List[ChatResponse])
def get_chats(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Retrieve chat history for current user."""
    try:
        user_id = int(current_user.get("sub"))
        chats = db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.timestamp.desc()).all()
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))