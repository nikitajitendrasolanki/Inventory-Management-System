import tkinter as tk
from tkinter import messagebox
from time import strftime
import mysql.connector

class InventoryApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1000x700")  # Adjust the window size

        self.db = mysql.connector.connect(
            host="localhost",      # MySQL server host (localhost for local MySQL server)
            user="root",           # MySQL username
            password="vcet123",    # Your MySQL password
            database="inventory"   # Database name
        )
        self.cursor = self.db.cursor()

        # Store Data
        self.available_products = {}  # product_id -> (name, quantity, price)
        self.cart = []  # list of (product_id, name, quantity, price)
        self.sailors = {}  # sailor_name -> (sailor_contact)
        self.receivers = {}  # receiver_name -> (receiver_contact, receiver_address)
        self.current_receivers = None  # Store current selected receiver

        # GUI Widgets Initialization
        self.create_widgets()
        self.load_products()  # Load products when the application starts

    def create_widgets(self):
        # Top frame for the current date and time
        self.frame_top = tk.Frame(self.root, bg="#005b96", height=30)
        self.frame_top.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        self.label_time = tk.Label(self.frame_top, text="", font=("Arial", 12), bg="#005b96", fg="white")
        self.label_time.pack(side="right", padx=10)
        
        # Available Products Section
        self.frame_products = tk.LabelFrame(self.root, text="Available Products", padx=10, pady=10, bg="#006f9b", fg="white")
        self.frame_products.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.product_listbox = tk.Listbox(self.frame_products, height=10, width=40, bg="#c6e0f7", fg="black")
        self.product_listbox.grid(row=0, column=0, columnspan=2)
        
        self.label_select_quantity = tk.Label(self.frame_products, text="Select Quantity:", bg="#006f9b", fg="white")
        self.label_select_quantity.grid(row=1, column=0, pady=5)
        
        self.entry_quantity = tk.Entry(self.frame_products)
        self.entry_quantity.grid(row=1, column=1, pady=5)
        
        self.button_add_to_cart = tk.Button(self.frame_products, text="Add to Cart", command=self.add_to_cart, bg="#0288d1", fg="white")
        self.button_add_to_cart.grid(row=2, column=0, columnspan=2, pady=10)

        # Product addition section for sailor
        self.label_product_name = tk.Label(self.frame_products, text="Product Name:", bg="#006f9b", fg="white")
        self.label_product_name.grid(row=3, column=0, pady=5)

        self.entry_product_name = tk.Entry(self.frame_products)
        self.entry_product_name.grid(row=3, column=1, pady=5)

        self.label_product_quantity = tk.Label(self.frame_products, text="Product Quantity:", bg="#006f9b", fg="white")
        self.label_product_quantity.grid(row=4, column=0, pady=5)

        self.entry_product_quantity = tk.Entry(self.frame_products)
        self.entry_product_quantity.grid(row=4, column=1, pady=5)

        self.label_product_price = tk.Label(self.frame_products, text="Product Price (₹):", bg="#006f9b", fg="white")
        self.label_product_price.grid(row=5, column=0, pady=5)

        self.entry_product_price = tk.Entry(self.frame_products)
        self.entry_product_price.grid(row=5, column=1, pady=5)

        self.button_add_product = tk.Button(self.frame_products, text="Add Product", command=self.add_product, bg="#0288d1", fg="white")
        self.button_add_product.grid(row=6, column=0, columnspan=2, pady=10)

        # Receiver Section
        self.frame_receiver = tk.LabelFrame(self.root, text="Receiver Information", padx=10, pady=10, bg="#006f9b", fg="white")
        self.frame_receiver.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.entry_receiver_name = tk.Entry(self.frame_receiver, width=30)
        self.entry_receiver_name.grid(row=0, column=1, pady=5)
        
        self.label_receiver_name = tk.Label(self.frame_receiver, text="Receiver Name:", bg="#006f9b", fg="white")
        self.label_receiver_name.grid(row=0, column=0, pady=5)
        
        self.entry_receiver_contact = tk.Entry(self.frame_receiver, width=30)
        self.entry_receiver_contact.grid(row=1, column=1, pady=5)
        
        self.label_receiver_contact = tk.Label(self.frame_receiver, text="Contact Number:", bg="#006f9b", fg="white")
        self.label_receiver_contact.grid(row=1, column=0, pady=5)
        
        self.entry_receiver_address = tk.Entry(self.frame_receiver, width=30)
        self.entry_receiver_address.grid(row=2, column=1, pady=5)
        
        self.label_receiver_address = tk.Label(self.frame_receiver, text="Address:", bg="#006f9b", fg="white")
        self.label_receiver_address.grid(row=2, column=0, pady=5)
        
        self.button_add_receiver = tk.Button(self.frame_receiver, text="Save Receiver", command=self.save_receiver, bg="#0288d1", fg="white")
        self.button_add_receiver.grid(row=3, column=0, columnspan=2, pady=10)

        # Sailor Section
        self.frame_sailor = tk.LabelFrame(self.root, text="Sailor Information", padx=10, pady=10, bg="#006f9b", fg="white")
        self.frame_sailor.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        self.entry_sailor_name = tk.Entry(self.frame_sailor, width=30)
        self.entry_sailor_name.grid(row=0, column=1, pady=5)

        self.label_sailor_name = tk.Label(self.frame_sailor, text="Sailor Name:", bg="#006f9b", fg="white")
        self.label_sailor_name.grid(row=0, column=0, pady=5)

        self.entry_sailor_contact = tk.Entry(self.frame_sailor, width=30)
        self.entry_sailor_contact.grid(row=1, column=1, pady=5)

        self.label_sailor_contact = tk.Label(self.frame_sailor, text="Sailor Contact:", bg="#006f9b", fg="white")
        self.label_sailor_contact.grid(row=1, column=0, pady=5)

        self.button_add_sailor = tk.Button(self.frame_sailor, text="Add Sailor", command=self.add_sailor, bg="#0288d1", fg="white")
        self.button_add_sailor.grid(row=2, column=0, columnspan=2, pady=10)

        # Cart Section
        self.frame_cart = tk.LabelFrame(self.root, text="Cart", padx=10, pady=10, bg="#006f9b", fg="white")
        self.frame_cart.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

        self.label_cart_details = tk.Label(self.frame_cart, text="Products in Cart:", font=("Arial", 12), bg="#006f9b", fg="white")
        self.label_cart_details.grid(row=0, column=0, columnspan=2)

        self.cart_listbox = tk.Listbox(self.frame_cart, height=10, width=50, bg="#c6e0f7", fg="black")
        self.cart_listbox.grid(row=1, column=0, columnspan=2)

        # Billing Section (Beside Cart Section)
        self.frame_billing = tk.LabelFrame(self.root, text="Billing", padx=10, pady=10, bg="#006f9b", fg="white")
        self.frame_billing.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")

        self.label_billing_details = tk.Label(self.frame_billing, text="Bill Details:", font=("Arial", 12), bg="#006f9b", fg="white")
        self.label_billing_details.grid(row=0, column=0, columnspan=2)

        self.button_generate_bill = tk.Button(self.frame_billing, text="Generate Bill", command=self.generate_bill, bg="#0288d1", fg="white")
        self.button_generate_bill.grid(row=1, column=0, columnspan=2, pady=10)

        self.text_bill = tk.Text(self.frame_billing, width=50, height=10, bg="#f2f2f2", fg="black")
        self.text_bill.grid(row=2, column=0, columnspan=2)

        # Make sure the grid expands to fill the window size
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(1, weight=2)
        self.root.grid_rowconfigure(2, weight=5)

        # Update the time and date display
        self.update_time()

    def update_time(self):
        """ Update the current time and date """
        current_time = strftime('%Y-%m-%d %H:%M:%S')
        self.label_time.config(text=current_time)
        self.label_time.after(1000, self.update_time)

    def load_products(self):
        """ Load available products into the listbox """
        self.product_listbox.delete(0, tk.END)
        self.available_products.clear()  # Clear the existing products

        self.cursor.execute("SELECT id, name, quantity, price FROM products")
        for (product_id, name, quantity, price) in self.cursor.fetchall():
            self.available_products[product_id] = (name, quantity, price)
            self.product_listbox.insert(tk.END, f"{name} - Quantity: {quantity}, Price: ₹{price:.2f}")

    def add_sailor(self):
        """ Add sailor details to the sailor section """
        sailor_name = self.entry_sailor_name.get()
        sailor_contact = self.entry_sailor_contact.get()

        if not sailor_name or not sailor_contact:
            messagebox.showerror("Input Error", "Please fill all sailor fields!")
            return
        try:
            self.cursor.execute("INSERT INTO sailors (name, contact) VALUES (%s, %s)", (sailor_name, sailor_contact))
            self.db.commit()
            messagebox.showinfo("Success", "Sailor added successfully!")
            self.entry_sailor_name.delete(0, tk.END)
            self.entry_sailor_contact.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def add_product(self):
        """ Add product to the store by the sailor """
        product_name = self.entry_product_name.get()
        quantity = self.entry_product_quantity.get()
        price = self.entry_product_price.get()

        if not product_name or not quantity or not price:
            messagebox.showerror("Input Error", "Please fill all product fields!")
            return

        if not quantity.isdigit() or not price.replace(".", "", 1).isdigit():
            messagebox.showerror("Input Error", "Invalid quantity or price!")
            return
        try:
            self.cursor.execute("INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)",
                                (product_name, int(quantity), float(price)))
            self.db.commit()
            messagebox.showinfo("Success", "Product added successfully!")
            self.entry_product_name.delete(0, tk.END)
            self.entry_product_quantity.delete(0, tk.END)
            self.entry_product_price.delete(0, tk.END)

            # Load products from the database after adding
            self.load_products()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def save_receiver(self):
        """ Save receiver details and check if products are added to cart """
        receiver_name = self.entry_receiver_name.get()
        receiver_contact = self.entry_receiver_contact.get()
        receiver_address = self.entry_receiver_address.get()

        if not receiver_name or not receiver_contact or not receiver_address:
            messagebox.showerror("Input Error", "Please fill all receiver fields!")
            return

        self.receivers[receiver_name] = (receiver_contact, receiver_address)

        # Store the current receiver for future bill generation
        self.current_receiver = receiver_name

        # Clear receiver fields
        self.entry_receiver_name.delete(0, tk.END)
        self.entry_receiver_contact.delete(0, tk.END)
        self.entry_receiver_address.delete(0, tk.END)

        messagebox.showinfo("Receiver Saved", "Receiver details saved successfully!")

        try:
            # Insert receiver details into the receivers table
            self.cursor.execute(
        "INSERT INTO receivers (name, contact, address) VALUES (%s, %s, %s)",
        (receiver_name, receiver_contact, receiver_address)  # Ensure receiver_address is included
    )

            self.db.commit()
            messagebox.showinfo("Receiver Added", f"{receiver_name} added to the receivers list.")

        except mysql.connector.Error as err:
            # Show an error message if there was a problem
            messagebox.showerror("Database Error", f"Error: {err}")  # Correctly reference err

    def add_to_cart(self):
        """ Add selected product and quantity to cart """
        selected_product = self.product_listbox.curselection()
        quantity = self.entry_quantity.get()

        if not selected_product or not quantity.isdigit():
            messagebox.showerror("Selection Error", "Please select a product and specify quantity!")
            return

        selected_product_id = list(self.available_products.keys())[selected_product[0]]
        product_name, available_quantity, price = self.available_products[selected_product_id]

        if int(quantity) > available_quantity:
            messagebox.showerror("Quantity Error", "Selected quantity exceeds available stock!")
            return

        self.cart.append((selected_product_id, product_name, int(quantity), price))
        self.update_cart_display()

        # Insert into cart table
        try:
            self.cursor.execute(
                "INSERT INTO cart (product_id, product_name, quantity, price) VALUES (%s, %s, %s, %s)",
                (selected_product_id, product_name, int(quantity), price)
            )
            self.db.commit()
            messagebox.showinfo("Product Added", f"{product_name} added to cart.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def update_cart_display(self):
        """ Update cart listbox to show current cart items """
        self.cart_listbox.delete(0, tk.END)
        for item in self.cart:
            self.cart_listbox.insert(tk.END, f"{item[1]} - Quantity: {item[2]}, Price: ₹{item[2] * item[3]:.2f}")

    def generate_bill(self):
        """ Generate and display bill """
        if not self.cart:
            messagebox.showerror("Cart Error", "Your cart is empty!")
            return

        if not self.current_receiver:
            messagebox.showerror("Receiver Error", "Receiver details not saved!")
            return

        receiver_name = self.current_receiver
        receiver_contact, receiver_address = self.receivers[receiver_name]

        # Calculate total bill
        total_amount = sum([item[2] * item[3] for item in self.cart])

        # Display Bill
        bill_details = f"Receiver: {receiver_name}\nContact: {receiver_contact}\nAddress: {receiver_address}\n\n"
        bill_details += "Products:\n"
        for item in self.cart:
            bill_details += f"{item[1]} - Quantity: {item[2]}, Price: ₹{item[2] * item[3]:.2f}\n"
        
        bill_details += f"\nTotal: ₹{total_amount:.2f}"
        self.text_bill.delete(1.0, tk.END)
        self.text_bill.insert(tk.END, bill_details)
        
        # Clear cart after generating bill
        self.cart.clear()
        self.update_cart_display()
        messagebox.showinfo("Bill Generated", f"Bill generated successfully for {receiver_name}")

if _name_ == "_main_":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
