
# Auto-generated schema definitions from MySQL dump

SCHEMA_DEFINITIONS = [
    """CREATE TABLE IF NOT EXISTS aggregated_insurance (
        state TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        insurance_type TEXT,
        insurance_count INTEGER DEFAULT NULL,
        insurance_amount REAL DEFAULT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS aggregated_transaction (
        state TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        transaction_type TEXT,
        transaction_count INTEGER DEFAULT NULL,
        transaction_amount REAL DEFAULT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS aggregated_user (
        state TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        registered_users INTEGER DEFAULT NULL,
        app_opens INTEGER DEFAULT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS aggregated_user_device (
        state TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        brand TEXT,
        count INTEGER DEFAULT NULL,
        percentage REAL DEFAULT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS map_insurance (
        state TEXT,
        district TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        insurance_count INTEGER DEFAULT NULL,
        insurance_amount REAL DEFAULT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS map_map (
        state TEXT,
        district TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        total_transactions INTEGER DEFAULT NULL,
        total_amount REAL DEFAULT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS map_user (
        state TEXT,
        district TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        registered_users INTEGER DEFAULT NULL,
        app_opens INTEGER DEFAULT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS top_insurance (
        state TEXT,
        entity_name TEXT,
        entity_type TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        insurance_count INTEGER DEFAULT NULL,
        insurance_amount REAL DEFAULT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS top_map (
        state TEXT,
        entity_name TEXT,
        entity_type TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        count INTEGER DEFAULT NULL,
        amount REAL DEFAULT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS top_user (
        state TEXT,
        entity_name TEXT,
        entity_type TEXT,
        year INTEGER DEFAULT NULL,
        quarter INTEGER DEFAULT NULL,
        registered_users INTEGER DEFAULT NULL
    );"""
]
