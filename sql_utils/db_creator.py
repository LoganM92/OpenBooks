import MySQLdb
from MySQLdb import _mysql

def create_sql_server_and_database(
    db_name="my_new_database",
    host="localhost",
    user="root",
    password="password",
):
    """Creates MySQL database and tables."""
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=password)
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")

        cursor.execute(f"USE {db_name}")

        # Create ChartOfAccounts table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ChartOfAccounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_name VARCHAR(255) NOT NULL UNIQUE,
                account_type VARCHAR(50) NOT NULL,
                account_subtype VARCHAR(50)
            );
        """
        )
        print("Table 'ChartOfAccounts' created or already exists.")

        # Create Transactions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                description VARCHAR(255),
                payee VARCHAR(255),
                category VARCHAR(255),
                spent DECIMAL(12, 2),
                received DECIMAL(12, 2),
                chart_of_accounts_id INT,
                FOREIGN KEY (chart_of_accounts_id) REFERENCES ChartOfAccounts(id)
            );
        """
        )
        print("Table 'Transactions' created or already exists.")

        # Create Vendors table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Vendors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vendor VARCHAR(255)
            );
        """
        )
        print("Table 'Vendors' created or already exists.")


        # Create AccountBalances table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS AccountBalances (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chart_of_accounts_id INT,
                balance_date DATE,
                openbooks_balance DECIMAL(12,2),
                bank_balance DECIMAL(12,2),
                FOREIGN KEY (chart_of_accounts_id) REFERENCES ChartOfAccounts(id)
            );

        """
        )
        print("Table 'AccountBalances' created or already exists.")



        return True

    except _mysql.MySQLError as err:
        print(f"An error occurred: {err}")
        return False

    finally:
        if "conn" in locals() and conn.open:
            conn.close()
