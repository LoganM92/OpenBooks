import MySQLdb

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
        
def add_account(account_name, account_type, account_subtype=None):
    """Adds a new account to the ChartOfAccounts table."""
    conn = connect_to_db()
    if not conn:
        return False, "Database connection error" # Return error information

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO ChartOfAccounts (account_name, account_type, account_subtype)
            VALUES (%s, %s, %s);
            """,
            (account_name, account_type, account_subtype),
        )
        conn.commit()
        return True, "Account added successfully"

    except MySQLdb.IntegrityError:  # Handle duplicate account name error
        conn.rollback()
        return False, "Account name already exists"  # More specific error message


    except Exception as e:
        conn.rollback()
        return False, str(e)   # General error message

    finally:
        cursor.close()
        conn.close()
