from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import Chat
from utils.ai_response import get_completion
from schemas.ai_response_schemas import AIRequest, AIResponse, ChatResponse
from utils.jwt_handler import verify_token

router = APIRouter()

@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, db: Session = Depends(get_db)):
    """Get response from AI model and store chat in chat_messages."""
    try:
        response = get_completion(request.message, request.system_prompt)
        
        # 1. Store User Message
        user_chat_entry = Chat(
            role="user",
            content=request.message
        )
        db.add(user_chat_entry)
        
        # 2. Store Assistant Response
        assistant_chat_entry = Chat(
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
def get_chats(db: Session = Depends(get_db)):
    """Retrieve chat history for current user."""
    try:
        chats = db.query(Chat).order_by(Chat.timestamp.desc()).all()
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))