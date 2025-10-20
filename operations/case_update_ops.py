# Import database connection functions to talk to PostgreSQL
from database.connection import get_connection, release_connection


# ADD NEW CASE UPDATE
def add_case_update(case_id, officer_id, update_note):
    """
    Add a progress note or update to an existing case
    Officers use this to document investigation progress
    
    Args:
        case_id: The case being updated
        officer_id: The officer adding the update
        update_note: The progress note or information to add
    
    Returns:
        update_id if successful, None if failed
    """
    # Get a database connection
    conn = get_connection()
    
    if conn:
        try:
            # Create cursor to execute SQL
            cur = conn.cursor()
            
            # Insert the update into the database
            # RETURNING gives us back the auto-generated update ID
            query = """
                INSERT INTO case_updates (case_id, officer_id, update_note)
                VALUES (%s, %s, %s)
                RETURNING update_id;
            """
            
            cur.execute(query, (case_id, officer_id, update_note))
            
            # Get the new update ID
            update_id = cur.fetchone()[0]
            
            # Save changes to database
            conn.commit()
            
            # Clean up
            cur.close()
            release_connection(conn)
            
            print(f"✓ Case update added successfully! Update ID: {update_id}")
            return update_id
            
        except Exception as e:
            # If something goes wrong, undo changes
            print(f"✗ Error adding case update: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return None
    
    return None


# GET ALL UPDATES FOR A CASE
def get_updates_by_case(case_id):
    """
    Retrieve all progress updates for a specific case
    Shows the investigation timeline
    
    Args:
        case_id: The case whose updates you want to see
    
    Returns:
        List of all updates for that case (newest first)
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Get all updates with officer information
            # JOIN combines update data with officer details
            # ORDER BY DESC shows newest updates first
            query = """
                SELECT 
                    cu.update_id,
                    cu.update_note,
                    cu.updated_at,
                    o.full_name AS officer_name,
                    o.badge_number
                FROM case_updates cu
                JOIN officers o ON cu.officer_id = o.officer_id
                WHERE cu.case_id = %s
                ORDER BY cu.updated_at DESC;
            """
            
            cur.execute(query, (case_id,))
            
            # Fetch all updates
            updates = cur.fetchall()
            
            # Clean up
            cur.close()
            release_connection(conn)
            
            return updates
            
        except Exception as e:
            print(f"✗ Error fetching case updates: {e}")
            if conn:
                release_connection(conn)
            return []
    
    return []


# DELETE A CASE UPDATE
def delete_case_update(update_id):
    """
    Remove a specific update from the database
    
    Args:
        update_id: The update to delete
    
    Returns:
        True if successful, False if failed
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Delete the update
            query = "DELETE FROM case_updates WHERE update_id = %s;"
            cur.execute(query, (update_id,))
            
            # Save changes
            conn.commit()
            
            cur.close()
            release_connection(conn)
            
            print(f"✓ Case update {update_id} deleted successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error deleting case update: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return False
    
    return False


# DISPLAY UPDATES IN A TABLE
def display_case_updates(updates):
    """
    Show case updates in a formatted table
    Makes it easy to read the investigation timeline
    
    Args:
        updates: List of updates to display
    """
    # If no updates found, show message and exit
    if not updates:
        print("\nNo updates found for this case.")
        return
    
    # Print table header
    print("\n" + "="*120)
    print(f"{'Update ID':<12} {'Officer':<25} {'Badge':<15} {'Updated At':<20} {'Note':<40}")
    print("="*120)
    
    # Print each update
    for update in updates:
        # Format the date nicely
        updated_date = update[2].strftime("%Y-%m-%d %H:%M") if update[2] else "N/A"
        
        # If note is too long, show preview with "..."
        # This keeps the table neat and readable
        note_preview = update[1][:37] + "..." if len(update[1]) > 40 else update[1]
        
        # Print the update row
        print(f"{update[0]:<12} {update[3]:<25} {update[4]:<15} {updated_date:<20} {note_preview:<40}")
    
    # Print table footer
    print("="*120)