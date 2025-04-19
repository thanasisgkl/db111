import psycopg2
from psycopg2 import Error

def get_db_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="Damiani13",  # Αλλάξτε το αν έχετε διαφορετικό κωδικό
            host="localhost",
            port="5432",
            database="casewise_db"
        )
        return connection
    except Error as e:
        print(f"Σφάλμα κατά τη σύνδεση με τη βάση δεδομένων: {e}")
        return None

def init_db():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Δημιουργία πίνακα laws
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS laws (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Δημιουργία πίνακα articles
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id SERIAL PRIMARY KEY,
                    law_id INTEGER REFERENCES laws(id),
                    number VARCHAR(50) NOT NULL,
                    title TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            connection.commit()
            print("Η βάση δεδομένων δημιουργήθηκε επιτυχώς!")
            
        except Error as e:
            print(f"Σφάλμα κατά τη δημιουργία των πινάκων: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

if __name__ == "__main__":
    init_db() 