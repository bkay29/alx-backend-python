


import sqlite3

class DatabaseConnection:
    """Custom context manager for handling sqlite3 database connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Open database connection and return it."""
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """Commit or rollback based on whether an exception occurred, then close connection."""
        if self.connection:
            try:
                if exc_type is not None:
                    self.connection.rollback()
                else:
                    self.connection.commit()
            finally:
                self.connection.close()

if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
