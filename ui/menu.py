# Import system module for screen clearing
import os

# Import all citizen-related functions
from operations.citizen_ops import (
    add_citizen, get_all_citizens, get_citizen_by_id, 
    update_citizen, delete_citizen, display_citizens
)

# Import all officer-related functions
from operations.officer_ops import (
    add_officer, get_all_officers, get_officer_by_id,
    update_officer, delete_officer, display_officers
)

# Import all case-related functions
from operations.case_ops import (
    add_case, get_all_cases, get_case_by_id,
    get_cases_by_status, get_cases_by_location, get_cases_by_crime_type,
    assign_officer_to_case, update_case_status, delete_case, display_cases
)

# Import case update functions
from operations.case_update_ops import (
    add_case_update, get_updates_by_case, delete_case_update, display_case_updates
)


# HELPER FUNCTIONS

def clear_screen():
    """
    Clear the terminal screen for a clean interface
    Works on both Windows and Mac/Linux
    """
    os.system('clear' if os.name != 'nt' else 'cls')


def pause():
    """
    Pause the program and wait for user to press Enter
    Gives user time to read information before continuing
    """
    input("\nPress Enter to continue...")


# MAIN MENU

def main_menu():
    """
    Display the main menu with three portal options
    
    Returns:
        User's choice as a string
    """
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


# CITIZEN PORTAL

def citizen_menu():
    """
    Display the citizen portal menu with all citizen options
    Loops until user chooses to go back to main menu
    """
    while True:
        clear_screen()
        print("\n" + "="*60)
        print(" "*20 + "CITIZEN PORTAL")
        print("="*60)
        print("\n1. Register as New Citizen")
        print("2. Report a Crime")
        print("3. View My Cases")
        print("4. Update My Information")
        print("5. Delete My Account")
        print("6. View All Citizens")
        print("7. Back to Main Menu")
        print("\n" + "="*60)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        # Call appropriate function based on user's choice
        if choice == '1':
            register_citizen()
        elif choice == '2':
            report_crime()
        elif choice == '3':
            view_citizen_cases()
        elif choice == '4':
            update_citizen_info()
        elif choice == '5':
            delete_citizen_account()
        elif choice == '6':
            view_all_citizens()
        elif choice == '7':
            break  # Exit to main menu
        else:
            print("Invalid choice! Please try again.")
            pause()


def register_citizen():
    """
    Register a new citizen in the system
    Collects name, phone, email (optional), and address (optional)
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "CITIZEN REGISTRATION")
    print("="*60)
    
    # Collect citizen information
    full_name = input("\nEnter full name: ").strip()
    phone_number = input("Enter phone number: ").strip()
    email = input("Enter email (optional, press Enter to skip): ").strip() or None
    address = input("Enter address (optional, press Enter to skip): ").strip() or None
    
    # Validate required fields
    if not (full_name and phone_number):
        print("\nError: Full name and phone number are required!")
        pause()
        return
    
    # Add citizen to database
    citizen_id = add_citizen(full_name, phone_number, email, address)
    if citizen_id:
        print(f"\nRegistration successful! Your Citizen ID is: {citizen_id}")
        print("Please remember this ID for future reference.")
    
    pause()


def report_crime():
    """
    Allow citizens to report a crime
    Verifies citizen ID before accepting the report
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*20 + "REPORT A CRIME")
    print("="*60)
    
    citizen_id = input("\nEnter your Citizen ID: ").strip()
    
    # Check if citizen exists in database
    citizen = get_citizen_by_id(citizen_id)
    if not citizen:
        print(f"\nError: Citizen ID {citizen_id} not found!")
        print("Please register first if you haven't already.")
        pause()
        return
    
    # Greet the citizen and collect crime details
    print(f"\nWelcome, {citizen[1]}!")
    print("\nCrime Types: Theft, Assault, Burglary, Robbery, Vandalism, Fraud, etc.")
    crime_type = input("Enter type of crime: ").strip()
    description = input("Enter detailed description of the incident: ").strip()
    location = input("Enter location where crime occurred: ").strip()
    
    # Validate all fields are filled
    if crime_type and description and location:
        # Submit the crime report
        case_id = add_case(citizen_id, crime_type, description, location)
        if case_id:
            print(f"\nCrime reported successfully!")
            print(f"Your Case ID is: {case_id}")
            print("An officer will be assigned to your case soon.")
    else:
        print("\nError: All fields are required!")
    
    pause()


def view_citizen_cases():
    """
    Show all cases reported by a specific citizen
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*22 + "MY CASES")
    print("="*60)
    
    citizen_id = input("\nEnter your Citizen ID: ").strip()
    
    # Get all cases and filter to find this citizen's cases
    all_cases = get_all_cases()
    citizen_cases = []
    
    for case in all_cases:
        # Get full case details to check citizen ID
        case_detail = get_case_by_id(case[0])
        if case_detail and str(case_detail[1]) == citizen_id:
            citizen_cases.append(case)
    
    # Display results
    if citizen_cases:
        display_cases(citizen_cases)
    else:
        print("\nNo cases found for this citizen ID.")
    
    pause()


def update_citizen_info():
    """
    Allow citizens to update their personal information
    Shows current info and lets them update specific fields
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*16 + "UPDATE CITIZEN INFORMATION")
    print("="*60)
    
    citizen_id = input("\nEnter your Citizen ID: ").strip()
    
    # Verify citizen exists
    citizen = get_citizen_by_id(citizen_id)
    if not citizen:
        print(f"\nError: Citizen ID {citizen_id} not found!")
        pause()
        return
    
    # Show current information
    print(f"\nCurrent information for: {citizen[1]}")
    print(f"Phone: {citizen[2]}")
    print(f"Email: {citizen[3] or 'Not provided'}")
    print(f"Address: {citizen[4] or 'Not provided'}")
    
    # Collect new information (press Enter to keep current)
    print("\n--- Enter new information (press Enter to keep current) ---")
    full_name = input("New full name: ").strip() or None
    phone_number = input("New phone number: ").strip() or None
    email = input("New email: ").strip() or None
    address = input("New address: ").strip() or None
    
    # Update the database
    if update_citizen(citizen_id, full_name, phone_number, email, address):
        print("\nInformation updated successfully!")
    else:
        print("\nNo changes made.")
    
    pause()


def delete_citizen_account():
    """
    Delete a citizen account permanently from the system
    Requires confirmation before deletion to prevent accidents
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "DELETE CITIZEN ACCOUNT")
    print("="*60)
    
    citizen_id = input("\nEnter your Citizen ID: ").strip()
    
    # Verify citizen exists
    citizen = get_citizen_by_id(citizen_id)
    if not citizen:
        print(f"\nError: Citizen ID {citizen_id} not found!")
        pause()
        return
    
    # Show warning and ask for confirmation
    print(f"\nWARNING: You are about to delete the account for: {citizen[1]}")
    print("This action cannot be undone!")
    print("All cases reported by this citizen will also be deleted.")
    confirm = input("\nType 'DELETE' to confirm deletion: ").strip()
    
    # Only proceed if user types exactly DELETE
    if confirm == 'DELETE':
        if delete_citizen(citizen_id):
            print("\nAccount deleted successfully!")
        else:
            print("\nFailed to delete account.")
    else:
        print("\nDeletion cancelled. Account not deleted.")
    
    pause()


def view_all_citizens():
    """
    Display a list of all registered citizens
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "ALL REGISTERED CITIZENS")
    print("="*60)
    
    citizens = get_all_citizens()
    display_citizens(citizens)
    pause()


# OFFICER PORTAL

def officer_menu():
    """
    Display the officer portal menu with all officer options
    Loops until user chooses to go back to main menu
    """
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
        print("10. Delete Case")
        print("11. Delete Case Update")
        print("12. View All Officers")
        print("13. Delete Officer Account")
        print("14. Back to Main Menu")
        print("\n" + "="*60)
        
        choice = input("\nEnter your choice (1-14): ").strip()
        
        # Call appropriate function based on user's choice
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
            delete_case_menu()
        elif choice == '11':
            delete_update_menu()
        elif choice == '12':
            view_all_officers()
        elif choice == '13':
            delete_officer_account()
        elif choice == '14':
            break  # Exit to main menu
        else:
            print("Invalid choice! Please try again.")
            pause()


def register_officer():
    """
    Register a new police officer in the system
    Collects name, badge number, rank, phone, and station (optional)
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "OFFICER REGISTRATION")
    print("="*60)
    
    # Collect officer information
    full_name = input("\nEnter full name: ").strip()
    badge_number = input("Enter badge number: ").strip()
    rank = input("Enter rank (e.g., Officer, Sergeant, Inspector): ").strip()
    phone_number = input("Enter phone number: ").strip()
    station = input("Enter police station (optional, press Enter to skip): ").strip() or None
    
    # Validate all required fields are filled
    if full_name and badge_number and rank and phone_number:
        # Add officer to database
        officer_id = add_officer(full_name, badge_number, rank, phone_number, station)
        if officer_id:
            print(f"\nRegistration successful! Your Officer ID is: {officer_id}")
    else:
        print("\nError: All required fields must be filled!")
    
    pause()


def view_all_cases_officer():
    """
    Display all crime cases in the system
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*22 + "ALL CASES")
    print("="*60)
    
    cases = get_all_cases()
    display_cases(cases)
    pause()


def filter_cases_by_status():
    """
    Filter and display cases by their status
    (Pending, Under Investigation, Resolved, Closed)
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "FILTER CASES BY STATUS")
    print("="*60)
    
    # Show status options
    print("\nAvailable statuses:")
    print("1. Pending")
    print("2. Under Investigation")
    print("3. Resolved")
    print("4. Closed")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    # Convert number choice to actual status text
    status_map = {
        '1': 'Pending',
        '2': 'Under Investigation',
        '3': 'Resolved',
        '4': 'Closed'
    }
    
    # Validate choice
    if choice not in status_map:
        print("\nInvalid choice!")
        pause()
        return
    
    status = status_map[choice]
    print(f"\nSearching for cases with status: {status}")
    
    # Get and display filtered cases
    cases = get_cases_by_status(status)
    display_cases(cases)
    pause()


def filter_cases_by_location():
    """
    Filter and display cases by location
    Uses partial matching (e.g., "Nairobi" will find "Nairobi CBD")
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "FILTER CASES BY LOCATION")
    print("="*60)
    
    location = input("\nEnter location to search: ").strip()
    
    # Get and display filtered cases
    cases = get_cases_by_location(location)
    display_cases(cases)
    pause()


def filter_cases_by_crime_type():
    """
    Filter and display cases by type of crime
    Uses partial matching (e.g., "Theft" will find "Grand Theft")
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*16 + "FILTER CASES BY CRIME TYPE")
    print("="*60)
    
    crime_type = input("\nEnter crime type to search: ").strip()
    
    # Get and display filtered cases
    cases = get_cases_by_crime_type(crime_type)
    display_cases(cases)
    pause()


def assign_officer():
    """
    Assign a police officer to handle a specific case
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "ASSIGN OFFICER TO CASE")
    print("="*60)
    
    case_id = input("\nEnter Case ID: ").strip()
    officer_id = input("Enter Officer ID: ").strip()
    
    # Attempt to assign officer to case
    if assign_officer_to_case(case_id, officer_id):
        print("\nOfficer assigned successfully!")
    else:
        print("\nFailed to assign officer!")
    
    pause()


def update_status():
    """
    Change the status of a case
    (e.g., from Pending to Under Investigation)
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*20 + "UPDATE CASE STATUS")
    print("="*60)
    
    case_id = input("\nEnter Case ID: ").strip()
    
    # Show status options
    print("\nAvailable statuses:")
    print("1. Pending")
    print("2. Under Investigation")
    print("3. Resolved")
    print("4. Closed")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    # Convert number choice to actual status text
    status_map = {
        '1': 'Pending',
        '2': 'Under Investigation',
        '3': 'Resolved',
        '4': 'Closed'
    }
    
    # Validate choice
    if choice not in status_map:
        print("\nInvalid choice!")
        pause()
        return
    
    status = status_map[choice]
    
    # Update the case status
    if update_case_status(case_id, status):
        print(f"\nCase status updated to '{status}' successfully!")
    else:
        print("\nFailed to update case status!")
    
    pause()


def add_update():
    """
    Add a progress note or update to a case
    Officers use this to document investigation progress
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*20 + "ADD CASE UPDATE")
    print("="*60)
    
    # Collect update information
    case_id = input("\nEnter Case ID: ").strip()
    officer_id = input("Enter your Officer ID: ").strip()
    update_note = input("Enter update note: ").strip()
    
    # Validate all fields are filled
    if case_id and officer_id and update_note:
        # Add update to database
        update_id = add_case_update(case_id, officer_id, update_note)
        if update_id:
            print("\nCase update added successfully!")
    else:
        print("\nAll fields are required!")
    
    pause()


def view_case_updates():
    """
    View all progress updates for a specific case
    Shows the investigation timeline
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*20 + "VIEW CASE UPDATES")
    print("="*60)
    
    case_id = input("\nEnter Case ID: ").strip()
    
    # Get and display all updates for this case
    updates = get_updates_by_case(case_id)
    display_case_updates(updates)
    pause()


def delete_case_menu():
    """
    Delete a crime case permanently from the system
    Requires confirmation before deletion
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*22 + "DELETE CASE")
    print("="*60)
    
    case_id = input("\nEnter Case ID to delete: ").strip()
    
    # Verify case exists
    case = get_case_by_id(case_id)
    if not case:
        print(f"\nError: Case ID {case_id} not found!")
        pause()
        return
    
    # Show warning and ask for confirmation
    print(f"\nWARNING: You are about to delete case #{case_id}")
    print(f"Crime Type: {case[3]}")
    print(f"Location: {case[4]}")
    print("\nThis action cannot be undone!")
    print("All updates associated with this case will also be deleted.")
    confirm = input("\nType 'DELETE' to confirm deletion: ").strip()
    
    # Only proceed if user types exactly DELETE
    if confirm == 'DELETE':
        if delete_case(case_id):
            print("\nCase deleted successfully!")
        else:
            print("\nFailed to delete case.")
    else:
        print("\nDeletion cancelled. Case not deleted.")
    
    pause()


def delete_update_menu():
    """
    Delete a specific case update from the system
    Requires confirmation before deletion
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*19 + "DELETE CASE UPDATE")
    print("="*60)
    
    # First show updates for a case
    case_id = input("\nEnter Case ID to view its updates: ").strip()
    updates = get_updates_by_case(case_id)
    
    if not updates:
        print("\nNo updates found for this case.")
        pause()
        return
    
    # Display updates
    display_case_updates(updates)
    
    # Ask which update to delete
    update_id = input("\nEnter Update ID to delete: ").strip()
    
    # Show warning and ask for confirmation
    print(f"\nWARNING: You are about to delete update #{update_id}")
    print("This action cannot be undone!")
    confirm = input("\nType 'DELETE' to confirm deletion: ").strip()
    
    # Only proceed if user types exactly DELETE
    if confirm == 'DELETE':
        if delete_case_update(update_id):
            print("\nCase update deleted successfully!")
        else:
            print("\nFailed to delete case update.")
    else:
        print("\nDeletion cancelled. Update not deleted.")
    
    pause()


def delete_officer_account():
    """
    Delete an officer account permanently from the system
    Requires confirmation before deletion
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "DELETE OFFICER ACCOUNT")
    print("="*60)
    
    officer_id = input("\nEnter Officer ID: ").strip()
    
    # Verify officer exists
    officer = get_officer_by_id(officer_id)
    if not officer:
        print(f"\nError: Officer ID {officer_id} not found!")
        pause()
        return
    
    # Show warning and ask for confirmation
    print(f"\nWARNING: You are about to delete the account for: {officer[1]}")
    print(f"Badge Number: {officer[2]}")
    print(f"Rank: {officer[3]}")
    print("\nThis action cannot be undone!")
    print("Cases assigned to this officer will remain but show no assigned officer.")
    confirm = input("\nType 'DELETE' to confirm deletion: ").strip()
    
    # Only proceed if user types exactly DELETE
    if confirm == 'DELETE':
        if delete_officer(officer_id):
            print("\nOfficer account deleted successfully!")
        else:
            print("\nFailed to delete officer account.")
    else:
        print("\nDeletion cancelled. Account not deleted.")
    
    pause()


def view_all_officers():
    """
    Display a list of all registered officers
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*18 + "ALL REGISTERED OFFICERS")
    print("="*60)
    
    officers = get_all_officers()
    display_officers(officers)
    pause()


# PUBLIC VIEWS

def view_all_cases_public():
    """
    Display all cases for public viewing
    Anyone can see this from the main menu
    """
    clear_screen()
    print("\n" + "="*60)
    print(" "*22 + "ALL CASES")
    print("="*60)
    
    cases = get_all_cases()
    display_cases(cases)
    pause()