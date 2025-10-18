from database.connection import get_connection, release_connection

def add_officer(full_name, badge_number, rank, phone_number, station=None):
    """Add a new officer to the database"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = """
                INSERT INTO officers (full_name, badge_number, rank, phone_number, station)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING officer_id;
            """
            cur.execute(query, (full_name, badge_number, rank, phone_number, station))
            officer_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            release_connection(conn)
            print(f"✓ Officer added successfully! ID: {officer_id}")
            return officer_id
        except Exception as e:
            print(f"✗ Error adding officer: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return None
    return None

def get_all_officers():
    """Get all officers from the database"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = "SELECT * FROM officers ORDER BY officer_id;"
            cur.execute(query)
            officers = cur.fetchall()
            cur.close()
            release_connection(conn)
            return officers
        except Exception as e:
            print(f"✗ Error fetching officers: {e}")
            if conn:
                release_connection(conn)
            return []
    return []

def get_officer_by_id(officer_id):
    """Get a specific officer by ID"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = "SELECT * FROM officers WHERE officer_id = %s;"
            cur.execute(query, (officer_id,))
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

def update_officer(officer_id, full_name=None, rank=None, phone_number=None, station=None):
    """Update officer information"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            updates = []
            values = []
            
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
            
            if not updates:
                print("✗ No fields to update")
                release_connection(conn)
                return False
            
            values.append(officer_id)
            query = f"UPDATE officers SET {', '.join(updates)} WHERE officer_id = %s;"
            cur.execute(query, values)
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

def delete_officer(officer_id):
    """Delete an officer from the database"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = "DELETE FROM officers WHERE officer_id = %s;"
            cur.execute(query, (officer_id,))
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

def display_officers(officers):
    """Display officers in a formatted way"""
    if not officers:
        print("\nNo officers found.")
        return
    
    print("\n" + "="*100)
    print(f"{'ID':<5} {'Name':<25} {'Badge':<15} {'Rank':<15} {'Phone':<15} {'Station':<20}")
    print("="*100)
    for officer in officers:
        print(f"{officer[0]:<5} {officer[1]:<25} {officer[2]:<15} {officer[3]:<15} {officer[4]:<15} {officer[5] or 'N/A':<20}")
    print("="*100)