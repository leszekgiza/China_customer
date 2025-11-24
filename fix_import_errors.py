import csv

# Ścieżki plików
input_file = r'D:\Projekty\China_customer\china_customers_oro_import_FINAL_20251120_130325.csv'
output_file = r'D:\Projekty\China_customer\china_customers_oro_import_FINAL_20251124_130325.csv'

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
external_id_idx = header.index('External Id')

# Incoterms columns
incoterm_old_cust_id_idx = header.index('Incoterms 1 icl.incoterms.customerincotermordered.old_customer_id.label')
incoterm_id_idx = header.index('Incoterms 1 ID')
incoterm_sorting_idx = header.index('Incoterms 1 Sorting Order')
incoterm_value_idx = header.index('Incoterms 1 Incoterm Id')

print(f"Indeksy kolumn:")
print(f"  Owner Primary Email: {owner_email_idx}")
print(f"  External Sales Organization Id: {sales_org_idx}")
print(f"  External System Code: {ext_sys_code_idx}")
print(f"  Addresses 1 External System Code: {addr_ext_sys_code_idx}")
print(f"  External Id: {external_id_idx}")
print(f"  Incoterms 1 old_customer_id: {incoterm_old_cust_id_idx}")
print(f"  Incoterms 1 ID: {incoterm_id_idx}")
print(f"  Incoterms 1 Sorting Order: {incoterm_sorting_idx}")
print(f"  Incoterms 1 Incoterm Id: {incoterm_value_idx}")
print()

# Zaktualizuj wiersze (pomijając nagłówek)
for i in range(1, len(rows)):
    if len(rows[i]) > max(owner_email_idx, sales_org_idx, ext_sys_code_idx,
                          addr_ext_sys_code_idx, incoterm_id_idx):
        # Podstawowe zmiany
        rows[i][owner_email_idx] = 'Fei.Gao@icl-group.com'
        rows[i][sales_org_idx] = '001 WH - El Heerlen'
        rows[i][ext_sys_code_idx] = 'QAD'
        rows[i][addr_ext_sys_code_idx] = 'QAD'

        # Incoterms - ustaw wartości
        external_id = rows[i][external_id_idx]
        rows[i][incoterm_old_cust_id_idx] = external_id  # old_customer_id = External Id
        rows[i][incoterm_id_idx] = '1'  # ID as integer
        rows[i][incoterm_sorting_idx] = '1'  # Sorting order
        # Incoterm Id już ma wartość "DAP" w oryginalnym pliku

        print(f"Wiersz {i}: External Id={external_id}, Incoterm set")

# Zapisz do nowego pliku
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"\nPlik został zapisany jako: {output_file}")
print(f"Zaktualizowano {len(rows)-1} wierszy danych")
print("\nZmiany:")
print("  - Owner Primary Email -> Fei.Gao@icl-group.com")
print("  - External Sales Organization Id -> 001 WH - El Heerlen")
print("  - External System Code -> QAD")
print("  - Addresses 1 External System Code -> QAD")
print("  - Incoterms 1 ID -> 1")
print("  - Incoterms 1 Sorting Order -> 1")
print("  - Incoterms 1 old_customer_id -> External Id")
