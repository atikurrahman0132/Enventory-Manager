import sqlite3
from tkinter import *
from tkinter import ttk

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System-Employee")
        self.root.state("zoomed")  # Fullscreen-friendly
        self.root.configure(bg="#d9d9d9")

        # === All Variables ===
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        # === Ensure Table Exists ===
        self.create_table()

        # === Search Frame ===
        SearchFrame = LabelFrame(
            self.root,
            text="Search Employee",
            bg="white",
            fg="black",
            font=("Times New Roman", 12, "bold"),
        )
        SearchFrame.pack(side=TOP, fill=X, padx=20, pady=10)

        cmb_search = ttk.Combobox(
            SearchFrame,
            textvariable=self.var_searchby,
            values=("Select", "eid", "name", "email", "contact"),
            state="readonly",
            font=("Arial", 12),
        )
        cmb_search.current(0)
        cmb_search.pack(side=LEFT, padx=10, pady=10)

        txt_search = Entry(
            SearchFrame,
            textvariable=self.var_searchtxt,
            font=("Arial", 12),
            bg="lightyellow",
        )
        txt_search.insert(0, "Search...")
        txt_search.pack(side=LEFT, padx=10, pady=10, fill=X, expand=True)

        def clear_placeholder(event):
            if txt_search.get() == "Search...":
                txt_search.delete(0, END)
                txt_search.config(fg="black")

        txt_search.bind("<FocusIn>", clear_placeholder)

        Button(
            SearchFrame,
            text="Search",
            command=self.search,
            font=("Arial", 12, "bold"),
            bg="#4caf50",
            fg="white",
        ).pack(side=LEFT, padx=10, pady=10)

        Button(
            SearchFrame,
            text="Refresh",
            command=self.show,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
        ).pack(side=LEFT, padx=10, pady=10)

        # === Title ===
        Label(
            self.root,
            text="Employee Details",
            font=("Arial", 16, "bold"),
            bg="#0F0E0E",
            fg="white",
        ).pack(side=TOP, fill=X, padx=20, pady=5)

        # === Form Frame ===
        form_frame = Frame(self.root, bg="#d9d9d9")
        form_frame.pack(fill=X, padx=20, pady=10)

        # Row 1
        self.make_label_entry(form_frame, "Emp ID:", self.var_emp_id, 0, 0)
        self.make_label_combo(form_frame, "Gender:", self.var_gender, ["Select", "Male", "Female", "Other"], 0, 1)
        self.make_label_entry(form_frame, "Contact:", self.var_contact, 0, 2)

        # Row 2
        self.make_label_entry(form_frame, "Name:", self.var_name, 1, 0)
        self.make_label_entry(form_frame, "D.O.B:", self.var_dob, 1, 1)
        self.make_label_entry(form_frame, "D.O.J:", self.var_doj, 1, 2)

        # Row 3
        self.make_label_entry(form_frame, "Email:", self.var_email, 2, 0)
        self.make_label_entry(form_frame, "Password:", self.var_pass, 2, 1)
        self.make_label_combo(
            form_frame, "User-Type", self.var_utype, ["Select", "Admin", "Employee"], 2, 2
        )

        # Row 4
        lbl_address = Label(form_frame, text="Address:", font=("Arial", 12), bg="#d9d9d9")
        lbl_address.grid(row=3, column=0, sticky=W, padx=10, pady=10)
        self.txt_address = Text(form_frame, font=("Arial", 12), height=2, width=30, bg="#FAD691")
        self.txt_address.grid(row=3, column=1, padx=10, pady=10)

        self.make_label_entry(form_frame, "Salary:", self.var_salary, 3, 2)

        # === Buttons ===
        btn_frame = Frame(self.root, bg="#d9d9d9")
        btn_frame.pack(fill=X, padx=20, pady=10)

        Button(btn_frame, text="Save", command=self.add, bg="#08CB00", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Update", command=self.update, bg="#1C6EA4", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Delete", command=self.delete, bg="#B9375D", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Clear", command=self.clear, bg="#7A85C1", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)

        # === Employee Table ===
        table_frame = Frame(self.root, bd=2, relief=RIDGE)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.EmployeeTable = ttk.Treeview(
            table_frame,
            columns=(
                "eid", "name", "email", "gender", "contact",
                "dob", "doj", "pass", "utype", "address", "salary"
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.EmployeeTable.xview)
        scroll_y.config(command=self.EmployeeTable.yview)

        # Table Headings
        headings = [
            "Employee ID", "Name", "Email", "Gender", "Contact",
            "Date of Birth", "Date of Joining", "Password", "User-Type",
            "Address", "Salary"
        ]
        for col, text in zip(self.EmployeeTable["columns"], headings):
            self.EmployeeTable.heading(col, text=text)
            self.EmployeeTable.column(col, width=150)

        self.EmployeeTable.pack(fill=BOTH, expand=True)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()  # load data initially

    # === Helper: Label + Entry ===
    def make_label_entry(self, frame, text, variable, row, col):
        Label(frame, text=text, font=("Arial", 12), bg="#d9d9d9").grid(row=row, column=col*2, sticky=W, padx=10, pady=10)
        Entry(frame, textvariable=variable, font=("Arial", 12), bg="#FAD691").grid(row=row, column=col*2+1, padx=10, pady=10)

    # === Helper: Label + Combobox ===
    def make_label_combo(self, frame, text, variable, values, row, col):
        Label(frame, text=text, font=("Arial", 12), bg="#d9d9d9").grid(row=row, column=col*2, sticky=W, padx=10, pady=10)
        cmb = ttk.Combobox(frame, textvariable=variable, values=values, state="readonly", font=("Arial", 12))
        cmb.current(0)
        cmb.grid(row=row, column=col*2+1, padx=10, pady=10)

    # === Create Table if not exists ===
    def create_table(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS employee(
            eid TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            dob TEXT,
            doj TEXT,
            pass TEXT,
            utype TEXT,
            address TEXT,
            salary TEXT
        )
        """)
        con.commit()
        con.close()

    # === Add Employee ===
    def add(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error", "Employee ID and Name are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                rows = cur.fetchall()
                if rows != []:
                    messagebox.showerror("Error", "Employee ID already exists", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            self.var_emp_id.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get("1.0", END).strip(),
                            self.var_salary.get(),
                        ),
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Update Employee ===
    def update(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Please select employee to update", parent=self.root)
            else:
                cur.execute("UPDATE employee SET name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? WHERE eid=?",
                            (
                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_gender.get(),
                                self.var_contact.get(),
                                self.var_dob.get(),
                                self.var_doj.get(),
                                self.var_pass.get(),
                                self.var_utype.get(),
                                self.txt_address.get("1.0", END).strip(),
                                self.var_salary.get(),
                                self.var_emp_id.get()
                            ))
                con.commit()
                messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Delete Employee ===
    def delete(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Select employee to delete", parent=self.root)
            else:
                confirm = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if confirm:
                    cur.execute("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Clear Form ===
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Select")
        self.txt_address.delete("1.0", END)
        self.var_salary.set("")
        self.show()

    # === Show All Employees ===
    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Search Employees ===
    def search(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select search by option", parent=self.root)
            elif self.var_searchtxt.get() == "" or self.var_searchtxt.get() == "Search...":
                messagebox.showerror("Error", "Enter search text", parent=self.root)
            else:
                cur.execute(f"SELECT * FROM employee WHERE {self.var_searchby.get()} LIKE ?", ("%"+self.var_searchtxt.get()+"%",))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert("", END, values=row)
                else:
                    messagebox.showinfo("No Result", "No matching record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Get Data from Table ===
    def get_data(self, event):
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content["values"]
        if row:
            self.var_emp_id.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_contact.set(row[4])
            self.var_dob.set(row[5])
            self.var_doj.set(row[6])
            self.var_pass.set(row[7])
            self.var_utype.set(row[8])
            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, row[9])
            self.var_salary.set(row[10])


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeApp(root)
    root.mainloop()

