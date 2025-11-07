
import time
import sqlite3
import functools

query_cache = {}

# Database connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('my_database.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# Caching decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Determine query from args or kwargs
        query = kwargs.get("query") or (args[0] if args else None)
        
        # Check if query exists in cache
        if query in query_cache:
            print("Using cached result for query.")
            return query_cache[query]

        print("Executing query and caching result...")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result  # Store result in cache
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call → runs query and caches it
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call → fetches result from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
