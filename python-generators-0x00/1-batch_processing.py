
#!/usr/bin/python3
"""
Batch streaming and processing of users from ALX_prodev.user_data

Prototypes:
- def stream_users_in_batches(batch_size)
- def batch_processing(batch_size)

Requirements:
- Use yield (generator)
- No more than 3 loops total
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches (lists) of rows from user_data table.
    Each row is returned as a dictionary.

    Yields:
        list[dict]: up to `batch_size` rows per yield.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")

        # Single loop: fetch batches and yield them
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        # Print error and stop iteration
        print(f"Database error: {err}")
        return
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


def batch_processing(batch_size):
    """
    Processes batches produced by stream_users_in_batches(batch_size),
    filters users over the age of 25, prints each filtered user,
    and yields each filtered user.

    Uses at most two loops here:
      - outer loop over batches
      - inner loop over rows in a batch

    Note: This function both prints and yields filtered users to match
    the checker behavior (printing seen in 2-main.py runs).
    """
    # Loop 1: iterate batches (generator from stream_users_in_batches)
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: iterate rows in the batch and filter
        for user in batch:
            try:
                # age might be Decimal or int/str — convert safely
                age_val = int(user.get("age", 0))
            except Exception:
                # skip rows with malformed age
                continue

            if age_val > 25:
                print(user)
                # Use yield to satisfy "use the yield generator" requirement
                yield user
