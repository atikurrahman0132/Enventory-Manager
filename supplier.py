import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System - Supplier")
        self.root.state("zoomed")  # Fullscreen-friendly
        self.root.configure(bg="#d9d9d9")

        # === All Variables ===
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_supplier_id = StringVar()
        self.var_supplier_name = StringVar()
        self.var_supplier_contact = StringVar()

        # === Ensure Supplier Table Exists ===
        self.create_table()

        # === Search Frame ===
        SearchFrame = LabelFrame(
            self.root,
            text="Search Supplier",
            bg="white",
            fg="black",
            font=("Times New Roman", 12, "bold"),
        )
        SearchFrame.pack(side=TOP, fill=X, padx=20, pady=10)

        cmb_search = ttk.Combobox(
            SearchFrame,
            textvariable=self.var_searchby,
            values=("Select", "sid", "name", "contact"),
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
            text="Supplier Details",
            font=("Arial", 16, "bold"),
            bg="#0F0E0E",
            fg="white",
        ).pack(side=TOP,fill=X, padx=20, pady=5)

        # === Form Frame ===
        form_frame = Frame(self.root, bg="#d9d9d9")
        form_frame.pack(fill=X, padx=20, pady=10)

        # Row 1
        self.make_label_entry(form_frame, "Supplier ID:", self.var_supplier_id, 0, 0)

        # Row 2
        self.make_label_entry(form_frame, "Supplier Name:", self.var_supplier_name, 1, 0)

        # Row 3
        self.make_label_entry(form_frame, "Contact:", self.var_supplier_contact, 2, 0)

        # Row 4
        lbl_desc = Label(form_frame, text="Description:", font=("Arial", 12), bg="#d9d9d9")
        lbl_desc.grid(row=3, column=0, sticky=W, padx=10, pady=10)
        self.txt_desc = Text(form_frame, font=("Arial", 12), height=2, width=30, bg="#FAD691")
        self.txt_desc.grid(row=3, column=1, padx=10, pady=10)

        # === Buttons ===
        btn_frame = Frame(self.root, bg="#d9d9d9")
        btn_frame.pack(fill=X, padx=20, pady=10)

        Button(btn_frame, text="Save", command=self.add, bg="#08CB00", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Update", command=self.update, bg="#1C6EA4", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Delete", command=self.delete, bg="#B9375D", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Clear", command=self.clear, bg="#7A85C1", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)

        # === Supplier Table ===
        table_frame = Frame(self.root, bd=2, relief=RIDGE)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.SupplierTable = ttk.Treeview(
            table_frame,
            columns=("sid", "name", "contact", "description"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.SupplierTable.xview)
        scroll_y.config(command=self.SupplierTable.yview)

        # Table Headings
        self.SupplierTable.heading("sid", text="Supplier Id")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("contact", text="Contact")
        self.SupplierTable.heading("description", text="Description")

        self.SupplierTable["show"] = "headings"

        for col in ("sid", "name", "contact", "description"):
            self.SupplierTable.column(col, width=200)

        self.SupplierTable.pack(fill=BOTH, expand=True)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()  # load data initially

    # === Helper: Label + Entry ===
    def make_label_entry(self, frame, text, variable, row, col):
        Label(frame, text=text, font=("Arial", 12), bg="#d9d9d9").grid(row=row, column=col * 2, sticky=W, padx=10, pady=10)
        Entry(frame, textvariable=variable, font=("Arial", 12), bg="#FAD691").grid(row=row, column=col * 2 + 1, padx=10, pady=10)

    # === Create Table if not exists ===
    def create_table(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS supplier (
            sid TEXT PRIMARY KEY,
            name TEXT,
            contact TEXT,
            description TEXT
        )
        """)
        con.commit()
        con.close()

    # === Add Supplier ===
    def add(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_supplier_id.get() == "" or self.var_supplier_name.get() == "":
                messagebox.showerror("Error", "Supplier ID and Name are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE sid=?", (self.var_supplier_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Supplier ID already exists", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO supplier (sid, name, contact, description) VALUES (?, ?, ?, ?)",
                        (
                            self.var_supplier_id.get(),
                            self.var_supplier_name.get(),
                            self.var_supplier_contact.get(),
                            self.txt_desc.get("1.0", END).strip(),
                        ),
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Update Supplier ===
    def update(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_supplier_id.get() == "":
                messagebox.showerror("Error", "Please select supplier to update", parent=self.root)
            else:
                cur.execute(
                    "UPDATE supplier SET name=?, contact=?, description=? WHERE sid=?",
                    (
                        self.var_supplier_name.get(),
                        self.var_supplier_contact.get(),
                        self.txt_desc.get("1.0", END).strip(),
                        self.var_supplier_id.get(),
                    ),
                )
                con.commit()
                messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Delete Supplier ===
    def delete(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_supplier_id.get() == "":
                messagebox.showerror("Error", "Select supplier to delete", parent=self.root)
            else:
                confirm = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if confirm:
                    cur.execute("DELETE FROM supplier WHERE sid=?", (self.var_supplier_id.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Clear Form ===
    def clear(self):
        self.var_supplier_id.set("")
        self.var_supplier_name.set("")
        self.var_supplier_contact.set("")
        self.txt_desc.delete("1.0", END)
        self.show()

    # === Show All Suppliers ===
    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Search Suppliers ===
    def search(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select search by option", parent=self.root)
            elif self.var_searchtxt.get() == "" or self.var_searchtxt.get() == "Search...":
                messagebox.showerror("Error", "Enter search text", parent=self.root)
            else:
                cur.execute(f"SELECT * FROM supplier WHERE {self.var_searchby.get()} LIKE ?", ("%"+self.var_searchtxt.get()+"%",))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    for row in rows:
                        self.SupplierTable.insert("", END, values=row)
                else:
                    messagebox.showinfo("No Result", "No matching record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Get Data from Table ===
    def get_data(self, event):
        f = self.SupplierTable.focus()
        content = self.SupplierTable.item(f)
        row = content["values"]
        if row:
            self.var_supplier_id.set(row[0])
            self.var_supplier_name.set(row[1])
            self.var_supplier_contact.set(row[2])
            self.txt_desc.delete("1.0", END)
            self.txt_desc.insert(END, row[3])


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
