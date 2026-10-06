import tkinter as tk
from tkinter import ttk, messagebox
import re
import sqlite3
from datetime import datetime

from database.db import get_connection
from services.validation import normalize_vehicle_number


class AddVehicleWindow:

    def __init__(
        self,
        parent,
        on_vehicle_added=None
    ):

        self.parent = parent

        self.on_vehicle_added = (
            on_vehicle_added
        )

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            "Add Vehicle"
        )

        self.window.geometry(
            "600x650"
        )

        self.window.resizable(
            False,
            False
        )

        self.window.transient(
            parent
        )

        self.window.grab_set()

        # ===================================
        # HEADER
        # ===================================

        header = tk.Frame(
            self.window,
            bg="#1F2937",
            height=90
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="ADD VEHICLE",
            font=("Arial", 22, "bold"),
            bg="#1F2937",
            fg="white"
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            header,
            text="Parking Entry Form",
            font=("Arial", 11),
            bg="#1F2937",
            fg="white"
        ).pack()

        # ===================================
        # FORM
        # ===================================

        form_frame = tk.Frame(
            self.window,
            padx=40,
            pady=25
        )

        form_frame.pack(
            fill="both",
            expand=True
        )

        # ===================================
        # PARKING ID
        # ===================================

        tk.Label(
            form_frame,
            text="Parking ID",
            font=("Arial", 11, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=10
        )

        self.parking_id_entry = tk.Entry(
            form_frame,
            width=32,
            font=("Arial", 11)
        )

        self.parking_id_entry.grid(
            row=0,
            column=1,
            pady=10,
            padx=20
        )

        # ===================================
        # VEHICLE NUMBER
        # ===================================

        tk.Label(
            form_frame,
            text="Vehicle Number",
            font=("Arial", 11, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=10
        )

        self.vehicle_number_entry = tk.Entry(
            form_frame,
            width=32,
            font=("Arial", 11)
        )

        self.vehicle_number_entry.grid(
            row=1,
            column=1,
            pady=10,
            padx=20
        )

        # ===================================
        # OWNER NAME
        # ===================================

        tk.Label(
            form_frame,
            text="Owner Name",
            font=("Arial", 11, "bold")
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=10
        )

        self.owner_name_entry = tk.Entry(
            form_frame,
            width=32,
            font=("Arial", 11)
        )

        self.owner_name_entry.grid(
            row=2,
            column=1,
            pady=10,
            padx=20
        )

        # ===================================
        # PHONE
        # ===================================

        tk.Label(
            form_frame,
            text="Phone Number",
            font=("Arial", 11, "bold")
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=10
        )

        self.phone_entry = tk.Entry(
            form_frame,
            width=32,
            font=("Arial", 11)
        )

        self.phone_entry.grid(
            row=3,
            column=1,
            pady=10,
            padx=20
        )

        # ===================================
        # VEHICLE TYPE
        # ===================================

        tk.Label(
            form_frame,
            text="Vehicle Type",
            font=("Arial", 11, "bold")
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=10
        )

        self.vehicle_type_combo = ttk.Combobox(
            form_frame,
            values=[
                "Car",
                "Bike"
            ],
            width=29,
            font=("Arial", 11),
            state="readonly"
        )

        self.vehicle_type_combo.grid(
            row=4,
            column=1,
            pady=10,
            padx=20
        )

        self.vehicle_type_combo.bind(
            "<<ComboboxSelected>>",
            self.on_vehicle_type_change
        )

        # ===================================
        # PARKING SLOT
        # ===================================

        tk.Label(
            form_frame,
            text="Parking Slot",
            font=("Arial", 11, "bold")
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=10
        )

        self.slot_combo = ttk.Combobox(
            form_frame,
            width=29,
            font=("Arial", 11),
            state="readonly"
        )

        self.slot_combo.grid(
            row=5,
            column=1,
            pady=10,
            padx=20
        )

        self.slot_combo["values"] = []

        # ===================================
        # BUTTONS
        # ===================================

        button_frame = tk.Frame(
            form_frame
        )

        button_frame.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=35
        )

        tk.Button(
            button_frame,
            text="Add Vehicle",
            width=15,
            height=2,
            font=("Arial", 10, "bold"),
            bg="#1F2937",
            fg="white",
            cursor="hand2",
            command=self.add_vehicle
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        tk.Button(
            button_frame,
            text="Cancel",
            width=15,
            height=2,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.window.destroy
        ).grid(
            row=0,
            column=1,
            padx=10
        )

        self.parking_id_entry.focus()

    # ===================================
    # VEHICLE TYPE CHANGE
    # ===================================

    def on_vehicle_type_change(
        self,
        event=None
    ):

        vehicle_type = (
            self.vehicle_type_combo
            .get()
            .strip()
        )

        self.slot_combo.set("")

        self.load_available_slots(
            vehicle_type
        )

    # ===================================
    # LOAD AVAILABLE SLOTS
    # ===================================

    def load_available_slots(
        self,
        vehicle_type
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT slot_number
            FROM parking_slots
            WHERE status = 'Available'
            AND slot_type = ?
            ORDER BY slot_number
        """, (
            vehicle_type,
        ))

        slots = cursor.fetchall()

        connection.close()

        self.slot_combo["values"] = [
            slot[0]
            for slot in slots
        ]

    # ===================================
    # PARKING ID EXISTS
    # ===================================

    def parking_id_exists(
        self,
        parking_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id
            FROM parking_records
            WHERE parking_id = ?
        """, (
            parking_id,
        ))

        result = cursor.fetchone()

        connection.close()

        return result is not None

    # ===================================
    # VEHICLE ALREADY PARKED
    # ===================================

    def vehicle_already_parked(
        self,
        vehicle_number
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                parking_id,
                vehicle_number,
                owner_name,
                slot_number,
                entry_time

            FROM parking_records

            WHERE vehicle_number = ?
            AND status = 'Parked'
        """, (
            vehicle_number,
        ))

        result = cursor.fetchone()

        connection.close()

        return result

    # ===================================
    # SLOT VALIDATION
    # ===================================

    def validate_parking_slot(
        self,
        parking_slot,
        vehicle_type
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                slot_number,
                slot_type,
                status

            FROM parking_slots

            WHERE slot_number = ?
        """, (
            parking_slot,
        ))

        slot = cursor.fetchone()

        connection.close()

        if slot is None:

            return (
                False,
                "Selected parking slot does not exist."
            )

        if slot[1] != vehicle_type:

            return (
                False,
                f"Slot {slot[0]} is reserved "
                f"for {slot[1]} vehicles."
            )

        if slot[2] != "Available":

            return (
                False,
                f"Slot {slot[0]} is currently occupied."
            )

        return (
            True,
            "Parking slot is valid."
        )

    # ===================================
    # SAFE DATABASE INSERTION
    # ===================================

    def save_vehicle(
        self,
        parking_id,
        vehicle_number,
        owner_name,
        phone,
        vehicle_type,
        parking_slot
    ):

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            connection.execute(
                "BEGIN"
            )

            # -----------------------------------
            # FINAL SLOT CHECK
            # -----------------------------------

            cursor.execute("""
                SELECT
                    status,
                    slot_type

                FROM parking_slots

                WHERE slot_number = ?
            """, (
                parking_slot,
            ))

            slot = cursor.fetchone()

            if slot is None:

                connection.rollback()

                return (
                    False,
                    "Selected parking slot does not exist."
                )

            if slot[0] != "Available":

                connection.rollback()

                return (
                    False,
                    f"Parking slot {parking_slot} "
                    "is no longer available."
                )

            if slot[1] != vehicle_type:

                connection.rollback()

                return (
                    False,
                    f"Parking slot {parking_slot} "
                    f"is reserved for {slot[1]} vehicles."
                )

            # -----------------------------------
            # FINAL PARKING ID CHECK
            # -----------------------------------

            cursor.execute("""
                SELECT id
                FROM parking_records
                WHERE parking_id = ?
            """, (
                parking_id,
            ))

            if cursor.fetchone():

                connection.rollback()

                return (
                    False,
                    f"Parking ID {parking_id} already exists."
                )

            # -----------------------------------
            # FINAL DUPLICATE VEHICLE CHECK
            # -----------------------------------

            cursor.execute("""
                SELECT id
                FROM parking_records
                WHERE vehicle_number = ?
                AND status = 'Parked'
            """, (
                vehicle_number,
            ))

            if cursor.fetchone():

                connection.rollback()

                return (
                    False,
                    f"Vehicle {vehicle_number} "
                    "is already parked."
                )

            # -----------------------------------
            # ENTRY TIME
            # -----------------------------------

            entry_time = (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            # -----------------------------------
            # INSERT RECORD
            # -----------------------------------

            cursor.execute("""
                INSERT INTO parking_records
                (
                    parking_id,
                    vehicle_number,
                    owner_name,
                    phone,
                    vehicle_type,
                    slot_number,
                    entry_time,
                    exit_time,
                    status
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                parking_id,
                vehicle_number,
                owner_name,
                phone,
                vehicle_type,
                parking_slot,
                entry_time,
                None,
                "Parked"
            ))

            # -----------------------------------
            # OCCUPY SLOT
            # -----------------------------------

            cursor.execute("""
                UPDATE parking_slots

                SET status = 'Occupied'

                WHERE slot_number = ?
                AND status = 'Available'
            """, (
                parking_slot,
            ))

            if cursor.rowcount != 1:

                connection.rollback()

                return (
                    False,
                    "Parking slot could not be reserved."
                )

            # -----------------------------------
            # COMMIT
            # -----------------------------------

            connection.commit()

            return (
                True,
                entry_time
            )

        except sqlite3.IntegrityError as error:

            if connection:

                connection.rollback()

            return (
                False,
                "Database rejected the entry "
                "because duplicate or invalid "
                "data was detected.\n\n"
                f"Details: {error}"
            )

        except sqlite3.Error as error:

            if connection:

                connection.rollback()

            return (
                False,
                "A database error occurred.\n\n"
                f"Details: {error}"
            )

        finally:

            if connection:

                connection.close()

    # ===================================
    # ADD VEHICLE
    # ===================================

    def add_vehicle(self):

        parking_id = (
            self.parking_id_entry
            .get()
            .strip()
        )

        vehicle_number = (
            self.vehicle_number_entry
            .get()
            .strip()
        )

        owner_name = (
            self.owner_name_entry
            .get()
            .strip()
        )

        phone = (
            self.phone_entry
            .get()
            .strip()
        )

        vehicle_type = (
            self.vehicle_type_combo
            .get()
            .strip()
        )

        parking_slot = (
            self.slot_combo
            .get()
            .strip()
        )

        # ===================================
        # REQUIRED FIELDS
        # ===================================

        if not parking_id:

            messagebox.showwarning(
                "Validation Error",
                "Parking ID is required.",
                parent=self.window
            )

            self.parking_id_entry.focus()
            return

        if not vehicle_number:

            messagebox.showwarning(
                "Validation Error",
                "Vehicle Number is required.",
                parent=self.window
            )

            self.vehicle_number_entry.focus()
            return

        if not owner_name:

            messagebox.showwarning(
                "Validation Error",
                "Owner Name is required.",
                parent=self.window
            )

            self.owner_name_entry.focus()
            return

        if not phone:

            messagebox.showwarning(
                "Validation Error",
                "Phone Number is required.",
                parent=self.window
            )

            self.phone_entry.focus()
            return

        if not vehicle_type:

            messagebox.showwarning(
                "Validation Error",
                "Please select a Vehicle Type.",
                parent=self.window
            )

            return

        if not parking_slot:

            messagebox.showwarning(
                "Validation Error",
                "Please select a Parking Slot.",
                parent=self.window
            )

            return

        # ===================================
        # PARKING ID VALIDATION
        # ===================================

        parking_id = (
            parking_id.upper()
        )

        if not re.fullmatch(
            r"P\d{3}",
            parking_id
        ):

            messagebox.showwarning(
                "Invalid Parking ID",
                "Parking ID must be in the format "
                "P001, P002, P003, etc.",
                parent=self.window
            )

            return

        self.parking_id_entry.delete(
            0,
            tk.END
        )

        self.parking_id_entry.insert(
            0,
            parking_id
        )

        if self.parking_id_exists(
            parking_id
        ):

            messagebox.showerror(
                "Duplicate Parking ID",
                f"Parking ID {parking_id} "
                "already exists.",
                parent=self.window
            )

            return

        # ===================================
        # OWNER VALIDATION
        # ===================================

        if not re.fullmatch(
            r"[A-Za-z ]+",
            owner_name
        ):

            messagebox.showwarning(
                "Invalid Owner Name",
                "Owner Name should contain "
                "only letters and spaces.",
                parent=self.window
            )

            return

        # ===================================
        # PHONE VALIDATION
        # ===================================

        if not phone.isdigit():

            messagebox.showwarning(
                "Invalid Phone Number",
                "Phone Number should contain "
                "digits only.",
                parent=self.window
            )

            return

        if len(phone) != 10:

            messagebox.showwarning(
                "Invalid Phone Number",
                "Phone Number must contain "
                "exactly 10 digits.",
                parent=self.window
            )

            return

        if phone[0] not in "6789":

            messagebox.showwarning(
                "Invalid Phone Number",
                "Phone Number must start with "
                "6, 7, 8 or 9.",
                parent=self.window
            )

            return

        # ===================================
        # VEHICLE NUMBER
        # ===================================

        vehicle_number = (
            normalize_vehicle_number(
                vehicle_number
            )
        )

        if not vehicle_number.isalnum():

            messagebox.showwarning(
                "Invalid Vehicle Number",
                "Vehicle Number should contain "
                "only letters and numbers.",
                parent=self.window
            )

            return

        if (
            len(vehicle_number) < 8
            or
            len(vehicle_number) > 11
        ):

            messagebox.showwarning(
                "Invalid Vehicle Number",
                "Please enter a valid vehicle "
                "registration number.",
                parent=self.window
            )

            return

        self.vehicle_number_entry.delete(
            0,
            tk.END
        )

        self.vehicle_number_entry.insert(
            0,
            vehicle_number
        )

        # ===================================
        # SEARCH BEFORE ADD
        # ===================================

        existing_vehicle = (
            self.vehicle_already_parked(
                vehicle_number
            )
        )

        if existing_vehicle:

            messagebox.showerror(
                "Duplicate Vehicle Detected",

                "This vehicle is already parked.\n\n"

                f"Parking ID: {existing_vehicle[0]}\n"
                f"Vehicle Number: {existing_vehicle[1]}\n"
                f"Owner: {existing_vehicle[2]}\n"
                f"Parking Slot: {existing_vehicle[3]}\n"
                f"Entry Time: {existing_vehicle[4]}\n\n"

                "Duplicate entry has been prevented.",

                parent=self.window
            )

            return

        # ===================================
        # SLOT VALIDATION
        # ===================================

        slot_valid, slot_message = (
            self.validate_parking_slot(
                parking_slot,
                vehicle_type
            )
        )

        if not slot_valid:

            messagebox.showerror(
                "Parking Slot Error",
                slot_message,
                parent=self.window
            )

            self.load_available_slots(
                vehicle_type
            )

            self.slot_combo.set("")

            return

        # ===================================
        # CONFIRMATION
        # ===================================

        confirmation = (
            messagebox.askyesno(
                "Confirm Vehicle Entry",

                "Please verify the parking details:\n\n"

                f"Parking ID: {parking_id}\n"
                f"Vehicle Number: {vehicle_number}\n"
                f"Owner Name: {owner_name}\n"
                f"Phone Number: {phone}\n"
                f"Vehicle Type: {vehicle_type}\n"
                f"Parking Slot: {parking_slot}\n\n"

                "Are all the details correct?",

                parent=self.window
            )
        )

        if not confirmation:

            return

        # ===================================
        # DATABASE INSERT
        # ===================================

        success, result = (
            self.save_vehicle(
                parking_id,
                vehicle_number,
                owner_name,
                phone,
                vehicle_type,
                parking_slot
            )
        )

        if not success:

            messagebox.showerror(
                "Entry Failed",
                result,
                parent=self.window
            )

            self.load_available_slots(
                vehicle_type
            )

            self.slot_combo.set("")

            return

        entry_time = result

        # ===================================
        # REFRESH MAIN DASHBOARD
        # ===================================

        if self.on_vehicle_added:

            self.on_vehicle_added()

        # ===================================
        # SUCCESS
        # ===================================

        messagebox.showinfo(
            "Vehicle Added Successfully",

            "Vehicle entry has been saved successfully.\n\n"

            f"Parking ID: {parking_id}\n"
            f"Vehicle Number: {vehicle_number}\n"
            f"Parking Slot: {parking_slot}\n"
            f"Entry Time: {entry_time}\n\n"

            f"Slot {parking_slot} is now Occupied.",

            parent=self.window
        )

        self.window.destroy()