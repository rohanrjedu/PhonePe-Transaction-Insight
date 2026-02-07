import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
from src.config import DB_CONFIG

def get_engine():
    """
    Creates and returns a SQLAlchemy engine for MySQL connection.
    """
    password = urllib.parse.quote_plus(DB_CONFIG['password'])
    conn_str = f"mysql+pymysql://{DB_CONFIG['user']}:{password}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    return create_engine(conn_str)

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
