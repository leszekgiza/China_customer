import csv
from datetime import datetime

# Ścieżki plików
input_file = r'D:\Projekty\China_customer\china_customers_oro_import_FINAL_20251120_130325.csv'
output_file = r'D:\Projekty\China_customer\china_customers_oro_import_FINAL_20251124_130325.csv'

# Odczytaj CSV
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Znajdź indeksy kolumn
header = rows[0]
owner_email_idx = header.index('Owner Primary Email')
sales_org_idx = header.index('External Sales Organization Id')

print(f"Owner Primary Email column index: {owner_email_idx}")
print(f"External Sales Organization Id column index: {sales_org_idx}")

# Zaktualizuj wiersze (pomijając nagłówek)
for i in range(1, len(rows)):
    if len(rows[i]) > max(owner_email_idx, sales_org_idx):
        rows[i][owner_email_idx] = 'Fei.Gao@icl-group.com'
        rows[i][sales_org_idx] = '001 WH - El Heerlen'

# Zapisz do nowego pliku
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"\nPlik został zapisany jako: {output_file}")
print(f"Zaktualizowano {len(rows)-1} wierszy danych")
