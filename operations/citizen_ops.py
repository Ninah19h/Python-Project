# Import database connection functions to talk to PostgreSQL
from database.connection import get_connection, release_connection


# ADD NEW CITIZEN
def add_citizen(full_name, phone_number, email=None, address=None):
    """
    Register a new citizen in the system
    
    Args:
        full_name: Citizen's full name
        phone_number: Contact phone number
        email: Email address (optional)
        address: Physical address (optional)
    
    Returns:
        citizen_id if successful, None if failed
    """
    # Get a database connection
    conn = get_connection()
    
    if conn:
        try:
            # Create cursor to execute SQL commands
            cur = conn.cursor()
            
            # Insert new citizen into database
            # RETURNING gives us back the auto-generated citizen ID
            query = """
                INSERT INTO citizens (full_name, phone_number, email, address)
                VALUES (%s, %s, %s, %s)
                RETURNING citizen_id;
            """
            
            cur.execute(query, (full_name, phone_number, email, address))
            
            # Get the newly created citizen ID
            citizen_id = cur.fetchone()[0]
            
            # Save changes to database
            conn.commit()
            
            # Clean up
            cur.close()
            release_connection(conn)
            
            print(f"✓ Citizen added successfully! ID: {citizen_id}")
            return citizen_id
            
        except Exception as e:
            # If something goes wrong, undo changes
            print(f"✗ Error adding citizen: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return None
    
    return None


# GET ALL CITIZENS
def get_all_citizens():
    """
    Retrieve all registered citizens from the database
    
    Returns:
        List of all citizens, empty list if none found
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Get all citizens ordered by their ID
            query = "SELECT * FROM citizens ORDER BY citizen_id;"
            cur.execute(query)
            
            # Fetch all results
            citizens = cur.fetchall()
            
            # Clean up
            cur.close()
            release_connection(conn)
            
            return citizens
            
        except Exception as e:
            print(f"✗ Error fetching citizens: {e}")
            if conn:
                release_connection(conn)
            return []
    
    return []


# GET SPECIFIC CITIZEN
def get_citizen_by_id(citizen_id):
    """
    Find a specific citizen by their ID
    
    Args:
        citizen_id: The ID of the citizen to find
    
    Returns:
        Citizen details if found, None if not found
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Search for citizen with matching ID
            query = "SELECT * FROM citizens WHERE citizen_id = %s;"
            cur.execute(query, (citizen_id,))
            
            # Fetch single result
            citizen = cur.fetchone()
            
            cur.close()
            release_connection(conn)
            
            return citizen
            
        except Exception as e:
            print(f"✗ Error fetching citizen: {e}")
            if conn:
                release_connection(conn)
            return None
    
    return None


# UPDATE CITIZEN INFORMATION
def update_citizen(citizen_id, full_name=None, phone_number=None, email=None, address=None):
    """
    Update a citizen's information
    Only updates fields that are provided (not None)
    
    Args:
        citizen_id: The citizen to update
        full_name: New name (optional)
        phone_number: New phone (optional)
        email: New email (optional)
        address: New address (optional)
    
    Returns:
        True if successful, False if failed
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Build update query dynamically based on what fields are provided
            updates = []  # Will hold SQL parts like "full_name = %s"
            values = []   # Will hold the actual values to update
            
            # Only add fields that were provided
            if full_name:
                updates.append("full_name = %s")
                values.append(full_name)
            if phone_number:
                updates.append("phone_number = %s")
                values.append(phone_number)
            if email:
                updates.append("email = %s")
                values.append(email)
            if address:
                updates.append("address = %s")
                values.append(address)
            
            # If no fields provided, nothing to update
            if not updates:
                print("✗ No fields to update")
                release_connection(conn)
                return False
            
            # Add citizen_id to the end of values list
            values.append(citizen_id)
            
            # Build and execute the update query
            query = f"UPDATE citizens SET {', '.join(updates)} WHERE citizen_id = %s;"
            cur.execute(query, values)
            
            # Save changes
            conn.commit()
            
            cur.close()
            release_connection(conn)
            
            print(f"✓ Citizen {citizen_id} updated successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error updating citizen: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return False
    
    return False


# DELETE CITIZEN
def delete_citizen(citizen_id):
    """
    Permanently remove a citizen from the database
    
    Args:
        citizen_id: The citizen to delete
    
    Returns:
        True if successful, False if failed
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Delete the citizen
            query = "DELETE FROM citizens WHERE citizen_id = %s;"
            cur.execute(query, (citizen_id,))
            
            # Save changes
            conn.commit()
            
            cur.close()
            release_connection(conn)
            
            print(f"✓ Citizen {citizen_id} deleted successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error deleting citizen: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return False
    
    return False


# DISPLAY CITIZENS IN A TABLE
def display_citizens(citizens):
    """
    Show citizens in a formatted table for easy reading
    
    Args:
        citizens: List of citizens to display
    """
    # If no citizens found, show message and exit
    if not citizens:
        print("\nNo citizens found.")
        return
    
    # Print table header
    print("\n" + "="*80)
    print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<25}")
    print("="*80)
    
    # Print each citizen
    for citizen in citizens:
        # Show "N/A" if email is not provided
        print(f"{citizen[0]:<5} {citizen[1]:<25} {citizen[2]:<15} {citizen[3] or 'N/A':<25}")
    
    # Print table footer
    print("="*80)