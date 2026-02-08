import os

# Database Configuration
# Database Configuration
DB_TYPE = os.getenv('DB_TYPE', 'sqlite') # Options: 'sqlite', 'mysql'

# MySQL Config (Legacy/Migration Source)
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Rakesh@181969',
    'database': 'phonepe'
}

# SQLite Config (New Target)
SQLITE_DB_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')), 'phonepe.db')

# For backward compatibility during migration scripts
DB_CONFIG = MYSQL_CONFIG

# Data Directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
