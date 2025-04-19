from database import get_db_connection


def drop_tables():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Διαγραφή πινάκων
        cursor.execute("DROP TABLE IF EXISTS articles CASCADE")
        cursor.execute("DROP TABLE IF EXISTS laws CASCADE")
        
        conn.commit()
        print("Οι πίνακες διαγράφηκαν επιτυχώς!")
        
    except Exception as e:
        print(f"Σφάλμα κατά τη διαγραφή των πινάκων: {e}")
        conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    drop_tables() 