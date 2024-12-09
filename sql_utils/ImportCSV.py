"""
Note for transactions to be added there needs to be an account in the chart of accounts 
with the same name already
"""
import csv
import MySQLdb
from datetime import datetime

# Database connection details  
DB_HOST = "localhost"
DB_USER = "root"  
DB_PASSWORD = "password"  
DB_NAME = "my_new_database"  


# Connect to the database
def connect_to_db():
    try:
        return MySQLdb.connect(
            host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME
        )
    except MySQLdb.Error as e:
        print(f"Error connecting to database: {e}")
        return None  # Or handle the error as needed


def parse_csv_and_insert_transactions(csv_filepath):
    """
    Parses a CSV file of transactions and inserts them into the Transactions table.

    Args:
        csv_filepath (str): The path to the CSV file.
    """
    conn = connect_to_db()
    if not conn:
        return  # Or raise an exception, handle error as needed


    cursor = conn.cursor()

    try:
        with open(csv_filepath, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)  # Use DictReader for named columns

            # Fetch ChartOfAccounts IDs for efficient lookup
            cursor.execute("SELECT id, account_name FROM ChartOfAccounts;")
            chart_of_accounts = dict(cursor.fetchall())

            # Fetch vendor IDs for efficient lookup
            cursor.execute("SELECT id, vendor FROM Vendors;")
            vendors = dict(cursor.fetchall())

            for row in reader:
                # Convert date string to date object
                try:
                    transaction_date = datetime.strptime(
                        row["date"], "%Y-%m-%d"
                    ).date()
                except ValueError:
                    print(
                        f"Skipping row due to invalid date format: {row.get('date', 'N/A')}"
                    )
                    continue

                # Data Cleaning and Preparation (important)
                description = row.get("description", None)
                payee_name = row.get("payee", None)


                try:  # Use try-except to get or create vendor IDs, if they don't exist.
                    payee_id = vendors[payee_name]
                except KeyError:
                    cursor.execute(
                        "INSERT INTO Vendors (vendor) VALUES (%s);", (payee_name,)
                    )
                    payee_id = cursor.lastrowid
                    vendors[
                        payee_name
                    ] = payee_id  # Update the vendors dictionary to prevent duplicates.


                category = row.get("category", None)

                try:
                    spent = float(row["spent"]) if row["spent"] else None
                except ValueError:
                    spent = None
                    print(f"Invalid 'spent' value: {row.get('spent', 'N/A')}, setting to None.")

                try:
                    received = float(row["received"]) if row["received"] else None
                except ValueError:
                    received = None
                    print(f"Invalid 'received' value: {row.get('received', 'N/A')}, setting to None.")

                # Get the chart_of_accounts_id
                account_name = row.get("account_name")
                try:
                    chart_of_accounts_id = chart_of_accounts[account_name]
                except KeyError:
                    print(
                        f"Account '{account_name}' not found in ChartOfAccounts. Skipping transaction."
                    )
                    continue

                cursor.execute(
                    """
                    INSERT INTO Transactions (date, description, payee, category, spent, received, chart_of_accounts_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        transaction_date,
                        description,
                        payee_name,  # Now storing vendor name
                        category,
                        spent,
                        received,
                        chart_of_accounts_id,  # Now using chart_of_accounts_id
                    ),
                )


        conn.commit()
        print(f"Transactions from '{csv_filepath}' inserted successfully.")

    except Exception as e:
        print(f"Error inserting transactions: {e}")
        conn.rollback()  # Rollback changes if there's an error

    finally:
        cursor.close()
        conn.close()
