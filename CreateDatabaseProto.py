from sql_utils.db_creator import create_sql_server_and_database

if __name__ == "__main__":
    # Define database and connection details
    database_name = "my_new_database"
    host = "localhost"
    user = "root"
    password = "password"

    # Create the database
    success = create_sql_server_and_database(database_name, host, user, password)
    if success:
        print(f"The database '{database_name}' is ready for use.")
    else:
        print(f"Failed to create the database '{database_name}'.")

