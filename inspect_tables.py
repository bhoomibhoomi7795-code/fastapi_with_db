import os
import sys
from sqlalchemy import create_engine, inspect

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from db import DATABASE_URL

def list_tables():
    print(f"Inspecting database: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    
    tables = inspector.get_table_names()
    print(f"\nTables found: {tables}")
    
    for table in tables:
        print(f"\nTable: {table}")
        columns = inspector.get_columns(table)
        for col in columns:
            print(f"  - {col['name']} ({col['type']})")

if __name__ == "__main__":
    list_tables()
