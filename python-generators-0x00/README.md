
# Python Generators: Streaming SQL Rows with MySQL

This project demonstrates how to **seed a MySQL database** and **stream rows efficiently using a Python generator**.  
It sets up a database, populates it with sample data from a CSV file, and provides a generator function that yields rows one-by-one — an approach ideal for memory-efficient data processing.

---

##  Objective

Create a Python script `seed.py` that:
- Connects to a MySQL database server.
- Creates a database named **`ALX_prodev`** (if it doesn’t exist).
- Creates a table **`user_data`** with specific fields.
- Populates the table with sample data from `user_data.csv`.
- Provides a **generator** that streams rows from the database one at a time.

---

Requirements

- Python 3.8+

- MySQL Server (running locally or remotely)

- Dependencies:

pip install mysql-connector-python


---

## Database Schema

**Database name:** `ALX_prodev`  
**Table name:** `user_data`

| Field     | Type         | Description                        |
|------------|--------------|------------------------------------|
| user_id    | CHAR(36) PK  | Unique UUID for each user (indexed)|
| name       | VARCHAR(255) | User’s full name (not null)        |
| email      | VARCHAR(255) | User’s email (not null)            |
| age        | DECIMAL(5,0) | User’s age (not null)              |

---

## Functions Implemented

### `connect_db()`
Connects to the MySQL server (no specific database).  
Returns a MySQL connection object.

### `create_database(connection)`
Creates the database **`ALX_prodev`** if it doesn’t exist.

### `connect_to_prodev()`
Connects directly to the **`ALX_prodev`** database.

### `create_table(connection)`
Creates the table **`user_data`** with the specified schema.

### `insert_data(connection, data)`
Reads data from `user_data.csv` and inserts it into the table.  
Skips duplicates using `ON DUPLICATE KEY UPDATE`.

### `stream_rows(connection, table='user_data', chunk_size=100)`
A **generator** that yields rows from the `user_data` table one-by-one — useful for processing large datasets without loading them entirely into memory.

---

## Example Usage

### Run the seeding process

```bash
$ ./0-main.py
connection successful
Table user_data created successfully
Database ALX_prodev is present
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]


## Stream rows using the generator
from seed import connect_to_prodev, stream_rows

conn = connect_to_prodev()
for row in stream_rows(conn):
    print(row)  # prints each record as a tuple



Sample user_data.csv

Example structure:

user_id,name,email,age
00234e50-34eb-4ce2-94ec-26e3fa749796,Dan Altenwerth Jr.,Molly59@gmail.com,67
006bfede-724d-4cdd-a2a6-59700f40d0da,Glenda Wisozk,Miriam21@gmail.com,119
00af05c9-0a86-419e-8c2d-5fb7e899ae1c,Ronnie Bechtelar,Sandra19@yahoo.com,22


How It Works

1. Database setup → Connect and create ALX_prodev if missing.

2. Table creation → Define the user_data schema with UUID primary keys.

3. Data seeding → Read CSV and insert/update records.

4. Streaming → Use stream_rows() to lazily fetch records.

This approach is efficient for large datasets because the generator doesn’t load all rows into memory at once — it fetches and yields them chunk by chunk.




Example Output

connection successful
Table user_data created successfully
Database ALX_prodev is present
Streaming rows (first 5 via generator):
('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67)
('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119)
('006e1f7f7-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49)


Cleanup

To remove the database:

DROP DATABASE ALX_prodev;
