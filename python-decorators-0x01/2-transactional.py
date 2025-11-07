
import sqlite3
import functools

# Decorator to handle database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('my_database.db')  # connect to database
        try:
            result = func(conn, *args, **kwargs)  # pass connection to function
        finally:
            conn.close()  # ensure connection is closed
        return result
    return wrapper


# Decorator to manage transactions (commit or rollback)
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # commit changes if successful
            return result
        except Exception as e:
            conn.rollback()  # rollback on error
            print(f"Transaction failed: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print("User email updated successfully.")


# Example usage
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
