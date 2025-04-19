import sqlite3

# Συνδεόμαστε στη βάση δεδομένων
conn = sqlite3.connect('law_db.sqlite')
cursor = conn.cursor()

# Ελέγχουμε αν υπάρχει ο ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ
cursor.execute("SELECT * FROM laws WHERE title = 'ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ'")
law = cursor.fetchone()

if law:
    print("Ο ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ βρέθηκε στη βάση:")
    print(f"ID: {law[0]}")
    print(f"Τίτλος: {law[1]}")
    print(f"Περιγραφή: {law[2]}")
else:
    print("Ο ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ δεν βρέθηκε στη βάση.")
    print("Προσθέτω τον ΑΣΤΙΚΟ ΚΩΔΙΚΑ...")
    cursor.execute('''
        INSERT INTO laws (title, description, created_at, updated_at)
        VALUES (?, ?, datetime('now'), datetime('now'))
    ''', ('ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ', 'Αστικός Κώδικας της Ελλάδας'))
    conn.commit()
    
    # Επιβεβαιώνουμε την εισαγωγή
    cursor.execute("SELECT * FROM laws WHERE title = 'ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ'")
    law = cursor.fetchone()
    print("Ο ΑΣΤΙΚΟΣ ΚΩΔΙΚΑΣ προστέθηκε στη βάση:")
    print(f"ID: {law[0]}")
    print(f"Τίτλος: {law[1]}")
    print(f"Περιγραφή: {law[2]}")

# Κλείνουμε τη σύνδεση
conn.close() 