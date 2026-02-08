import os
import sys
import urllib.parse
import pandas as pd
from sqlalchemy import create_engine, text
from src.config import MYSQL_CONFIG, SQLITE_DB_PATH

# 1. Database Connections
def get_mysql_engine():
    password = urllib.parse.quote_plus(MYSQL_CONFIG['password'])
    conn_str = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{password}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"
    return create_engine(conn_str)

def get_sqlite_engine():
    return create_engine(f"sqlite:///{SQLITE_DB_PATH}")

def migrate_data():
    mysql_engine = get_mysql_engine()
    sqlite_engine = get_sqlite_engine()
    
    tables = [
        'aggregated_insurance', 'aggregated_transaction', 'aggregated_user',
        'aggregated_user_device', 'map_insurance', 'map_map', 'map_user',
        'top_insurance', 'top_map', 'top_user'
    ]
    
    print("starting Migration Phase 3...")
    print(f"Source: MySQL ({MYSQL_CONFIG['database']})")
    print(f"Target: SQLite ({SQLITE_DB_PATH})")
    
    try:
        connection = sqlite_engine.connect()
        # Begin transaction for safety involves ignoring constraint errors if we just append?
        # Actually, let's just do table by table.
        connection.close()
    except Exception as e:
        print(f"CRITICAL: Cannot connect to SQLite. {e}")
        sys.exit(1)

    total_tables = len(tables)
    success_count = 0

    for table in tables:
        print(f"\n[Migrating Table: {table}]")
        
        # 1. Read from MySQL
        try:
            df = pd.read_sql(f"SELECT * FROM {table}", mysql_engine)
            rows_mysql = len(df)
            print(f" - Read {rows_mysql} rows from MySQL.")
        except Exception as e:
            print(f" - CRITICAL: Failed to read from MySQL. {e}")
            sys.exit(1)

        # 2. Write to SQLite
        try:
            # We clear the table first to avoid duplicates if re-running
            with sqlite_engine.begin() as conn:
                conn.execute(text(f"DELETE FROM {table}"))
            
            df.to_sql(table, sqlite_engine, if_exists='append', index=False)
            print(f" - Wrote {len(df)} rows to SQLite.")
            
        except Exception as e:
            print(f" - CRITICAL: Failed to write to SQLite. {e}")
            sys.exit(1)
            
        # 3. Verify
        try:
             with sqlite_engine.connect() as conn:
                 result = conn.execute(text(f"SELECT count(*) FROM {table}"))
                 rows_sqlite = result.scalar()
             
             if rows_mysql == rows_sqlite:
                 print(f" - SUCCESS: Row counts match ({rows_mysql}).")
                 success_count += 1
             else:
                 print(f" - FAILURE: Row count mismatch! MySQL: {rows_mysql}, SQLite: {rows_sqlite}")
                 sys.exit(1) # Stop immediately as per instructions
                 
        except Exception as e:
            print(f" - CRITICAL: Verification failed. {e}")
            sys.exit(1)

    print(f"\nMigration Complete. {success_count}/{total_tables} tables migrated successfully.")

if __name__ == "__main__":
    migrate_data()
