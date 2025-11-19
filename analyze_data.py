#!/usr/bin/env python3
"""
Script to analyze China customer data and prepare import files for Oro STG China platform
"""
import pandas as pd
import sys

def main():
    print("=" * 80)
    print("Analyzing China Customer Data")
    print("=" * 80)

    # Read the Excel file with China customer IDs
    print("\n1. Reading 'customer browse China.xlsx'...")
    try:
        china_df = pd.read_excel('customer browse China.xlsx')
        print(f"   - Found {len(china_df)} rows")
        print(f"   - Columns: {list(china_df.columns)}")
        print(f"\n   First few rows:")
        print(china_df.head())
    except Exception as e:
        print(f"   ERROR: {e}")
        return 1

    # Check if 'Customer' column exists
    if 'Customer' in china_df.columns:
        china_customer_ids = china_df['Customer'].dropna().unique()
        print(f"\n   - Found {len(china_customer_ids)} unique China customer IDs")
        print(f"   - Sample IDs: {china_customer_ids[:5]}")
    else:
        print(f"   WARNING: 'Customer' column not found!")
        print(f"   Available columns: {list(china_df.columns)}")
        # Try to find similar column
        customer_cols = [col for col in china_df.columns if 'customer' in col.lower() or 'id' in col.lower()]
        if customer_cols:
            print(f"   Possible customer columns: {customer_cols}")
        return 1

    # Read customer.csv
    print("\n2. Reading 'customer.csv'...")
    try:
        customers_df = pd.read_csv('customer.csv')
        print(f"   - Found {len(customers_df)} customers")
        print(f"   - Columns: {list(customers_df.columns)[:10]}... ({len(customers_df.columns)} total)")
    except Exception as e:
        print(f"   ERROR: {e}")
        return 1

    # Read addresses.csv
    print("\n3. Reading 'addresses.csv'...")
    try:
        addresses_df = pd.read_csv('addresses.csv')
        print(f"   - Found {len(addresses_df)} addresses")
        print(f"   - Columns: {list(addresses_df.columns)[:10]}... ({len(addresses_df.columns)} total)")
    except Exception as e:
        print(f"   ERROR: {e}")
        return 1

    # Read import template
    print("\n4. Reading import template...")
    try:
        template_df = pd.read_csv('import_template_2025_11_19_13_20_13_691dc40d472f7.csv')
        print(f"   - Template has {len(template_df.columns)} columns")
        print(f"   - Sample columns: {list(template_df.columns)[:10]}...")
    except Exception as e:
        print(f"   ERROR: {e}")
        return 1

    # Filter China customers from customer.csv
    print("\n5. Filtering China customers...")
    # Try matching by 'External Id' column which seems to be the customer ID
    if 'External Id' in customers_df.columns:
        china_customers = customers_df[customers_df['External Id'].isin(china_customer_ids)]
        print(f"   - Found {len(china_customers)} matching customers by 'External Id'")
    elif 'Id' in customers_df.columns:
        china_customers = customers_df[customers_df['Id'].isin(china_customer_ids)]
        print(f"   - Found {len(china_customers)} matching customers by 'Id'")
    else:
        print("   ERROR: Could not find ID column in customers.csv")
        return 1

    if len(china_customers) == 0:
        print("   WARNING: No matching customers found! Trying different approach...")
        # Try to find by converting to string and matching
        china_customer_ids_str = [str(x) for x in china_customer_ids]
        if 'External Id' in customers_df.columns:
            customers_df['External Id'] = customers_df['External Id'].astype(str)
            china_customers = customers_df[customers_df['External Id'].isin(china_customer_ids_str)]
            print(f"   - Found {len(china_customers)} matching customers (string match)")

    # Filter addresses for China customers
    print("\n6. Filtering addresses for China customers...")
    if 'Customer Id' in addresses_df.columns and len(china_customers) > 0:
        china_customer_db_ids = china_customers['Id'].unique()
        china_addresses = addresses_df[addresses_df['Customer Id'].isin(china_customer_db_ids)]
        print(f"   - Found {len(china_addresses)} addresses for China customers")
    else:
        print("   ERROR: Could not match addresses")
        china_addresses = pd.DataFrame()

    print("\n" + "=" * 80)
    print("Summary:")
    print("=" * 80)
    print(f"China Customer IDs from Excel: {len(china_customer_ids)}")
    print(f"Matching Customers found: {len(china_customers)}")
    print(f"Matching Addresses found: {len(china_addresses)}")
    print("\n")

    if len(china_customers) > 0:
        print("Sample China customer:")
        print(china_customers.iloc[0][['Id', 'Name', 'External Id', 'Country ISO2 code']].to_dict())

    return 0

if __name__ == '__main__':
    sys.exit(main())
