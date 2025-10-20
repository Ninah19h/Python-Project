# Import database connection functions to talk to PostgreSQL
from database.connection import get_connection, release_connection


#ADD NEW CASE 
def add_case(citizen_id, crime_type, description, location, officer_id=None):
    """
    Report a new crime case to the database
    
    Args:
        citizen_id: ID of the citizen reporting the crime
        crime_type: Type of crime (e.g., Theft, Assault)
        description: Detailed description of what happened
        location: Where the crime occurred
        officer_id: (Optional) Officer assigned to the case
    
    Returns:
        case_id if successful, None if failed
    """
    # Get a database connection from the pool
    conn = get_connection()
    
    if conn:
        try:
            # Create a cursor to execute SQL commands
            cur = conn.cursor()
            
            # SQL query to insert a new case into the database
            # RETURNING case_id gives us back the auto-generated ID
            query = """
                INSERT INTO cases (citizen_id, officer_id, crime_type, description, location)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING case_id;
            """
            
            # Execute the query with the provided data
            cur.execute(query, (citizen_id, officer_id, crime_type, description, location))
            
            # Get the newly created case ID
            case_id = cur.fetchone()[0]
            
            # Save changes to the database
            conn.commit()
            
            # Clean up
            cur.close()
            release_connection(conn)
            
            # Show success message
            print(f"✓ Case reported successfully! Case ID: {case_id}")
            return case_id
            
        except Exception as e:
            # If something goes wrong, undo changes and show error
            print(f"✗ Error adding case: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return None
    
    return None


#GET ALL CASES
def get_all_cases():
    """
    Retrieve all crime cases from the database with citizen and officer names
    
    Returns:
        List of all cases with their details, empty list if none found
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # SQL query to get all cases with related citizen and officer information
            # JOIN combines data from multiple tables
            # LEFT JOIN includes cases even if no officer is assigned yet
            query = """
                SELECT 
                    c.case_id,
                    c.crime_type,
                    c.description,
                    c.location,
                    c.status,
                    c.reported_at,
                    cit.full_name AS citizen_name,
                    o.full_name AS officer_name
                FROM cases c
                JOIN citizens cit ON c.citizen_id = cit.citizen_id
                LEFT JOIN officers o ON c.officer_id = o.officer_id
                ORDER BY c.case_id DESC;
            """
            
            cur.execute(query)
            
            # Fetch all results
            cases = cur.fetchall()
            
            # Clean up
            cur.close()
            release_connection(conn)
            
            return cases
            
        except Exception as e:
            print(f"✗ Error fetching cases: {e}")
            if conn:
                release_connection(conn)
            return []
    
    return []


#SPECIFIC CASE 
def get_case_by_id(case_id):
    """
    Get detailed information about a specific case
    
    Args:
        case_id: The ID of the case to retrieve
    
    Returns:
        Case details including citizen and officer info, None if not found
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Get all case details plus citizen and officer information
            query = """
                SELECT 
                    c.*,
                    cit.full_name AS citizen_name,
                    cit.phone_number AS citizen_phone,
                    o.full_name AS officer_name,
                    o.badge_number AS officer_badge
                FROM cases c
                JOIN citizens cit ON c.citizen_id = cit.citizen_id
                LEFT JOIN officers o ON c.officer_id = o.officer_id
                WHERE c.case_id = %s;
            """
            
            cur.execute(query, (case_id,))
            
            # Fetch single result
            case = cur.fetchone()
            
            cur.close()
            release_connection(conn)
            
            return case
            
        except Exception as e:
            print(f"✗ Error fetching case: {e}")
            if conn:
                release_connection(conn)
            return None
    
    return None


#BY STATUS 
def get_cases_by_status(status):
    """
    Find all cases with a specific status
    
    Args:
        status: The status to filter by (e.g., "Pending", "Resolved")
    
    Returns:
        List of cases matching the status
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Get cases that match the specified status
            query = """
                SELECT 
                    c.case_id,
                    c.crime_type,
                    c.location,
                    c.status,
                    c.reported_at,
                    cit.full_name AS citizen_name
                FROM cases c
                JOIN citizens cit ON c.citizen_id = cit.citizen_id
                WHERE c.status = %s
                ORDER BY c.reported_at DESC;
            """
            
            cur.execute(query, (status,))
            cases = cur.fetchall()
            
            cur.close()
            release_connection(conn)
            
            return cases
            
        except Exception as e:
            print(f"✗ Error filtering cases by status: {e}")
            if conn:
                release_connection(conn)
            return []
    
    return []


#FILTER BY LOCATION 
def get_cases_by_location(location):
    """
    Find all cases reported in a specific location
    
    Args:
        location: The location to search for (partial match)
    
    Returns:
        List of cases from that location
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # ILIKE allows case-insensitive search
            # %location% means "contains this word anywhere"
            query = """
                SELECT 
                    c.case_id,
                    c.crime_type,
                    c.location,
                    c.status,
                    c.reported_at,
                    cit.full_name AS citizen_name
                FROM cases c
                JOIN citizens cit ON c.citizen_id = cit.citizen_id
                WHERE c.location ILIKE %s
                ORDER BY c.reported_at DESC;
            """
            
            cur.execute(query, (f"%{location}%",))
            cases = cur.fetchall()
            
            cur.close()
            release_connection(conn)
            
            return cases
            
        except Exception as e:
            print(f"✗ Error filtering cases by location: {e}")
            if conn:
                release_connection(conn)
            return []
    
    return []


#FILTER BY CRIME TYPE
def get_cases_by_crime_type(crime_type):
    """
    Find all cases of a specific crime type
    
    Args:
        crime_type: The type of crime to search for (e.g., "Theft")
    
    Returns:
        List of cases of that crime type
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Search for cases with matching crime type
            query = """
                SELECT 
                    c.case_id,
                    c.crime_type,
                    c.location,
                    c.status,
                    c.reported_at,
                    cit.full_name AS citizen_name
                FROM cases c
                JOIN citizens cit ON c.citizen_id = cit.citizen_id
                WHERE c.crime_type ILIKE %s
                ORDER BY c.reported_at DESC;
            """
            
            cur.execute(query, (f"%{crime_type}%",))
            cases = cur.fetchall()
            
            cur.close()
            release_connection(conn)
            
            return cases
            
        except Exception as e:
            print(f"✗ Error filtering cases by crime type: {e}")
            if conn:
                release_connection(conn)
            return []
    
    return []


#OFFICER 
def assign_officer_to_case(case_id, officer_id):
    """
    Assign a police officer to handle a specific case
    
    Args:
        case_id: The case to assign
        officer_id: The officer who will handle it
    
    Returns:
        True if successful, False if failed
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Update the case with the officer's ID
            query = "UPDATE cases SET officer_id = %s WHERE case_id = %s;"
            cur.execute(query, (officer_id, case_id))
            
            # Save changes
            conn.commit()
            
            cur.close()
            release_connection(conn)
            
            print(f"✓ Officer {officer_id} assigned to case {case_id}")
            return True
            
        except Exception as e:
            print(f"✗ Error assigning officer: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return False
    
    return False


#UPDATE CASE STATUS
def update_case_status(case_id, status):
    """
    Change the status of a case (e.g., from Pending to Under Investigation)
    
    Args:
        case_id: The case to update
        status: The new status
    
    Returns:
        True if successful, False if failed
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Update the case status
            query = "UPDATE cases SET status = %s WHERE case_id = %s;"
            cur.execute(query, (status, case_id))
            
            conn.commit()
            
            cur.close()
            release_connection(conn)
            
            print(f"✓ Case {case_id} status updated to '{status}'")
            return True
            
        except Exception as e:
            print(f"✗ Error updating case status: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return False
    
    return False


# CASE 
def delete_case(case_id):
    """
    Permanently remove a case from the database
    
    Args:
        case_id: The case to delete
    
    Returns:
        True if successful, False if failed
    """
    conn = get_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Delete the case
            query = "DELETE FROM cases WHERE case_id = %s;"
            cur.execute(query, (case_id,))
            
            conn.commit()
            
            cur.close()
            release_connection(conn)
            
            print(f"✓ Case {case_id} deleted successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error deleting case: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return False
    
    return False


# DISPLAY CASES
def display_cases(cases):
    """
    Show cases in a nice, formatted table
    
    Args:
        cases: List of cases to display
    """
    # If no cases found, show message and exit
    if not cases:
        print("\nNo cases found.")
        return
    
    # Print table header
    print("\n" + "="*120)
    print(f"{'ID':<5} {'Crime Type':<20} {'Location':<20} {'Status':<15} {'Reported':<20} {'Citizen':<20}")
    print("="*120)
    
    # Print each case
    for case in cases:
        # Get case ID and crime type (always in same position)
        case_id = case[0]
        crime_type = case[1]
        
        # Different queries return different numbers of columns
        # So we check and extract data accordingly
        if len(case) >= 8:  # Full case details (8 columns)
            location = case[3]
            status = case[4]
            reported = case[5]
            citizen_name = case[6]
        else:  # Filtered results (6 columns)
            location = case[2]
            status = case[3]
            reported = case[4]
            citizen_name = case[5]
        
        # Format the date nicely (if it exists)
        if hasattr(reported, 'strftime'):
            reported_date = reported.strftime("%Y-%m-%d %H:%M")
        else:
            reported_date = str(reported) if reported else "N/A"
        
        # Print the row
        print(f"{case_id:<5} {crime_type:<20} {location:<20} {status:<15} {reported_date:<20} {citizen_name:<20}")
    
    # Print table footer
    print("="*120)