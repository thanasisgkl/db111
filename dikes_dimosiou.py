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
        with open('Κώδικας-Δικών-Δημοσίου.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Κρατάμε μόνο τις γραμμές 18-696
        article_lines = lines[17:696]  # -1 γιατί οι γραμμές ξεκινούν από 0
        text = ''.join(article_lines)
        
        print("Διάβασα το αρχείο")
        
        # Καθαρίζουμε το κείμενο
        text = clean_text(text)
        print("Καθάρισα το κείμενο")
        
        # Βρίσκουμε τα άρθρα με το σωστό pattern
        pattern = r'Αρθρο:\s*(\d+).*?(?:Περιγραφή όρου θησαυρού:.*?)?(?:Τίτλος Αρθρου\s*(.*?)\s*)?(?:Σχόλια.*?)?Κείμενο Αρθρου\s*(.*?)(?=Αρθρο:|$)'
        articles = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        
        print(f"Βρήκα {len(articles)} άρθρα")
        
        # Δημιουργούμε το DataFrame
        data = []
        for article in articles:
            number = article[0].strip()
            
            # Αν δεν υπάρχει τίτλος, χρησιμοποιούμε την Περιγραφή όρου θησαυρού
            title = article[1].strip() if article[1] else None
            content = article[2].strip() if article[2] else None
            
            # Αν δεν έχουμε τίτλο, ψάχνουμε για Περιγραφή όρου θησαυρού
            if not title and content:
                thesaurus_match = re.search(r'Περιγραφή όρου θησαυρού:\s*(.*?)(?=\s*(?:Τίτλος Αρθρου|Κείμενο Αρθρου))', text, re.DOTALL)
                if thesaurus_match:
                    title = thesaurus_match.group(1).strip()
                else:
                    # Αν δεν βρούμε ούτε αυτό, χρησιμοποιούμε την αρχή του περιεχομένου
                    title = content[:100]
            
            data.append({
                'article_number': number,
                'title': title,
                'content': content
            })
        
        df = pd.DataFrame(data)
        print("Δημιούργησα το DataFrame")
        
        # Αποθηκεύουμε σε CSV
        df.to_csv('dikes_dimosiou.csv', index=False, encoding='utf-8')
        print("Αποθήκευσα το CSV")
        
        # Εισάγουμε στη βάση δεδομένων
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Βρίσκουμε το ID του νόμου
            cursor.execute("SELECT id FROM laws WHERE name = 'ΚΩΔΙΚΑΣ ΔΙΚΩΝ ΔΗΜΟΣΙΟΥ'")
            law_id = cursor.fetchone()
            
            if not law_id:
                # Αν δεν υπάρχει ο νόμος, τον προσθέτουμε
                cursor.execute(
                    "INSERT INTO laws (name) VALUES ('ΚΩΔΙΚΑΣ ΔΙΚΩΝ ΔΗΜΟΣΙΟΥ') RETURNING id"
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
            cursor.close()
            conn.close()
                
    except Exception as e:
        print(f"Σφάλμα: {e}")


if __name__ == "__main__":
    process_articles() 