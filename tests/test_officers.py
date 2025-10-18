from database.connection import init_pool, close_all_connections
from operations.officer_ops import (
    add_officer,
    get_all_officers,
    get_officer_by_id,
    update_officer,
    delete_officer,
    display_officers
)

def test_officers():
    """Test all officer operations"""
    print("\n" + "="*50)
    print("TESTING OFFICER OPERATIONS")
    print("="*50)
    
    # Initialize connection pool
    init_pool()
    
    # Test 1: Add officers
    print("\n1. Adding officers...")
    officer1_id = add_officer("Inspector James", "BADGE001", "Inspector", "0722111111", "Central Police Station")
    officer2_id = add_officer("Sergeant Mary", "BADGE002", "Sergeant", "0733222222", "Westlands Station")
    officer3_id = add_officer("Corporal David", "BADGE003", "Corporal", "0744333333", "Kilimani Station")
    
    # Test 2: Get all officers
    print("\n2. Fetching all officers...")
    all_officers = get_all_officers()
    display_officers(all_officers)
    
    # Test 3: Get officer by ID
    print("\n3. Fetching officer by ID...")
    officer = get_officer_by_id(officer1_id)
    if officer:
        print(f"Found: {officer[1]} - Badge: {officer[2]}")
    
    # Test 4: Update officer
    print("\n4. Updating officer...")
    update_officer(officer2_id, rank="Senior Sergeant", station="New Station")
    
    # Test 5: Display updated officers
    print("\n5. Displaying updated officers...")
    all_officers = get_all_officers()
    display_officers(all_officers)
    
    # Test 6: Delete officer
    print("\n6. Deleting an officer...")
    delete_officer(officer3_id)
    
    # Test 7: Display final list
    print("\n7. Final officer list...")
    all_officers = get_all_officers()
    display_officers(all_officers)
    
    # Close connections
    close_all_connections()
    print("\n" + "="*50)
    print("OFFICER TESTS COMPLETED!")
    print("="*50)

if __name__ == "__main__":
    test_officers()