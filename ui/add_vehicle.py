import tkinter as tk
from tkinter import ttk, messagebox
import re

from database.db import get_connection


class AddVehicleWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Add Vehicle")
        self.window.geometry("600x650")
        self.window.resizable(False, False)

        # Keep window above main dashboard
        self.window.transient(parent)
        self.window.grab_set()

        # -----------------------------------
        # HEADER
        # -----------------------------------

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

        # -----------------------------------
        # FORM
        # -----------------------------------

        form_frame = tk.Frame(
            self.window,
            padx=40,
            pady=25
        )

        form_frame.pack(fill="both", expand=True)

        # -----------------------------------
        # PARKING ID
        # -----------------------------------

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

        # -----------------------------------
        # VEHICLE NUMBER
        # -----------------------------------

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

        # -----------------------------------
        # OWNER NAME
        # -----------------------------------

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

        # -----------------------------------
        # PHONE NUMBER
        # -----------------------------------

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

        # -----------------------------------
        # VEHICLE TYPE
        # -----------------------------------

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

        # -----------------------------------
        # PARKING SLOT
        # -----------------------------------

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

        # Load available parking slots
        self.load_available_slots()

        # -----------------------------------
        # BUTTONS
        # -----------------------------------

        button_frame = tk.Frame(form_frame)

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

    # -----------------------------------
    # LOAD AVAILABLE PARKING SLOTS
    # -----------------------------------

    def load_available_slots(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT slot_number
            FROM parking_slots
            WHERE status = 'Available'
            ORDER BY slot_number
        """)

        slots = cursor.fetchall()

        connection.close()

        # Convert:
        # [('A01',), ('A02',)]
        #
        # into:
        # ['A01', 'A02']

        slot_list = [slot[0] for slot in slots]

        self.slot_combo["values"] = slot_list

    # -----------------------------------
    # ADD VEHICLE
    # -----------------------------------

    def add_vehicle(self):

        # Get values from form

        parking_id = self.parking_id_entry.get().strip()

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

        phone = self.phone_entry.get().strip()

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

        # -----------------------------------
        # PRE-ADD VALIDATION
        # -----------------------------------

        # Parking ID validation

        if not parking_id:

            messagebox.showwarning(
                "Validation Error",
                "Parking ID is required.",
                parent=self.window
            )

            self.parking_id_entry.focus()

            return

        # Vehicle Number validation

        if not vehicle_number:

            messagebox.showwarning(
                "Validation Error",
                "Vehicle Number is required.",
                parent=self.window
            )

            self.vehicle_number_entry.focus()

            return

        # Owner Name validation

        if not owner_name:

            messagebox.showwarning(
                "Validation Error",
                "Owner Name is required.",
                parent=self.window
            )

            self.owner_name_entry.focus()

            return

        # Phone Number validation

        if not phone:

            messagebox.showwarning(
                "Validation Error",
                "Phone Number is required.",
                parent=self.window
            )

            self.phone_entry.focus()

            return

        # Vehicle Type validation

        if not vehicle_type:

            messagebox.showwarning(
                "Validation Error",
                "Please select a Vehicle Type.",
                parent=self.window
            )

            return

        # Parking Slot validation

        if not parking_slot:

            messagebox.showwarning(
                "Validation Error",
                "Please select a Parking Slot.",
                parent=self.window
            )

            return

        # -----------------------------------
        # VALIDATION SUCCESS
        # -----------------------------------
                # -----------------------------------
        # DATA FORMAT VALIDATION
        # -----------------------------------

        # Parking ID format
        # Valid examples: P001, P002, P100

        if not re.fullmatch(r"P\d{3}", parking_id.upper()):

            messagebox.showwarning(
                "Invalid Parking ID",
                "Parking ID must be in the format P001, P002, P003, etc.",
                parent=self.window
            )

            self.parking_id_entry.focus()

            return

        # -----------------------------------
        # OWNER NAME VALIDATION
        # -----------------------------------

        if not re.fullmatch(r"[A-Za-z ]+", owner_name):

            messagebox.showwarning(
                "Invalid Owner Name",
                "Owner Name should contain only letters and spaces.",
                parent=self.window
            )

            self.owner_name_entry.focus()

            return

        # -----------------------------------
        # PHONE NUMBER VALIDATION
        # -----------------------------------

        if not phone.isdigit():

            messagebox.showwarning(
                "Invalid Phone Number",
                "Phone Number should contain digits only.",
                parent=self.window
            )

            self.phone_entry.focus()

            return

        if len(phone) != 10:

            messagebox.showwarning(
                "Invalid Phone Number",
                "Phone Number must contain exactly 10 digits.",
                parent=self.window
            )

            self.phone_entry.focus()

            return

        # Indian mobile numbers normally begin with 6, 7, 8 or 9

        if phone[0] not in "6789":

            messagebox.showwarning(
                "Invalid Phone Number",
                "Phone Number must start with 6, 7, 8 or 9.",
                parent=self.window
            )

            self.phone_entry.focus()

            return

        # -----------------------------------
        # VEHICLE NUMBER BASIC VALIDATION
        # -----------------------------------

        cleaned_vehicle_number = (
            vehicle_number
            .upper()
            .replace(" ", "")
            .replace("-", "")
        )

        if not cleaned_vehicle_number.isalnum():

            messagebox.showwarning(
                "Invalid Vehicle Number",
                "Vehicle Number should contain only letters and numbers.",
                parent=self.window
            )

            self.vehicle_number_entry.focus()

            return

        if len(cleaned_vehicle_number) < 8 or len(cleaned_vehicle_number) > 11:

            messagebox.showwarning(
                "Invalid Vehicle Number",
                "Please enter a valid vehicle registration number.",
                parent=self.window
            )

            self.vehicle_number_entry.focus()

            return
        messagebox.showinfo(
            "Validation Successful",
            "All required fields are valid.",
            parent=self.window
        )

        print("Pre-add validation passed.")