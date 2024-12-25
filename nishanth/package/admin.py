import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CustomLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Admin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#A294F9", width=1500, height=750)
        self.controller = controller
        self.pack_propagate(0) 

        label = CustomLabel(self, text="HI NISHANTH,welcome back....",bg="#A294F9", fg="#1B1833", cursor="hand2",font=("Arial",30))
        label.pack(pady=10, padx=10)
        label.place(x=30,y=30)
         
        # Date selection widgets
        self.from_date_label = tk.Label(self, text="From Date:", bg="#A294F9", fg="#1B1833", font=("Arial", 20))
        self.from_date_label.pack(pady=10)
        self.from_date_label.place(x=670,y=37)
        self.from_date_entry = DateEntry(self, width=10, background='darkblue', foreground='white', borderwidth=2,font=("Arial", 15),date_pattern='dd/mm/yyyy',size=10)
        self.from_date_entry.pack()
        self.from_date_entry.place(x=830,y=40)

        self.to_date_label = tk.Label(self, text="To Date:", bg="#A294F9", fg="#1B1833", font=("Arial", 20))
        self.to_date_label.pack(pady=10)
        self.to_date_label.place(x=990,y=37)
        self.to_date_entry = DateEntry(self, width=10, background='darkblue', foreground='white', borderwidth=2,font=("Arial", 15),date_pattern='dd/mm/yyyy',size=10)
        self.to_date_entry.pack()
        self.to_date_entry.place(x=1120,y=40)

        report_button = tk.Button(self, text="check", command=self.generate_report,font=("Arial",15),height=1, width=12,bg="#1B1833",fg="#A294F9")
        report_button.pack()
        report_button.place(x=1300,y=35)

        self.report_frame = tk.Frame(self, bg="#A294F9", relief=tk.SUNKEN)
        self.report_frame.place(x=20, y=100, width=1500, height=650)
        
        label = CustomLabel(self, text="back",bg="#A294F9",fg="#1B1833",cursor="hand2",font=("Arial",35))
        label.pack()
        label.place(x=30,y=650)
        # Bind the back button to switch to Home frame
        label.bind("<Button-1>", lambda event, name="Home": controller.show_frame(name))
    
    def generate_report(self):
        # Fetch data based on selected dates
        from_date = self.from_date_entry.get_date()
        to_date = self.to_date_entry.get_date()

        # List of table names to fetch data from
        table_names = ['sticker', 'flex', 'frame', 'others']

        combined_data = fetch_sales_data(table_names, from_date, to_date)
        best_customer_data = fetch_best_customer(from_date, to_date)

        # Clear the report frame
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        if not combined_data:
            report_text = "No sales data available for the selected dates."
            report_label = tk.Label(self.report_frame, text=report_text, bg="#A294F9", fg="#1B1833", font=("Arial", 45), justify=tk.LEFT)
            report_label.pack()
            report_label.place(x=100, y=100)
        else:
            # Determine the number of columns in combined_data
            num_columns = len(combined_data[0])
            
            # Create DataFrame based on the number of columns
            if num_columns == 3:
                df = pd.DataFrame(combined_data, columns=['Customer', 'Product', 'Total Sales'])
            elif num_columns == 2:
                df = pd.DataFrame(combined_data, columns=['Product', 'Total Sales'])
            else:
                print("Unexpected number of columns in combined_data")
                return

            total_sales = df['Total Sales'].sum()
            most_sales = df.loc[df['Total Sales'].idxmax()]
            least_sales = df.loc[df['Total Sales'].idxmin()]

            report_text = f"Total Sales: {total_sales}\n\n"
            most_sales_report = f"Most Sales: {most_sales['Product']} with {most_sales['Total Sales']}\n\n"
            least_sales_report = f"Least Sales: {least_sales['Product']} with {least_sales['Total Sales']}\n\n"

            report_label = tk.Label(self.report_frame, text=report_text, bg="#A294F9", fg="#1B1833", font=("Arial", 15), border=2, justify=tk.LEFT)
            report_label.pack()
            report_label.place(x=80, y=50)

            most_sales_report_label = tk.Label(self.report_frame, text=most_sales_report, bg="#A294F9", fg="#1B1833", font=("Arial", 15), border=2, justify=tk.LEFT)
            most_sales_report_label.pack()
            most_sales_report_label.place(x=80, y=90)

            least_sales_report_label = tk.Label(self.report_frame, text=least_sales_report, bg="#A294F9", fg="#1B1833", font=("Arial", 15), border=2, justify=tk.LEFT)
            least_sales_report_label.pack()
            least_sales_report_label.place(x=80, y=130)

            separate_report = ""
            for _, row in df.iterrows():
                separate_report += f"{row['Product']}: {row['Total Sales']}\n\n"

            separate_report_label = tk.Label(self.report_frame, text=separate_report, bg="#A294F9", fg="#1B1833", font=("Arial", 15), border=2, justify=tk.LEFT)
            separate_report_label.pack()
            separate_report_label.place(x=80, y=220)

             # If customer data is present, display the best customer details
            if best_customer_data:
                best_customer = best_customer_data[0]
                best_customer_text = f"Best Customer:\n{best_customer[0]} with {best_customer[1]} in purchases"
                best_customer_label = tk.Label(self.report_frame, text=best_customer_text, bg="#A294F9", fg="#FFF574", font=("Arial", 20), justify=tk.LEFT)
                best_customer_label.pack()
                best_customer_label.place(x=80, y=450)

            # Plotting the data
            fig, ax = plt.subplots(figsize=(7.3, 6.3))
            bars = ax.bar(df['Product'], df['Total Sales'], color='#1B1833')  # Set bar color here

            # Set title color
            ax.set_title('Sales Report', color='#1B1833')

            # Set x-axis and y-axis label colors
            ax.set_xlabel('Product', color='#1B1833')
            ax.set_ylabel('Total Sales', color='#1B1833')

            # Set x-tick and y-tick label colors
            ax.tick_params(axis='x', colors='#1B1833')
            ax.tick_params(axis='y', colors='#1B1833')

            # Set spine (border) colors
            ax.spines['bottom'].set_color('#1B1833')
            ax.spines['top'].set_color('#1B1833')
            ax.spines['left'].set_color('#1B1833')
            ax.spines['right'].set_color('#1B1833')

            ax.set_xticks(range(len(df['Product'])))
            ax.set_xticklabels(df['Product'], rotation=0, color='#1B1833')

            # Set background colors
            fig.patch.set_facecolor('#A294F9')  # Background color of the figure
            ax.set_facecolor('#A294F9')  # Background color of the plot

            canvas = FigureCanvasTkAgg(fig, master=self.report_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(padx=10, pady=10)
            canvas.get_tk_widget().place(x=700, y=20)

def get_db_connection():
    conn = sqlite3.connect('am.db')
    return conn

def fetch_sales_data(table_names, from_date, to_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    combined_data = []

    for table_name in table_names:
        if table_name == 'sticker' or table_name == 'flex' or table_name == 'frame' or table_name == 'others':
            product_column = 'product'
            query = f"""
                SELECT {product_column} as product, SUM(amount) as total_sales
                FROM {table_name}
                WHERE date BETWEEN ? AND ?
                GROUP BY {product_column}
            """
            cursor.execute(query, (from_date, to_date))
            data = cursor.fetchall()
            combined_data.extend(data)
        else:
            # Handle unknown table_name or product_column = 'product_name' case
            pass

    conn.close()

    return combined_data

def fetch_best_customer(from_date, to_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Combine the results from all four tables to get total sales per customer
    queries = []
    for table_name in ['sticker', 'flex', 'frame', 'others']:
        query = f"""
            SELECT customer_name, SUM(amount) as total_sales
            FROM {table_name}
            WHERE date BETWEEN ? AND ?
            GROUP BY customer_name
        """
        queries.append(query)
    
    union_query = " UNION ALL ".join(queries)
    final_query = f"""
        SELECT customer_name, SUM(total_sales) as total_sales
        FROM ({union_query})
        GROUP BY customer_name
        ORDER BY total_sales DESC
        LIMIT 1
    """
    cursor.execute(final_query, (from_date, to_date, from_date, to_date, from_date, to_date, from_date, to_date))
    best_customer = cursor.fetchall()

    conn.close()
    return best_customer
