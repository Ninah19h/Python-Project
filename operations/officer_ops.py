# Import database connection functions to talk to PostgreSQL
from database.connection import get_connection, release_connection


# ADD NEW OFFICER
def add_officer(full_name, badge_number, rank, phone_number, station=None):
    """
    Register a new police officer in the system
    
    Args:
        full_name: Officer's full name
        badge_number: Unique badge/ID number
        rank: Officer's rank (e.g., Sergeant, Inspector)
        phone_number: Contact phone number
        station: Police station assignment (optional)
    
    Returns:
        officer_id if successful, None if failed
    """
    # Get a database connection
    conn = get_connection()
    
    if conn:
        try:
            # Create cursor to execute SQL commands
            cur = conn.cursor()
            
            # Insert new officer into database
            # RETURNING gives us back the auto-generated officer ID
            query = """
                INSERT INTO officers (full_name, badge_number, rank, phone_number, station)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING officer_id;
            """
            
            cur.execute(query, (full_name, badge_number, rank, phone_number, station))
            
            # Get the newly created officer ID
            officer_id = cur.fetchone()[0]
            
            # Save changes to database
            conn.commit()
            
            # Clean up
            cur.close()
            release_connection(conn)
            
            print(f"✓ Officer added successfully! ID: {officer_id}")
            return officer_id
            
        except Exception as e:
            # If something goes wrong, undo changes
            print(f"✗ Error adding officer: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return None
    
    return None


# GET ALL OFFICERS
def get_all_officers():
    """
    Retrieve all registered officers from the database
    
    Returns:
        List of all officers, empty list if none found
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Get all officers ordered by their ID
            query = "SELECT * FROM officers ORDER BY officer_id;"
            cur.execute(query)
            
            # Fetch all results
            officers = cur.fetchall()
            
            # Clean up
            cur.close()
            release_connection(conn)
            
            return officers
            
        except Exception as e:
            print(f"✗ Error fetching officers: {e}")
            if conn:
                release_connection(conn)
            return []
    
    return []


# GET SPECIFIC OFFICER
def get_officer_by_id(officer_id):
    """
    Find a specific officer by their ID
    
    Args:
        officer_id: The ID of the officer to find
    
    Returns:
        Officer details if found, None if not found
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Search for officer with matching ID
            query = "SELECT * FROM officers WHERE officer_id = %s;"
            cur.execute(query, (officer_id,))
            
            # Fetch single result
            officer = cur.fetchone()
            
            cur.close()
            release_connection(conn)
            
            return officer
            
        except Exception as e:
            print(f"✗ Error fetching officer: {e}")
            if conn:
                release_connection(conn)
            return None
    
    return None


# UPDATE OFFICER INFORMATION
def update_officer(officer_id, full_name=None, rank=None, phone_number=None, station=None):
    """
    Update an officer's information
    Only updates fields that are provided (not None)
    
    Args:
        officer_id: The officer to update
        full_name: New name (optional)
        rank: New rank (optional)
        phone_number: New phone (optional)
        station: New station (optional)
    
    Returns:
        True if successful, False if failed
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Build update query dynamically based on what fields are provided
            updates = []  # Will hold SQL parts like "rank = %s"
            values = []   # Will hold the actual values to update
            
            # Only add fields that were provided
            if full_name:
                updates.append("full_name = %s")
                values.append(full_name)
            if rank:
                updates.append("rank = %s")
                values.append(rank)
            if phone_number:
                updates.append("phone_number = %s")
                values.append(phone_number)
            if station:
                updates.append("station = %s")
                values.append(station)
            
            # If no fields provided, nothing to update
            if not updates:
                print("✗ No fields to update")
                release_connection(conn)
                return False
            
            # Add officer_id to the end of values list
            values.append(officer_id)
            
            # Build and execute the update query
            query = f"UPDATE officers SET {', '.join(updates)} WHERE officer_id = %s;"
            cur.execute(query, values)
            
            # Save changes
            conn.commit()
            
            cur.close()
            release_connection(conn)
            
            print(f"✓ Officer {officer_id} updated successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error updating officer: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return False
    
    return False


# DELETE OFFICER
def delete_officer(officer_id):
    """
    Permanently remove an officer from the database
    
    Args:
        officer_id: The officer to delete
    
    Returns:
        True if successful, False if failed
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Delete the officer
            query = "DELETE FROM officers WHERE officer_id = %s;"
            cur.execute(query, (officer_id,))
            
            # Save changes
            conn.commit()
            
            cur.close()
            release_connection(conn)
            
            print(f"✓ Officer {officer_id} deleted successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error deleting officer: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return False
    
    return False


# DISPLAY OFFICERS IN A TABLE
def display_officers(officers):
    """
    Show officers in a formatted table for easy reading
    
    Args:
        officers: List of officers to display
    """
    # If no officers found, show message and exit
    if not officers:
        print("\nNo officers found.")
        return
    
    # Print table header
    print("\n" + "="*100)
    print(f"{'ID':<5} {'Name':<25} {'Badge':<15} {'Rank':<15} {'Phone':<15} {'Station':<20}")
    print("="*100)
    
    # Print each officer
    for officer in officers:
        # Show "N/A" if station is not provided
        print(f"{officer[0]:<5} {officer[1]:<25} {officer[2]:<15} {officer[3]:<15} {officer[4]:<15} {officer[5] or 'N/A':<20}")
    
    # Print table footer
    print("="*100)