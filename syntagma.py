import re
import pandas as pd
from database import get_db_connection

def clean_text(text):
    # Αφαιρούμε περιττά κενά διατηρώντας τις αλλαγές γραμμής
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def process_articles():
    try:
        # Διαβάζουμε το αρχείο
        with open('syntagma1_1.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        
        print("Διάβασα το αρχείο")
        
        # Παίρνουμε μόνο το κείμενο μετά τη γραμμή 481
        lines = text.split('\n')
        text = '\n'.join(lines[479:])  # Ξεκινάμε από το ΤΜΗΜΑ Α'
        
        # Καθαρίζουμε το κείμενο
        text = clean_text(text)
        print("Καθάρισα το κείμενο")
        
        # Βρίσκουμε τα τμήματα και τα άρθρα τους
        sections = []
        current_section = None
        current_section_desc = None
        
        # Χωρίζουμε το κείμενο σε γραμμές για να βρούμε τα τμήματα
        lines = text.split('\n')
        current_text = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Έλεγχος για νέο τμήμα
            tmima_match = re.match(r'(?:TMHMA|ΤΜΗΜΑ)\s+([Α-Ω]\'?)', line, re.IGNORECASE)
            if tmima_match:
                if current_section and current_text:
                    sections.append((current_section, current_section_desc, '\n'.join(current_text)))
                current_section = tmima_match.group(1)
                current_section_desc = None
                current_text = []
                continue
                
            # Η επόμενη μη-κενή γραμμή μετά το ΤΜΗΜΑ είναι η περιγραφή του
            if current_section and not current_section_desc:
                current_section_desc = line
                continue
                
            current_text.append(line)
            
        # Προσθέτουμε και το τελευταίο τμήμα
        if current_section and current_text:
            sections.append((current_section, current_section_desc, '\n'.join(current_text)))
        
        # Επεξεργαζόμαστε κάθε τμήμα για να βρούμε τα άρθρα του
        data = []
        for section_num, section_desc, section_text in sections:
            # Βρίσκουμε τα άρθρα στο τρέχον τμήμα
            pattern = r'Άρθρo[:]?\s+(\d+)[^\n]*\n((?:(?!Άρθρo[:]?\s+\d+).)*)'
            articles = re.findall(pattern, section_text, re.DOTALL | re.IGNORECASE)
            
            for article in articles:
                number = article[0].strip()
                content = article[1].strip()
                
                # Χωρίζουμε το περιεχόμενο σε παραγράφους
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                
                # Αφαιρούμε τις ερμηνευτικές δηλώσεις και σχόλια
                main_content = []
                for p in paragraphs:
                    if p.startswith('**Ερμηνευτική δήλωση') or p.startswith('Ερμηνευτική δήλωση'):
                        break
                    if p.startswith('**') or p.startswith('Σχόλια'):
                        break
                    main_content.append(p)
                
                # Το πλήρες περιεχόμενο χωρίς ερμηνευτικές δηλώσεις
                content = '\n\n'.join(main_content)
                
                # Ο τίτλος είναι "ΤΜΗΜΑ Χ' - Περιγραφή"
                title = f"ΤΜΗΜΑ {section_num} - {section_desc}"
                
                data.append({
                    'article_number': number,
                    'title': title,
                    'content': content
                })
        
        df = pd.DataFrame(data)
        print(f"Βρήκα {len(df)} άρθρα σε {len(sections)} τμήματα")
        
        # Αποθηκεύουμε σε CSV
        df.to_csv('syntagma.csv', index=False, encoding='utf-8')
        print("Αποθήκευσα το CSV")
        
        # Εισάγουμε στη βάση δεδομένων
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Βρίσκουμε το ID του νόμου
            cursor.execute("SELECT id FROM laws WHERE name = 'ΣΥΝΤΑΓΜΑ'")
            law_id = cursor.fetchone()
            
            if not law_id:
                # Αν δεν υπάρχει ο νόμος, τον προσθέτουμε
                cursor.execute(
                    "INSERT INTO laws (name) VALUES ('ΣΥΝΤΑΓΜΑ') RETURNING id"
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