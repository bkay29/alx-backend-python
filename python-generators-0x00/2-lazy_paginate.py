#!/usr/bin/python3
"""
Lazy pagination generator for user_data.

Prototypes required:
- def paginate_users(page_size, offset)
- def lazy_pagination(page_size)

Behavior:
- paginate_users fetches a single page (LIMIT ... OFFSET ...)
- lazy_pagination yields pages (lists of dicts) one by one, fetching each
  page only when needed. Starts at offset 0.
- Uses only one loop (while) and uses yield.
"""

from seed import connect_to_prodev
import mysql.connector


def paginate_users(page_size, offset):
    """
    Fetch a single page of rows from user_data.
    Returns a list of rows (each row is a dict).
    """
    conn = None
    cur = None
    try:
        conn = connect_to_prodev()
        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cur.fetchall()
        return rows
    except mysql.connector.Error as err:
        # On DB error, print and return empty list to stop pagination
        print(f"Database error: {err}")
        return []
    finally:
        if cur:
            try:
                cur.close()
            except Exception:
                pass
        if conn:
            try:
                conn.close()
            except Exception:
                pass


def lazy_pagination(page_size):
    """
    Generator that lazily yields pages of users (lists of dicts).
    Starts at offset 0 and fetches subsequent pages only when needed.
    Uses a single loop.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
