from database import get_db_connection

def count_articles():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Μετράμε τα άρθρα του Αστικού Κώδικα
        cursor.execute("""
            SELECT COUNT(*)
            FROM articles a
            JOIN laws l ON a.law_id = l.id
            WHERE l.name = 'ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ'
        """)
        
        count = cursor.fetchone()[0]
        print(f"Στη βάση δεδομένων υπάρχουν {count} άρθρα του Αστικού Κώδικα")
            
    except Exception as e:
        print(f"Σφάλμα κατά την καταμέτρηση των άρθρων: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    count_articles() 