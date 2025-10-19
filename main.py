from database.connection import init_pool, test_connection, close_all_connections
from ui.menu import main_menu, citizen_menu, officer_menu, view_all_cases_public

def main():
    """Main application entry point"""
    # Initialize database connection pool
    print("\n🔄 Initializing Crime Reporting System...")
    init_pool()
    
    # Test database connection
    if not test_connection():
        print("\n❌ Failed to connect to database. Please check your configuration.")
        return
    
    print("\n✅ System ready!\n")
    
    # Main application loop
    while True:
        choice = main_menu()
        
        if choice == '1':
            citizen_menu()
        elif choice == '2':
            officer_menu()
        elif choice == '3':
            view_all_cases_public()
        elif choice == '4':
            print("\n👋 Thank you for using Crime Reporting System. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 4.")
            input("\nPress Enter to continue...")
    
    # Cleanup
    close_all_connections()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ System interrupted by user. Exiting...")
        close_all_connections()
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        close_all_connections()