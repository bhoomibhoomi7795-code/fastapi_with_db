import os
import sys
from sqlalchemy import create_engine, text

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from db import DATABASE_URL

def migrate():
    print(f"Connecting to: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            print("Renaming column user_message to chat_message in table chats...")
            conn.execute(text("ALTER TABLE chats RENAME COLUMN user_message TO chat_message;"))
            conn.commit()
            print("Migration successful!")
        except Exception as e:
            print(f"Migration failed or column already renamed: {e}")

if __name__ == "__main__":
    migrate()
