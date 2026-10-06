import tkinter as tk

from database.db import get_connection
from ui.add_vehicle import AddVehicleWindow
from ui.search_vehicle import SearchVehicleWindow
from ui.vehicle_exit import VehicleExitWindow
from ui.parking_records import ParkingRecordsWindow
from ui.parking_slots import ParkingSlotsWindow


class Dashboard:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Parking Management System"
        )

        self.root.geometry(
            "1100x700"
        )

        self.root.minsize(
            900,
            600
        )

        # ===================================
        # HEADER
        # ===================================

        header = tk.Frame(
            root,
            bg="#1F2937",
            height=100
        )

        header.pack(
            fill="x"
        )

        title = tk.Label(
            header,
            text="PARKING MANAGEMENT SYSTEM",
            font=("Arial", 24, "bold"),
            bg="#1F2937",
            fg="white"
        )

        title.pack(
            pady=(20, 5)
        )

        subtitle = tk.Label(
            header,
            text="TQM-Based Quality Management System",
            font=("Arial", 11),
            bg="#1F2937",
            fg="white"
        )

        subtitle.pack()

        # ===================================
        # MAIN FRAME
        # ===================================

        main_frame = tk.Frame(
            root,
            bg="#F3F4F6"
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        dashboard_title = tk.Label(
            main_frame,
            text="Parking Dashboard",
            font=("Arial", 20, "bold"),
            bg="#F3F4F6",
            fg="#111827"
        )

        dashboard_title.pack(
            pady=25
        )

        # ===================================
        # STATISTICS
        # ===================================

        stats_frame = tk.Frame(
            main_frame,
            bg="#F3F4F6"
        )

        stats_frame.pack(
            pady=10
        )

        total, available, occupied = (
            self.get_parking_statistics()
        )

        self.create_stat_card(
            stats_frame,
            "TOTAL SLOTS",
            total,
            0
        )

        self.create_stat_card(
            stats_frame,
            "AVAILABLE",
            available,
            1
        )

        self.create_stat_card(
            stats_frame,
            "OCCUPIED",
            occupied,
            2
        )

        # ===================================
        # BUTTONS
        # ===================================

        button_frame = tk.Frame(
            main_frame,
            bg="#F3F4F6"
        )

        button_frame.pack(
            pady=35
        )

        buttons = [

            (
                "+ Add Vehicle",
                self.add_vehicle
            ),

            (
                "Search Vehicle",
                self.search_vehicle
            ),

            (
                "Vehicle Exit",
                self.vehicle_exit
            ),

            (
                "Parking Records",
                self.parking_records
            ),

            (
                "Parking Slots",
                self.parking_slots
            ),

            (
                "Quality Dashboard",
                self.quality_dashboard
            )
        ]

        row = 0
        column = 0

        for text, command in buttons:

            button = tk.Button(
                button_frame,
                text=text,
                width=22,
                height=2,
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#111827",
                cursor="hand2",
                relief="groove",
                command=command
            )

            button.grid(
                row=row,
                column=column,
                padx=15,
                pady=12
            )

            column += 1

            if column == 2:

                column = 0
                row += 1

        # ===================================
        # FOOTER
        # ===================================

        footer = tk.Label(
            main_frame,

            text=(
                "Quality Goal: Reduce duplicate "
                "entries and improve parking "
                "data accuracy"
            ),

            font=("Arial", 10),

            bg="#F3F4F6",

            fg="#6B7280"
        )

        footer.pack(
            side="bottom",
            pady=15
        )

    # ===================================
    # PARKING STATISTICS
    # ===================================

    def get_parking_statistics(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM parking_slots
        """)

        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM parking_slots
            WHERE status = 'Available'
        """)

        available = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM parking_slots
            WHERE status = 'Occupied'
        """)

        occupied = cursor.fetchone()[0]

        connection.close()

        return (
            total,
            available,
            occupied
        )

    # ===================================
    # CREATE STAT CARD
    # ===================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = tk.Frame(
            parent,
            bg="white",
            width=220,
            height=110,
            bd=1,
            relief="solid"
        )

        card.grid(
            row=0,
            column=column,
            padx=15
        )

        card.grid_propagate(
            False
        )

        title_label = tk.Label(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#6B7280"
        )

        title_label.pack(
            pady=(20, 5)
        )

        value_label = tk.Label(
            card,
            text=str(value),
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#111827"
        )

        value_label.pack()

    # ===================================
    # ADD VEHICLE
    # ===================================

    def add_vehicle(self):

        AddVehicleWindow(
            self.root
        )

    # ===================================
    # SEARCH VEHICLE
    # ===================================

    def search_vehicle(self):

        SearchVehicleWindow(
            self.root
        )

    # ===================================
    # VEHICLE EXIT
    # ===================================

    def vehicle_exit(self):

        VehicleExitWindow(
            self.root
        )

    # ===================================
    # PARKING RECORDS
    # ===================================

    def parking_records(self):

        ParkingRecordsWindow(
            self.root
        )

    # ===================================
    # PARKING SLOTS
    # ===================================

    def parking_slots(self):

        ParkingSlotsWindow(
            self.root
        )

    # ===================================
    # QUALITY DASHBOARD
    # ===================================

    def quality_dashboard(self):

        print(
            "Quality Dashboard clicked"
        )