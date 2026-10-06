import tkinter as tk
from tkinter import ttk

from database.db import get_connection


class ParkingSlotsWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Parking Slots")
        self.window.geometry("950x650")
        self.window.minsize(850, 550)

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
            text="PARKING SLOTS",
            font=("Arial", 22, "bold"),
            bg="#1F2937",
            fg="white"
        ).pack(pady=(20, 5))

        tk.Label(
            header,
            text="Live Parking Slot Monitoring",
            font=("Arial", 11),
            bg="#1F2937",
            fg="white"
        ).pack()

        # ===================================
        # MAIN FRAME
        # ===================================

        main_frame = tk.Frame(
            self.window,
            bg="#F3F4F6",
            padx=20,
            pady=20
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        # ===================================
        # STATISTICS FRAME
        # ===================================

        stats_frame = tk.Frame(
            main_frame,
            bg="#F3F4F6"
        )
        stats_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.total_var = tk.StringVar(
            value="Total: 0"
        )

        self.available_var = tk.StringVar(
            value="Available: 0"
        )

        self.occupied_var = tk.StringVar(
            value="Occupied: 0"
        )

        tk.Label(
            stats_frame,
            textvariable=self.total_var,
            width=18,
            height=2,
            bg="white",
            font=("Arial", 11, "bold"),
            relief="solid",
            bd=1
        ).pack(
            side="left",
            padx=5
        )

        tk.Label(
            stats_frame,
            textvariable=self.available_var,
            width=18,
            height=2,
            bg="white",
            font=("Arial", 11, "bold"),
            relief="solid",
            bd=1
        ).pack(
            side="left",
            padx=5
        )

        tk.Label(
            stats_frame,
            textvariable=self.occupied_var,
            width=18,
            height=2,
            bg="white",
            font=("Arial", 11, "bold"),
            relief="solid",
            bd=1
        ).pack(
            side="left",
            padx=5
        )

        # ===================================
        # FILTER FRAME
        # ===================================

        filter_frame = tk.Frame(
            main_frame,
            bg="#F3F4F6"
        )
        filter_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            filter_frame,
            text="Slot Type:",
            font=("Arial", 10, "bold"),
            bg="#F3F4F6"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.type_combo = ttk.Combobox(
            filter_frame,
            values=[
                "All",
                "Car",
                "Bike"
            ],
            width=12,
            state="readonly"
        )
        self.type_combo.pack(
            side="left",
            padx=5
        )
        self.type_combo.set("All")

        tk.Label(
            filter_frame,
            text="Status:",
            font=("Arial", 10, "bold"),
            bg="#F3F4F6"
        ).pack(
            side="left",
            padx=(20, 5)
        )

        self.status_combo = ttk.Combobox(
            filter_frame,
            values=[
                "All",
                "Available",
                "Occupied"
            ],
            width=12,
            state="readonly"
        )
        self.status_combo.pack(
            side="left",
            padx=5
        )
        self.status_combo.set("All")

        refresh_button = tk.Button(
            filter_frame,
            text="Refresh",
            width=12,
            cursor="hand2",
            command=self.load_slots
        )
        refresh_button.pack(
            side="left",
            padx=20
        )

        clear_button = tk.Button(
            filter_frame,
            text="Clear Filter",
            width=12,
            cursor="hand2",
            command=self.clear_filters
        )
        clear_button.pack(
            side="left",
            padx=5
        )

        # ===================================
        # TABLE FRAME
        # ===================================

        table_frame = tk.Frame(
            main_frame
        )
        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "slot_number",
            "slot_type",
            "status",
            "parking_id",
            "vehicle_number",
            "owner_name"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # ===================================
        # TABLE HEADINGS
        # ===================================

        self.tree.heading(
            "slot_number",
            text="Slot Number"
        )

        self.tree.heading(
            "slot_type",
            text="Slot Type"
        )

        self.tree.heading(
            "status",
            text="Status"
        )

        self.tree.heading(
            "parking_id",
            text="Parking ID"
        )

        self.tree.heading(
            "vehicle_number",
            text="Vehicle Number"
        )

        self.tree.heading(
            "owner_name",
            text="Owner Name"
        )

        # ===================================
        # COLUMN WIDTHS
        # ===================================

        self.tree.column(
            "slot_number",
            width=110,
            anchor="center"
        )

        self.tree.column(
            "slot_type",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "status",
            width=110,
            anchor="center"
        )

        self.tree.column(
            "parking_id",
            width=110,
            anchor="center"
        )

        self.tree.column(
            "vehicle_number",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "owner_name",
            width=160
        )

        # ===================================
        # SCROLLBARS
        # ===================================

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        # ===================================
        # BOTTOM
        # ===================================

        bottom_frame = tk.Frame(
            main_frame,
            bg="#F3F4F6"
        )
        bottom_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        self.display_count_var = tk.StringVar(
            value="Showing 0 slots"
        )

        tk.Label(
            bottom_frame,
            textvariable=self.display_count_var,
            font=("Arial", 10),
            bg="#F3F4F6",
            fg="#4B5563"
        ).pack(
            side="left"
        )

        close_button = tk.Button(
            bottom_frame,
            text="Close",
            width=15,
            height=2,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.window.destroy
        )
        close_button.pack(
            side="right"
        )

        # ===================================
        # FILTER EVENTS
        # ===================================

        self.type_combo.bind(
            "<<ComboboxSelected>>",
            self.filter_changed
        )

        self.status_combo.bind(
            "<<ComboboxSelected>>",
            self.filter_changed
        )

        # ===================================
        # INITIAL LOAD
        # ===================================

        self.load_slots()

    # ===================================
    # CLEAR TABLE
    # ===================================

    def clear_table(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

    # ===================================
    # GET OVERALL STATISTICS
    # ===================================

    def update_statistics(self):

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

        self.total_var.set(
            f"Total: {total}"
        )

        self.available_var.set(
            f"Available: {available}"
        )

        self.occupied_var.set(
            f"Occupied: {occupied}"
        )

    # ===================================
    # LOAD SLOTS
    # ===================================

    def load_slots(self):

        self.clear_table()

        slot_type = (
            self.type_combo
            .get()
            .strip()
        )

        slot_status = (
            self.status_combo
            .get()
            .strip()
        )

        connection = get_connection()
        cursor = connection.cursor()

        # ===================================
        # QUERY
        # ===================================

        query = """
            SELECT
                ps.slot_number,
                ps.slot_type,
                ps.status,
                pr.parking_id,
                pr.vehicle_number,
                pr.owner_name

            FROM parking_slots ps

            LEFT JOIN parking_records pr

                ON ps.slot_number = pr.slot_number
                AND pr.status = 'Parked'

            WHERE 1 = 1
        """

        parameters = []

        if slot_type != "All":

            query += """
                AND ps.slot_type = ?
            """

            parameters.append(
                slot_type
            )

        if slot_status != "All":

            query += """
                AND ps.status = ?
            """

            parameters.append(
                slot_status
            )

        query += """
            ORDER BY ps.slot_number
        """

        cursor.execute(
            query,
            parameters
        )

        slots = cursor.fetchall()

        connection.close()

        # ===================================
        # DISPLAY SLOTS
        # ===================================

        for slot in slots:

            slot_number = slot[0]
            slot_type_value = slot[1]
            status = slot[2]

            parking_id = (
                slot[3]
                if slot[3]
                else "-"
            )

            vehicle_number = (
                slot[4]
                if slot[4]
                else "-"
            )

            owner_name = (
                slot[5]
                if slot[5]
                else "-"
            )

            self.tree.insert(
                "",
                tk.END,
                values=(
                    slot_number,
                    slot_type_value,
                    status,
                    parking_id,
                    vehicle_number,
                    owner_name
                )
            )

        self.display_count_var.set(
            f"Showing {len(slots)} slots"
        )

        self.update_statistics()

    # ===================================
    # FILTER CHANGED
    # ===================================

    def filter_changed(
        self,
        event=None
    ):

        self.load_slots()

    # ===================================
    # CLEAR FILTERS
    # ===================================

    def clear_filters(self):

        self.type_combo.set(
            "All"
        )

        self.status_combo.set(
            "All"
        )

        self.load_slots()