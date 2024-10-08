# Import necessary modules
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import psycopg2
from datetime import date

# Global variable to store the database connection
conn = None
selected_invoice_id = None  # Variable to store the currently selected invoice ID
# Modify connect_to_db function to change button background color
def connect_to_db():
    global conn
    if conn:
        messagebox.showinfo("Connection Status", "Already connected to the database.")
        return

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="12345678"
        )
        messagebox.showinfo("Connection Status", "Successfully connected to the database.")
        button_frame1.config(bg="blue")  # Change color to green upon successful connection
        tab_control.select(tab1)  # Switch to the "App" tab upon successful connection
        load_invoice_data()  # Load invoices into Tab 3 after connection
    except Exception as e:
        messagebox.showerror("Database Error", f"Error connecting to the database: {e}")

# Modify disconnect_from_db function to change button background color
def disconnect_from_db():
    global conn
    if conn:
        conn.close()
        conn = None
        messagebox.showinfo("Connection Status", "Successfully disconnected from the database.")
        button_frame1.config(bg=default_color)  # Change color back to default upon disconnection
        invoice_tree.delete(*invoice_tree.get_children())  # Clear Tab 3 data
    else:
        messagebox.showinfo("Connection Status", "No active database connection.")

def exit_app():
    root.quit()

def show_about():
    messagebox.showinfo("About", "This is a simple purchase invoice app with database connectivity.\nVersion 1.0")

def switch_to_tab2():
    if conn:  # Only switch if connected
        tab_control.select(tab2)  # Switch to the "Hóa đơn" tab
    else:
        messagebox.showwarning("Warning", "Please connect to the database first.")

def insert_invoice():
    supplier_name = entry_supplier.get()
    item_name = entry_item.get()
    quantity = entry_quantity.get()
    price_per_item = entry_price.get()

    if not (supplier_name and item_name and quantity.isdigit() and price_per_item.isdigit()):
        messagebox.showerror("Input Error", "Please fill out all fields correctly.")
        return

    try:
        if conn:
            cursor = conn.cursor()
            total = int(quantity) * float(price_per_item)
            query = "INSERT INTO purchase_invoice (supplier_name, item_name, quantity, price_per_item, total, purchase_date) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (supplier_name, item_name, quantity, price_per_item, total, date.today()))
            conn.commit()
            cursor.close()
            messagebox.showinfo("Success", "Invoice saved successfully.")
            load_invoice_data()  # Reload the data in Tab 3 after insertion
        else:
            messagebox.showerror("Connection Error", "No database connection.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error saving invoice: {e}")

def load_invoice_data():
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM purchase_invoice")
            rows = cursor.fetchall()
            invoice_tree.delete(*invoice_tree.get_children())  # Clear existing data
            for row in rows:
                invoice_tree.insert('', 'end', values=row)
            cursor.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching invoices: {e}")
    else:
        messagebox.showerror("Connection Error", "No database connection.")

def select_invoice(event):
    global selected_invoice_id
    selected_item = invoice_tree.selection()
    if selected_item:
        values = invoice_tree.item(selected_item, 'values')
        selected_invoice_id = values[0]  # Assuming invoice ID is in the first column
        entry_supplier_tab3.delete(0, tk.END)
        entry_item_tab3.delete(0, tk.END)
        entry_quantity_tab3.delete(0, tk.END)
        entry_price_tab3.delete(0, tk.END)
        entry_supplier_tab3.insert(0, values[1])
        entry_item_tab3.insert(0, values[2])
        entry_quantity_tab3.insert(0, values[3])
        entry_price_tab3.insert(0, values[4])

def save_edited_invoice():
    global selected_invoice_id
    if not selected_invoice_id:
        messagebox.showwarning("Warning", "No invoice selected for editing.")
        return

    # Get the updated values from the fields
    new_supplier = entry_supplier_tab3.get()
    new_item = entry_item_tab3.get()
    new_quantity = entry_quantity_tab3.get()
    new_price = entry_price_tab3.get()

    # Validate that necessary fields are filled
    if not (new_supplier and new_item):
        messagebox.showerror("Input Error", "Please fill out all fields correctly.")
        return

    try:
        cursor = conn.cursor()

        # Get current values for the selected invoice
        cursor.execute("SELECT supplier_name, item_name, quantity, price_per_item FROM purchase_invoice WHERE id = %s", (selected_invoice_id,))
        current_invoice = cursor.fetchone()

        if current_invoice is None:
            messagebox.showerror("Error", "Invoice not found.")
            cursor.close()
            return

        # Set the values to the new ones, or keep the original if they are unchanged
        if not new_quantity.isdigit():
            new_quantity = current_invoice[2]  # Use the original quantity if input is not valid
        if not new_price.isdigit():
            new_price = current_invoice[3]  # Use the original price if input is not valid

        # Build the SQL query dynamically based on updated fields
        total = int(new_quantity) * float(new_price)
        query = "UPDATE purchase_invoice SET supplier_name = %s, item_name = %s, quantity = %s, price_per_item = %s, total = %s WHERE id = %s"
        params = (new_supplier, new_item, new_quantity, new_price, total, selected_invoice_id)

        # Execute the query and commit changes
        cursor.execute(query, params)
        conn.commit()
        cursor.close()

        # Reload the data in Tab 3 after update
        load_invoice_data()
        messagebox.showinfo("Success", "Invoice updated successfully.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error updating invoice: {e}")

def delete_invoice():
    global selected_invoice_id
    if not selected_invoice_id:
        messagebox.showwarning("Warning", "No invoice selected for deletion.")
        return

    # Confirmation dialog
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this invoice?")
    if confirm:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM purchase_invoice WHERE id = %s"
            cursor.execute(query, (selected_invoice_id,))
            conn.commit()
            cursor.close()
            load_invoice_data()  # Reload the data in Tab 3 after deletion
            messagebox.showinfo("Success", "Invoice deleted successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error deleting invoice: {e}")

# Create the main application window
root = tk.Tk()
root.title("Purchase APP ")
root.geometry("800x600")  # Set window size

# Create the menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Connect SQL", command=connect_to_db)
file_menu.add_command(label="Disconnect SQL", command=disconnect_from_db)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Configure the menu bar
root.config(menu=menu_bar)

# Create the Tab Control
tab_control = ttk.Notebook(root)

# Create Tab 1 (App tab)
tab1 = tk.Frame(tab_control)  # Use tk.Frame here for color manipulation
tab_control.add(tab1, text="App")

# Default color for the button
default_color = "gray"  # Set default color to gray

# Add content to Tab 1 using one frame (button_frame1)
button_frame1 = tk.Frame(tab1, padx=20, pady=20)  # Use tk.Frame for the logo, welcome message, and button
button_frame1.pack(expand=True, anchor='center')

# Attempt to load the logo image
logo_path = r'D:\LTPTNC\DAMH\Test\Image\logo1.png'

try:
    img = Image.open(logo_path)
    logo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(button_frame1, image=logo)
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)
except Exception as e:
    print("Error loading logo:", e)  # Print the error for debugging
    tk.Label(button_frame1, text="Logo not found").pack(pady=10)

welcome_label = tk.Label(button_frame1, text="Welcome to Purchase Invoice App", font=("Helvetica", 16))
welcome_label.pack()

# Add the SQL connect button to button_frame1 with default background color
connect_button = tk.Button(button_frame1, text="Connect SQL", font=("Helvetica", 12), bg=default_color, command=connect_to_db)
connect_button.pack(pady=20)

# Create Tab 2 (Invoice Entry tab)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text="Add Purchase")

# Add content to Tab 2 (Invoice entry fields)
entry_frame = tk.Frame(tab2, padx=20, pady=20)
entry_frame.pack(padx=10, pady=10)

label_supplier = tk.Label(entry_frame, text="Supplier Name:", font=("Helvetica", 12))
label_supplier.grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_supplier = tk.Entry(entry_frame, font=("Helvetica", 12))
entry_supplier.grid(row=0, column=1, padx=5, pady=5)

label_item = tk.Label(entry_frame, text="Item Name:", font=("Helvetica", 12))
label_item.grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_item = tk.Entry(entry_frame, font=("Helvetica", 12))
entry_item.grid(row=1, column=1, padx=5, pady=5)

label_quantity = tk.Label(entry_frame, text="Quantity:", font=("Helvetica", 12))
label_quantity.grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_quantity = tk.Entry(entry_frame, font=("Helvetica", 12))
entry_quantity.grid(row=2, column=1, padx=5, pady=5)

label_price = tk.Label(entry_frame, text="Price per Item:", font=("Helvetica", 12))
label_price.grid(row=3, column=0, sticky="w", padx=5, pady=5)
entry_price = tk.Entry(entry_frame, font=("Helvetica", 12))
entry_price.grid(row=3, column=1, padx=5, pady=5)

# Save button for invoice entry
save_button = tk.Button(tab2, text="Save Invoice", font=("Helvetica", 12), command=insert_invoice)
save_button.pack(pady=10)

# Create Tab 3 (Invoice Management tab)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text="Manage Invoices")

# Treeview widget for displaying invoices in Tab 3
tree_frame = tk.Frame(tab3, padx=20, pady=20)
tree_frame.pack(padx=10, pady=10)

invoice_tree = ttk.Treeview(tree_frame, columns=("id", "supplier", "item", "quantity", "price", "total", "date"), show="headings", height=8)
invoice_tree.pack(side=tk.LEFT, fill=tk.BOTH)

# Configure treeview column headings
invoice_tree.heading("id", text="ID")
invoice_tree.heading("supplier", text="Supplier")
invoice_tree.heading("item", text="Item")
invoice_tree.heading("quantity", text="Quantity")
invoice_tree.heading("price", text="Price")
invoice_tree.heading("total", text="Total")
invoice_tree.heading("date", text="Date")

# Configure treeview column widths
invoice_tree.column("id", width=30)
invoice_tree.column("supplier", width=150)
invoice_tree.column("item", width=150)
invoice_tree.column("quantity", width=70)
invoice_tree.column("price", width=70)
invoice_tree.column("total", width=100)
invoice_tree.column("date", width=100)

# Vertical scrollbar for the treeview
scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=invoice_tree.yview)
invoice_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Bind treeview selection event
invoice_tree.bind("<<TreeviewSelect>>", select_invoice)

# Frame for editing selected invoice
edit_frame = tk.Frame(tab3, padx=20, pady=20)
edit_frame.pack(padx=10, pady=10)

label_supplier_tab3 = tk.Label(edit_frame, text="Supplier Name:", font=("Helvetica", 12))
label_supplier_tab3.grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_supplier_tab3 = tk.Entry(edit_frame, font=("Helvetica", 12))
entry_supplier_tab3.grid(row=0, column=1, padx=5, pady=5)

label_item_tab3 = tk.Label(edit_frame, text="Item Name:", font=("Helvetica", 12))
label_item_tab3.grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_item_tab3 = tk.Entry(edit_frame, font=("Helvetica", 12))
entry_item_tab3.grid(row=1, column=1, padx=5, pady=5)

label_quantity_tab3 = tk.Label(edit_frame, text="Quantity:", font=("Helvetica", 12))
label_quantity_tab3.grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_quantity_tab3 = tk.Entry(edit_frame, font=("Helvetica", 12))
entry_quantity_tab3.grid(row=2, column=1, padx=5, pady=5)

label_price_tab3 = tk.Label(edit_frame, text="Price per Item:", font=("Helvetica", 12))
label_price_tab3.grid(row=3, column=0, sticky="w", padx=5, pady=5)
entry_price_tab3 = tk.Entry(edit_frame, font=("Helvetica", 12))
entry_price_tab3.grid(row=3, column=1, padx=5, pady=5)

# Save and Delete buttons
save_button_tab3 = tk.Button(tab3, text="Save Changes", font=("Helvetica", 12), command=save_edited_invoice)
save_button_tab3.pack(pady=10)

delete_button_tab3 = tk.Button(tab3, text="Delete Invoice", font=("Helvetica", 12), command=delete_invoice)
delete_button_tab3.pack(pady=10)

# Pack and display the tabs
tab_control.pack(expand=1, fill="both")

# Start the main event loop
root.mainloop()
