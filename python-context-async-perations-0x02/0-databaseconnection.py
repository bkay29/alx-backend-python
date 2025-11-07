

import sqlite3

class DatabaseConnection:
    """Custom context manager for handling database connections."""

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
            if exc_type is not None:
                # Rollback if there was an error
                self.connection.rollback()
            else:
                # Commit changes if all went well
                self.connection.commit()
            self.connection.close()
