#!/usr/bin/env python3
"""
Script to match China customers with fuzzy matching on External ID
"""
import pandas as pd
import re

def main():
    # Read data
    china_df = pd.read_excel('customer browse China.xlsx')
    customers_df = pd.read_csv('customer.csv', low_memory=False)
    addresses_df = pd.read_csv('addresses.csv', low_memory=False)

    # Get China customer IDs
    china_customer_ids = china_df['Customer'].dropna().unique()
    print(f"China Customer IDs from Excel: {len(china_customer_ids)}")
    print(f"Sample IDs: {list(china_customer_ids[:10])}\n")

    # Convert to string for matching
    china_customer_ids_str = [str(int(x)) if isinstance(x, (int, float)) else str(x) for x in china_customer_ids]

    # Try to find customers with fuzzy matching
    # External ID might have suffix like "D", "S", "B", etc.
    print("Searching for customers with fuzzy matching...")

    matched_customers = []
    for china_id in china_customer_ids_str:
        # Try exact match first
        exact_match = customers_df[customers_df['External Id'].astype(str) == china_id]

        if len(exact_match) > 0:
            matched_customers.append(exact_match)
            print(f"  ✓ {china_id}: Exact match found")
        else:
            # Try fuzzy match (ID might have suffix)
            fuzzy_match = customers_df[customers_df['External Id'].astype(str).str.startswith(china_id)]
            if len(fuzzy_match) > 0:
                matched_customers.append(fuzzy_match)
                print(f"  ✓ {china_id}: Fuzzy match found ({len(fuzzy_match)} matches)")
                for idx, row in fuzzy_match.iterrows():
                    print(f"      - External Id: {row['External Id']}, Name: {row['Name']}")
            else:
                print(f"  ✗ {china_id}: No match found")

    if matched_customers:
        china_customers = pd.concat(matched_customers, ignore_index=True)
        print(f"\n✓ Total matched customers: {len(china_customers)}")

        # Get addresses for these customers
        china_customer_db_ids = china_customers['Id'].unique()
        china_addresses = addresses_df[addresses_df['Customer Id'].isin(china_customer_db_ids)]
        print(f"✓ Total matched addresses: {len(china_addresses)}")

        # Save intermediate results
        china_customers.to_csv('china_customers_filtered.csv', index=False)
        china_addresses.to_csv('china_addresses_filtered.csv', index=False)

        print(f"\n✓ Saved intermediate files:")
        print(f"  - china_customers_filtered.csv ({len(china_customers)} rows)")
        print(f"  - china_addresses_filtered.csv ({len(china_addresses)} rows)")

        return 0
    else:
        print("\n✗ No customers matched!")
        return 1

if __name__ == '__main__':
    exit(main())
