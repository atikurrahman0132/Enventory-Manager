import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System - Product")
        self.root.state("zoomed")  # Fullscreen-friendly
        self.root.configure(bg="#d9d9d9")

        title=Label(
            text="Product Deatils",
            background="black",
            fg="white",
            font=("arial", 20, "bold")
        ).pack(side=TOP,fill=X, padx=20, pady=5)





if __name__ == '__main__':
    root = Tk()
    obj = productClass(root)
    root.mainloop()