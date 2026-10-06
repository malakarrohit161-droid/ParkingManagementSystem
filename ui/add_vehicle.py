import tkinter as tk
from tkinter import ttk, messagebox
import re

from database.db import get_connection
from services.validation import normalize_vehicle_number


class AddVehicleWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Add Vehicle")
        self.window.geometry("600x650")
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

        title = tk.Label(
            header,
            text="ADD VEHICLE",
            font=("Arial", 22, "bold"),
            bg="#1F2937",
            fg="white"
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            header,
            text="Parking Entry Form",
            font=("Arial", 11),
            bg="#1F2937",
            fg="white"
        )
        subtitle.pack()

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
        # PHONE NUMBER
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
            values=["Car", "Bike"],
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

        add_button = tk.Button(
            button_frame,
            text="Add Vehicle",
            width=15,
            height=2,
            font=("Arial", 10, "bold"),
            bg="#1F2937",
            fg="white",
            cursor="hand2",
            command=self.add_vehicle
        )
        add_button.grid(
            row=0,
            column=0,
            padx=10
        )

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            width=15,
            height=2,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.window.destroy
        )
        cancel_button.grid(
            row=0,
            column=1,
            padx=10
        )

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
        """, (vehicle_type,))

        slots = cursor.fetchall()

        connection.close()

        slot_list = [
            slot[0]
            for slot in slots
        ]

        self.slot_combo["values"] = (
            slot_list
        )

    # ===================================
    # CHECK PARKING ID
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
        """, (parking_id,))

        result = cursor.fetchone()

        connection.close()

        return result is not None

    # ===================================
    # SEARCH BEFORE ADD
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
        """, (vehicle_number,))

        result = cursor.fetchone()

        connection.close()

        return result

    # ===================================
    # VALIDATE PARKING SLOT
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
        """, (parking_slot,))

        slot = cursor.fetchone()

        connection.close()

        if slot is None:

            return (
                False,
                "Selected parking slot does not exist."
            )

        slot_number = slot[0]
        slot_type = slot[1]
        slot_status = slot[2]

        if slot_type != vehicle_type:

            return (
                False,
                f"Slot {slot_number} is reserved "
                f"for {slot_type} vehicles."
            )

        if slot_status != "Available":

            return (
                False,
                f"Slot {slot_number} is currently occupied."
            )

        return (
            True,
            "Parking slot is valid."
        )

    # ===================================
    # ADD VEHICLE
    # ===================================

    def add_vehicle(self):

        # ===================================
        # GET FORM DATA
        # ===================================

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
        # 1. REQUIRED FIELD VALIDATION
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

            self.vehicle_type_combo.focus()
            return

        if not parking_slot:

            messagebox.showwarning(
                "Validation Error",
                "Please select a Parking Slot.",
                parent=self.window
            )

            self.slot_combo.focus()
            return

        # ===================================
        # 2. PARKING ID NORMALIZATION
        # ===================================

        parking_id = parking_id.upper()

        # ===================================
        # 3. PARKING ID FORMAT
        # ===================================

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

            self.parking_id_entry.focus()
            return

        self.parking_id_entry.delete(
            0,
            tk.END
        )

        self.parking_id_entry.insert(
            0,
            parking_id
        )

        # ===================================
        # 4. UNIQUE PARKING ID
        # ===================================

        if self.parking_id_exists(
            parking_id
        ):

            messagebox.showerror(
                "Duplicate Parking ID",

                f"Parking ID {parking_id} "
                "already exists.\n\n"
                "Please use a different Parking ID.",

                parent=self.window
            )

            self.parking_id_entry.focus()
            return

        # ===================================
        # 5. OWNER NAME VALIDATION
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

            self.owner_name_entry.focus()
            return

        # ===================================
        # 6. PHONE VALIDATION
        # ===================================

        if not phone.isdigit():

            messagebox.showwarning(
                "Invalid Phone Number",
                "Phone Number should contain "
                "digits only.",
                parent=self.window
            )

            self.phone_entry.focus()
            return

        if len(phone) != 10:

            messagebox.showwarning(
                "Invalid Phone Number",
                "Phone Number must contain "
                "exactly 10 digits.",
                parent=self.window
            )

            self.phone_entry.focus()
            return

        if phone[0] not in "6789":

            messagebox.showwarning(
                "Invalid Phone Number",
                "Phone Number must start with "
                "6, 7, 8 or 9.",
                parent=self.window
            )

            self.phone_entry.focus()
            return

        # ===================================
        # 7. VEHICLE NUMBER NORMALIZATION
        # ===================================

        vehicle_number = (
            normalize_vehicle_number(
                vehicle_number
            )
        )

        # ===================================
        # 8. VEHICLE NUMBER VALIDATION
        # ===================================

        if not vehicle_number.isalnum():

            messagebox.showwarning(
                "Invalid Vehicle Number",
                "Vehicle Number should contain "
                "only letters and numbers.",
                parent=self.window
            )

            self.vehicle_number_entry.focus()
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

            self.vehicle_number_entry.focus()
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
        # 9. SEARCH BEFORE ADD
        # ===================================

        existing_vehicle = (
            self.vehicle_already_parked(
                vehicle_number
            )
        )

        if existing_vehicle:

            existing_parking_id = (
                existing_vehicle[0]
            )

            existing_vehicle_number = (
                existing_vehicle[1]
            )

            existing_owner = (
                existing_vehicle[2]
            )

            existing_slot = (
                existing_vehicle[3]
            )

            existing_entry_time = (
                existing_vehicle[4]
            )

            messagebox.showerror(
                "Duplicate Vehicle Detected",

                "This vehicle is already parked.\n\n"

                f"Parking ID: {existing_parking_id}\n"
                f"Vehicle Number: {existing_vehicle_number}\n"
                f"Owner: {existing_owner}\n"
                f"Parking Slot: {existing_slot}\n"
                f"Entry Time: {existing_entry_time}\n\n"

                "Duplicate entry has been prevented.",

                parent=self.window
            )

            self.vehicle_number_entry.focus()
            return

        # ===================================
        # 10. PARKING SLOT VALIDATION
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
            self.slot_combo.focus()

            return

        # ===================================
        # 11. CONFIRMATION DIALOG
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

        # ===================================
        # USER SELECTED NO
        # ===================================

        if not confirmation:

            messagebox.showinfo(
                "Entry Cancelled",

                "Vehicle entry was not submitted.\n\n"
                "Please correct the details if required.",

                parent=self.window
            )

            return

        # ===================================
        # USER SELECTED YES
        # ===================================

        messagebox.showinfo(
            "Confirmation Successful",

            "Vehicle details have been confirmed.\n\n"
            "All TQM quality checks passed.\n\n"
            "Database insertion will be added "
            "in the next development step.",

            parent=self.window
        )

        # ===================================
        # DEBUG OUTPUT
        # ===================================

        print("------------------------------")
        print("VEHICLE ENTRY CONFIRMED")
        print("------------------------------")

        print(
            "Parking ID:",
            parking_id
        )

        print(
            "Vehicle Number:",
            vehicle_number
        )

        print(
            "Owner Name:",
            owner_name
        )

        print(
            "Phone:",
            phone
        )

        print(
            "Vehicle Type:",
            vehicle_type
        )

        print(
            "Parking Slot:",
            parking_slot
        )

        print(
            "Confirmation: YES"
        )

        print("------------------------------")