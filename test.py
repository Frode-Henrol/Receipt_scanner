import sqlite3

# Connect to the database
connection = sqlite3.connect("example.db")
cursor = connection.cursor()

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    count INTEGER NOT NULL
)
""")

# Function to add or update the item
def add_or_update_item(name, price):
    cursor.execute("""
    INSERT INTO items (name, price, count)
    VALUES (?, ?, 1)
    ON CONFLICT(name) DO UPDATE SET
        price = price + EXCLUDED.price,
        count = count + 1
    """, (name, price))
    connection.commit()

# Test cases
add_or_update_item("apple", 1.2)  # New entry
add_or_update_item("banana", 0.8)  # New entry
add_or_update_item("apple", 1.5)  # Updates the "apple" entry
add_or_update_item("apple", 1.5)  # Updates the "apple" entry
add_or_update_item("apple", 1.5)  # Updates the "apple" entry
add_or_update_item("apple", 1.5)  # Updates the "apple" entry
add_or_update_item("apple", 1.5)  # Updates the "apple" entry


# Query to verify the results
cursor.execute("SELECT * FROM items")
for row in cursor.fetchall():
    print(row)

# Close the connection
connection.close()
