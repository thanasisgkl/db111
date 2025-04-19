from database import get_db_connection


def remove_duplicates():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Βρίσκουμε το law_id του Κώδικα Διοικητικής Δικονομίας
        law_name = 'ΚΩΔΙΚΑΣ ΔΙΟΙΚΗΤΙΚΗΣ ΔΙΚΟΝΟΜΙΑΣ'
        cursor.execute("SELECT id FROM laws WHERE name = %s", (law_name,))
        law_id = cursor.fetchone()[0]
        
        # Διαγράφουμε τα διπλότυπα, κρατώντας μόνο το πιο πρόσφατο
        cursor.execute("""
            DELETE FROM articles a
            WHERE a.law_id = %s 
            AND a.id NOT IN (
                SELECT MAX(id)
                FROM articles
                WHERE law_id = %s
                GROUP BY law_id, number
            )
        """, (law_id, law_id))
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        # Μετράμε πόσα άρθρα έμειναν
        cursor.execute("""
            SELECT COUNT(*)
            FROM articles
            WHERE law_id = %s
        """, (law_id,))
        
        remaining_count = cursor.fetchone()[0]
        
        print(f"Διαγράφηκαν {deleted_count} διπλότυπα άρθρα")
        print(f"Έμειναν {remaining_count} μοναδικά άρθρα στον ΚΔΔ")
            
    except Exception as e:
        print(f"Σφάλμα κατά τη διαγραφή διπλοτύπων: {e}")
        conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    remove_duplicates() 