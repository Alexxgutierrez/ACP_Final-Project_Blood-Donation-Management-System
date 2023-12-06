import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import tkcalendar as tkc
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from tkinter import PhotoImage, font

class BasePage(tk.Tk): 
    def __init__(self, title, geometry):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.configure(bg="#fff")
        self.resizable(True, True)

        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Blood_DB"
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

class LoginPage(BasePage):
    def __init__(self):
        super().__init__('Login', '850x500')

        self.login_frame = Frame(self, background="white")
        self.login_frame.pack(expand=20)

        self.heading = Label(self.login_frame, text='Login', fg='#df4145', bg='white', font=('MonoLisa', 23, 'bold'))
        self.heading.grid(row=1, column=1, pady=(20, 0)) 
        self.img = PhotoImage(file='bdms.png')
        Label(self.login_frame, image=self.img, bg='white').grid(row=1, column=0, rowspan=3, padx=(20, 0)) 

        self.user = Entry(self.login_frame, width=25, fg='#df4145', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
        self.user.place(x=430, y=120) 
        
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', self.on_enter_user)
        self.user.bind('<FocusOut>', self.on_leave_user)

        Frame(self.login_frame, width=200, height=2, bg='black').place(x=430, y=150) 

        self.code = Entry(self.login_frame, width=25, fg='#df4145', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
        self.code.grid(row=3, column=1, pady=10)
        
        self.code.place(x=430,y=200)
        self.code.insert(0, 'Password')
        self.code.bind('<FocusIn>', self.on_enter_code)
        self.code.bind('<FocusOut>', self.on_leave_code)

        Frame(self.login_frame, width=200, height=2, bg='black').place(x=430, y=230) 

        Button(self.login_frame, width=22, pady=7, text='Login', bg='#df4145', fg='white', border=0, command=self.signin).grid(row=3, column=1, pady=(190, 20))
        
    def on_enter_user(self, e):
        if (self.user.get() == 'Username'):
            self.user.delete(0, 'end')

    def on_leave_user(self, e):
        name = self.user.get()
        if name == '':
            self.user.insert(0, 'Username')

    def on_enter_code(self, e):
        if (self.code.get() == 'Password'):
            self.code.delete(0, 'end')
        self.code.config(show='*')

    def on_leave_code(self, e):
        name = self.code.get()
        if name == '':
            self.code.config(show='')  
            self.code.insert(0, 'Password')

    def signin(self):
        username = self.user.get()
        password = self.code.get()

        if username == 'admin' and password == '1234':
            self.open_home_page()
        else:
            messagebox.showerror("Invalid", "Invalid username and password")

    def open_home_page(self):
        self.destroy()
        home_page = HomePage()
        home_page.mainloop()
         
class HomePage(BasePage):
    def __init__(self):
        super().__init__('HomePage', '1920x1080')

        self.sidebar_frame = Frame(self, bg='#353A40', width=200)
        self.sidebar_frame.pack(side=LEFT, fill=Y)

        self.topbar_frame = Frame(self, bg='#df4145', height=75)
        self.topbar_frame.pack(side=TOP, fill=X)

        logo_image = PhotoImage(file="bdmslogo.png")

        logo_label = Label(self.sidebar_frame, image=logo_image, bg='#353A40')
        logo_label.image = logo_image
        logo_label.grid(row=0, column=0, sticky="nw", padx=40, pady=5)

        self.content_frame = Frame(self, bg='#E5E4E2', width=700, height=400)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True) 

        button_font = font.Font(family='Verdana', size=12)

        self.selected_button = None  

        dashboard_button = tk.Button(self.sidebar_frame, text="DASHBOARD", command=lambda: self.handle_button_click(self.show_dashboard, dashboard_button), fg='#df4145', bg='white', height=2, width=15, font=button_font, relief='flat')
        dashboard_button.grid(row=1, column=0, pady=(20, 25))

        manage_donors_button = tk.Button(self.sidebar_frame, text="DONORS", command=lambda: self.handle_button_click(self.open_manage_donors, manage_donors_button), fg='#df4145', bg='white', height=2, width=15, font=button_font, relief='flat')
        manage_donors_button.grid(row=2, column=0, pady=25)

        manage_donations_button = tk.Button(self.sidebar_frame, text="DONATIONS", command=lambda: self.handle_button_click(self.open_manage_donations, manage_donations_button), bg='white', fg='#df4145', height=2, width=15, font=button_font, relief='flat')
        manage_donations_button.grid(row=3, column=0, pady=25)

        logout_button = tk.Button(self.sidebar_frame, text="LOGOUT", command=lambda: self.handle_button_click(self.logout, logout_button), fg='#df4145', bg='white', height=2, width=15, font=button_font, relief='flat')
        logout_button.grid(row=4, column=0, pady=25)

        self.heading_label = tk.Label(self.topbar_frame, text="DASHBOARD    ", font=("Helvetica", 37), bg='#df4145',fg='white')
        self.heading_label.pack(side=tk.LEFT, padx=20, pady=20)

        self.show_dashboard()

    def highlight_button(self, button):
        if self.selected_button:
            self.selected_button.config(bg='white')

        self.selected_button = button

    def handle_button_click(self, callback, button):
        if self.selected_button:
            self.selected_button.config(bg='white')

        if button.cget("text") != "LOGOUT":
            self.selected_button = button

            page_title = button.cget("text")
            self.heading_label.config(text=page_title)

        callback()

    def show_dashboard(self):
        blood_type_donations = self.calculate_blood_type_donations()

        for widget in self.content_frame.winfo_children():
            widget.destroy()
  
        blood_image = PhotoImage(file='bloodrop2.png')
        
        blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        for i, blood_type in enumerate(blood_types):
            row = i // 4  
            col = i % 4   

            frame = Frame(self.content_frame, bg='#E0FFFF', width=200, height=105, bd=2, relief="groove")
            frame.pack_propagate(False)
            frame.grid(row=row, column=col, padx=55, pady=60)

            blood_label = Label(frame, image=blood_image, bg='#E0FFFF')
            blood_label.image = blood_image
            blood_label.place(x=160,y=5)

            type_label = Label(frame, text=blood_type, font=("Helvetica", 16, "bold"), bg='#E0FFFF')
            type_label.place(x=115, y=10)

            amount_label = Label(frame, text=f"{blood_type_donations.get(blood_type, 0)} mL", bg='#E0FFFF')
            amount_label.place(x=2, y=80)

        self.content_frame.grid_columnconfigure(4, weight=1)

    def calculate_blood_type_donations(self):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "SELECT DISTINCT Blood_Type, SUM(Amount) AS Total_Amount FROM Blood_Donations GROUP BY Blood_Type"
            cursor.execute(query)
            blood_type_donations = {row[0]: row[1] for row in cursor.fetchall()}

            blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            for blood_type in blood_types:
                if blood_type not in blood_type_donations:
                    blood_type_donations[blood_type] = 0

            return blood_type_donations

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error fetching blood type donations.")

        finally:
            if cursor:
                cursor.close()

    def open_manage_donors(self):
        self.content_frame.pack_forget()
        self.content_frame = Frame(self, bg='#E5E4E2', width=600, height=400)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        manage_donors_page = ManageDonorsPage(master=self.content_frame, connection=self.connection)
        manage_donors_page.pack(fill=BOTH, expand=True)

    def open_manage_donations(self):
        self.content_frame.pack_forget()
        self.content_frame = Frame(self, bg='#E5E4E2', width=600, height=400)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        manage_donations_page = ManageDonationsPage(master=self.content_frame, connection=self.connection)
        manage_donations_page.pack(fill=BOTH, expand=True)

    def logout(self):
        confirm_logout = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        
        if confirm_logout:
            self.destroy()
            LoginPage().mainloop()
        
class ManageDonorsPage(Frame):
    def __init__(self, master=None, connection=None):
        super().__init__(master)
        self.connection = connection  
        self.add_donor_window = None
        self.update_donor_window = None
        
        self.name_entry = None
        self.age_entry = None
        self.sex_entry = None
        self.blood_type = None
        self.address_entry = None
        self.contact_number_entry = None

        columns = ("Donor ID", "Name", "Sex", "Age", "Blood Type", "Address", "Contact Number")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        self.tree.column("Donor ID", width=100)  
        self.tree.column("Name", width=250)  
        self.tree.column("Sex", width=100)  
        self.tree.column("Age", width=100)
        self.tree.column("Blood Type", width=100)  
        self.tree.column("Address", width=250)  
        self.tree.column("Contact Number", width=200)  

        for col in columns:
            self.tree.heading(col, text=col)
            
        self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF")
        self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41")

        self.tree.pack(pady=20) 
        self.populate_table()
        
        style = ttk.Style()
        style.configure('Blood.TButton', foreground='#353A40', background='#df4145', font=('Arial', 12, 'bold'))

        add_button = ttk.Button(self, text="Add Donor", command=self.add_donor, style='Blood.TButton')
        update_button = ttk.Button(self, text="Update Donor", command=self.update_donor, style='Blood.TButton')
        delete_button = ttk.Button(self, text="Delete Donor", command=self.delete_donor, style='Blood.TButton')
        filter_button = ttk.Button(self, text="Filter by Blood Type", command=self.apply_filters, style='Blood.TButton')

        add_button.place(x=115, y=320)
        update_button.place(x=360, y=320)
        delete_button.place(x=640, y=320) 
        filter_button.place(x=925, y=320)

        self.blood_type_filter_entry = ttk.Combobox(self, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        self.blood_type_filter_entry.configure(state='readonly') 
        
        self.blood_type_filter_entry.place(x=925, y=360)

    def apply_filters(self):
        blood_type_filter = self.blood_type_filter_entry.get()
        try:
            cursor = self.connection.cursor()

            self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF", anchor='center')
            self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41", anchor='center')
            
            query = "SELECT Donor_ID, Name, Sex, Age, Blood_Type, Address, Contact_Number FROM donors WHERE Blood_Type=%s"
            cursor.execute(query, (blood_type_filter,))
            filtered_donors = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, donor in enumerate(filtered_donors):
                row_tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.tree.insert("", "end", values=donor, tags=row_tags)

        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()

    def add_donor(self):
        add_donor_window = tk.Toplevel(self)
        add_donor_window.title("Add Donor")

        name_entry = tk.Entry(add_donor_window)
        sex_entry = ttk.Combobox(add_donor_window, values=["Male", "Female"])
        sex_entry.configure(state='readonly')
        age_entry = tk.Entry(add_donor_window)
        blood_type = ttk.Combobox(add_donor_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        blood_type.configure(state='readonly') 
        address_entry = tk.Entry(add_donor_window)
        contact_number_entry = tk.Entry(add_donor_window)

        tk.Label(add_donor_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Sex:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Age:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Blood Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Address:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Contact Number:").grid(row=5, column=0, padx=10, pady=5, sticky="e")

        name_entry.grid(row=0, column=1, padx=10, pady=5)
        sex_entry.grid(row=1, column=1, padx=10, pady=5)
        age_entry.grid(row=2, column=1, padx=10, pady=5)
        blood_type.grid(row=3, column=1, padx=10, pady=5)
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        contact_number_entry.grid(row=5, column=1, padx=10, pady=5)

        save_button = tk.Button(add_donor_window, text="Save Donor", command=lambda: self.save_donor_info_entry(
        name_entry.get(), sex_entry.get(), age_entry.get(), blood_type.get(), address_entry.get(), contact_number_entry.get()))
        save_button.grid(row=6, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.set('')
            age_entry.delete(0, 'end')
            blood_type.set('') 
            address_entry.delete(0, 'end')
            contact_number_entry.delete(0, 'end')

        clear_button = tk.Button(add_donor_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=7, columnspan=2, pady=10)

    def update_donor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donor to update.")
            return

        donor_info = self.tree.item(selected_item, 'values')
        donor_id = donor_info[0]

        update_donor_window = tk.Toplevel(self)
        update_donor_window.title("Update Donor")

        name_entry = tk.Entry(update_donor_window)
        sex_entry = ttk.Combobox(update_donor_window, values=["Male", "Female"])
        sex_entry.configure(state='readonly') 
        age_entry = tk.Entry(update_donor_window)
        blood_type = ttk.Combobox(update_donor_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        blood_type.configure(state='readonly')  
        address_entry = tk.Entry(update_donor_window)
        contact_number_entry = tk.Entry(update_donor_window)

        tk.Label(update_donor_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Sex:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Age:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Blood Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Address:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Contact Number:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        sex_entry.grid(row=1, column=1, padx=10, pady=5)
        age_entry.grid(row=2, column=1, padx=10, pady=5)
        blood_type.grid(row=3, column=1, padx=10, pady=5)
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        contact_number_entry.grid(row=5, column=1, padx=10, pady=5)

        name_entry.insert(0, donor_info[1])
        sex_entry.set(donor_info[2])
        age_entry.insert(0, donor_info[3])
        blood_type.set(donor_info[4])
        address_entry.insert(0, donor_info[5])
        contact_number_entry.insert(0, donor_info[6])

        save_button = tk.Button(update_donor_window, text="Save Changes", command=lambda: self.save_updated_donor_info(
        donor_id, name_entry.get(), sex_entry.get(), age_entry.get(), blood_type.get(), address_entry.get(), contact_number_entry.get()))
        save_button.grid(row=6, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.set('')
            age_entry.delete(0, 'end')
            blood_type.set('')
            address_entry.delete(0, 'end')
            contact_number_entry.delete(0, 'end')

        clear_button = tk.Button(update_donor_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=7, columnspan=2, pady=10)
        
    def save_donor_info_entry(self, name, sex, age, blood_type, address, contact_number):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO donors (Name, Sex, Age, Blood_Type, Address, Contact_Number) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, sex, age, blood_type, address, contact_number)
            cursor.execute(query, values)
            
            self.connection.commit()
            messagebox.showinfo("Success", "Donor information saved successfully!")

            self.populate_table()
            self.clear_add_donor_fields()

            self.add_donor_window.destroy()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error saving donor information.")

        finally:
            if cursor:
                cursor.close()

    def save_updated_donor_info(self, donor_id, name, sex, age, blood_type, address, contact_number):
        print(donor_id)
        try:
            cursor = self.connection.cursor()
            query = "UPDATE donors SET Name=%s, Sex=%s, Age=%s, Blood_Type=%s, Address=%s, Contact_Number=%s WHERE Donor_ID=%s"
            values = (name, sex, age, blood_type, address, contact_number, donor_id)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Donor information updated successfully!")

            self.populate_table()
            self.clear_update_donor_fields()
            self.update_donor_window.destroy()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error updating donor information.")

        finally:
            if cursor:
                cursor.close()
                
    def clear_add_donor_fields(self):
        self.name_entry.__delattr__(0,'end')
        self.sex_entry.__setattr__('')
        self.age_entry.__delattr__(0,'end')
        self.blood_type.__setattr__('')  
        self.address_entry.__delattr__(0,'end')
        self.contact_number_entry.__delattr__(0,'end')
        
    def clear_update_donor_fields(self):
        self.name_entry.__delattr__(0, 'end')
        self.sex_entry.__setattr__('')
        self.age_entry.__delattr__(0, 'end')
        self.blood_type.__setattr__('')  
        self.address_entry.__delattr__(0, 'end')
        self.contact_number_entry.__delattr__(0, 'end')
                
    def delete_donor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donor to delete.")
            return

        donor_info = self.tree.item(selected_item, 'values')
        donor_id = donor_info[0] 
        
        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {donor_info[1]}?")
        if confirmation:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM donors WHERE Donor_ID=%s"
                cursor.execute(query, (donor_id,))

                self.connection.commit()
                messagebox.showinfo("Success", "Donor deleted successfully!")

                self.populate_table()

            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Error deleting donor.")

            finally:
                if cursor:
                    cursor.close()

    def populate_table(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT Donor_Id, Name, Sex, Age, Blood_Type, Address, Contact_Number FROM donors"
            cursor.execute(query)
            donors = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)
            
            center_columns = ("Donor ID", "Name", "Sex", "Age", "Blood Type", "Address", "Contact Number")
            for col in center_columns:
                self.tree.column(col, anchor='center')

            self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF", anchor='center')
            self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41", anchor='center')

            for i, donor in enumerate(donors):
                row_tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.tree.insert("", "end", values=donor, tags=row_tags)

        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()

class ManageDonationsPage(Frame):
    def __init__(self, master=None, connection=None):
        super().__init__(master)
        self.connection = connection 
        self.add_donation_window = None
        self.update_donation_window = None
        
        self.name_entry = None
        self.sex_entry = None
        self.blood_type = None
        self.donation_date = None
        self.blood_amount = None

        columns = ("Donation ID", "Name", "Sex", "Blood Type", "Date of Donation", "Amount (ml)")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
      
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        self.tree.column("Donation ID", width=100) 
        self.tree.column("Name", width=250)
        self.tree.column("Sex", width=100)
        self.tree.column("Blood Type", width=100)
        self.tree.column("Date of Donation", width=250)
        self.tree.column("Amount (ml)", width=170)
        
        for col in columns:
            self.tree.heading(col, text=col)
            
        self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF")
        self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41")
        
        self.tree.pack(pady=20)
        self.tree.place(x=115,y=50)
        
        style = ttk.Style()
        style.configure('Blood.TButton', foreground='#353A40', background='#df4145', font=('Arial', 12, 'bold'))
        
        add_button = ttk.Button(self, text="Add Donation", command=self.add_donation, style='Blood.TButton')
        update_button = ttk.Button(self, text="Update Donation", command=self.update_donation, style='Blood.TButton')
        delete_button = ttk.Button(self, text="Delete Donation", command=self.delete_donation, style='Blood.TButton')
        filter_button = ttk.Button(self, text="Filter by Blood Type", command=self.apply_filters, style='Blood.TButton')

        add_button.place(x=115, y=320)
        update_button.place(x=360, y=320)
        delete_button.place(x=640, y=320) 
        filter_button.place(x=925, y=320)

        self.blood_type_filter_entry = ttk.Combobox(self, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        self.blood_type_filter_entry.configure(state='readonly')  
        
        self.blood_type_filter_entry.place(x=925, y=360)

        self.populate_table()
        
    def add_donation(self):
        add_donation_window = tk.Toplevel(self)
        add_donation_window.title("Add Donation")

        name_entry = tk.Entry(add_donation_window)
        sex_entry = ttk.Combobox(add_donation_window, values=["Male", "Female"])
        sex_entry.configure(state='readonly')  
        blood_type = ttk.Combobox(add_donation_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        blood_type.configure(state='readonly')  
        donation_date = tkc.DateEntry(add_donation_window)
        donation_date.configure(state='readonly') 
        blood_amount = tk.Entry(add_donation_window)

        tk.Label(add_donation_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donation_window, text="Sex:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donation_window, text="Blood Type:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donation_window, text="Date of Donation:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donation_window, text="Amount (mL):").grid(row=4, column=0, padx=10, pady=5, sticky="e")

        name_entry.grid(row=0, column=1, padx=10, pady=5)
        sex_entry.grid(row=1, column=1, padx=10, pady=5)
        blood_type.grid(row=2, column=1, padx=10, pady=5)
        donation_date.grid(row=3, column=1, padx=10, pady=5)
        blood_amount.grid(row=4, column=1, padx=10, pady=5)

        save_button = tk.Button(add_donation_window, text="Save Donation", command=lambda: self.save_donation(
        name_entry.get(), sex_entry.get(), blood_type.get(), donation_date.get(), blood_amount.get()))
        save_button.grid(row=5, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.set('')
            blood_type.set('')  
            donation_date.set_date('01/01/01')
            blood_amount.delete(0, 'end')

        clear_button = tk.Button(add_donation_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=6, columnspan=2, pady=10)

    def update_donation(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donation to update.")
            return

        donation_info = self.tree.item(selected_item, 'values')
        donation_id = donation_info[0]

        update_donation_window = tk.Toplevel(self)
        update_donation_window.title("Update Donation")

        name_entry = tk.Entry(update_donation_window)
        sex_entry = ttk.Combobox(update_donation_window, values=["Male", "Female"])
        sex_entry.configure(state='readonly') 
        blood_type = ttk.Combobox(update_donation_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        blood_type.configure(state='readonly')  
        donation_date = tkc.DateEntry(update_donation_window)
        donation_date.configure(state='readonly') 
        blood_amount = tk.Entry(update_donation_window)

        tk.Label(update_donation_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donation_window, text="Sex:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donation_window, text="Blood Type:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donation_window, text="Date of Donation:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donation_window, text="Amount (mL):").grid(row=4, column=0, padx=10, pady=5, sticky="e")

        name_entry.grid(row=0, column=1, padx=10, pady=5)
        sex_entry.grid(row=1, column=1, padx=10, pady=5)
        blood_type.grid(row=2, column=1, padx=10, pady=5)
        donation_date.grid(row=3, column=1, padx=10, pady=5)
        blood_amount.grid(row=4, column=1, padx=10, pady=5)
      
        name_entry.insert(0, donation_info[1])
        sex_entry.set(donation_info[2])
        blood_type.set(donation_info[3])

        old_date_format = "%Y-%m-%d"  
        new_date_format = "%m/%d/%y" 

        parsed_date = datetime.strptime(donation_info[4], old_date_format)
        formatted_date = parsed_date.strftime(new_date_format)
        donation_date.set_date(formatted_date)
        
        blood_amount.insert(0, donation_info[5])

        save_button = tk.Button(update_donation_window, text="Save Donation", command=lambda: self.save_update_donation(donation_id,
        name_entry.get(), sex_entry.get(), blood_type.get(), donation_date.get(), blood_amount.get()))
        save_button.grid(row=5, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.set('')  
            blood_type.set('')  
            donation_date.set_date('01/01/01') 
            blood_amount.delete(0, 'end')  

        clear_button = tk.Button(update_donation_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=6, columnspan=2, pady=10)
                
    def clear_add_donation_fields(self):
        self.name_entry.__delattr__(0, 'end')
        self.sex_entry.__setattr__('')
        self.blood_type.__setattr__('') 
        self.donation_date.__setattr__('01/01/01')
        self.blood_amount.__delattr__(0, 'end')
                
    def clear_update_donation_fields(self):
        self.name_entry.__delattr__(0, 'end')
        self.sex_entry.__setattr__('')
        self.blood_type.__setattr__('')  
        self.donation_date.__setattr__('01/01/01')
        self.blood_amount.__delattr__(0, 'end')

    def save_donation(self, name, sex, blood_type, date, amount):
        try:
            formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")

            cursor = self.connection.cursor()
            query = "INSERT INTO blood_donations (Name, Sex, Blood_Type, Date_of_Donation, Amount) VALUES (%s, %s, %s, %s, %s)"
            values = (name, sex, blood_type, formatted_date, amount)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Blood donation information added successfully!")

            self.populate_table()
            self.clear_add_donation_fields()
            self.add_donation_window.destroy() 

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error adding blood donation information.")

        finally:
            if cursor:
                cursor.close()

    def save_update_donation(self, donation_id, name, sex, blood_type, date, amount):
        try:
            formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")

            
            cursor = self.connection.cursor()
            query = "UPDATE blood_donations SET Name=%s, Sex=%s, Blood_Type=%s, Date_of_Donation=%s, Amount=%s WHERE Donation_ID=%s"
            values = (name, sex, blood_type, formatted_date, amount, donation_id)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Blood donation information updated successfully!")

            self.populate_table()
            self.clear_update_donation_fields() 
            self.update_donation_window.destroy()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error updating blood donation information.")

        finally:
            if cursor:
                cursor.close()

    def delete_donation(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donation to delete.")
            return

        donation_info = self.tree.item(selected_item, 'values')
        donation_id = donation_info[0] 

        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {donation_info[1]}?")
        if confirmation:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM blood_donations WHERE Donation_ID=%s"
                cursor.execute(query, (donation_id,))

                self.connection.commit()
                messagebox.showinfo("Success", "Blood donation deleted successfully!")

                self.populate_table()

            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Error deleting blood donation.")

            finally:
                if cursor:
                    cursor.close()

    def apply_filters(self):
        blood_type_filter = self.blood_type_filter_entry.get()

        try:
            cursor = self.connection.cursor()
            query = "SELECT Donation_ID, Name, Sex, Blood_Type, Date_of_Donation, Amount FROM blood_donations WHERE Blood_Type=%s"
            cursor.execute(query, (blood_type_filter,))
            filtered_donors = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF", anchor='center')
            self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41", anchor='center')

            for i, donor in enumerate(filtered_donors):
                row_tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.tree.insert("", "end", values=donor, tags=row_tags)

        except Error as e:
                print(f"Error: {e}")

        finally:
                if cursor:
                    cursor.close()
        pass

    def populate_table(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT Donation_ID, Name, Sex, Blood_Type, Date_of_Donation, Amount FROM blood_donations"
            cursor.execute(query)
            donations = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            center_columns = ("Donation ID", "Name", "Sex", "Blood Type", "Date of Donation", "Amount (ml)")
            for col in center_columns:
                self.tree.column(col, anchor='center')

            self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF", anchor='center')
            self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41", anchor='center')

            for i, donor in enumerate(donations):
                row_tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.tree.insert("", "end", values=donor, tags=row_tags)

        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()

if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()