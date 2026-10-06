import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

from database.db import get_connection
from services.validation import normalize_vehicle_number


class VehicleExitWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Vehicle Exit")
        self.window.geometry("750x650")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self.current_record = None

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
            text="VEHICLE EXIT",
            font=("Arial", 22, "bold"),
            bg="#1F2937",
            fg="white"
        ).pack(pady=(20, 5))

        tk.Label(
            header,
            text="Search, Verify and Complete Vehicle Exit",
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
        # SEARCH BY
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
            text="Search Parked Vehicle",
            width=20,
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
        # VEHICLE DETAILS
        # ===================================

        result_frame = tk.LabelFrame(
            main_frame,
            text="Parked Vehicle Details",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=15
        )

        result_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=15,
            sticky="ew"
        )

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

        self.status_var = tk.StringVar(
            value="-"
        )

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
            "Status",
            self.status_var,
            7
        )

        # ===================================
        # BUTTONS
        # ===================================

        button_frame = tk.Frame(
            main_frame
        )

        button_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=20
        )

        self.exit_button = tk.Button(
            button_frame,
            text="Confirm Vehicle Exit",
            width=20,
            height=2,
            bg="#1F2937",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.exit_vehicle,
            state="disabled"
        )

        self.exit_button.grid(
            row=0,
            column=0,
            padx=10
        )

        close_button = tk.Button(
            button_frame,
            text="Close",
            width=15,
            height=2,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.window.destroy
        )

        close_button.grid(
            row=0,
            column=1,
            padx=10
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

        self.current_record = None

        self.parking_id_var.set("-")
        self.vehicle_number_var.set("-")
        self.owner_name_var.set("-")
        self.phone_var.set("-")
        self.vehicle_type_var.set("-")
        self.slot_var.set("-")
        self.entry_time_var.set("-")
        self.status_var.set("-")

        self.exit_button.config(
            state="disabled"
        )

    # ===================================
    # SEARCH PARKED VEHICLE
    # ===================================

    def search_vehicle(self):

        self.clear_result()

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

        if not search_value:

            messagebox.showwarning(
                "Search Required",
                "Please enter a value to search.",
                parent=self.window
            )

            self.search_entry.focus()

            return

        # ===================================
        # NORMALIZATION
        # ===================================

        if search_type == "Parking ID":

            search_value = (
                search_value.upper()
            )

        else:

            search_value = (
                normalize_vehicle_number(
                    search_value
                )
            )

        self.search_entry.delete(
            0,
            tk.END
        )

        self.search_entry.insert(
            0,
            search_value
        )

        # ===================================
        # DATABASE SEARCH
        # ===================================

        connection = get_connection()
        cursor = connection.cursor()

        if search_type == "Parking ID":

            cursor.execute("""
                SELECT
                    id,
                    parking_id,
                    vehicle_number,
                    owner_name,
                    phone,
                    vehicle_type,
                    slot_number,
                    entry_time,
                    status
                FROM parking_records
                WHERE parking_id = ?
                AND status = 'Parked'
            """, (search_value,))

        else:

            cursor.execute("""
                SELECT
                    id,
                    parking_id,
                    vehicle_number,
                    owner_name,
                    phone,
                    vehicle_type,
                    slot_number,
                    entry_time,
                    status
                FROM parking_records
                WHERE vehicle_number = ?
                AND status = 'Parked'
                ORDER BY id DESC
                LIMIT 1
            """, (search_value,))

        record = cursor.fetchone()

        connection.close()

        # ===================================
        # VEHICLE NOT FOUND
        # ===================================

        if record is None:

            messagebox.showinfo(
                "Parked Vehicle Not Found",

                "No active parked vehicle was found.\n\n"
                "The vehicle may already have exited "
                "or the entered information may be incorrect.",

                parent=self.window
            )

            return

        # ===================================
        # STORE RECORD
        # ===================================

        self.current_record = record

        # ===================================
        # DISPLAY RECORD
        # ===================================

        self.parking_id_var.set(
            record[1]
        )

        self.vehicle_number_var.set(
            record[2]
        )

        self.owner_name_var.set(
            record[3]
        )

        self.phone_var.set(
            record[4]
        )

        self.vehicle_type_var.set(
            record[5]
        )

        self.slot_var.set(
            record[6]
        )

        self.entry_time_var.set(
            record[7]
        )

        self.status_var.set(
            record[8]
        )

        self.exit_button.config(
            state="normal"
        )

    # ===================================
    # EXIT VEHICLE
    # ===================================

    def exit_vehicle(self):

        if self.current_record is None:

            messagebox.showwarning(
                "No Vehicle Selected",
                "Please search for a parked vehicle first.",
                parent=self.window
            )

            return

        record_id = self.current_record[0]
        parking_id = self.current_record[1]
        vehicle_number = self.current_record[2]
        owner_name = self.current_record[3]
        slot_number = self.current_record[6]
        entry_time = self.current_record[7]

        # ===================================
        # CONFIRMATION DIALOG
        # ===================================

        confirmation = messagebox.askyesno(
            "Confirm Vehicle Exit",

            "Please verify the vehicle exit details:\n\n"

            f"Parking ID: {parking_id}\n"
            f"Vehicle Number: {vehicle_number}\n"
            f"Owner Name: {owner_name}\n"
            f"Parking Slot: {slot_number}\n"
            f"Entry Time: {entry_time}\n\n"

            "Do you want to complete the vehicle exit?",

            parent=self.window
        )

        if not confirmation:

            return

        # ===================================
        # EXIT TIME
        # ===================================

        exit_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            connection.execute(
                "BEGIN"
            )

            # ===================================
            # FINAL ACTIVE RECORD CHECK
            # ===================================

            cursor.execute("""
                SELECT
                    status,
                    slot_number
                FROM parking_records
                WHERE id = ?
            """, (record_id,))

            current_status = (
                cursor.fetchone()
            )

            if current_status is None:

                connection.rollback()

                messagebox.showerror(
                    "Exit Failed",
                    "Parking record no longer exists.",
                    parent=self.window
                )

                return

            if current_status[0] != "Parked":

                connection.rollback()

                messagebox.showerror(
                    "Exit Failed",

                    "This vehicle is no longer "
                    "marked as Parked.",

                    parent=self.window
                )

                self.clear_result()

                return

            # ===================================
            # UPDATE PARKING RECORD
            # ===================================

            cursor.execute("""
                UPDATE parking_records

                SET
                    exit_time = ?,
                    status = 'Exited'

                WHERE id = ?
                AND status = 'Parked'
            """, (
                exit_time,
                record_id
            ))

            if cursor.rowcount != 1:

                connection.rollback()

                messagebox.showerror(
                    "Exit Failed",

                    "Vehicle record could not "
                    "be updated.",

                    parent=self.window
                )

                return

            # ===================================
            # RELEASE PARKING SLOT
            # ===================================

            cursor.execute("""
                UPDATE parking_slots

                SET status = 'Available'

                WHERE slot_number = ?
                AND status = 'Occupied'
            """, (
                slot_number,
            ))

            if cursor.rowcount != 1:

                connection.rollback()

                messagebox.showerror(
                    "Exit Failed",

                    "Parking slot could not be released.\n\n"
                    "No database changes were saved.",

                    parent=self.window
                )

                return

            # ===================================
            # SAVE BOTH CHANGES
            # ===================================

            connection.commit()

            messagebox.showinfo(
                "Vehicle Exit Successful",

                "Vehicle exit completed successfully.\n\n"

                f"Parking ID: {parking_id}\n"
                f"Vehicle Number: {vehicle_number}\n"
                f"Parking Slot: {slot_number}\n"
                f"Exit Time: {exit_time}\n\n"

                f"Slot {slot_number} is now Available.",

                parent=self.window
            )

            print("------------------------------")
            print("VEHICLE EXIT COMPLETED")
            print("------------------------------")
            print("Parking ID:", parking_id)
            print("Vehicle Number:", vehicle_number)
            print("Parking Slot:", slot_number)
            print("Entry Time:", entry_time)
            print("Exit Time:", exit_time)
            print("Status: Exited")
            print("------------------------------")

            # Clear old result
            self.clear_result()

            # Clear search field
            self.search_entry.delete(
                0,
                tk.END
            )

            self.search_entry.focus()

        except sqlite3.Error as error:

            if connection:

                connection.rollback()

            messagebox.showerror(
                "Database Error",

                "Vehicle exit could not be completed.\n\n"
                f"Details: {error}",

                parent=self.window
            )

        finally:

            if connection:

                connection.close()