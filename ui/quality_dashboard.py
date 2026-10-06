import tkinter as tk
from tkinter import ttk

from services.quality_service import (
    get_quality_counts,
    get_total_quality_events,
    get_recent_quality_events,
    VEHICLE_ADDED,
    VEHICLE_EXITED,
    DUPLICATE_ATTEMPT,
    VALIDATION_FAILED,
    SLOT_CONFLICT
)


class QualityDashboardWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Quality Dashboard"
        )

        self.window.geometry(
            "1100x700"
        )

        self.window.minsize(
            950,
            600
        )

        self.window.transient(parent)

        # ==========================================
        # HEADER
        # ==========================================

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
            text="QUALITY DASHBOARD",
            font=("Arial", 22, "bold"),
            bg="#1F2937",
            fg="white"
        ).pack(
            pady=(18, 4)
        )

        tk.Label(
            header,
            text="TQM Performance Monitoring & Quality Control",
            font=("Arial", 11),
            bg="#1F2937",
            fg="white"
        ).pack()

        # ==========================================
        # MAIN FRAME
        # ==========================================

        self.main_frame = tk.Frame(
            self.window,
            bg="#F3F4F6"
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # ==========================================
        # TITLE
        # ==========================================

        tk.Label(
            self.main_frame,
            text="Quality Performance Metrics",
            font=("Arial", 18, "bold"),
            bg="#F3F4F6",
            fg="#111827"
        ).pack(
            pady=(20, 10)
        )

        # ==========================================
        # METRIC CARDS
        # ==========================================

        cards_frame = tk.Frame(
            self.main_frame,
            bg="#F3F4F6"
        )

        cards_frame.pack(
            pady=5
        )

        self.successful_entries_value = (
            self.create_metric_card(
                cards_frame,
                "SUCCESSFUL ENTRIES",
                0,
                0,
                0
            )
        )

        self.vehicle_exits_value = (
            self.create_metric_card(
                cards_frame,
                "VEHICLE EXITS",
                0,
                0,
                1
            )
        )

        self.duplicate_attempts_value = (
            self.create_metric_card(
                cards_frame,
                "DUPLICATE ATTEMPTS",
                0,
                0,
                2
            )
        )

        self.validation_failures_value = (
            self.create_metric_card(
                cards_frame,
                "VALIDATION FAILURES",
                0,
                1,
                0
            )
        )

        self.slot_conflicts_value = (
            self.create_metric_card(
                cards_frame,
                "SLOT CONFLICTS",
                0,
                1,
                1
            )
        )

        self.total_events_value = (
            self.create_metric_card(
                cards_frame,
                "TOTAL QUALITY EVENTS",
                0,
                1,
                2
            )
        )

        # ==========================================
        # RECENT EVENTS TITLE
        # ==========================================

        history_header = tk.Frame(
            self.main_frame,
            bg="#F3F4F6"
        )

        history_header.pack(
            fill="x",
            padx=40,
            pady=(20, 5)
        )

        tk.Label(
            history_header,
            text="Recent Quality Events",
            font=("Arial", 15, "bold"),
            bg="#F3F4F6",
            fg="#111827"
        ).pack(
            side="left"
        )

        tk.Button(
            history_header,
            text="Refresh",
            width=12,
            font=("Arial", 9, "bold"),
            cursor="hand2",
            command=self.refresh_dashboard
        ).pack(
            side="right"
        )

        # ==========================================
        # EVENT TABLE FRAME
        # ==========================================

        table_frame = tk.Frame(
            self.main_frame,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(5, 15)
        )

        # ==========================================
        # TREEVIEW
        # ==========================================

        columns = (
            "event_type",
            "description",
            "event_time"
        )

        self.event_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.event_table.heading(
            "event_type",
            text="Event Type"
        )

        self.event_table.heading(
            "description",
            text="Description"
        )

        self.event_table.heading(
            "event_time",
            text="Date & Time"
        )

        self.event_table.column(
            "event_type",
            width=170,
            anchor="center"
        )

        self.event_table.column(
            "description",
            width=580,
            anchor="w"
        )

        self.event_table.column(
            "event_time",
            width=170,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.event_table.yview
        )

        self.event_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.event_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ==========================================
        # FOOTER
        # ==========================================

        footer = tk.Label(
            self.main_frame,
            text=(
                "TQM Principle: Fact-Based Decision Making | "
                "PDCA Phase: Check"
            ),
            font=("Arial", 10, "bold"),
            bg="#F3F4F6",
            fg="#6B7280"
        )

        footer.pack(
            pady=(0, 12)
        )

        # ==========================================
        # INITIAL DATA LOAD
        # ==========================================

        self.refresh_dashboard()

    # ==========================================
    # CREATE METRIC CARD
    # ==========================================

    def create_metric_card(
        self,
        parent,
        title,
        value,
        row,
        column
    ):

        card = tk.Frame(
            parent,
            bg="white",
            width=270,
            height=90,
            bd=1,
            relief="solid"
        )

        card.grid(
            row=row,
            column=column,
            padx=10,
            pady=8
        )

        card.grid_propagate(
            False
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#6B7280"
        ).pack(
            pady=(15, 4)
        )

        value_label = tk.Label(
            card,
            text=str(value),
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#111827"
        )

        value_label.pack()

        return value_label

    # ==========================================
    # REFRESH DASHBOARD
    # ==========================================

    def refresh_dashboard(self):

        counts = get_quality_counts()

        total_events = (
            get_total_quality_events()
        )

        self.successful_entries_value.config(
            text=str(
                counts.get(
                    VEHICLE_ADDED,
                    0
                )
            )
        )

        self.vehicle_exits_value.config(
            text=str(
                counts.get(
                    VEHICLE_EXITED,
                    0
                )
            )
        )

        self.duplicate_attempts_value.config(
            text=str(
                counts.get(
                    DUPLICATE_ATTEMPT,
                    0
                )
            )
        )

        self.validation_failures_value.config(
            text=str(
                counts.get(
                    VALIDATION_FAILED,
                    0
                )
            )
        )

        self.slot_conflicts_value.config(
            text=str(
                counts.get(
                    SLOT_CONFLICT,
                    0
                )
            )
        )

        self.total_events_value.config(
            text=str(
                total_events
            )
        )

        self.load_recent_events()

    # ==========================================
    # LOAD RECENT EVENTS
    # ==========================================

    def load_recent_events(self):

        for item in (
            self.event_table.get_children()
        ):

            self.event_table.delete(
                item
            )

        events = (
            get_recent_quality_events(
                20
            )
        )

        for event in events:

            self.event_table.insert(
                "",
                "end",
                values=(
                    event[0],
                    event[1],
                    event[2]
                )
            )