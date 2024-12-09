import random
import csv
from datetime import date, timedelta

def generate_fake_data_csv(num_transactions=50, csv_filepath="fake_transactions.csv"):
    """Generates fake transaction data and saves it to a CSV file."""

    try:
        with open(csv_filepath, "w", newline="") as csvfile:
            fieldnames = [
                "date",
                "description",
                "payee",
                "category",
                "spent",
                "received",
                "account_name",  # Added account_name
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Chart of Accounts Data (for account_name generation)
            accounts_data = {
                "Asset": [
                    "Cash",
                    "Accounts Receivable",
                    "Inventory",
                ],
                "Liability": [
                    "Accounts Payable",
                    "Credit Card Payable",
                ],
                "Equity": [
                    "Retained Earnings",
                    "Owner's Equity",
                ],
            }

            all_account_names = [account for sublist in accounts_data.values() for account in sublist]  # Flattened list


            # Vendors Data (for payee generation)
            vendors = ["Vendor A", "Vendor B", "Vendor C", "Vendor D", "Vendor E"]
            categories = ["Sales", "Purchases", "Payroll", "Rent", "Utilities"]
            today = date.today()

            for _ in range(num_transactions):
                days_ago = random.randint(0, 365)
                transaction_date = today - timedelta(days=days_ago)

                transaction = {
                    "date": transaction_date.strftime("%Y-%m-%d"),  # Format date for CSV
                    "description": f"Transaction {_ + 1}",
                    "payee": random.choice(vendors),
                    "category": random.choice(categories),
                    "spent": round(random.uniform(0, 500), 2)
                    if random.random() < 0.7
                    else None,
                    "received": round(random.uniform(0, 1000), 2)
                    if random.random() < 0.5
                    else None,
                    "account_name": random.choice(all_account_names),

                }
                writer.writerow(transaction)


        print(f"Fake transaction data saved to '{csv_filepath}'")

    except Exception as e:
        print(f"Error generating CSV data: {e}")


if __name__ == "__main__":
    generate_fake_data_csv()