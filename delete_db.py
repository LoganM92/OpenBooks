import MySQLdb
from MySQLdb import _mysql

def delete_database(db_name, host="localhost", user="root", password="password"):
    """
    Deletes the specified database from the MariaDB server.

    Args:
        db_name (str): The name of the database to delete.
        host (str): The host address of the MariaDB server.
        user (str): The username for MariaDB authentication.
        password (str): The password for MariaDB authentication (empty for no password).

    Returns:
        bool: True if the database was deleted, False otherwise.
    """
    try:
        # Connect to MariaDB server 
        conn = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password  
        )
        cursor = conn.cursor()

        # Attempt to drop the database
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"Database '{db_name}' has been deleted (if it existed).")
        return True

    except _mysql.MySQLError as err:
        print(f"An error occurred: {err}")
        return False

    finally:
        # Close the connection
        if 'conn' in locals() and conn.open:
            conn.close()

if __name__ == "__main__":
    # Define database and connection details
    database_name = "my_new_database"
    host = "localhost"
    user = "root"
    password = "password" 
    
    # Delete the database
    success = delete_database(database_name, host, user, password)
    if success:
        print(f"Successfully removed the database '{database_name}'.")
    else:
        print(f"Could not remove the database '{database_name}'.")

