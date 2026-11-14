import tkinter as tk
from tkinter import ttk, messagebox
class ContactBookUI:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.selected_id = None
        # Main window settings
        self.root.title("Contact Book")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#101426")
        # Heading
        heading = tk.Label(
            root,
            text="CONTACT BOOK",
            font=("times new roman", 24, "bold"),
            bg="#101426",
            fg="white"
        )
        heading.pack(pady=15)
        subtitle = tk.Label(
            root,
            text="Manage your contacts in one place",
            font=("times new roman", 11),
            bg="#101426",
            fg="#F6F4F4"
        )
        subtitle.pack(pady=(0, 15))
        # Form frame
        form_frame = tk.Frame(root, bg="#1B2038", padx=20, pady=15)
        form_frame.pack(fill="x", padx=25)
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.search_var = tk.StringVar()
        # Input fields
        self.create_field(form_frame, "Name", self.name_var, 0, 0)
        self.create_field(form_frame, "Phone", self.phone_var, 0, 2)
        self.create_field(form_frame, "Email", self.email_var, 1, 0)
        self.create_field(form_frame, "Address", self.address_var, 1, 2)
        # Buttons frame
        button_frame = tk.Frame(root, bg="#101426")
        button_frame.pack(pady=15)
        self.create_button(button_frame, "Add Contact", self.add_contact, 0, "#7655D9")
        self.create_button(button_frame, "Update", self.update_contact, 1, "#287C91")
        self.create_button(button_frame, "Delete", self.delete_contact, 2, "#B84B63")
        self.create_button(button_frame, "Clear", self.clear_fields, 3, "#555D78")
        # Search area
        search_frame = tk.Frame(root, bg="#101426")
        search_frame.pack(fill="x", padx=25, pady=5)
        tk.Label(
            search_frame,
            text="Search:",
            font=("times new roman", 16, "bold"),
            bg="#101426",
            fg="white"
        ).pack(side="left", padx=5)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("times new roman", 12),
            width=35
        )
        search_entry.pack(side="left", padx=8, ipady=5)
        self.search_var.trace_add("write", self.search_contacts)
        # Contact table
        table_frame = tk.Frame(root, bg="#101426")
        table_frame.pack(fill="both", expand=True, padx=25, pady=15)
        columns = ("ID", "Name", "Phone", "Email", "Address")
        self.contact_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )
        for column in columns:
            self.contact_table.heading(column, text=column)
            self.contact_table.column(column, width=150)
        self.contact_table.column("ID", width=40)
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.contact_table.yview
        )
        self.contact_table.configure(yscrollcommand=scrollbar.set)
        self.contact_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.contact_table.bind("<<TreeviewSelect>>", self.select_contact)
        # Load contacts when the app opens
        self.load_contacts()
        # Close database when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
    def create_field(self, parent, label, variable, row, column):
        # Create a label and entry field
        tk.Label(
            parent,
            text=label,
            font=("times new roman", 10, "bold"),
            bg="#1B2038",
            fg="white"
        ).grid(row=row * 2, column=column, sticky="w", padx=10, pady=5)
        tk.Entry(
            parent,
            textvariable=variable,
            font=("times new roman", 11),
            width=30
        ).grid(row=row * 2 + 1, column=column, padx=10, pady=5, ipady=5)
    def create_button(self, parent, text, command, column, color):
        # Create an action button
        tk.Button(
            parent,
            text=text,
            command=command,
            font=("times new roman", 10, "bold"),
            bg=color,
            fg="white",
            activebackground="#9575E8",
            activeforeground="white",
            bd=0,
            width=15,
            cursor="hand2"
        ).grid(row=0, column=column, padx=7, ipady=7)
    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()
        if not name or not phone:
            messagebox.showwarning("Missing Details", "Name and phone are required.")
            return
        self.manager.add_contact(name, phone, email, address)
        messagebox.showinfo("Success", "Contact added successfully!")
        self.clear_fields()
        self.load_contacts()
    def load_contacts(self):
        # Remove old rows from the table
        for item in self.contact_table.get_children():
            self.contact_table.delete(item)
        # Insert updated contacts
        for contact in self.manager.get_contacts():
            self.contact_table.insert("", "end", values=contact)
    def search_contacts(self, *args):
        keyword = self.search_var.get().strip()
        for item in self.contact_table.get_children():
            self.contact_table.delete(item)
        for contact in self.manager.search_contacts(keyword):
            self.contact_table.insert("", "end", values=contact)
    def select_contact(self, event):
        selected = self.contact_table.selection()
        if not selected:
            return
        contact = self.contact_table.item(selected[0], "values")
        self.selected_id = contact[0]
        self.name_var.set(contact[1])
        self.phone_var.set(contact[2])
        self.email_var.set(contact[3])
        self.address_var.set(contact[4])
    def update_contact(self):
        if self.selected_id is None:
            messagebox.showwarning("Select Contact", "Please select a contact first.")
            return
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()
        if not name or not phone:
            messagebox.showwarning("Missing Details", "Name and phone are required.")
            return
        self.manager.update_contact(
            self.selected_id, name, phone, email, address
        )
        messagebox.showinfo("Success", "Contact updated successfully!")
        self.clear_fields()
        self.load_contacts()
    def delete_contact(self):
        if self.selected_id is None:
            messagebox.showwarning("Select Contact", "Please select a contact first.")
            return
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this contact?"
        )
        if confirm:
            self.manager.delete_contact(self.selected_id)
            messagebox.showinfo("Success", "Contact deleted successfully!")
            self.clear_fields()
            self.load_contacts()
    def clear_fields(self):
        self.selected_id = None
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        for item in self.contact_table.selection():
            self.contact_table.selection_remove(item)
    def close_app(self):
        self.manager.close_connection()
        self.root.destroy()