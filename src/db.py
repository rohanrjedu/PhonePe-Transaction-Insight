import os
import pandas as pd
from sqlalchemy import create_engine, text
import urllib.parse
from src.config import DB_CONFIG, DB_TYPE, SQLITE_DB_PATH, MYSQL_CONFIG
try:
    from src.schema import SCHEMA_DEFINITIONS
except ImportError:
    SCHEMA_DEFINITIONS = []

def get_engine():
    """
    Creates and returns a SQLAlchemy engine based on DB_TYPE.
    """
    if DB_TYPE == 'sqlite':
        # Ensure the directory exists
        os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
        return create_engine(f"sqlite:///{SQLITE_DB_PATH}")
    
    # Legacy MySQL Support
    password = urllib.parse.quote_plus(MYSQL_CONFIG['password'])
    conn_str = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{password}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"
    return create_engine(conn_str)

def initialize_database():
    """
    Initializes the database schema if proper tables are missing.
    Safe to run multiple times (idempotent).
    """
    if DB_TYPE != 'sqlite':
        return # Skip for MySQL to avoid altering legacy DB during audit/migration

    engine = get_engine()
    try:
        with engine.connect() as conn:
            for query in SCHEMA_DEFINITIONS:
                conn.execute(text(query))
            # SQLite doesn't strictly need commit for DDL, but good practice
            pass
    except Exception as e:
        print(f"Database Initialization Error: {e}")

def execute_query(query):
    """
    Executes a read query and returns the results as a pandas DataFrame.
    """
    engine = get_engine()
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        # Silent fail or log as needed
        print(f"Database Query Error: {e}")
        return pd.DataFrame()
