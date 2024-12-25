import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3


class CustomLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Others(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#A294F9", width=1500, height=750)
        self.controller = controller
        self.pack_propagate(0)

        label = CustomLabel(self, text="OTHERS", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 45))
        label.pack(pady=15, padx=10)

        # Create the input fields as instance variables
        date = tk.Label(self, text="DATE :", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 35))
        date.pack(pady=10, padx=10) 
        date.place(x=350, y=150)
        self.entry_date = DateEntry(self, width=20, font=('Arial', 35), date_pattern='dd/mm/yyyy')
        self.entry_date.pack(pady=10, padx=10)
        self.entry_date.place(x=900, y=150)
        self.modify_calendar()

        # Vehicle number input field
        product_name = tk.Label(self, text="PRODUCT NAME :", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 35))
        product_name.pack(pady=10, padx=10)
        product_name.place(x=350, y=250)
        self.entry_product_name = tk.Entry(self, width=20, font=('Arial', 35))
        self.entry_product_name.pack(pady=10, padx=10)
        self.entry_product_name.place(x=900, y=250)

        # Vehicle type input field
        customer_name = tk.Label(self, text="CUSTOMER :", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 35))
        customer_name.pack(padx=100, pady=30)
        customer_name.place(x=350, y=350)
        self.entry_customer_name = tk.Entry(self, width=20, font=('Arial', 35))
        self.entry_customer_name.pack(pady=10, padx=10)
        self.entry_customer_name.place(x=900, y=350)

        # Customer name input field
        location = tk.Label(self, text="LOCATION :", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 35))
        location.pack(pady=10, padx=10)
        location.place(x=350, y=450)
        self.entry_location = tk.Entry(self, width=20, font=('Arial', 35))
        self.entry_location.pack(pady=10, padx=10)
        self.entry_location.place(x=900, y=450)

        # Amount input field
        amount = tk.Label(self, text="AMOUNT :", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 35))
        amount.pack(pady=10, padx=10)
        amount.place(x=350, y=550)
        self.entry_amount = tk.Entry(self, width=20, font=('Arial', 35))
        self.entry_amount.pack(pady=10, padx=10)
        self.entry_amount.place(x=900, y=550)

        # Submit button
        submit = tk.Button(self, text="Submit", command=self.insert_data, bg="#1B1833", fg="#A294F9", cursor="hand2", font=("Arial", 30))
        submit.pack()
        submit.place(x=1270, y=650)

       
        # Navigation labels
        labels = [
            ("Sticker", "Sticker"),
            ("Flex", "Flex"),
            ("Frame", "Frame"),
            ("Others", "Others"),
            ("Admin", "Admin"),
            ("Home","Home"),
            ]

        for i, (text, frame_name) in enumerate(labels):
            label = tk.Label(
            self, text=text, font=("Arial", 35), fg="#1B1833",
            cursor="hand2", bg="#A294F9",anchor="w"  # You can set background color if needed
            )
    
            # Set label position using place
            label.place(x=100, y=150 + (i * 100))  # Adjust the x, y coordinates as needed

            # Bind the label to switch frames on click
            label.bind("<Button-1>", lambda event, name=frame_name: controller.show_frame(name))


    # Insert data into the database function
    def insert_data(self):
        # Get the values from the input fields
        date = self.entry_date.get_date()
        product_name = self.entry_product_name.get()
        customer_name = self.entry_customer_name.get()
        location = self.entry_location.get()
        amount = self.entry_amount.get()

        # Message box for validation
        if not date or not product_name or not customer_name or not location  or not amount:
            messagebox.showerror("Error", "Fill in all fields!")
            return 

        # Insert the data into the database
        conn = sqlite3.connect("am.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS others (date TEXT, size TEXT, customer_name TEXT, location TEXT, amount TEXT)")
        cursor.execute("INSERT INTO others (date, product_name, customer_name,location, amount) VALUES (?, ?, ?, ?, ?)", 
                       (date, product_name, customer_name, location , amount))
        conn.commit()
        conn.close()

        # Show success message
        messagebox.showinfo("Success", "Data inserted successfully!")

        # Clear the input fields
        self.entry_date.set_date("")
        self.entry_product_name.delete(0, tk.END)
        self.entry_customer_name.delete(0, tk.END)
        self.entry_location.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)

    def modify_calendar(self):
        # Access the calendar popup and modify its size
        cal = self.entry_date._top_cal
        if cal:
            cal.update_idletasks()
            cal.geometry('610x450')  # Adjust the size as needed
