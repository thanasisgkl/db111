from database import get_db_connection

def check_duplicates():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Βρίσκουμε διπλότυπα άρθρα
        cursor.execute("""
            SELECT number, COUNT(*) as count
            FROM articles a
            JOIN laws l ON a.law_id = l.id
            WHERE l.name = 'ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ'
            GROUP BY number
            HAVING COUNT(*) > 1
            ORDER BY number
        """)
        
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"Βρέθηκαν {len(duplicates)} άρθρα με διπλότυπα:")
            for number, count in duplicates:
                print(f"Άρθρο {number}: {count} φορές")
                
            # Διαγράφουμε τα διπλότυπα, κρατώντας μόνο το πιο πρόσφατο
            cursor.execute("""
                DELETE FROM articles a
                WHERE a.id NOT IN (
                    SELECT MAX(id)
                    FROM articles
                    GROUP BY law_id, number
                )
                AND law_id = (SELECT id FROM laws WHERE name = 'ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ')
            """)
            conn.commit()
            print(f"Διαγράφηκαν {cursor.rowcount} διπλότυπα άρθρα")
        else:
            print("Δεν βρέθηκαν διπλότυπα άρθρα")
            
    except Exception as e:
        print(f"Σφάλμα κατά τον έλεγχο διπλοτύπων: {e}")
        conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    check_duplicates() 