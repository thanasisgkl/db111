import pandas as pd

# Διαβάζουμε το CSV
df = pd.read_csv('astikos_kodikas.csv', encoding='utf-8')

# Μετράμε πόσα NaN υπάρχουν στη στήλη title
nan_count = df['title'].isna().sum()
total_count = len(df)

print(f"Σύνολο άρθρων: {total_count}")
print(f"Άρθρα χωρίς τίτλο (NaN): {nan_count}")
print(f"Ποσοστό άρθρων χωρίς τίτλο: {(nan_count/total_count)*100:.2f}%")

# Εμφανίζουμε μερικά παραδείγματα άρθρων χωρίς τίτλο
print("\nΠαραδείγματα άρθρων χωρίς τίτλο:")
print(df[df['title'].isna()].head()) 