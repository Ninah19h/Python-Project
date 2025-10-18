from database.connection import init_pool, close_all_connections
from operations.citizen_ops import (
    add_citizen, 
    get_all_citizens, 
    get_citizen_by_id, 
    update_citizen, 
    delete_citizen,
    display_citizens
)

def test_citizens():
    """Test all citizen operations"""
    print("\n" + "="*50)
    print("TESTING CITIZEN OPERATIONS")
    print("="*50)
    
    # Initialize connection pool
    init_pool()
    
    # Test 1: Add citizens
    print("\n1. Adding citizens...")
    citizen1_id = add_citizen("John Doe", "12345678", "0712345678", "john@email.com", "Nairobi")
    citizen2_id = add_citizen("Jane Smith", "87654321", "0787654321", "jane@email.com", "Mombasa")
    citizen3_id = add_citizen("Peter Mwangi", "11223344", "0711223344", None, "Kisumu")
    
    # Test 2: Get all citizens
    print("\n2. Fetching all citizens...")
    all_citizens = get_all_citizens()
    display_citizens(all_citizens)
    
    # Test 3: Get citizen by ID
    print("\n3. Fetching citizen by ID...")
    citizen = get_citizen_by_id(citizen1_id)
    if citizen:
        print(f"Found: {citizen[1]} - {citizen[2]}")
    
    # Test 4: Update citizen
    print("\n4. Updating citizen...")
    update_citizen(citizen2_id, phone_number="0700000000", address="Updated Address")
    
    # Test 5: Display updated citizens
    print("\n5. Displaying updated citizens...")
    all_citizens = get_all_citizens()
    display_citizens(all_citizens)
    
    # Test 6: Delete citizen
    print("\n6. Deleting a citizen...")
    delete_citizen(citizen3_id)
    
    # Test 7: Display final list
    print("\n7. Final citizen list...")
    all_citizens = get_all_citizens()
    display_citizens(all_citizens)
    
    # Close connections
    close_all_connections()
    print("\n" + "="*50)
    print("CITIZEN TESTS COMPLETED!")
    print("="*50)

if __name__ == "__main__":
    test_citizens()