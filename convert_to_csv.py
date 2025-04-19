import codecs
import re


def convert_txt_to_csv():
    # Ορισμός των αρχείων εισόδου και εξόδου
    input_file = 'ΠΟΙΝΙΚΟΣ ΚΩΔΙΚΑΣ.txt'
    output_file = 'penal_codes_new.csv'
    
    # Διάβασμα του αρχείου κειμένου με διαφορετικές κωδικοποιήσεις
    encodings = ['utf-8', 'utf-8-sig', 'cp1253', 'iso-8859-7']
    content = None
    
    for encoding in encodings:
        try:
            with codecs.open(input_file, 'r', encoding=encoding) as f:
                content = f.read()
                break
        except UnicodeDecodeError:
            continue

    if content is None:
        error_msg = (
            "Δεν ήταν δυνατή η ανάγνωση του αρχείου με καμία από τις "
            "υποστηριζόμενες κωδικοποιήσεις"
        )
        raise ValueError(error_msg)
    
    # Καθαρισμός του κειμένου από μη εκτυπώσιμους χαρακτήρες
    content = re.sub(r'[^\x20-\x7E\u0370-\u03FF\n]', '', content)
    
    # Εύρεση όλων των άρθρων με βελτιωμένο pattern
    pattern = r'Αρθρο:\s*(\d+)\s*Ημ/νία:.*?Τίτλος\s*Αρθρου\s*(.*?)(?:Λήμματα.*?)?(?:Σχόλια.*?)?Κείμενο\s*Αρθρου\s*(.*?)(?=\s*Αρθρο:|$)'
    articles = re.findall(pattern, content, re.DOTALL)
    
    # Εγγραφή στο CSV αρχείο
    with codecs.open(output_file, 'w', encoding='utf-8-sig') as f:
        f.write('Αριθμός Άρθρου,Τίτλος,Κείμενο\n')
        for number, title, text in articles:
            # Καθαρισμός τίτλου και κειμένου
            title = re.sub(r'[^\x20-\x7E\u0370-\u03FF]', '', title)
            title = title.strip()
            title = title.replace('"', '""')
            # Αφαίρεση των Λημμάτων και Σχολίων από τον τίτλο
            title = re.sub(r'Λήμματα.*?(?=Κείμενο|$)', '', title)
            title = re.sub(r'Σχόλια.*?(?=Κείμενο|$)', '', title)

            text = re.sub(r'[^\x20-\x7E\u0370-\u03FF\n]', '', text)
            text = text.strip()
            text = text.replace('"', '""')
            
            # Εγγραφή στο CSV μόνο αν έχουμε έγκυρο αριθμό άρθρου
            if number.strip():
                f.write(f'{number},"{title}","{text}"\n')


if __name__ == '__main__':
    convert_txt_to_csv() 