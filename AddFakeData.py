"""
This code assumes the database has already been built
The script generates some fake data and adds it into the database
"""

import random
import MySQLdb
from datetime import date as dt_date, timedelta

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "my_new_database"  

# Connect to the database
def connect_to_db():
    return MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )

def generate_fake_data(num_transactions=50):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Chart of Accounts Data
        accounts_data = {
            "Asset": [
                {"account_name": "Cash", "account_subtype": "Current Asset"},
                {"account_name": "Accounts Receivable", "account_subtype": "Current Asset"},
                {"account_name": "Inventory", "account_subtype": "Current Asset"},
            ],
            "Liability": [
                {"account_name": "Accounts Payable", "account_subtype": "Current Liability"},
                {"account_name": "Credit Card Payable", "account_subtype": "Current Liability"},
            ],
            "Equity": [
                {"account_name": "Retained Earnings", "account_subtype": "Equity"},
                {"account_name": "Owner's Equity", "account_subtype": "Equity"},
            ],
        }

        for account_type, accounts in accounts_data.items():
            for account in accounts:
                cursor.execute(
                    """
                    INSERT IGNORE INTO ChartOfAccounts (account_name, account_type, account_subtype) 
                    VALUES (%s, %s, %s);
                    """,
                    (account["account_name"], account_type, account["account_subtype"]),
                )

        # Fetch ChartOfAccounts IDs
        cursor.execute("SELECT id, account_name FROM ChartOfAccounts;")
        chart_of_accounts_ids = dict(cursor.fetchall())

        # AccountBalances Data
        today = dt_date.today()
        for account_id in chart_of_accounts_ids:
            openbooks_balance = round(random.uniform(1000, 10000), 2)
            bank_balance = round(random.uniform(800, openbooks_balance), 2)  # Ensure bank_balance <= openbooks_balance
            cursor.execute(
                """
                INSERT INTO AccountBalances (chart_of_accounts_id, balance_date, openbooks_balance, bank_balance)
                VALUES (%s, %s, %s, %s);
                """,
                (account_id, today, openbooks_balance, bank_balance),
            )

        # Vendors Data
        vendors = ["Vendor A", "Vendor B", "Vendor C", "Vendor D", "Vendor E"]
        for vendor in vendors:
            cursor.execute(
                "INSERT IGNORE INTO Vendors (vendor) VALUES (%s);", (vendor,)
            )

        cursor.execute("SELECT id, vendor FROM Vendors;")
        vendor_ids = dict(cursor.fetchall())

        # Transactions Data
        categories = ["Sales", "Purchases", "Payroll", "Rent", "Utilities"]
        
        for _ in range(num_transactions):
            # Generate a random date within the past year
            days_ago = random.randint(0, 365)
            
            transaction_date = today - timedelta(days=days_ago)  # Rename 'date' to 'transaction_date'

            description = f"Transaction {_ + 1}"
            vendor_id = random.choice(list(vendor_ids.keys()))
            chart_of_account_id = random.choice(list(chart_of_accounts_ids.keys()))

            spent = round(random.uniform(0, 500), 2) if random.random() < 0.7 else None
            received = round(random.uniform(0, 1000), 2) if random.random() < 0.5 else None

            cursor.execute(
                """
                INSERT INTO Transactions (date, description, payee, category, spent, received, chart_of_accounts_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    transaction_date,
                    description,
                    vendor_ids[vendor_id],
                    random.choice(categories),
                    spent,
                    received,
                    chart_of_account_id,
                ),
            )

        conn.commit()
        print("Fake data generated successfully.")

    except Exception as e:
        print(f"Error generating data: {e}")
        conn.rollback()  # Rollback on error

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_fake_data()

