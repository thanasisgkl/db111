import sqlite3

# Συνδεόμαστε στη βάση δεδομένων
conn = sqlite3.connect('law_db.sqlite')
cursor = conn.cursor()

# Δημιουργούμε τον πίνακα laws αν δεν υπάρχει
cursor.execute('''
    CREATE TABLE IF NOT EXISTS laws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    )
''')

# Δημιουργούμε τον πίνακα articles αν δεν υπάρχει
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER NOT NULL,
        title TEXT,
        content TEXT,
        law_id INTEGER NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        FOREIGN KEY (law_id) REFERENCES laws (id)
    )
''')

# Αποθηκεύουμε τις αλλαγές
conn.commit()
conn.close()

print("Οι πίνακες δημιουργήθηκαν επιτυχώς!") 