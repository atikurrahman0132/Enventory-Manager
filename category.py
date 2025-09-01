import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image


class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System - Category")
        self.root.state("zoomed")  # Fullscreen-friendly
        self.root.configure(bg="#d9d9d9")
        # ======= variables======
        self.var_cat_id = StringVar()
        self.var_cat_name = StringVar()

        # ======= Title ======
        lbl_title=Label(self.root,text='Manage product category',bg="#0D1164",bd=3,relief=RIDGE, fg="white", font=("JetBrains Mono", 32, "bold")).pack(side=TOP,fill=X, padx=10, pady=20)

        lbl_name=Label(self.root,text='Enter Category Name:',bg="#d9d9d9", fg="black", font=("JetBrains Mono", 32, "bold")).place(relx=0.05, rely=0.09)
        txt_name=Entry(self.root,textvariable=self.var_cat_name ,bg="lightyellow", fg="black", font=("JetBrains Mono", 20, "bold")).place(relx=0.05, rely=0.15)

        txt_add=Button(self.root,text='Add',command=self.add,bg="#08CB00",cursor='hand2', fg="black", font=("JetBrains Mono", 13, "bold")).place(relx=0.22, rely=0.15,width=150, height=35)
        txt_delete=Button(self.root,text='Delete',command=self.delete,bg="#E4004B",cursor='hand2', fg="black", font=("JetBrains Mono", 13, "bold")).place(relx=0.31, rely=0.15,width=150, height=35)

        # ======= Category Details======
        cat_frame=Frame(self.root,bd=3, relief=RIDGE)
        cat_frame.place(x=750, y=100, width=600, height=90)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx=Scrollbar(cat_frame, orient=HORIZONTAL)

        self.cat_table = ttk.Treeview(
            cat_frame,
            columns=("cid", "name"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.cat_table.yview)
        scrollx.config(command=self.cat_table.xview)

        self.cat_table.heading('cid', text='Cid')
        self.cat_table.heading('name', text='Name')
        self.cat_table['show'] = 'headings'
        self.cat_table.column('cid', width=100)
        self.cat_table.column('name', width=100)
        self.cat_table.pack(fill=BOTH, expand=1)
        self.cat_table.bind("<ButtonRelease-1>", self.get_data)


        # ======= Images 1 ======
        self.im1=Image.open('cat.png')
        self.im1 = self.im1.resize((850, 400))
        self.ims1 = ImageTk.PhotoImage(self.im1)

        self.lbl_im1 = Label(self.root, image=self.ims1,bd=2,relief=RIDGE).place(x=100, y=220)

        # ======= Images 1 ======
        self.im2=Image.open('cat.png')
        self.im2 = self.im2.resize((850, 400))
        self.ims2 = ImageTk.PhotoImage(self.im2)

        self.lbl_im2 = Label(self.root, image=self.ims2,bd=2,relief=RIDGE).place(x=970, y=220)

        self.show()

    # ======= add button func ======
    def add(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_cat_name.get() == "" or self.var_cat_name.get() == "":
                    messagebox.showerror("Error", "Category Name are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_cat_name.get(),))
                rows = cur.fetchall()
                if rows != []:
                        messagebox.showerror("Error", "Category Name already exists", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO category (name) VALUES (?)",
                            (
                            self.var_cat_name.get(),

                            ),
                        )
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # === Show All Employees ===
    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.cat_table.delete(*self.cat_table.get_children())
            for row in rows:
                    self.cat_table.insert("", END, values=row)
        except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, event):
        f = self.cat_table.focus()
        content = self.cat_table.item(f)
        row = content["values"]
        if row:
            self.var_cat_id.set(row[0])
            self.var_cat_name.set(row[1])
    # ======= delete btn func======
    def delete(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Select Category to delete", parent=self.root)
            else:
                confirm = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if confirm:
                    cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()



if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()