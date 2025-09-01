import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

class loginClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System - Supplier")
        self.root.state("zoomed")  # Fullscreen-friendly
        self.root.configure(bg="#d9d9d9")


if __name__ == "__main__":
    root = Tk()
    obj = loginClass(root)
    root.mainloop()