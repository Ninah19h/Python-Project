import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'crime_reporting_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
    'port': os.getenv('DB_PORT', '5432')
}

# Connection pool
connection_pool = None

def init_pool():
    """Initialize connection pool"""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20, **DB_CONFIG)
        if connection_pool:
            print("✓ Database connection pool created successfully")
    except Exception as e:
        print(f"✗ Error creating connection pool: {e}")

def get_connection():
    """Get a connection from the pool"""
    try:
        if connection_pool:
            return connection_pool.getconn()
    except Exception as e:
        print(f"✗ Error getting connection: {e}")
        return None

def release_connection(conn):
    """Return connection to the pool"""
    try:
        if connection_pool and conn:
            connection_pool.putconn(conn)
    except Exception as e:
        print(f"✗ Error releasing connection: {e}")

def close_all_connections():
    """Close all connections"""
    try:
        if connection_pool:
            connection_pool.closeall()
            print("✓ All database connections closed")
    except Exception as e:
        print(f"✗ Error closing connections: {e}")

def test_connection():
    """Test database connection"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT version();")
            db_version = cur.fetchone()
            print(f"✓ Connected to PostgreSQL: {db_version[0]}")
            cur.close()
            release_connection(conn)
            return True
        except Exception as e:
            print(f"✗ Connection test failed: {e}")
            if conn:
                release_connection(conn)
            return False
    return False

def execute_schema():
    """Execute schema.sql to create tables"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            with open('database/schema.sql', 'r') as f:
                schema = f.read()
            cur.execute(schema)
            conn.commit()
            print("✓ Database schema created successfully")
            cur.close()
            release_connection(conn)
            return True
        except Exception as e:
            print(f"✗ Error creating schema: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return False
    return False