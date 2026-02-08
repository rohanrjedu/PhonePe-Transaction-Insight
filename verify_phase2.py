import os
import sys
from sqlalchemy import create_engine, inspect

# Force SQLite
os.environ['DB_TYPE'] = 'sqlite'

try:
    from src.db import initialize_database, get_engine
    from src.config import SQLITE_DB_PATH
except ImportError:
    # Fix python path if running from root
    sys.path.append(os.getcwd())
    from src.db import initialize_database, get_engine
    from src.config import SQLITE_DB_PATH

def verify_phase2():
    print(f"Target DB Path: {SQLITE_DB_PATH}")
    
    # 1. Initialize
    print("Initializing Database...")
    initialize_database()
    
    # 2. Check File
    if os.path.exists(SQLITE_DB_PATH):
        print("PASS: Database file created.")
    else:
        print("FAIL: Database file not found.")
        return

    # 3. Check Tables
    engine = get_engine()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    expected_tables = [
        'aggregated_insurance', 'aggregated_transaction', 'aggregated_user',
        'aggregated_user_device', 'map_insurance', 'map_map', 'map_user',
        'top_insurance', 'top_map', 'top_user'
    ]
    
    missing = [t for t in expected_tables if t not in tables]
    
    if not missing:
        print(f"PASS: All {len(expected_tables)} tables created.")
        for t in tables:
            print(f" - {t}")
    else:
        print(f"FAIL: Missing tables: {missing}")

if __name__ == "__main__":
    verify_phase2()
