#!/usr/bin/env python3
"""
Create Oro import CSV files for China customers (STG China platform)
"""
import pandas as pd

def create_customers_import():
    """Create customers import CSV file"""
    print("=" * 80)
    print("Creating Oro Import Files for STG China")
    print("=" * 80)

    # Read template to get column structure
    template_df = pd.read_csv('import_template_2025_11_19_13_20_13_691dc40d472f7.csv')
    template_columns = list(template_df.columns)

    print(f"\n1. Template has {len(template_columns)} columns")

    # Read filtered China customers
    china_customers = pd.read_csv('china_customers_filtered.csv')
    china_addresses = pd.read_csv('china_addresses_filtered.csv')

    print(f"2. Processing {len(china_customers)} customer records")
    print(f"3. Processing {len(china_addresses)} address records")

    # ============================================================================
    # CREATE CUSTOMERS CSV
    # ============================================================================
    print("\n" + "=" * 80)
    print("Creating Customers Import CSV")
    print("=" * 80)

    # Create empty dataframe with template columns
    customers_export = pd.DataFrame(columns=template_columns)

    # Map customer data to template columns
    # Core customer fields
    if 'Id' in china_customers.columns:
        customers_export['Id'] = china_customers['Id']
    if 'Name' in china_customers.columns:
        customers_export['Name'] = china_customers['Name']
    if 'Parent Id' in china_customers.columns:
        customers_export['Parent Id'] = china_customers['Parent Id']
    if 'Parent Name' in china_customers.columns:
        customers_export['Parent Name'] = china_customers['Parent Name']
    if 'Parent External Id' in china_customers.columns:
        customers_export['Parent External Id'] = china_customers['Parent External Id']
    if 'Parent Country ISO2 code' in china_customers.columns:
        customers_export['Parent Country ISO2 code'] = china_customers['Parent Country ISO2 code']
    if 'Group Name' in china_customers.columns:
        customers_export['Group Name'] = china_customers['Group Name']
    if 'Owner Id' in china_customers.columns:
        customers_export['Owner Id'] = china_customers['Owner Id']
    if 'Owner Primary Email' in china_customers.columns:
        customers_export['Owner Primary Email'] = china_customers['Owner Primary Email']
    if 'Tax code' in china_customers.columns:
        customers_export['Tax code'] = china_customers['Tax code']
    if 'Account Id' in china_customers.columns:
        customers_export['Account Id'] = china_customers['Account Id']
    if 'Chamber of Commerce' in china_customers.columns:
        customers_export['Chamber of Commerce'] = china_customers['Chamber of Commerce']
    if 'Contract' in china_customers.columns:
        customers_export['Contract'] = china_customers['Contract']
    if 'External Id' in china_customers.columns:
        customers_export['External Id'] = china_customers['External Id']
    if 'Invoice Email' in china_customers.columns:
        customers_export['Invoice Email'] = china_customers['Invoice Email']
    if 'Order Confirmation Email' in china_customers.columns:
        customers_export['Order Confirmation Email'] = china_customers['Order Confirmation Email']
    if 'Safety Data Sheet Email' in china_customers.columns:
        customers_export['Safety Data Sheet Email'] = china_customers['Safety Data Sheet Email']
    if 'VAT Number' in china_customers.columns:
        customers_export['VAT Number'] = china_customers['VAT Number']
    if 'Country ISO2 code' in china_customers.columns:
        customers_export['Country ISO2 code'] = china_customers['Country ISO2 code']
    if 'External System Code' in china_customers.columns:
        customers_export['External System Code'] = china_customers['External System Code']
    if 'Payment term Code' in china_customers.columns:
        customers_export['Payment term Code'] = china_customers['Payment term Code']
    if 'Payment term Label' in china_customers.columns:
        customers_export['Payment term Label'] = china_customers['Payment term Label']
    if 'Order Acknowledgement recipient(s)' in china_customers.columns:
        customers_export['Order Acknowledgement recipient(s)'] = china_customers['Order Acknowledgement recipient(s)']

    # Additional fields - copy all matching columns
    for col in china_customers.columns:
        if col in template_columns and col not in customers_export.columns:
            customers_export[col] = china_customers[col]

    # Save customers CSV
    output_file_customers = 'china_customers_oro_import.csv'
    customers_export.to_csv(output_file_customers, index=False)
    print(f"\n✓ Created: {output_file_customers}")
    print(f"  - Rows: {len(customers_export)}")
    print(f"  - Columns: {len(customers_export.columns)}")

    # Show sample data
    print("\n  Sample customer records:")
    for idx, row in customers_export.iterrows():
        print(f"    - {row['Name']} (ID: {row['Id']}, External ID: {row['External Id']})")

    # ============================================================================
    # CREATE ADDRESSES CSV
    # ============================================================================
    print("\n" + "=" * 80)
    print("Creating Addresses Import CSV")
    print("=" * 80)

    # For addresses, we need to create a different format
    # The template has "Addresses 1 Label", "Addresses 1 Organization", etc.
    # But addresses.csv has separate rows for each address

    # Group addresses by customer
    addresses_by_customer = {}
    for idx, addr in china_addresses.iterrows():
        customer_id = addr['Customer Id']
        if customer_id not in addresses_by_customer:
            addresses_by_customer[customer_id] = []
        addresses_by_customer[customer_id].append(addr)

    print(f"\nAddresses grouped by customer:")
    for cust_id, addrs in addresses_by_customer.items():
        customer_name = addrs[0]['Customer Name'] if 'Customer Name' in addrs[0] else 'Unknown'
        print(f"  - Customer {cust_id} ({customer_name}): {len(addrs)} address(es)")

    # Create addresses export with template columns
    addresses_export = pd.DataFrame(columns=template_columns)

    # Add customer base data and their addresses
    rows = []
    for idx, customer in customers_export.iterrows():
        customer_id = customer['Id']

        # Start with customer data
        row = customer.to_dict()

        # Add addresses for this customer
        if customer_id in addresses_by_customer:
            for addr_idx, addr in enumerate(addresses_by_customer[customer_id], start=1):
                # Add address fields with index (Addresses 1, Addresses 2, etc.)
                row[f'Addresses {addr_idx} Label'] = addr.get('Label', '')
                row[f'Addresses {addr_idx} Organization'] = addr.get('Organization', '')
                row[f'Addresses {addr_idx} Name prefix'] = addr.get('Name prefix', '')
                row[f'Addresses {addr_idx} First name'] = addr.get('First name', '')
                row[f'Addresses {addr_idx} Middle name'] = addr.get('Middle name', '')
                row[f'Addresses {addr_idx} Last name'] = addr.get('Last name', '')
                row[f'Addresses {addr_idx} Name suffix'] = addr.get('Name suffix', '')
                row[f'Addresses {addr_idx} Street'] = addr.get('Street', '')
                row[f'Addresses {addr_idx} Street 2'] = addr.get('Street 2', '')
                row[f'Addresses {addr_idx} Zip/Postal Code'] = addr.get('Zip/Postal Code', '')
                row[f'Addresses {addr_idx} City'] = addr.get('City', '')
                row[f'Addresses {addr_idx} State'] = addr.get('State', '')
                row[f'Addresses {addr_idx} State Combined code'] = addr.get('State Combined code', '')
                row[f'Addresses {addr_idx} Country ISO2 code'] = addr.get('Country ISO2 code', '')
                row[f'Addresses {addr_idx} Comments'] = addr.get('Comments', '')
                row[f'Addresses {addr_idx} Email'] = addr.get('Email', '')
                row[f'Addresses {addr_idx} External Id'] = addr.get('External Id', '')
                row[f'Addresses {addr_idx} Address ID'] = addr.get('Address ID', '')
                row[f'Addresses {addr_idx} Phone'] = addr.get('Phone', '')
                row[f'Addresses {addr_idx} Primary'] = addr.get('Primary', '')
                row[f'Addresses {addr_idx} Vat No.'] = addr.get('Vat No.', '')
                row[f'Addresses {addr_idx} External System Code'] = addr.get('External System Code', '')

                # Only add first address per row (Oro format limitation)
                if addr_idx == 1:
                    break

        rows.append(row)

    addresses_export = pd.DataFrame(rows, columns=template_columns)

    # Save addresses CSV
    output_file_addresses = 'china_addresses_oro_import.csv'
    addresses_export.to_csv(output_file_addresses, index=False)
    print(f"\n✓ Created: {output_file_addresses}")
    print(f"  - Rows: {len(addresses_export)}")
    print(f"  - Columns: {len(addresses_export.columns)}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✓ Customers file: {output_file_customers}")
    print(f"  - {len(customers_export)} customer records")
    print(f"\n✓ Addresses file: {output_file_addresses}")
    print(f"  - {len(addresses_export)} customer records with addresses")
    print("\n" + "=" * 80)

    return output_file_customers, output_file_addresses

if __name__ == '__main__':
    create_customers_import()
