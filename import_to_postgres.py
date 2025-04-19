import psycopg2
import pandas as pd
from database import get_db_connection

def import_to_postgres():
    # Σύνδεση στη βάση δεδομένων
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Διαβάζουμε το CSV αρχείο
        df = pd.read_csv('astikos_kodikas.csv', encoding='utf-8')
        
        # Εισάγουμε πρώτα τον νόμο αν δεν υπάρχει
        cursor.execute("""
            INSERT INTO laws (name)
            VALUES ('ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ')
            ON CONFLICT (name) DO NOTHING
            RETURNING id
        """)
        
        # Παίρνουμε το ID του νόμου
        law_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None
        
        if not law_id:
            cursor.execute("SELECT id FROM laws WHERE name = 'ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ'")
            law_id = cursor.fetchone()[0]
        
        # Εισάγουμε τα άρθρα
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO articles (law_id, number, title, content)
                VALUES (%s, %s, %s, %s)
            """, (law_id, row['article_number'], row['title'], row['content']))
        
        # Αποθηκεύουμε τις αλλαγές
        conn.commit()
        print(f"Εισήχθησαν {len(df)} άρθρα στη βάση δεδομένων")
        
    except Exception as e:
        print(f"Σφάλμα κατά την εισαγωγή δεδομένων: {e}")
        conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    import_to_postgres() 