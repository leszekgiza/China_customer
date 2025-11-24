import csv
from datetime import datetime

# Ścieżki plików
input_file = r'D:\Projekty\China_customer\china_customers_oro_import_FINAL_20251124_152349.csv'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = rf'D:\Projekty\China_customer\china_customers_oro_import_FINAL_{timestamp}.csv'

print("="*80)
print("Dodawanie Incoterms do pliku importu klientów z Chin")
print("="*80)

# Odczytaj CSV
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Znajdź indeksy kolumn
header = rows[0]

external_id_idx = header.index('External Id')
name_idx = header.index('Name')

# Incoterms columns
incoterm_old_cust_id_idx = header.index('Incoterms 1 icl.incoterms.customerincotermordered.old_customer_id.label')
incoterm_id_idx = header.index('Incoterms 1 ID')
incoterm_sorting_idx = header.index('Incoterms 1 Sorting Order')
incoterm_value_idx = header.index('Incoterms 1 Incoterm Id')

print(f"\nDodaję Incoterms dla klientów:\n")

# Zaktualizuj wiersze (pomijając nagłówek)
for i in range(1, len(rows)):
    if len(rows[i]) > max(external_id_idx, incoterm_value_idx):
        external_id = rows[i][external_id_idx]
        customer_name = rows[i][name_idx]

        # Ustaw Incoterms - DAP dla wszystkich
        rows[i][incoterm_value_idx] = 'DAP'  # Incoterm code
        rows[i][incoterm_sorting_idx] = '1'   # Sorting order
        rows[i][incoterm_id_idx] = ''         # Leave ID empty (auto-generated)
        rows[i][incoterm_old_cust_id_idx] = '' # Leave empty

        print(f"{i}. {customer_name} (External ID: {external_id})")
        print(f"   Incoterms 1 Incoterm Id: DAP")
        print(f"   Incoterms 1 Sorting Order: 1")
        print()

# Zapisz do nowego pliku
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"{'='*80}")
print(f"Plik zapisany jako: {output_file}")
print(f"Zaktualizowano {len(rows)-1} wierszy danych")
print(f"\n{'='*80}")
print("DODANE DANE:")
print("  Incoterms 1 Incoterm Id: DAP (dla wszystkich 6 klientów)")
print("  Incoterms 1 Sorting Order: 1")
print(f"{'='*80}")
