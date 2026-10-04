import tkinter as tk
from tkinter import ttk


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

        # Parking ID
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

        # Vehicle Number
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

        # Owner Name
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

        # Phone Number
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

        # Vehicle Type
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

        # Parking Slot
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
    # TEMPORARY FUNCTION
    # -----------------------------------

    def add_vehicle(self):

        print("Add Vehicle button clicked")