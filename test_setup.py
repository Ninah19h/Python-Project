from database.connection import init_pool, test_connection, execute_schema, close_all_connections

if __name__ == "__main__":
    print("=== Testing Database Setup ===\n")
    
    init_pool()
    
    if test_connection():
        execute_schema()
    
    close_all_connections()