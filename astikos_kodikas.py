import re
import pandas as pd
import sqlite3
from datetime import datetime

# Διαβάζουμε το αρχείο κειμένου
print("Αρχίζω την ανάγνωση του αρχείου...")
with open('ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ.txt', 'r', encoding='utf-8-sig') as file:
    text = file.read()
print(f"Μήκος κειμένου: {len(text)} χαρακτήρες")

# Καθαρίζουμε το κείμενο από περιττά κενά
print("Καθαρίζω το κείμενο...")
text = re.sub(r'\n\s*\n', '\n', text)
text = re.sub(r'\s+', ' ', text)
print(f"Μήκος κειμένου μετά τον καθαρισμό: {len(text)} χαρακτήρες")

# Βρίσκουμε όλα τα άρθρα
print("Αναζητώ άρθρα...")
pattern = (
    r'Αρθρο:\s*(\d+).*?'
    r'(?:Περιγραφή όρου θησαυρού:\s*(.*?)\s*(?=Τίτλος|Λήμματα|Κείμενο|$))?'
    r'(?:Τίτλος Αρθρου\s*(.*?)\s*(?=Λήμματα|Κείμενο|$))?'
    r'(?:Λήμματα.*?)?'
    r'(?:Κείμενο Αρθρου\s*(.*?))?'
    r'(?=Αρθρο:|$)'
)
matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
print(f"Βρέθηκαν {len(matches)} άρθρα")

# Επεξεργαζόμαστε κάθε άρθρο
print("Επεξεργάζομαι τα άρθρα...")
data = []
for article_number, description, title, content in matches:
    # Χρησιμοποιούμε την περιγραφή ως τίτλο αν δεν υπάρχει τίτλος
    final_title = title.strip() if title.strip() else description.strip()
    data.append({
        'article_number': int(article_number),
        'title': final_title,
        'content': content.strip()
    })

print(f"Επεξεργάστηκαν {len(data)} άρθρα")

# Δημιουργούμε το DataFrame
print("Δημιουργώ DataFrame...")
df = pd.DataFrame(data)

# Ταξινομούμε με βάση τον αριθμό άρθρου
df = df.sort_values('article_number')

# Αποθηκεύουμε σε CSV
print("Αποθηκεύω σε CSV...")
df.to_csv('astikos_kodikas.csv', index=False, encoding='utf-8-sig')

# Συνδεόμαστε στη βάση δεδομένων
print("Συνδέομαι στη βάση δεδομένων...")
conn = sqlite3.connect('law_db.sqlite')
cursor = conn.cursor()

# Εισάγουμε τα άρθρα στη βάση
print("Εισάγω τα άρθρα στη βάση...")
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO articles (number, title, content, law_id, created_at, updated_at)
        VALUES (?, ?, ?, 
            (SELECT id FROM laws WHERE title = 'ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ' LIMIT 1),
            ?, ?)
    ''', (
        row['article_number'],
        row['title'],
        row['content'],
        current_time,
        current_time
    ))

# Αποθηκεύουμε τις αλλαγές
conn.commit()
conn.close()

print("Ολοκληρώθηκε η εισαγωγή στη βάση δεδομένων!") 