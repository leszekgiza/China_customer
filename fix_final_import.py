import csv
from datetime import datetime

# Ścieżki plików
input_file = r'D:\Projekty\China_customer\china_customers_oro_import_FINAL_20251120_130325.csv'
output_file = r'D:\Projekty\China_customer\china_customers_oro_import_FINAL_20251124_130325.csv'

print("="*80)
print("Naprawa pliku importu klientów z Chin")
print("="*80)

# Odczytaj CSV
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Znajdź indeksy kolumn
header = rows[0]

# Kolumny do aktualizacji
owner_email_idx = header.index('Owner Primary Email')
sales_org_idx = header.index('External Sales Organization Id')
ext_sys_code_idx = header.index('External System Code')
addr_ext_sys_code_idx = header.index('Addresses 1 External System Code')

# Incoterms columns - wyczyść je wszystkie
incoterm_old_cust_id_idx = header.index('Incoterms 1 icl.incoterms.customerincotermordered.old_customer_id.label')
incoterm_id_idx = header.index('Incoterms 1 ID')
incoterm_sorting_idx = header.index('Incoterms 1 Sorting Order')
incoterm_value_idx = header.index('Incoterms 1 Incoterm Id')

print(f"\nZnalezione kolumny:")
print(f"  Owner Primary Email: kolumna {owner_email_idx}")
print(f"  External Sales Organization Id: kolumna {sales_org_idx}")
print(f"  External System Code: kolumna {ext_sys_code_idx}")
print(f"  Addresses 1 External System Code: kolumna {addr_ext_sys_code_idx}")
print(f"  Incoterms 1 ID: kolumna {incoterm_id_idx}")
print()

# Zaktualizuj wiersze (pomijając nagłówek)
for i in range(1, len(rows)):
    if len(rows[i]) > max(owner_email_idx, sales_org_idx, ext_sys_code_idx,
                          addr_ext_sys_code_idx, incoterm_id_idx):
        # Podstawowe zmiany wymagane
        rows[i][owner_email_idx] = 'Fei.Gao@icl-group.com'
        rows[i][sales_org_idx] = '001 WH - El Heerlen'
        rows[i][ext_sys_code_idx] = 'QAD'
        rows[i][addr_ext_sys_code_idx] = 'QAD'

        # Wyczyść wszystkie pola Incoterms (to rozwiąże błędy walidacji)
        rows[i][incoterm_old_cust_id_idx] = ''
        rows[i][incoterm_id_idx] = ''  # To pole miało "DAP" - musi być puste lub integer
        rows[i][incoterm_sorting_idx] = ''
        rows[i][incoterm_value_idx] = ''

        print(f"  ✓ Wiersz {i} zaktualizowany")

# Zapisz do nowego pliku
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"\n{'='*80}")
print(f"✓ Plik zapisany jako: {output_file}")
print(f"✓ Zaktualizowano {len(rows)-1} wierszy danych")
print(f"\n{'='*80}")
print("Wprowadzone zmiany:")
print("  1. Owner Primary Email → Fei.Gao@icl-group.com")
print("  2. External Sales Organization Id → 001 WH - El Heerlen")
print("  3. External System Code → QAD")
print("  4. Addresses 1 External System Code → QAD")
print("  5. Wszystkie pola Incoterms → PUSTE (usunięto nieprawidłowe wartości)")
print(f"{'='*80}")
print("\nPlik gotowy do importu!")
