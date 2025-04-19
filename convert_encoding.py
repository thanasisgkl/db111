import csv

# Διάβασμα του αρχικού CSV με την σωστή κωδικοποίηση
with open('penal_codes_new.csv', 'r', encoding='cp1253', errors='replace') as input_file:
    # Δημιουργία του νέου CSV με UTF-8 κωδικοποίηση
    with open('penal_codes_utf8.csv', 'w', encoding='utf-8', newline='') as output_file:
        csv_reader = csv.reader(input_file, delimiter=';')
        csv_writer = csv.writer(output_file, delimiter=';')
        
        # Αντιγραφή των δεδομένων
        for row in csv_reader:
            csv_writer.writerow(row) 