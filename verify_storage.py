import os
import sys
from unittest.mock import patch

# Add the current directory to sys.path so we can import modules
sys.path.append(os.getcwd())

from models import Chat
from routes.ai_response_routes import ask_ai, get_chats
from schemas.ai_response_schemas import AIRequest
from db import SessionLocal

def test_chat_flow():
    print("Testing chat flow (Store -> Retrieve)...")
    
    test_message = "Flow Test Message " + str(os.urandom(4).hex())
    mock_response_content = "Flow Mock Response " + str(os.urandom(4).hex())
    
    # Mock the get_completion function
    with patch('routes.ai_response_routes.get_completion') as mock_get:
        mock_get.return_value = mock_response_content
        
        request = AIRequest(message=test_message, system_prompt="sys")
        
        # Create a real DB session
        db = SessionLocal()
        
        try:
            # 1. Store Chat
            print(f"1. Calling ask_ai with message: {test_message}")
            response = ask_ai(request, db=db)
            print(f"   Stored response: {response.response}")
            
            # 2. Retrieve Chat
            print(f"2. Calling get_chats...")
            chats = get_chats(db=db)
            print(f"   Retrieved {len(chats)} chats.")
            
            # 3. Verify
            found = False
            for chat in chats:
                if chat.user_message == test_message:
                    print(f"   SUCCESS: Found message in retrieved list!")
                    print(f"   ID: {chat.id}, Response: {chat.ai_response}")
                    found = True
                    break
            
            if not found:
                print("   FAILED: Message not found in retrieved list.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    test_chat_flow()
