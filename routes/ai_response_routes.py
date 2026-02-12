from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Chat
from utils.ai_response import get_completion
from schemas.ai_response_schemas import AIRequest, AIResponse

router = APIRouter()


@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, db: Session = Depends(get_db)):
    """Get response from AI model and store chat."""
    try:
        response = get_completion(request.message, request.system_prompt)
        
        # Store in DB
        chat_entry = Chat(
            user_message=request.message,
            ai_response=response
        )
        db.add(chat_entry)
        db.commit()
        db.refresh(chat_entry)
        
        return AIResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/chats")
def get_chats(db: Session = Depends(get_db)):
    """Retrieve chat history."""
    try:
        chats = db.query(Chat).order_by(Chat.timestamp.desc()).all()
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
        