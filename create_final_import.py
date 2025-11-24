import csv
from datetime import datetime

# Ścieżki plików
input_file = r'D:\Projekty\China_customer\china_customers_oro_import_FINAL_20251120_130325.csv'
output_file = r'D:\Projekty\China_customer\china_customers_oro_import_FINAL_20251124_130325.csv'

print("="*80)
print("Tworzenie poprawnego pliku importu klientów z Chin")
print("="*80)

# Definicja: które klienci są nowi, a które już istnieją
existing_customers = {
    '500015': 'Monique.vanSlobbe@icl-group.com',  # Shanghai Mei Zhi
    '500811': 'Periklis.Evangelopoulos@icl-group.com'  # Yunnan Longbang
}

new_customers_owner = 'Fei.Gao@icl-group.com'

# Odczytaj CSV
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Znajdź indeksy kolumn
header = rows[0]

# Kolumny do aktualizacji
external_id_idx = header.index('External Id')
owner_email_idx = header.index('Owner Primary Email')
sales_org_idx = header.index('External Sales Organization Id')
ext_sys_code_idx = header.index('External System Code')
addr_ext_sys_code_idx = header.index('Addresses 1 External System Code')
name_idx = header.index('Name')

# Incoterms columns - wyczyść je wszystkie
incoterm_old_cust_id_idx = header.index('Incoterms 1 icl.incoterms.customerincotermordered.old_customer_id.label')
incoterm_id_idx = header.index('Incoterms 1 ID')
incoterm_sorting_idx = header.index('Incoterms 1 Sorting Order')
incoterm_value_idx = header.index('Incoterms 1 Incoterm Id')

print(f"\nZaktualizuję następujące wiersze:\n")

# Zaktualizuj wiersze (pomijając nagłówek)
for i in range(1, len(rows)):
    if len(rows[i]) > max(owner_email_idx, sales_org_idx, ext_sys_code_idx,
                          addr_ext_sys_code_idx, incoterm_id_idx):

        external_id = rows[i][external_id_idx]
        customer_name = rows[i][name_idx]

        # Ustal właściwego ownera
        if external_id in existing_customers:
            owner = existing_customers[external_id]
            customer_type = "ISTNIEJĄCY"
        else:
            owner = new_customers_owner
            customer_type = "NOWY"

        # Aktualizuj dane
        rows[i][owner_email_idx] = owner
        rows[i][sales_org_idx] = '001'
        rows[i][ext_sys_code_idx] = 'QAD'
        rows[i][addr_ext_sys_code_idx] = 'QAD'

        # Wyczyść wszystkie pola Incoterms
        rows[i][incoterm_old_cust_id_idx] = ''
        rows[i][incoterm_id_idx] = ''
        rows[i][incoterm_sorting_idx] = ''
        rows[i][incoterm_value_idx] = ''

        print(f"{i}. [{customer_type}] External ID: {external_id}")
        print(f"   Nazwa: {customer_name}")
        print(f"   Owner: {owner}")
        print(f"   External System Code: QAD")
        print(f"   External Sales Org: 001")
        print()

# Zapisz do nowego pliku
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"{'='*80}")
print(f"✓ Plik zapisany jako: {output_file}")
print(f"✓ Zaktualizowano {len(rows)-1} wierszy danych")
print(f"\n{'='*80}")
print("PODSUMOWANIE ZMIAN:")
print("  1. External System Code → QAD (wszystkie)")
print("  2. External Sales Organization Id → 001 (wszystkie)")
print("  3. Addresses 1 External System Code → QAD (wszystkie)")
print("  4. Owner Email:")
print("     - 2 istniejących: zachowano oryginalnych ownerów")
print("     - 4 nowych: Fei.Gao@icl-group.com")
print("  5. Incoterms: wszystkie pola wyczyszczone (błędy naprawione)")
print(f"{'='*80}")
