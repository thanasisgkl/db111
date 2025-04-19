import re
import pandas as pd
from database import get_db_connection


def clean_text(text):
    # Αφαιρούμε περιττά κενά διατηρώντας τις αλλαγές γραμμής
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text


def process_articles():
    try:
        # Διαβάζουμε το αρχείο
        all_lines = []
        with open('kwdikas_dikigorwn.txt', 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, 1):
                if 261 <= i <= 4270:  # Διορθώνουμε το εύρος γραμμών
                    all_lines.append(line)
        
        text = ''.join(all_lines)
        print("Διάβασα το αρχείο")
        
        # Καθαρίζουμε το κείμενο
        text = clean_text(text)
        print("Καθάρισα το κείμενο")
        
        # Βρίσκουμε τα άρθρα
        pattern = (
            r'Αρθρο:\s*(\d+)\s*\n'          # Αριθμός άρθρου
            r'Ημ/νία:[^\n]*\n'              # Αγνοούμε την ημερομηνία
            r'([^\n]+)'                      # Τίτλος (μία γραμμή)
            r'(.*?)(?=\nΑρθρο:|$)'          # Περιεχόμενο μέχρι το επόμενο άρθρο
        )
        
        articles = re.findall(pattern, text, re.DOTALL)
        print(f"Βρήκα {len(articles)} άρθρα")
        
        # Δημιουργούμε το DataFrame
        data = []
        for article in articles:
            number = article[0].strip()
            title = article[1].strip()
            content = article[2].strip()
            
            # Καθαρίζουμε το περιεχόμενο από τυχόν επικεφαλίδες κεφαλαίων
            content = re.sub(r'^(?:ΚΕΦΑΛΑΙΟ|ΤΜΗΜΑ)[^\n]*\n', '', content)
            content = re.sub(r'^(?:Γενικό\s+Μέρος\s*\n)', '', content)
            
            data.append({
                'article_number': number,
                'title': title,
                'content': content
            })
        
        df = pd.DataFrame(data)
        print("Δημιούργησα το DataFrame")
        
        # Αποθηκεύουμε σε CSV
        df.to_csv('kwdikas_dikigorwn.csv', index=False, encoding='utf-8')
        print("Αποθήκευσα το CSV")
        
        # Εισάγουμε στη βάση δεδομένων
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Βρίσκουμε το ID του νόμου
            law_name = 'ΚΩΔΙΚΑΣ ΔΙΚΗΓΟΡΩΝ'
            cursor.execute("SELECT id FROM laws WHERE name = %s", (law_name,))
            law_id = cursor.fetchone()
            
            if not law_id:
                # Αν δεν υπάρχει ο νόμος, τον προσθέτουμε
                cursor.execute(
                    "INSERT INTO laws (name) VALUES (%s) RETURNING id",
                    (law_name,)
                )
                law_id = cursor.fetchone()[0]
            else:
                law_id = law_id[0]
            
            # Εισάγουμε τα άρθρα
            for _, row in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO articles (law_id, number, title, content) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (law_id, row['article_number'], row['title'], 
                     row['content'])
                )
            
            conn.commit()
            print(f"Εισήχθησαν {len(df)} άρθρα στη βάση δεδομένων")
            
        except Exception as e:
            print(f"Σφάλμα κατά την εισαγωγή στη βάση δεδομένων: {e}")
            conn.rollback()
        finally:
            if conn:
                cursor.close()
                conn.close()
                
    except Exception as e:
        print(f"Σφάλμα: {e}")


if __name__ == "__main__":
    process_articles() 