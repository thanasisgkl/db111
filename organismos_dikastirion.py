import re
import pandas as pd
from database import get_db_connection


def clean_text(text):
    # Αφαιρούμε ειδικούς χαρακτήρες και κενές γραμμές
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def process_articles():
    try:
        # Διαβάζουμε το αρχείο
        with open('Κώδικας-Οργανισμού-Δικαστηρίων.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        
        print("Διάβασα το αρχείο")
        
        # Καθαρίζουμε το κείμενο
        text = clean_text(text)
        print("Καθάρισα το κείμενο")
        
        # Βρίσκουμε τα άρθρα
        pattern = (r'Αρθρο:\s*(\d+).*?(?:Τίτλος\s*Αρθρου\s*(.*?))?'
                  r'(?:Λήμματα|Σχόλια|Κείμενο\s*Αρθρου).*?'
                  r'(?:Κείμενο\s*Αρθρου\s*(.*?)(?=Αρθρο:|$)|$)')
        articles = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        
        print(f"Βρήκα {len(articles)} άρθρα")
        
        # Δημιουργούμε το DataFrame
        data = []
        for article in articles:
            number = article[0].strip()
            title = article[1].strip() if article[1] else None
            content = article[2].strip() if article[2] else None
            
            # Αν δεν υπάρχει τίτλος, χρησιμοποιούμε την περιγραφή
            if not title and content:
                # Προσπαθούμε να βρούμε την "Περιγραφή όρου θησαυρού"
                description_pattern = r'Περιγραφή\s*όρου\s*θησαυρού\s*(.*?)(?=\n|$)'
                description_match = re.search(description_pattern, content, 
                                           re.IGNORECASE)
                if description_match:
                    title = description_match.group(1).strip()
                else:
                    # Εναλλακτικά χρησιμοποιούμε τους πρώτους 100 χαρακτήρες
                    title = content[:100]
            
            data.append({
                'article_number': number,
                'title': title,
                'content': content
            })
        
        df = pd.DataFrame(data)
        print("Δημιούργησα το DataFrame")
        
        # Αποθηκεύουμε σε CSV
        df.to_csv('organismos_dikastirion.csv', index=False, encoding='utf-8')
        print("Αποθήκευσα το CSV")
        
        # Εισάγουμε στη βάση δεδομένων
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Βρίσκουμε το ID του νόμου
            law_name = 'ΚΩΔΙΚΑΣ ΟΡΓΑΝΙΣΜΟΥ ΔΙΚΑΣΤΗΡΙΩΝ'
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
                    (law_id, row['article_number'], row['title'], row['content'])
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