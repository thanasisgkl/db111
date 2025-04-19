import re
import pandas as pd
from datetime import datetime
from database import get_db_connection


def clean_text(text):
    # Αφαίρεση πολλαπλών κενών γραμμών
    text = re.sub(r'\n\s*\n', '\n', text)
    # Αφαίρεση κενών στην αρχή και το τέλος
    text = text.strip()
    return text


def process_articles():
    try:
        # Διάβασμα ολόκληρου του αρχείου
        with open('Πτωχευτικός-Κώδικας.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        
        print("Διάβασα το αρχείο")
        
        # Καθαρισμός κειμένου
        content = clean_text(content)
        print("Καθάρισα το κείμενο")
        
        # Εύρεση όλων των άρθρων με το νέο pattern
        pattern = (
            r'\s*Αρθρο:\s*(\d+[Α-Ω]*)\s*\n'
            r'Ημ/νία:[^\n]*\n'
            r'Περιγραφή όρου θησαυρού:[^\n]*\n'
            r'(?:Τίτλος Αρθρου\s*([^\n]*)\s*\n)?'
            r'(?:Σχόλια[^\n]*(?:\n(?!Αρθρο:|Κείμενο Αρθρου)[^\n]*)*\s*\n)?'
            r'Κείμενο Αρθρου\s*\n'
            r'((?:(?!Αρθρο:)[^\n]*(?:\n(?!Αρθρο:)[^\n]*)*)*)'
        )
        
        articles_text = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        # Λίστες για αποθήκευση των δεδομένων
        article_numbers = []
        titles = []
        contents = []
        
        for article_number, title, content in articles_text:
            # Καθαρισμός περιεχομένου
            content = clean_text(content)
            
            # Έλεγχος αν το άρθρο έχει καταργηθεί
            if (
                "καταργήθηκε" in content.lower() or 
                "κατηργήθη" in content.lower() or
                "κατηργήθηκε" in content.lower() or
                "Το παρόν κατηργήθη" in content or
                "Το παρόν καταργήθηκε" in content
            ):
                content = "ΚΑΤΑΡΓΗΘΗΚΕ"
            
            article_numbers.append(article_number)
            titles.append(title if title else "")
            contents.append(content)
        
        # Δημιουργία DataFrame
        df = pd.DataFrame({
            'article_number': article_numbers,
            'title': titles,
            'content': contents
        })
        
        # Ταξινόμηση με βάση τον αριθμό άρθρου
        df['sort_key'] = df['article_number'].apply(
            lambda x: float(re.sub(r'[Α-Ω]', '.1', x))
        )
        df = df.sort_values('sort_key')
        df = df.drop('sort_key', axis=1)
        
        print(f"Βρέθηκαν {len(df)} άρθρα")
        
        # Αποθήκευση σε CSV
        df.to_csv('ptoxeutikos.csv', index=False, encoding='utf-8')
        print("Αποθήκευσα το CSV")
        
        # Εισαγωγή στη βάση δεδομένων
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Έλεγχος αν υπάρχει ο νόμος
            cursor.execute(
                "SELECT id FROM laws WHERE name = 'ΠΤΩΧΕΥΤΙΚΟΣ ΚΩΔΙΚΑΣ'"
            )
            result = cursor.fetchone()
            
            if result is None:
                # Εισαγωγή νέου νόμου
                cursor.execute(
                    "INSERT INTO laws (name, created_at) VALUES (%s, %s) RETURNING id",
                    ('ΠΤΩΧΕΥΤΙΚΟΣ ΚΩΔΙΚΑΣ', datetime.now())
                )
                law_id = cursor.fetchone()[0]
            else:
                law_id = result[0]
                # Διαγραφή υπαρχόντων άρθρων
                cursor.execute(
                    "DELETE FROM articles WHERE law_id = %s", (law_id,)
                )
            
            # Εισαγωγή άρθρων
            for _, row in df.iterrows():
                cursor.execute(
                    """INSERT INTO articles (law_id, number, title, content) 
                    VALUES (%s, %s, %s, %s)""",
                    (law_id, row['article_number'], row['title'], row['content'])
                )
            
            conn.commit()
            print(f"Εισήχθησαν {len(df)} άρθρα στη βάση δεδομένων")
            
        except Exception as e:
            print(f"Σφάλμα κατά την εισαγωγή δεδομένων: {str(e)}")
            conn.rollback()
        finally:
            if conn:
                cursor.close()
                conn.close()
                
    except Exception as e:
        print(f"Σφάλμα: {e}")


if __name__ == "__main__":
    process_articles() 