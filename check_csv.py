import pandas as pd

# Διαβάζουμε το CSV
df = pd.read_csv('astikos_kodikas.csv', encoding='utf-8')

# Εμφανίζουμε τις στήλες
print("Στήλες του CSV:")
print(df.columns.tolist())

# Εμφανίζουμε την πρώτη γραμμή
print("\nΠρώτη γραμμή:")
print(df.iloc[0]) 