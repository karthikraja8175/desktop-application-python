import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3


class CustomLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Sticker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#A294F9", width=1500, height=750)
        self.controller = controller
        self.pack_propagate(0)

        label = CustomLabel(self, text="STICKER", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 45))
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
        vehichle_number = tk.Label(self, text="VEHICHLE NUMBER :", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 35))
        vehichle_number.pack(pady=10, padx=10)
        vehichle_number.place(x=350, y=250)
        self.entry_vehichle_number = tk.Entry(self, width=20, font=('Arial', 35))
        self.entry_vehichle_number.pack(pady=10, padx=10)
        self.entry_vehichle_number.place(x=900, y=250)

        # Vehicle type input field
        vehichle_type = tk.Label(self, text="VEHICLE TYPE :", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 35))
        vehichle_type.pack(padx=100, pady=30)
        vehichle_type.place(x=350, y=350)
        self.entry_vehichle_type = tk.Entry(self, width=20, font=('Arial', 35))
        self.entry_vehichle_type.pack(pady=10, padx=10)
        self.entry_vehichle_type.place(x=900, y=350)

        # Customer name input field
        vehichle_name = tk.Label(self, text="CUSTOMER NAME :", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 35))
        vehichle_name.pack(pady=10, padx=10)
        vehichle_name.place(x=350, y=450)
        self.entry_vehichle_name = tk.Entry(self, width=20, font=('Arial', 35))
        self.entry_vehichle_name.pack(pady=10, padx=10)
        self.entry_vehichle_name.place(x=900, y=450)

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
        vehicle_number = self.entry_vehichle_number.get()
        vehicle_type = self.entry_vehichle_type.get()
        vehicle_name = self.entry_vehichle_name.get()
        amount = self.entry_amount.get()

        # Message box for validation
        if not date or not vehicle_number or not vehicle_type or not vehicle_name or not amount:
            messagebox.showerror("Error", "Fill in all fields!")
            return 

        # Insert the data into the database
        conn = sqlite3.connect("am.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS sticker (date TEXT, vehicle_number TEXT, vehicle_type TEXT, customer_name TEXT, amount TEXT)")
        cursor.execute("INSERT INTO sticker (date, vehicle_number, vehicle_type, customer_name, amount) VALUES (?, ?, ?, ?, ?)", 
                       (date, vehicle_number, vehicle_type, vehicle_name, amount))
        conn.commit()
        conn.close()

        # Show success message
        messagebox.showinfo("Success", "Data inserted successfully!")

        # Clear the input fields
        self.entry_date.set_date("")
        self.entry_vehichle_number.delete(0, tk.END)
        self.entry_vehichle_type.delete(0, tk.END)
        self.entry_vehichle_name.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)

    def modify_calendar(self):
        # Access the calendar popup and modify its size
        cal = self.entry_date._top_cal
        if cal:
            cal.update_idletasks()
            cal.geometry('610x450')  # Adjust the size as needed
