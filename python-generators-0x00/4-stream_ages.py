

#!/usr/bin/python3
"""
Stream user ages and compute the average age without loading
the entire dataset into memory.

Requirements:
- Function stream_user_ages() that yields ages one by one
- Function calculate_average_age() that uses the generator
- No more than two loops
- Must print: "Average age of users: <average>"
- Must NOT use SQL AVG()
"""

from seed import connect_to_prodev
import mysql.connector


def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    Uses a single loop to stream results directly from the database.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data;")

        # One loop to yield each age
        for (age,) in cursor:
            yield int(age)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if connection:
            try:
                connection.close()
            except Exception:
                pass


def calculate_average_age():
    """
    Uses the stream_user_ages generator to calculate
    the average age without loading all rows into memory.
    Uses one loop to iterate through ages.
    """
    total_age = 0
    count = 0

    # Second loop (allowed)
    for age in stream_user_ages():
        total_age += age
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
