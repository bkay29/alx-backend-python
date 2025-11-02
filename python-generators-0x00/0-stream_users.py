
#!/usr/bin/python3
"""
Generator function that streams user data rows from MySQL one by one
"""

import mysql.connector


def stream_users():
    """
    Connects to the ALX_prodev database and yields user rows one by one
    from the user_data table.
    Each row is returned as a dictionary.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # update if your username differs
            password="",       # add password if applicable
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        # Use a single loop to yield each row
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
