#!/usr/bin/env python3
"""
Detailed analysis of China customer data
"""
import pandas as pd

def main():
    # Read Excel with all customer info
    print("=" * 80)
    print("DETAILED ANALYSIS OF CHINA CUSTOMERS")
    print("=" * 80)

    china_df = pd.read_excel('customer browse China.xlsx')
    customers_df = pd.read_csv('customer.csv', low_memory=False)

    print(f"\n1. China Customer Excel file has {len(china_df)} rows")
    print(f"   Columns: {list(china_df.columns[:20])}...\n")

    # Check for 'Site' or 'Domain' columns
    if 'Site' in china_df.columns:
        print(f"   Sites found: {china_df['Site'].unique()}")

    if 'Domain' in china_df.columns:
        print(f"   Domains found: {china_df['Domain'].unique()}")

    # Analyze customer types
    if 'Type' in china_df.columns:
        print(f"\n   Customer Types in Excel:")
        print(china_df['Type'].value_counts())

    # Check 'External System Code' in customer.csv
    print(f"\n2. Customer.csv External System Codes:")
    if 'External System Code' in customers_df.columns:
        print(customers_df['External System Code'].value_counts())

    # Find which External IDs exist in customer.csv
    print(f"\n3. Checking which China IDs exist in customer.csv...")

    china_ids_str = [str(int(x)) if isinstance(x, (int, float)) else str(x) for x in china_df['Customer'].dropna().unique()]

    # Get all External IDs from customer.csv that might match
    customers_df['External Id Clean'] = customers_df['External Id'].astype(str).str.strip()

    matched_count = 0
    missing_ids = []

    for china_id in china_ids_str:
        matches = customers_df[
            (customers_df['External Id Clean'] == china_id) |
            (customers_df['External Id Clean'].str.startswith(china_id + 'D')) |
            (customers_df['External Id Clean'].str.startswith(china_id + 'S')) |
            (customers_df['External Id Clean'].str.startswith(china_id + 'B'))
        ]

        if len(matches) > 0:
            matched_count += 1
        else:
            missing_ids.append(china_id)

    print(f"\n   ✓ Matched: {matched_count} out of {len(china_ids_str)}")
    print(f"   ✗ Missing: {len(missing_ids)}")

    if len(missing_ids) > 0:
        print(f"\n   Missing IDs (first 10): {missing_ids[:10]}")

    # Check Article data file
    try:
        print(f"\n4. Checking 'Article data ICLink China.xlsx'...")
        article_df = pd.read_excel('Article data ICLink China.xlsx')
        print(f"   - Found {len(article_df)} rows")
        print(f"   - Columns: {list(article_df.columns)}")
    except Exception as e:
        print(f"   ERROR reading Article data: {e}")

    # Get full info about matched customers
    print(f"\n5. Matched Customers Details:")
    matched_customers_df = pd.read_csv('china_customers_filtered.csv')
    print(matched_customers_df[['Id', 'Name', 'External Id', 'Country ISO2 code', 'External System Code', 'Group Name']].to_string())

    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()
