import os
from operations.citizen_ops import (
    add_citizen, get_all_citizens, get_citizen_by_id, 
    update_citizen, delete_citizen, display_citizens
)
from operations.officer_ops import (
    add_officer, get_all_officers, get_officer_by_id,
    update_officer, delete_officer, display_officers
)
from operations.case_ops import (
    add_case, get_all_cases, get_case_by_id,
    get_cases_by_status, get_cases_by_location, get_cases_by_crime_type,
    assign_officer_to_case, update_case_status, delete_case, display_cases
)
from operations.case_update_ops import (
    add_case_update, get_updates_by_case, display_case_updates
)

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def pause():
    """Pause and wait for user to press Enter"""
    input("\nPress Enter to continue...")

def main_menu():
    """Display main menu"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*15 + "CRIME REPORTING & TRACKING SYSTEM")
    print("="*60)
    print("\n1. Citizen Portal")
    print("2. Officer Portal")
    print("3. View All Cases")
    print("4. Exit")
    print("\n" + "="*60)
    
    choice = input("\nEnter your choice (1-4): ").strip()
    return choice

# ==================== CITIZEN PORTAL ====================

def citizen_menu():
    """Citizen portal menu"""
    while True:
        clear_screen()
        print("\n" + "="*60)
        print(" "*20 + "CITIZEN PORTAL")
        print("="*60)
        print("\n1. Register as New Citizen")
        print("2. Report a Crime")
        print("3. View My Cases")
        print("4. Update My Information")
        print("5. View All Citizens")
        print("6. Back to Main Menu")
        print("\n" + "="*60)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            register_citizen()
        elif choice == '2':
            report_crime()
        elif choice == '3':
            view_citizen_cases()
        elif choice == '4':
            update_citizen_info()
        elif choice == '5':
            view_all_citizens()
        elif choice == '6':
            break
        else:
            print("❌ Invalid choice! Please try again.")
            pause()

def register_citizen():
    """Register a new citizen"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "CITIZEN REGISTRATION")
    print("="*60)
    
    full_name = input("\nEnter full name: ").strip()
    phone_number = input("Enter phone number: ").strip()
    email = input("Enter email (optional, press Enter to skip): ").strip() or None
    address = input("Enter address (optional, press Enter to skip): ").strip() or None
    
    if not (full_name and phone_number):
        print("\n❌ Error: Full name and phone number are required!")
        pause()
        return
    
    citizen_id = add_citizen(full_name, phone_number, email, address)
    if citizen_id:
        print(f"\n✅ Registration successful! Your Citizen ID is: {citizen_id}")
        print("Please remember this ID for future reference.")
    
    pause()

def report_crime():
    """Report a new crime"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*20 + "REPORT A CRIME")
    print("="*60)
    
    citizen_id = input("\nEnter your Citizen ID: ").strip()
    
    # Verify citizen exists
    citizen = get_citizen_by_id(citizen_id)
    if not citizen:
        print(f"\n❌ Error: Citizen ID {citizen_id} not found!")
        print("Please register first if you haven't already.")
        pause()
        return
    
    print(f"\nWelcome, {citizen[1]}!")
    print("\nCrime Types: Theft, Assault, Burglary, Robbery, Vandalism, Fraud, etc.")
    crime_type = input("Enter type of crime: ").strip()
    description = input("Enter detailed description of the incident: ").strip()
    location = input("Enter location where crime occurred: ").strip()
    
    if crime_type and description and location:
        case_id = add_case(citizen_id, crime_type, description, location)
        if case_id:
            print(f"\n✅ Crime reported successfully!")
            print(f"Your Case ID is: {case_id}")
            print("An officer will be assigned to your case soon.")
    else:
        print("\n❌ Error: All fields are required!")
    
    pause()

def view_citizen_cases():
    """View cases reported by a citizen"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*22 + "MY CASES")
    print("="*60)
    
    citizen_id = input("\nEnter your Citizen ID: ").strip()
    
    # Get all cases and filter by citizen
    all_cases = get_all_cases()
    # Filter cases where the citizen_id matches (checking the correct index)
    citizen_cases = []
    for case in all_cases:
        # In get_all_cases, citizen_id is not directly in the result
        # We need to modify the query or get it differently
        # For now, let's get it properly
        case_detail = get_case_by_id(case[0])
        if case_detail and str(case_detail[1]) == citizen_id:
            citizen_cases.append(case)
    
    if citizen_cases:
        display_cases(citizen_cases)
    else:
        print("\n📭 No cases found for this citizen ID.")
    
    pause()

def update_citizen_info():
    """Update citizen information"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*16 + "UPDATE CITIZEN INFORMATION")
    print("="*60)
    
    citizen_id = input("\nEnter your Citizen ID: ").strip()
    
    # Verify citizen exists
    citizen = get_citizen_by_id(citizen_id)
    if not citizen:
        print(f"\n❌ Error: Citizen ID {citizen_id} not found!")
        pause()
        return
    
    print(f"\nCurrent information for: {citizen[1]}")
    print(f"Phone: {citizen[2]}")
    print(f"Email: {citizen[3] or 'Not provided'}")
    print(f"Address: {citizen[4] or 'Not provided'}")
    
    print("\n--- Enter new information (press Enter to keep current) ---")
    full_name = input("New full name: ").strip() or None
    phone_number = input("New phone number: ").strip() or None
    email = input("New email: ").strip() or None
    address = input("New address: ").strip() or None
    
    if update_citizen(citizen_id, full_name, phone_number, email, address):
        print("\n✅ Information updated successfully!")
    else:
        print("\n❌ No changes made.")
    
    pause()

def view_all_citizens():
    """View all registered citizens"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "ALL REGISTERED CITIZENS")
    print("="*60)
    
    citizens = get_all_citizens()
    display_citizens(citizens)
    pause()

# ==================== OFFICER PORTAL ====================

def officer_menu():
    """Officer portal menu"""
    while True:
        clear_screen()
        print("\n" + "="*60)
        print(" "*20 + "OFFICER PORTAL")
        print("="*60)
        print("\n1. Register as New Officer")
        print("2. View All Cases")
        print("3. View Cases by Status")
        print("4. View Cases by Location")
        print("5. View Cases by Crime Type")
        print("6. Assign Officer to Case")
        print("7. Update Case Status")
        print("8. Add Case Update/Note")
        print("9. View Case Updates")
        print("10. View All Officers")
        print("11. Back to Main Menu")
        print("\n" + "="*60)
        
        choice = input("\nEnter your choice (1-11): ").strip()
        
        if choice == '1':
            register_officer()
        elif choice == '2':
            view_all_cases_officer()
        elif choice == '3':
            filter_cases_by_status()
        elif choice == '4':
            filter_cases_by_location()
        elif choice == '5':
            filter_cases_by_crime_type()
        elif choice == '6':
            assign_officer()
        elif choice == '7':
            update_status()
        elif choice == '8':
            add_update()
        elif choice == '9':
            view_case_updates()
        elif choice == '10':
            view_all_officers()
        elif choice == '11':
            break
        else:
            print("❌ Invalid choice! Please try again.")
            pause()

def register_officer():
    """Register a new officer"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "OFFICER REGISTRATION")
    print("="*60)
    
    full_name = input("\nEnter full name: ").strip()
    badge_number = input("Enter badge number: ").strip()
    rank = input("Enter rank (e.g., Officer, Sergeant, Inspector): ").strip()
    phone_number = input("Enter phone number: ").strip()
    station = input("Enter police station (optional, press Enter to skip): ").strip() or None
    
    if full_name and badge_number and rank and phone_number:
        officer_id = add_officer(full_name, badge_number, rank, phone_number, station)
        if officer_id:
            print(f"\n✅ Registration successful! Your Officer ID is: {officer_id}")
    else:
        print("\n❌ Error: All required fields must be filled!")
    
    pause()

def view_all_cases_officer():
    """View all cases"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*22 + "ALL CASES")
    print("="*60)
    
    cases = get_all_cases()
    display_cases(cases)
    pause()

def filter_cases_by_status():
    """Filter cases by status"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "FILTER CASES BY STATUS")
    print("="*60)
    
    print("\nAvailable statuses:")
    print("1. Pending")
    print("2. Under Investigation")
    print("3. Resolved")
    print("4. Closed")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    # Map choice to actual status
    status_map = {
        '1': 'Pending',
        '2': 'Under Investigation',
        '3': 'Resolved',
        '4': 'Closed'
    }
    
    if choice not in status_map:
        print("\n❌ Invalid choice!")
        pause()
        return
    
    status = status_map[choice]
    print(f"\nSearching for cases with status: {status}")
    
    cases = get_cases_by_status(status)
    display_cases(cases)
    pause()

def filter_cases_by_location():
    """Filter cases by location"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "FILTER CASES BY LOCATION")
    print("="*60)
    
    location = input("\nEnter location to search: ").strip()
    
    cases = get_cases_by_location(location)
    display_cases(cases)
    pause()

def filter_cases_by_crime_type():
    """Filter cases by crime type"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*16 + "FILTER CASES BY CRIME TYPE")
    print("="*60)
    
    crime_type = input("\nEnter crime type to search: ").strip()
    
    cases = get_cases_by_crime_type(crime_type)
    display_cases(cases)
    pause()

def assign_officer():
    """Assign officer to a case"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "ASSIGN OFFICER TO CASE")
    print("="*60)
    
    case_id = input("\nEnter Case ID: ").strip()
    officer_id = input("Enter Officer ID: ").strip()
    
    if assign_officer_to_case(case_id, officer_id):
        print("\n✅ Officer assigned successfully!")
    else:
        print("\n❌ Failed to assign officer!")
    
    pause()

def update_status():
    """Update case status"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*20 + "UPDATE CASE STATUS")
    print("="*60)
    
    case_id = input("\nEnter Case ID: ").strip()
    
    print("\nAvailable statuses:")
    print("1. Pending")
    print("2. Under Investigation")
    print("3. Resolved")
    print("4. Closed")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    # Map choice to actual status
    status_map = {
        '1': 'Pending',
        '2': 'Under Investigation',
        '3': 'Resolved',
        '4': 'Closed'
    }
    
    if choice not in status_map:
        print("\n❌ Invalid choice!")
        pause()
        return
    
    status = status_map[choice]
    
    if update_case_status(case_id, status):
        print(f"\n✅ Case status updated to '{status}' successfully!")
    else:
        print("\n❌ Failed to update case status!")
    
    pause()

def add_update():
    """Add update note to a case"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*20 + "ADD CASE UPDATE")
    print("="*60)
    
    case_id = input("\nEnter Case ID: ").strip()
    officer_id = input("Enter your Officer ID: ").strip()
    update_note = input("Enter update note: ").strip()
    
    if case_id and officer_id and update_note:
        update_id = add_case_update(case_id, officer_id, update_note)
        if update_id:
            print("\n✅ Case update added successfully!")
    else:
        print("\n❌ All fields are required!")
    
    pause()

def view_case_updates():
    """View all updates for a case"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*20 + "VIEW CASE UPDATES")
    print("="*60)
    
    case_id = input("\nEnter Case ID: ").strip()
    
    updates = get_updates_by_case(case_id)
    display_case_updates(updates)
    pause()

def view_all_officers():
    """View all registered officers"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "ALL REGISTERED OFFICERS")
    print("="*60)
    
    officers = get_all_officers()
    display_officers(officers)
    pause()

# ==================== PUBLIC VIEWS ====================

def view_all_cases_public():
    """View all cases (public view)"""
    clear_screen()
    print("\n" + "="*60)
    print(" "*22 + "ALL CASES")
    print("="*60)
    
    cases = get_all_cases()
    display_cases(cases)
    pause()