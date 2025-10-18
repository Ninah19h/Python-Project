from database.connection import get_connection, release_connection

def add_case_update(case_id, officer_id, update_note):
    """Add a new update to a case"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = """
                INSERT INTO case_updates (case_id, officer_id, update_note)
                VALUES (%s, %s, %s)
                RETURNING update_id;
            """
            cur.execute(query, (case_id, officer_id, update_note))
            update_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            release_connection(conn)
            print(f"✓ Case update added successfully! Update ID: {update_id}")
            return update_id
        except Exception as e:
            print(f"✗ Error adding case update: {e}")
            conn.rollback()
            if conn:
                release_connection(conn)
            return None
    return None

def get_updates_by_case(case_id):
    """Get all updates for a specific case"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
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
            updates = cur.fetchall()
            cur.close()
            release_connection(conn)
            return updates
        except Exception as e:
            print(f"✗ Error fetching case updates: {e}")
            if conn:
                release_connection(conn)
            return []
    return []

def delete_case_update(update_id):
    """Delete a case update"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = "DELETE FROM case_updates WHERE update_id = %s;"
            cur.execute(query, (update_id,))
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

def display_case_updates(updates):
    """Display case updates in a formatted way"""
    if not updates:
        print("\nNo updates found for this case.")
        return
    
    print("\n" + "="*120)
    print(f"{'Update ID':<12} {'Officer':<25} {'Badge':<15} {'Updated At':<20} {'Note':<40}")
    print("="*120)
    for update in updates:
        updated_date = update[2].strftime("%Y-%m-%d %H:%M") if update[2] else "N/A"
        note_preview = update[1][:37] + "..." if len(update[1]) > 40 else update[1]
        print(f"{update[0]:<12} {update[3]:<25} {update[4]:<15} {updated_date:<20} {note_preview:<40}")
    print("="*120)