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
        
def add_user(account_ID, account_username, account_password):
    """Adds a new account to the users table."""
    conn = connect_to_db()
    if not conn:
        return False, "Database connection error" # Return error information

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (id, username, password)
            VALUES (%s, %s, %s);
            """,
            (account_ID, account_username, account_password),
        )
        conn.commit()
        return True, "User added successfully"

    except MySQLdb.IntegrityError:  # Handle duplicate account name error
        conn.rollback()
        return False, "Username already exists"  # More specific error message


    except Exception as e:
        conn.rollback()
        return False, str(e)   # General error message

    finally:
        cursor.close()
        conn.close()

def get_password(username):
    """Retrieves the password of a given username"""
    conn = connect_to_db()
    if not conn:
        return False, "Database connection error" # Return error information

    cursor = conn.cursor()
    try:
        cursor.execute(
        "SELECT password FROM users WHERE username = %s", (username,)
        )
        result = cursor.fetchone()

        if result:
            print(f"DEBUG: Query result = {result}")
            return result[0]
        return None

    except MySQLdb.Error as e:
        print(f"Database error: {e}")
        return None
    
    finally:
        cursor.close()
        conn.close()




