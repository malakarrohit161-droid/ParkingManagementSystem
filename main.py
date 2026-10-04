import tkinter as tk

from database.db import create_tables, initialize_parking_slots
from ui.dashboard import Dashboard


def main():

    # -----------------------------
    # DATABASE SETUP
    # -----------------------------

    create_tables()
    initialize_parking_slots()

    # -----------------------------
    # APPLICATION
    # -----------------------------

    root = tk.Tk()

    Dashboard(root)

    root.mainloop()


if __name__ == "__main__":
    main()