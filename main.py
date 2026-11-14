import tkinter as tk
from contact_logic import ContactManager
from ui import ContactBookUI
# Create the main application window
root = tk.Tk()
# Create the contact manager
manager = ContactManager()
# Open the Contact Book interface
app = ContactBookUI(root, manager)
# Keep the application running
root.mainloop()