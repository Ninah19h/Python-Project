# Import database connection management functions
from database.connection import init_pool, test_connection, close_all_connections

# Import all menu functions from the UI
from ui.menu import main_menu, citizen_menu, officer_menu, view_all_cases_public


def main():
    """
    Main entry point for the Crime Reporting System
    This is what runs when you start the application
    """
    
    # STEP 1: Initialize the database connection pool
    print("\n Initializing Crime Reporting System...")
    init_pool()
    
    # STEP 2: Test if we can connect to the database
    if not test_connection():
        print("\n Failed to connect to database. Please check your configuration.")
        return  # Exit if database is unreachable
    
    print("\n System ready!\n")
    
    # STEP 3: Main application loop - keeps running until user exits
    while True:
        # Show main menu and get user's choice
        choice = main_menu()
        
        # Route user to the appropriate portal based on their choice
        if choice == '1':
            citizen_menu()  # Go to citizen portal
        elif choice == '2':
            officer_menu()  # Go to officer portal
        elif choice == '3':
            view_all_cases_public()  # Show all cases
        elif choice == '4':
            # User wants to exit
            print("\n👋 Thank you for using Crime Reporting System. Goodbye!")
            break  # Exit the loop
        else:
            # Invalid choice - show error and continue
            print("\n Invalid choice! Please enter a number between 1 and 4.")
            input("\nPress Enter to continue...")
    
    # STEP 4: Clean up - close all database connections before exiting
    close_all_connections()


# This ensures main() only runs when the script is executed directly
# (not when imported as a module)
if __name__ == "__main__":
    try:
        # Run the main application
        main()
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C to force quit
        print("\n\n System interrupted by user. Exiting...")
        close_all_connections()
        
    except Exception as e:
        # Something unexpected went wrong
        print(f"\n An error occurred: {e}")
        close_all_connections()