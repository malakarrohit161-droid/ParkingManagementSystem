import tkinter as tk
from tkinter import ttk, messagebox

from database.db import get_connection
from services.validation import normalize_vehicle_number


class ParkingRecordsWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Parking Records")
        self.window.geometry("1200x700")
        self.window.minsize(1000, 600)

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
            text="PARKING RECORDS",
            font=("Arial", 22, "bold"),
            bg="#1F2937",
            fg="white"
        ).pack(pady=(20, 5))

        tk.Label(
            header,
            text="Complete Vehicle Entry and Exit History",
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
        # FILTER SECTION
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
            text="Status:",
            font=("Arial", 10, "bold"),
            bg="#F3F4F6"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.status_combo = ttk.Combobox(
            filter_frame,
            values=[
                "All",
                "Parked",
                "Exited"
            ],
            width=15,
            state="readonly"
        )
        self.status_combo.pack(
            side="left",
            padx=5
        )
        self.status_combo.set("All")

        tk.Label(
            filter_frame,
            text="Search:",
            font=("Arial", 10, "bold"),
            bg="#F3F4F6"
        ).pack(
            side="left",
            padx=(25, 5)
        )

        self.search_entry = tk.Entry(
            filter_frame,
            width=25,
            font=("Arial", 10)
        )
        self.search_entry.pack(
            side="left",
            padx=5
        )

        search_button = tk.Button(
            filter_frame,
            text="Search",
            width=10,
            cursor="hand2",
            command=self.search_records
        )
        search_button.pack(
            side="left",
            padx=5
        )

        refresh_button = tk.Button(
            filter_frame,
            text="Refresh",
            width=10,
            cursor="hand2",
            command=self.load_records
        )
        refresh_button.pack(
            side="left",
            padx=5
        )

        clear_button = tk.Button(
            filter_frame,
            text="Clear Filter",
            width=12,
            cursor="hand2",
            command=self.clear_filter
        )
        clear_button.pack(
            side="left",
            padx=5
        )

        # ===================================
        # RECORD COUNT
        # ===================================

        self.record_count_var = tk.StringVar(
            value="Total Records: 0"
        )

        count_label = tk.Label(
            main_frame,
            textvariable=self.record_count_var,
            font=("Arial", 10, "bold"),
            bg="#F3F4F6",
            fg="#374151"
        )
        count_label.pack(
            anchor="w",
            pady=(0, 8)
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

        # ===================================
        # TREEVIEW
        # ===================================

        columns = (
            "parking_id",
            "vehicle_number",
            "owner_name",
            "phone",
            "vehicle_type",
            "slot_number",
            "entry_time",
            "exit_time",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # ===================================
        # HEADINGS
        # ===================================

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

        self.tree.heading(
            "phone",
            text="Phone"
        )

        self.tree.heading(
            "vehicle_type",
            text="Type"
        )

        self.tree.heading(
            "slot_number",
            text="Slot"
        )

        self.tree.heading(
            "entry_time",
            text="Entry Time"
        )

        self.tree.heading(
            "exit_time",
            text="Exit Time"
        )

        self.tree.heading(
            "status",
            text="Status"
        )

        # ===================================
        # COLUMN WIDTHS
        # ===================================

        self.tree.column(
            "parking_id",
            width=90,
            anchor="center"
        )

        self.tree.column(
            "vehicle_number",
            width=130,
            anchor="center"
        )

        self.tree.column(
            "owner_name",
            width=140
        )

        self.tree.column(
            "phone",
            width=110,
            anchor="center"
        )

        self.tree.column(
            "vehicle_type",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "slot_number",
            width=70,
            anchor="center"
        )

        self.tree.column(
            "entry_time",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "exit_time",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "status",
            width=90,
            anchor="center"
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
        # BOTTOM BUTTON
        # ===================================

        bottom_frame = tk.Frame(
            main_frame,
            bg="#F3F4F6"
        )
        bottom_frame.pack(
            fill="x",
            pady=(15, 0)
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
        # EVENTS
        # ===================================

        self.status_combo.bind(
            "<<ComboboxSelected>>",
            self.status_filter_changed
        )

        self.search_entry.bind(
            "<Return>",
            self.search_records
        )

        # ===================================
        # LOAD DATABASE RECORDS
        # ===================================

        self.load_records()

    # ===================================
    # CLEAR TABLE
    # ===================================

    def clear_table(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

    # ===================================
    # DISPLAY RECORDS
    # ===================================

    def display_records(
        self,
        records
    ):

        self.clear_table()

        for record in records:

            parking_id = record[0]
            vehicle_number = record[1]
            owner_name = record[2]
            phone = record[3]
            vehicle_type = record[4]
            slot_number = record[5]
            entry_time = record[6]

            if record[7]:

                exit_time = record[7]

            else:

                exit_time = "Not Exited"

            status = record[8]

            self.tree.insert(
                "",
                tk.END,
                values=(
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
            )

        self.record_count_var.set(
            f"Total Records: {len(records)}"
        )

    # ===================================
    # LOAD ALL / FILTERED RECORDS
    # ===================================

    def load_records(
        self
    ):

        status = (
            self.status_combo
            .get()
            .strip()
        )

        connection = get_connection()
        cursor = connection.cursor()

        if status == "All":

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

                ORDER BY id DESC
            """)

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

                WHERE status = ?

                ORDER BY id DESC
            """, (status,))

        records = cursor.fetchall()

        connection.close()

        self.display_records(
            records
        )

    # ===================================
    # STATUS FILTER
    # ===================================

    def status_filter_changed(
        self,
        event=None
    ):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.load_records()

    # ===================================
    # SEARCH RECORDS
    # ===================================

    def search_records(
        self,
        event=None
    ):

        search_value = (
            self.search_entry
            .get()
            .strip()
        )

        status = (
            self.status_combo
            .get()
            .strip()
        )

        if not search_value:

            self.load_records()
            return

        # -----------------------------------
        # Prepare possible search formats
        # -----------------------------------

        parking_id_search = (
            search_value.upper()
        )

        vehicle_search = (
            normalize_vehicle_number(
                search_value
            )
        )

        owner_search = (
            f"%{search_value}%"
        )

        # -----------------------------------
        # DATABASE SEARCH
        # -----------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        if status == "All":

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

                WHERE
                    parking_id = ?
                    OR vehicle_number = ?
                    OR owner_name LIKE ?

                ORDER BY id DESC
            """, (
                parking_id_search,
                vehicle_search,
                owner_search
            ))

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

                WHERE status = ?

                AND (
                    parking_id = ?
                    OR vehicle_number = ?
                    OR owner_name LIKE ?
                )

                ORDER BY id DESC
            """, (
                status,
                parking_id_search,
                vehicle_search,
                owner_search
            ))

        records = cursor.fetchall()

        connection.close()

        self.display_records(
            records
        )

        if not records:

            messagebox.showinfo(
                "No Records Found",

                "No parking records matched "
                "your search.",

                parent=self.window
            )

    # ===================================
    # CLEAR FILTER
    # ===================================

    def clear_filter(
        self
    ):

        self.status_combo.set(
            "All"
        )

        self.search_entry.delete(
            0,
            tk.END
        )

        self.load_records()