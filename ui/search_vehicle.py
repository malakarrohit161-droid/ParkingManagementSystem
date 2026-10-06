import tkinter as tk
from tkinter import ttk, messagebox

from database.db import get_connection
from services.validation import normalize_vehicle_number


class SearchVehicleWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Search Vehicle")
        self.window.geometry("750x600")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        # ===================================
        # HEADER
        # ===================================

        header = tk.Frame(
            self.window,
            bg="#1F2937",
            height=90
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="SEARCH VEHICLE",
            font=("Arial", 22, "bold"),
            bg="#1F2937",
            fg="white"
        ).pack(pady=(20, 5))

        tk.Label(
            header,
            text="Find Parking Records Quickly",
            font=("Arial", 11),
            bg="#1F2937",
            fg="white"
        ).pack()

        # ===================================
        # MAIN FRAME
        # ===================================

        main_frame = tk.Frame(
            self.window,
            padx=35,
            pady=25
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        # ===================================
        # SEARCH TYPE
        # ===================================

        tk.Label(
            main_frame,
            text="Search By",
            font=("Arial", 11, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=10
        )

        self.search_type_combo = ttk.Combobox(
            main_frame,
            values=[
                "Parking ID",
                "Vehicle Number"
            ],
            width=25,
            state="readonly",
            font=("Arial", 11)
        )

        self.search_type_combo.grid(
            row=0,
            column=1,
            padx=15,
            pady=10
        )

        self.search_type_combo.set(
            "Vehicle Number"
        )

        # ===================================
        # SEARCH VALUE
        # ===================================

        tk.Label(
            main_frame,
            text="Search Value",
            font=("Arial", 11, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=10
        )

        self.search_entry = tk.Entry(
            main_frame,
            width=28,
            font=("Arial", 11)
        )

        self.search_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=10
        )

        # ===================================
        # SEARCH BUTTON
        # ===================================

        search_button = tk.Button(
            main_frame,
            text="Search",
            width=15,
            height=2,
            bg="#1F2937",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.search_vehicle
        )

        search_button.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=15
        )

        # ===================================
        # RESULT SECTION
        # ===================================

        result_frame = tk.LabelFrame(
            main_frame,
            text="Parking Record",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=15
        )

        result_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=20,
            sticky="ew"
        )

        # Result variables

        self.parking_id_var = tk.StringVar(
            value="-"
        )

        self.vehicle_number_var = tk.StringVar(
            value="-"
        )

        self.owner_name_var = tk.StringVar(
            value="-"
        )

        self.phone_var = tk.StringVar(
            value="-"
        )

        self.vehicle_type_var = tk.StringVar(
            value="-"
        )

        self.slot_var = tk.StringVar(
            value="-"
        )

        self.entry_time_var = tk.StringVar(
            value="-"
        )

        self.exit_time_var = tk.StringVar(
            value="-"
        )

        self.status_var = tk.StringVar(
            value="-"
        )

        # ===================================
        # RESULT ROWS
        # ===================================

        self.create_result_row(
            result_frame,
            "Parking ID",
            self.parking_id_var,
            0
        )

        self.create_result_row(
            result_frame,
            "Vehicle Number",
            self.vehicle_number_var,
            1
        )

        self.create_result_row(
            result_frame,
            "Owner Name",
            self.owner_name_var,
            2
        )

        self.create_result_row(
            result_frame,
            "Phone Number",
            self.phone_var,
            3
        )

        self.create_result_row(
            result_frame,
            "Vehicle Type",
            self.vehicle_type_var,
            4
        )

        self.create_result_row(
            result_frame,
            "Parking Slot",
            self.slot_var,
            5
        )

        self.create_result_row(
            result_frame,
            "Entry Time",
            self.entry_time_var,
            6
        )

        self.create_result_row(
            result_frame,
            "Exit Time",
            self.exit_time_var,
            7
        )

        self.create_result_row(
            result_frame,
            "Status",
            self.status_var,
            8
        )

        # ===================================
        # CLOSE BUTTON
        # ===================================

        close_button = tk.Button(
            main_frame,
            text="Close",
            width=15,
            height=2,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.window.destroy
        )

        close_button.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=10
        )

        self.search_entry.focus()

    # ===================================
    # CREATE RESULT ROW
    # ===================================

    def create_result_row(
        self,
        parent,
        label_text,
        variable,
        row
    ):

        tk.Label(
            parent,
            text=label_text + ":",
            width=18,
            anchor="w",
            font=("Arial", 10, "bold")
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=4
        )

        tk.Label(
            parent,
            textvariable=variable,
            width=35,
            anchor="w",
            font=("Arial", 10)
        ).grid(
            row=row,
            column=1,
            sticky="w",
            pady=4
        )

    # ===================================
    # CLEAR RESULT
    # ===================================

    def clear_result(self):

        self.parking_id_var.set("-")
        self.vehicle_number_var.set("-")
        self.owner_name_var.set("-")
        self.phone_var.set("-")
        self.vehicle_type_var.set("-")
        self.slot_var.set("-")
        self.entry_time_var.set("-")
        self.exit_time_var.set("-")
        self.status_var.set("-")

    # ===================================
    # SEARCH VEHICLE
    # ===================================

    def search_vehicle(self):

        search_type = (
            self.search_type_combo
            .get()
            .strip()
        )

        search_value = (
            self.search_entry
            .get()
            .strip()
        )

        # -----------------------------------
        # EMPTY SEARCH VALIDATION
        # -----------------------------------

        if not search_value:

            messagebox.showwarning(
                "Search Required",
                "Please enter a value to search.",
                parent=self.window
            )

            self.search_entry.focus()

            return

        # -----------------------------------
        # NORMALIZE SEARCH VALUE
        # -----------------------------------

        if search_type == "Parking ID":

            search_value = (
                search_value.upper()
            )

        elif search_type == "Vehicle Number":

            search_value = (
                normalize_vehicle_number(
                    search_value
                )
            )

        # Show normalized value

        self.search_entry.delete(
            0,
            tk.END
        )

        self.search_entry.insert(
            0,
            search_value
        )

        # -----------------------------------
        # DATABASE SEARCH
        # -----------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        if search_type == "Parking ID":

            cursor.execute("""
                SELECT
                    parking_id,
                    vehicle_number,
                    owner_name,
                    phone,
                    vehicle_type,
                    slot_number,
                    entry_time,
                    exit_time,
                    status
                FROM parking_records
                WHERE parking_id = ?
            """, (search_value,))

        else:

            cursor.execute("""
                SELECT
                    parking_id,
                    vehicle_number,
                    owner_name,
                    phone,
                    vehicle_type,
                    slot_number,
                    entry_time,
                    exit_time,
                    status
                FROM parking_records
                WHERE vehicle_number = ?
                ORDER BY id DESC
                LIMIT 1
            """, (search_value,))

        record = cursor.fetchone()

        connection.close()

        # -----------------------------------
        # NOT FOUND
        # -----------------------------------

        if record is None:

            self.clear_result()

            messagebox.showinfo(
                "Vehicle Not Found",

                "No parking record was found "
                "for the entered search value.",

                parent=self.window
            )

            return

        # -----------------------------------
        # DISPLAY RESULT
        # -----------------------------------

        self.parking_id_var.set(
            record[0]
        )

        self.vehicle_number_var.set(
            record[1]
        )

        self.owner_name_var.set(
            record[2]
        )

        self.phone_var.set(
            record[3]
        )

        self.vehicle_type_var.set(
            record[4]
        )

        self.slot_var.set(
            record[5]
        )

        self.entry_time_var.set(
            record[6]
        )

        self.exit_time_var.set(
            record[7]
            if record[7]
            else "Not Exited"
        )

        self.status_var.set(
            record[8]
        )