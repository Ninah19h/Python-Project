from database.connection import get_connection, release_connection

def add_citizen(full_name, phone_number, email=None, address=None):
    """Add a new citizen to the database"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = """
                INSERT INTO citizens (full_name, phone_number, email, address)
                VALUES (%s, %s, %s, %s)
                RETURNING citizen_id;
            """
            cur.execute(query, (full_name, phone_number, email, address))
            citizen_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            release_connection(conn)
            print(f"✓ Citizen added successfully! ID: {citizen_id}")
            return citizen_id
        except Exception as e:
            print(f"✗ Error adding citizen: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return None
    return None

def get_all_citizens():
    """Get all citizens from the database"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = "SELECT * FROM citizens ORDER BY citizen_id;"
            cur.execute(query)
            citizens = cur.fetchall()
            cur.close()
            release_connection(conn)
            return citizens
        except Exception as e:
            print(f"✗ Error fetching citizens: {e}")
            if conn:
                release_connection(conn)
            return []
    return []

def get_citizen_by_id(citizen_id):
    """Get a specific citizen by ID"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = "SELECT * FROM citizens WHERE citizen_id = %s;"
            cur.execute(query, (citizen_id,))
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

def update_citizen(citizen_id, full_name=None, phone_number=None, email=None, address=None):
    """Update citizen information"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            updates = []
            values = []
            
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
            
            if not updates:
                print("✗ No fields to update")
                release_connection(conn)
                return False
            
            values.append(citizen_id)
            query = f"UPDATE citizens SET {', '.join(updates)} WHERE citizen_id = %s;"
            cur.execute(query, values)
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

def delete_citizen(citizen_id):
    """Delete a citizen from the database"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = "DELETE FROM citizens WHERE citizen_id = %s;"
            cur.execute(query, (citizen_id,))
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

def display_citizens(citizens):
    """Display citizens in a formatted way"""
    if not citizens:
        print("\nNo citizens found.")
        return
    
    print("\n" + "="*80)
    print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<25}")
    print("="*80)
    for citizen in citizens:
        print(f"{citizen[0]:<5} {citizen[1]:<25} {citizen[2]:<15} {citizen[3] or 'N/A':<25}")
    print("="*80)