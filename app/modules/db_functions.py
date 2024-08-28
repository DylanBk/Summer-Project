import os
import sqlite3

db_path = 'app/instance/game.db'


# --- CREATE DATABASE ---

def create(db_path):
    db = check_db(db_path)
    if db:
        print("Database already exists")
    else:
        print("Creating Database...")

        connection = connect(db_path)
        print("Connected to Database")

        connection.execute("PRAGMA foreign_keys = ON")

        create_table(connection, "armour", [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name TEXT NOT NULL", "armour_points INTEGER NOT NULL",
            "durability INTEGER NOT NULL",
            "description TEXT NOT NULL",
            "category TEXT NOT NULL"
            ])
        create_table(connection, "blocks", [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name TEXT NOT NULL",
            "description TEXT NOT NULL",
            "category TEXT NOT NULL"
            ])
        create_table(connection, "food", [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name TEXT NOT NULL",
            "hunger_points INTEGER NOT NULL",
            "description TEXT NOT NULL",
            "category TEXT NOT NULL"
            ])
        create_table(connection, "items", [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name TEXT NOT NULL",
            "description TEXT NOT NULL",
            "category TEXT NOT NULL"
            ])
        create_table(connection, "mobs", [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name TEXT NOT NULL",
            "behaviour TEXT NOT NULL",
            "hitpoints INTEGER NOT NULL",
            "description TEXT NOT NULL",
            "category TEXT NOT NULL"
            ])
        create_table(connection, "potions", [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name TEXT NOT NULL",
            "effect TEXT NOT NULL",
            "duration TEXT NOT NULL",
            "description TEXT NOT NULL",
            "category TEXT NOT NULL"
            ])
        create_table(connection, "tools", [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name TEXT NOT NULL",
            "durability INTEGER NOT NULL",
            "description TEXT NOT NULL",
            "category TEXT NOT NULL"
            ])

        print("Database Tables Created Successfully")
        connection.close()


# --- CONNECTION ---

def connect(db_path):
    """
    ...Connects to the given database.

    Parameters:
        db_path:The file path for the database.
    Returns:
        sqlite3 connection:Returns database connection.
    """
    return sqlite3.connect(db_path)


# --- TABLES ---

def create_table(conn, table, columns):
    """
    ...Creates a table in the SQL database using the passed parameters.

    Parameters:
        conn:The database connection.
        table (STR):The name of the table to be created.
        columns (LIST):The names of the columns to be added to the table.
    """
    c = conn.cursor()
    sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})"

    try:
        c.execute(sql)
        conn.commit()  # Optional commit for schema changes
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")


# --- CHECKS ---

def check_db(db_path):
    """
    ...Checks if the database exists.

    Parameters:
        db_path:The file path for the database to be checked.
    """
    if not os.path.exists(db_path):
        return False
    else:
        return True


# --- VIEW RAW DATABASE ---

def print_db(conn):
    """
    ...Prints all data into the terminal.

    Parameters:
        conn:The database connection.
    """
    c = conn.cursor()
    c.execute("SELECT * FROM sqlite_master WHERE type='table';")
    for row in c:
        print(row[0])
    conn.close()


# --- WIKI FUNCTIONS ---

def read_table_data(conn, table):
    """
    ...Fetches all data from a given table.

    Parameters:
        conn:The database connection.
        table (STR):The name of the table for the data to be fetched from.
    """    
    try:
        c = conn.cursor()
        res = c.execute(f"SELECT * FROM {table}")
        return res.fetchall()
    except Exception as e:
        print(f"An error occured: {e}")

        return str(e)

def create_table_data(conn, table, columns, values):
    """
    ...Inserts data into given columns of a given table.

    Parameters:
        conn:The database connection.
        table (STR):The name of the table to insert data into.
        columns (LIST):The names of the columns to insert the data into.
        values (LIST):The data to be inserted into the table.

    Returns:
        lastrowid (INT):Returns the id of the row inserted
    """
    try:
        c = conn.cursor()
        placeholder = ', '.join(['?'] * len(values))
        columns = ', '.join(columns)

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholder})"

        c.execute(sql, values)

        lastrowid = c.lastrowid
        conn.commit()

        return lastrowid
    except Exception as e:
        print(f"An error occured: {e}")
        return str(e)

def update_table_data(conn, table, id, data):
    """
    ...Updates a specific column value for a specific table item based on id.

    Parameters:
        conn:The database connection.
        table (STR):The name of the table to update.
        id (INT):The id of the table item to update.
        column (STR):The name of the column to update.
        value (ANY): The data to update the table with.

    Returns:
        rowcount (INT):The number of rows in the table.
    """
    try:
        c = conn.cursor()
        columns = ', '.join([f"{column} = ?" for column in data.keys()])

        sql = f"UPDATE {table} SET {columns} WHERE id = ?"
        c.execute(sql, list(data.values() + [id]))

        rowcount = c.rowcount
        conn.commit()

        return rowcount
    except Exception as e:
        print(f"An error occured: {e}")

        return str(e)

def delete_table_data(conn, table, id):
    """
    ...Deletes data from a row in a given table based on id.

    Parameters:
        conn:The database connection.
        table (STR):The name of the table to be deleted from.
        id (INT):The id of the row to be deleted.

    Returns:
        rowcount (INT):The number of rows remaining in the given table.
    """
    try:
        c = conn.cursor()
        sql = f"DELETE FROM {table} WHERE id = ?"
        c.execute(sql, (id,))

        rowcount = c.rowcount
        conn.commit()

        return rowcount
    except Exception as e:
        print(f"An error occured: {e}")
        return str(e)