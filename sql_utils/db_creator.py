import MySQLdb
from MySQLdb import _mysql

def create_sql_server_and_database(
    db_name="placeholder",
    host="localhost",
    user="root",
    password="password"
):
    """
    Connects to MariaDB/MySQL server and creates a database if it does not already exist.
    Then it creates the Transactions table within the database.

    Args:
        db_name (str): The name of the database to create.
        host (str): The host address of the MariaDB server.
        user (str): The username for MariaDB authentication.
        password (str): The password for MariaDB authentication (empty for no password).

    Returns:
        bool: True if the database and table were created or already exist, False otherwise.
    """
    try:
        # Connect to MariaDB/MySQL server
        conn = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password  
        )
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' has been created or already exists.")

        # Select the newly created database
        cursor.execute(f"USE {db_name}")

        # Create the Transactions table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                description CHAR(255),
                payee CHAR(255),
                category CHAR(255),
                spent DOUBLE(12, 2),
                received DOUBLE(12, 2)
            );
        """)
        print(f"Table 'Transactions' has been created or already exists.")
        
        # Create the Vendors table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Vendors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vendor CHAR(255)
            );
        """)
        print(f"Table 'Vendors' has been created or already exists.")
	
        # Create the Accounts table if it doesn't exist
        cursor.execute("""
            CREATE TABLE accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_name CHAR(255),            -- Account name
                account_type CHAR(255),            -- Type of account (e.g., 'Expense', 'Revenue')
                parent_account_id INT NULL,        -- Self-referencing parent account
                openbooks_balance DOUBLE(12, 2),  -- Openbooks balance for the account
                bank_balance DOUBLE(12, 2),       -- Bank balance for the account
                FOREIGN KEY (parent_account_id) REFERENCES accounts(id) -- Foreign key for parent account
            );
        """)
        print(f"Table 'Accounts' has been created or already exists.")
        
        return True

    except _mysql.MySQLError as err:
        print(f"An error occurred: {err}")
        return False

    finally:
        # Close the connection
        if 'conn' in locals() and conn.open:
            conn.close()

