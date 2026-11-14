import sqlite3
class ContactManager:
    def __init__(self):
        # Connect to the database
        self.connection = sqlite3.connect("contacts.db")
        self.cursor = self.connection.cursor()
        # Create the contacts table if it does not exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT
            )
        """)
        self.connection.commit()
    def add_contact(self, name, phone, email, address):
        # Insert a new contact into the database
        self.cursor.execute(
            "INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
            (name, phone, email, address)
        )
        self.connection.commit()
    def get_contacts(self):
        # Get all contacts
        self.cursor.execute("SELECT * FROM contacts ORDER BY name")
        return self.cursor.fetchall()
    def search_contacts(self, keyword):
        # Search contacts by name or phone number
        self.cursor.execute(
            "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? ORDER BY name",
            ("%" + keyword + "%", "%" + keyword + "%")
        )
        return self.cursor.fetchall()
    def update_contact(self, contact_id, name, phone, email, address):
        # Update the selected contact
        self.cursor.execute(
            """UPDATE contacts
               SET name = ?, phone = ?, email = ?, address = ?
               WHERE id = ?""",
            (name, phone, email, address, contact_id)
        )
        self.connection.commit()
    def delete_contact(self, contact_id):
        # Delete the selected contact
        self.cursor.execute(
            "DELETE FROM contacts WHERE id = ?",
            (contact_id,)
        )
        self.connection.commit()
    def close_connection(self):
        # Close the database connection
        self.connection.close()