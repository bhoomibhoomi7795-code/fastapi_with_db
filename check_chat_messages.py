import os
import sys
from sqlalchemy import create_engine, text

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from db import DATABASE_URL

def check_chat_messages():
    print(f"Checking table: chat_messages at {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            result = conn.execute(text("SELECT * FROM chat_messages LIMIT 5;"))
            rows = result.fetchall()
            print(f"\nFound {len(rows)} rows in chat_messages:")
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_chat_messages()
