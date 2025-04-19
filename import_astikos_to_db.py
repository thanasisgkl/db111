import sqlite3
import pandas as pd


def import_to_database():
    # Σύνδεση στη βάση δεδομένων
    conn = sqlite3.connect('penal_codes.db')
    cursor = conn.cursor()
    
    # Διαβάζουμε το CSV αρχείο
    df = pd.read_csv('astikos_kodikas.csv', encoding='utf-8')
    
    # Εισάγουμε τα δεδομένα στη βάση
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR IGNORE INTO articles (article_number, article_text, law_id)
            VALUES (?, ?, (SELECT id FROM laws WHERE name = 'Αστικός Κώδικας'))
        ''', (row['article_number'], row['article_text']))
    
    # Αποθηκεύουμε τις αλλαγές
    conn.commit()
    print(f"Εισήχθησαν {len(df)} άρθρα στη βάση δεδομένων")
    
    # Κλείνουμε τη σύνδεση
    conn.close()


if __name__ == "__main__":
    import_to_database() 