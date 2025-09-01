from tkinter import *
import time
from employee import EmployeeApp # Correct import
from supplier import supplierClass
from category import categoryClass
from login import loginClass



class IMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.configure(background="#d9d9d9")

        # ===== Responsive Window =====
        self.root.state('zoomed')          # Fullscreen-friendly
        self.root.minsize(800, 500)        # Minimum usable size

        # ===== Title =====
        title = Label(
            self.root,
            text="All Inventory Manager",
            font=("times new roman", 38, "bold"),
            bg="lightblue",
            fg="black",
            anchor="w",
            padx=20
        )
        title.pack(side=TOP, fill=X)

        # ===== Logout Button =====
        btn_logout = Button(
            self.root,
            text="Logout",
            command=self.login,
            font=("times new roman", 12, "bold"),
            bg="red",
            fg="white",
            cursor="hand2"
        )
        btn_logout.place(relx=0.8, rely=0.01, relwidth=0.18, relheight=0.05)

        # ===== Clock =====
        self.lab_clock = Label(
            self.root,
            font=("times new roman", 12),
            bg="#4d636d",
            fg="white"
        )
        self.lab_clock.pack(fill=X)
        self.update_clock()  # Start clock

        # ===== Main Layout =====
        main_frame = Frame(self.root, bg="#d9d9d9")
        main_frame.pack(fill=BOTH, expand=True)

        # ===== Left Menu =====
        LeftMenu = Frame(main_frame, bd=2, relief=RIDGE, bg="white")
        LeftMenu.pack(side=LEFT, fill=Y)

        lbl_menu = Label(
            LeftMenu,
            text="📂 Main Menu",
            font=("times new roman", 18, "bold"),
            bg="#009688",
            fg="white",
            pady=10
        )
        lbl_menu.pack(fill=X)

        # --- Menu Buttons ---
        btn_Emp = Button(
            LeftMenu, text="⏩ Employee", command=self.employee,
            font=("times new roman", 14, "bold"), bg="white", bd=3,
            anchor="w", padx=10, cursor="hand2"
        )
        btn_Emp.pack(fill=X)

        btn_Supplier = Button(
            LeftMenu, text="⏩ Supplier", command=self.supplier,
            font=("times new roman", 14, "bold"), bg="white", bd=3,
            anchor="w", padx=10, cursor="hand2"
        )
        btn_Supplier.pack(fill=X)

        btn_Category = Button(
            LeftMenu, text="⏩ Category",command=self.category,
            font=("times new roman", 14, "bold"), bg="white", bd=3,
            anchor="w", padx=10, cursor="hand2"
        )
        btn_Category.pack(fill=X)

        btn_Product = Button(
            LeftMenu, text="⏩ Product",
            font=("times new roman", 14, "bold"), bg="white", bd=3,
            anchor="w", padx=10, cursor="hand2"
        )
        btn_Product.pack(fill=X)

        btn_Sales = Button(
            LeftMenu, text="⏩ Sales",
            font=("times new roman", 14, "bold"), bg="white", bd=3,
            anchor="w", padx=10, cursor="hand2"
        )
        btn_Sales.pack(fill=X)

        btn_Exit = Button(
            LeftMenu, text="⏩ Exit",
            font=("times new roman", 14, "bold"), bg="white", bd=3,
            anchor="w", padx=10, cursor="hand2",
            command=self.root.destroy
        )
        btn_Exit.pack(fill=X)

        # ===== Dashboard (Right Side) =====
        dashboard = Frame(main_frame, bg="#d9d9d9")
        dashboard.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        dashboard.grid_rowconfigure(0, weight=1)
        dashboard.grid_rowconfigure(1, weight=1)
        dashboard.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # --- Content Cards ---
        self.lab_employee = Label(dashboard, text="Total Employee\n[0]",
                                  bd=5, relief=RIDGE, bg="#009688", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lab_employee.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.lab_supplier = Label(dashboard, text="Total Supplier\n[0]",
                                  bd=5, relief=RIDGE, bg="#E4004B", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lab_supplier.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.lab_category = Label(dashboard, text="Total Category\n[0]",
                                  bd=5, relief=RIDGE, bg="#ED775A", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lab_category.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        self.lab_product = Label(dashboard, text="Total Product\n[0]",
                                 bd=5, relief=RIDGE, bg="#3E0703", fg="white",
                                 font=("goudy old style", 20, "bold"))
        self.lab_product.grid(row=0, column=3, sticky="nsew", padx=10, pady=10)

        self.lab_sales = Label(dashboard, text="Sales Record\n[0]",
                               bd=5, relief=RIDGE, bg="#4D2D8C", fg="white",
                               font=("goudy old style", 20, "bold"))
        self.lab_sales.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # ===== Footer =====
        lab_footer = Label(
            self.root,
            text="Inventory Management System | Created by Shishir\nFor any Technical Issue Contact: <Atikurrahman01322@gmail.com>",
            font=("times new roman", 12),
            bg="#4d636d",
            fg="white"
        )
        lab_footer.pack(side=BOTTOM, fill=X)

    # === Functions ===
    def update_clock(self):
        current_time = time.strftime("%d-%m-%Y   %H:%M:%S")
        self.lab_clock.config(text=f"Welcome to all manager\t\t {current_time}")
        self.lab_clock.after(1000, self.update_clock)   # প্রতি 1 সেকেন্ডে আপডেট হবে

    def employee(self):
        new_win = Toplevel(self.root)
        new_obj = EmployeeApp(new_win)   # Correct class

    def supplier(self):
        new_win = Toplevel(self.root)
        new_obj = supplierClass(new_win)   # Correct class

    def category(self):
        new_win = Toplevel(self.root)
        new_obj = categoryClass(new_win)   # Correct class

    def login(self):
        new_win = Toplevel(self.root)
        new_obj = loginClass(new_win)   # Correct class


if __name__ == '__main__':
    root = Tk()
    obj = IMS(root)
    root.mainloop()
