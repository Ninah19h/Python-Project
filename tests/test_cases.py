from database.connection import init_pool, close_all_connections
from operations.citizen_ops import add_citizen
from operations.officer_ops import add_officer
from operations.case_ops import (
    add_case,
    get_all_cases,
    get_case_by_id,
    get_cases_by_status,
    get_cases_by_location,
    get_cases_by_crime_type,
    assign_officer_to_case,
    update_case_status,
    delete_case,
    display_cases
)
from operations.case_update_ops import (
    add_case_update,
    get_updates_by_case,
    display_case_updates
)

def test_cases():
    """Test all case and case update operations"""
    print("\n" + "="*50)
    print("TESTING CASE OPERATIONS")
    print("="*50)
    
    # Initialize connection pool
    init_pool()
    
    # Setup: Add test citizen and officer
    print("\n0. Setting up test data...")
    citizen_id = add_citizen("Test Citizen", "99999999", "0799999999", "test@email.com", "Nairobi")
    officer_id = add_officer("Test Officer", "TEST001", "Detective", "0788888888", "Test Station")
    
    # Test 1: Add cases
    print("\n1. Adding cases...")
    case1_id = add_case(citizen_id, "Theft", "Phone stolen at bus stop", "Nairobi CBD")
    case2_id = add_case(citizen_id, "Assault", "Physical attack", "Westlands", officer_id)
    case3_id = add_case(citizen_id, "Burglary", "House broken into", "Karen")
    
    # Test 2: Get all cases
    print("\n2. Fetching all cases...")
    all_cases = get_all_cases()
    display_cases(all_cases)
    
    # Test 3: Get case by ID
    print("\n3. Fetching case by ID...")
    case = get_case_by_id(case1_id)
    if case:
        print(f"Case ID: {case[0]} - Type: {case[3]} - Status: {case[6]}")
    
    # Test 4: Filter by status
    print("\n4. Filtering by status (Pending)...")
    pending_cases = get_cases_by_status("Pending")
    display_cases(pending_cases)
    
    # Test 5: Filter by location
    print("\n5. Filtering by location (Nairobi)...")
    nairobi_cases = get_cases_by_location("Nairobi")
    display_cases(nairobi_cases)
    
    # Test 6: Filter by crime type
    print("\n6. Filtering by crime type (Theft)...")
    theft_cases = get_cases_by_crime_type("Theft")
    display_cases(theft_cases)
    
    # Test 7: Assign officer to case
    print("\n7. Assigning officer to case...")
    assign_officer_to_case(case1_id, officer_id)
    
    # Test 8: Update case status
    print("\n8. Updating case status...")
    update_case_status(case2_id, "Under Investigation")
    
    # Test 9: Add case updates
    print("\n9. Adding case updates...")
    add_case_update(case1_id, officer_id, "Started investigation, collecting evidence")
    add_case_update(case1_id, officer_id, "Witness interviewed, suspect identified")
    add_case_update(case2_id, officer_id, "Victim statement recorded")
    
    # Test 10: Get case updates
    print("\n10. Fetching case updates...")
    updates = get_updates_by_case(case1_id)
    display_case_updates(updates)
    
    # Test 11: Display final cases
    print("\n11. Final case list...")
    all_cases = get_all_cases()
    display_cases(all_cases)
    
    # Test 12: Delete a case
    print("\n12. Deleting a case...")
    delete_case(case3_id)
    
    # Close connections
    close_all_connections()
    print("\n" + "="*50)
    print("CASE TESTS COMPLETED!")
    print("="*50)

if __name__ == "__main__":
    test_cases()