import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the current directory to sys.path so we can import modules
sys.path.append(os.getcwd())

from models import Chat, Base
from db import DATABASE_URL

def dump_db():
    print(f"Connecting to: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        chats = session.query(Chat).order_by(Chat.timestamp.desc()).limit(20).all()
        print(f"\nFound {len(chats)} recent records in chat_messages:")
        print("-" * 50)
        for chat in chats:
            print(f"ID: {chat.id}")
            print(f"User ID: {chat.user_id}")
            print(f"Role: [{chat.role}]")
            print(f"Content: [{chat.content[:100]}...]")
            print(f"Timestamp: {chat.timestamp}")
            print("-" * 50)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    dump_db()
