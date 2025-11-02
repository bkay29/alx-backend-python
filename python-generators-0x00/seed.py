
#!/usr/bin/env python3
# seed.py
"""
Seed script for ALX_prodev.user_data and a streaming generator for rows.

Prototypes implemented:
- connect_db()
- create_database(connection)
- connect_to_prodev()
- create_table(connection)
- insert_data(connection, data)  # data is CSV filename
- stream_rows(connection, table='user_data', chunk_size=100) -> generator yielding rows one by one
"""

import os
import csv
import mysql.connector
from mysql.connector import errorcode

def connect_db():
    """
    Connect to MySQL server (no specific database).
    Reads connection details from env vars if present, otherwise uses defaults.
    Returns a mysql.connector connection or None on failure.
    """
    host = os.getenv('MYSQL_HOST', '127.0.0.1')
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', '')
    port = int(os.getenv('MYSQL_PORT', 3306))
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            autocommit=True
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """
    Create database ALX_prodev if it does not exist.
    """
    DB_NAME = 'ALX_prodev'
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET 'utf8mb4'")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        raise

def connect_to_prodev():
    """
    Connect to the ALX_prodev database and return the connection.
    """
    host = os.getenv('MYSQL_HOST', '127.0.0.1')
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', '')
    port = int(os.getenv('MYSQL_PORT', 3306))
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database='ALX_prodev',
            autocommit=False  # we'll commit explicitly
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """
    Create user_data table with:
      user_id CHAR(36) PRIMARY KEY (UUID string)
      name VARCHAR NOT NULL
      email VARCHAR NOT NULL
      age DECIMAL NOT NULL
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) NOT NULL,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,0) NOT NULL,
        PRIMARY KEY (user_id),
        INDEX idx_email (email)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
        raise

def insert_data(connection, csv_file_path):
    """
    Insert data from CSV into user_data table if user_id does not already exist.
    CSV expected columns: user_id,name,email,age (header allowed).
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    insert_sql = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      name = VALUES(name),
      email = VALUES(email),
      age = VALUES(age)
    """
    # We'll upsert (insert or update) to avoid duplicates; primary key is user_id.
    # If you prefer skip-on-duplicate, change to INSERT IGNORE.

    try:
        cursor = connection.cursor()
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows_to_insert = []
            count = 0
            for row in reader:
                # Trim values and basic validations
                uid = row.get('user_id') or row.get('id') or row.get('uuid')
                name = row.get('name', '').strip()
                email = row.get('email', '').strip()
                age = row.get('age', '').strip()

                if not uid or not name or not email or not age:
                    # Skip incomplete rows
                    continue
                # Convert age to numeric value acceptable by DECIMAL(5,0)
                try:
                    age_val = int(float(age))
                except ValueError:
                    # skip rows with malformed age
                    continue

                rows_to_insert.append((uid.strip(), name, email, age_val))
                # Bulk insert in batches to be efficient
                if len(rows_to_insert) >= 200:
                    cursor.executemany(insert_sql, rows_to_insert)
                    connection.commit()
                    count += len(rows_to_insert)
                    rows_to_insert = []

            if rows_to_insert:
                cursor.executemany(insert_sql, rows_to_insert)
                connection.commit()
                count += len(rows_to_insert)

        cursor.close()
        print(f"Inserted/updated {count} rows from {csv_file_path}")
    except mysql.connector.Error as err:
        print(f"MySQL error during insert: {err}")
        connection.rollback()
        raise

def stream_rows(connection, table='user_data', chunk_size=100):
    """
    Generator that streams rows from the given table one by one.
    Yields tuples (user_id, name, email, age) or dictionaries if dictionary cursor is used.

    Usage:
        for row in stream_rows(conn):
            process(row)
    """
    cursor = connection.cursor(buffered=False)  # unbuffered cursor for streaming behaviour
    try:
        cursor.execute(f"SELECT user_id, name, email, age FROM {table}")
        while True:
            rows = cursor.fetchmany(chunk_size)
            if not rows:
                break
            for r in rows:
                yield r
    finally:
        try:
            cursor.close()
        except Exception:
            pass

# --- If run as script, allow quick end-to-end seeding ---
if __name__ == "__main__":
    # basic demo flow that mirrors the 0-main behavior you showed
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
        print("connection successful")

        conn2 = connect_to_prodev()
        if conn2:
            create_table(conn2)
            # Adjust the CSV filename/path if needed
            csv_path = os.path.join(os.getcwd(), 'user_data.csv')
            try:
                insert_data(conn2, csv_path)
            except FileNotFoundError:
                print(f"CSV file not found at {csv_path} -- skipping insert_data")
            # show DB presence
            cur = conn2.cursor()
            cur.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
            result = cur.fetchone()
            if result:
                print("Database ALX_prodev is present ")
            # show first 5 rows
            cur.execute("SELECT user_id, name, email, age FROM user_data LIMIT 5;")
            rows = cur.fetchall()
            print(rows)
            cur.close()

            # Example of streaming (generator) usage:
            print("\nStreaming rows (first 5 via generator):")
            streamed = stream_rows(conn2)
            for i, row in enumerate(streamed):
                print(row)
                if i >= 4:
                    break

            conn2.close()
