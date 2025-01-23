import sqlite3

class DatabaseManager:
    def __init__(self, db_file: str ="example.db"):
        # Initialize connection and cursor
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        # Create the table if it doesn't already exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            name TEXT PRIMARY KEY,
            price REAL NOT NULL,
            count INTEGER NOT NULL
        )
        """)

    def add_or_update_item(self, name: str, price: int):
        # Add a new item or update an existing one
        self.cursor.execute("""
        INSERT INTO items (name, price, count)
        VALUES (?, ?, 1)
        ON CONFLICT(name) DO UPDATE SET
            price = price + EXCLUDED.price,
            count = count + 1
        """, (name, price))
        self.connection.commit()

    def fetch_all_items(self):
        # Fetch all items from the database
        self.cursor.execute("SELECT * FROM items")
        return self.cursor.fetchall()
    
    def clear_item(self, name: str):
        # Remove a specific item from the database
        self.cursor.execute("DELETE FROM items WHERE name = ?", (name,))
        self.connection.commit()

    def clear_all_items(self):
        # Remove all items from the database
        self.cursor.execute("DELETE FROM items")
        self.connection.commit()

    def close(self):
        # Close the database connection
        self.connection.close()
