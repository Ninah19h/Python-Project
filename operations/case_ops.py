from database.connection import get_connection, release_connection

def add_case(citizen_id, crime_type, description, location, officer_id=None):
    """Add a new case to the database"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = """
                INSERT INTO cases (citizen_id, officer_id, crime_type, description, location)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING case_id;
            """
            cur.execute(query, (citizen_id, officer_id, crime_type, description, location))
            case_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            release_connection(conn)
            print(f"✓ Case reported successfully! Case ID: {case_id}")
            return case_id
        except Exception as e:
            print(f"✗ Error adding case: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return None
    return None

def get_all_cases():
    """Get all cases with citizen and officer details"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
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
            cases = cur.fetchall()
            cur.close()
            release_connection(conn)
            return cases
        except Exception as e:
            print(f"✗ Error fetching cases: {e}")
            if conn:
                release_connection(conn)
            return []
    return []

def get_case_by_id(case_id):
    """Get a specific case by ID with details"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
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

def get_cases_by_status(status):
    """Filter cases by status"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
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

def get_cases_by_location(location):
    """Filter cases by location"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
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

def get_cases_by_crime_type(crime_type):
    """Filter cases by crime type"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
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

def assign_officer_to_case(case_id, officer_id):
    """Assign an officer to a case"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = "UPDATE cases SET officer_id = %s WHERE case_id = %s;"
            cur.execute(query, (officer_id, case_id))
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

def update_case_status(case_id, status):
    """Update case status"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
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

def delete_case(case_id):
    """Delete a case from the database"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
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

def display_cases(cases):
    """Display cases in a formatted way"""
    if not cases:
        print("\nNo cases found.")
        return
    
    print("\n" + "="*120)
    print(f"{'ID':<5} {'Crime Type':<20} {'Location':<20} {'Status':<15} {'Reported':<20} {'Citizen':<20}")
    print("="*120)
    for case in cases:
        # Handle different query formats
        case_id = case[0]
        crime_type = case[1]
        
        # Check if it's from get_all_cases (8 columns) or filtered query (6 columns)
        if len(case) >= 8:  # get_all_cases format
            location = case[3]
            status = case[4]
            reported = case[5]
            citizen_name = case[6]
        else:  # filtered query format (6 columns)
            location = case[2]
            status = case[3]
            reported = case[4]
            citizen_name = case[5]
        
        # Handle datetime formatting
        if hasattr(reported, 'strftime'):
            reported_date = reported.strftime("%Y-%m-%d %H:%M")
        else:
            reported_date = str(reported) if reported else "N/A"
        
        print(f"{case_id:<5} {crime_type:<20} {location:<20} {status:<15} {reported_date:<20} {citizen_name:<20}")
    print("="*120)