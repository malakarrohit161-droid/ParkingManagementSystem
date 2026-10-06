import tkinter as tk
from tkinter import ttk

from services.quality_service import (
    get_quality_metrics,
    get_recent_quality_events
)


class QualityDashboardWindow:

    def __init__(
        self,
        parent
    ):

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            "TQM Quality Dashboard"
        )

        self.window.geometry(
            "1200x760"
        )

        self.window.minsize(
            1050,
            650
        )

        self.window.transient(
            parent
        )

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
            text="TQM QUALITY DASHBOARD",
            font=("Arial", 22, "bold"),
            bg="#1F2937",
            fg="white"
        ).pack(
            pady=(18, 4)
        )

        tk.Label(
            header,
            text=(
                "Quality Performance Monitoring "
                "and Continuous Improvement"
            ),
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
            text="Quality Performance Indicators",
            font=("Arial", 18, "bold"),
            bg="#F3F4F6",
            fg="#111827"
        ).pack(
            pady=(15, 8)
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

        self.duplicate_attempts_value = (
            self.create_metric_card(
                cards_frame,
                "DUPLICATE ATTEMPTS",
                0,
                0,
                1
            )
        )

        self.actual_duplicates_value = (
            self.create_metric_card(
                cards_frame,
                "ACTUAL DUPLICATES",
                0,
                0,
                2
            )
        )

        self.duplicate_rate_value = (
            self.create_metric_card(
                cards_frame,
                "DUPLICATE PREVENTION",
                "0%",
                0,
                3
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

        self.vehicle_exits_value = (
            self.create_metric_card(
                cards_frame,
                "VEHICLE EXITS",
                0,
                1,
                2
            )
        )

        self.success_rate_value = (
            self.create_metric_card(
                cards_frame,
                "ENTRY SUCCESS RATE",
                "0%",
                1,
                3
            )
        )

        # ==========================================
        # QUALITY STATUS
        # ==========================================

        status_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        status_frame.pack(
            fill="x",
            padx=40,
            pady=(10, 8)
        )

        tk.Label(
            status_frame,
            text="DATA QUALITY STATUS:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#6B7280"
        ).pack(
            side="left",
            padx=(20, 10),
            pady=12
        )

        self.quality_status_value = tk.Label(
            status_frame,
            text="-",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#111827"
        )

        self.quality_status_value.pack(
            side="left",
            pady=12
        )

        tk.Label(
            status_frame,
            text=(
                "Target: 0 active duplicate vehicles"
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6B7280"
        ).pack(
            side="right",
            padx=20,
            pady=12
        )

        # ==========================================
        # HISTORY HEADER
        # ==========================================

        history_header = tk.Frame(
            self.main_frame,
            bg="#F3F4F6"
        )

        history_header.pack(
            fill="x",
            padx=40,
            pady=(8, 5)
        )

        tk.Label(
            history_header,
            text="Recent Quality Events",
            font=("Arial", 14, "bold"),
            bg="#F3F4F6",
            fg="#111827"
        ).pack(
            side="left"
        )

        tk.Button(
            history_header,
            text="Refresh Metrics",
            width=15,
            font=("Arial", 9, "bold"),
            cursor="hand2",
            command=self.refresh_dashboard
        ).pack(
            side="right"
        )

        # ==========================================
        # EVENT TABLE
        # ==========================================

        table_frame = tk.Frame(
            self.main_frame,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(5, 10)
        )

        columns = (
            "event_type",
            "description",
            "event_time"
        )

        self.event_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=7
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
            width=180,
            anchor="center"
        )

        self.event_table.column(
            "description",
            width=650,
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

        tk.Label(
            self.main_frame,
            text=(
                "TQM | Defect Prevention | "
                "Fact-Based Decision Making | "
                "PDCA: Check"
            ),
            font=("Arial", 9, "bold"),
            bg="#F3F4F6",
            fg="#6B7280"
        ).pack(
            pady=(0, 10)
        )

        # ==========================================
        # LOAD DATA
        # ==========================================

        self.refresh_dashboard()

    # ==========================================
    # CREATE CARD
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
            width=250,
            height=85,
            bd=1,
            relief="solid"
        )

        card.grid(
            row=row,
            column=column,
            padx=7,
            pady=7
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
            pady=(14, 3)
        )

        value_label = tk.Label(
            card,
            text=str(value),
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#111827"
        )

        value_label.pack()

        return value_label

    # ==========================================
    # REFRESH DASHBOARD
    # ==========================================

    def refresh_dashboard(
        self
    ):

        metrics = (
            get_quality_metrics()
        )

        self.successful_entries_value.config(
            text=str(
                metrics[
                    "successful_entries"
                ]
            )
        )

        self.duplicate_attempts_value.config(
            text=str(
                metrics[
                    "duplicate_attempts"
                ]
            )
        )

        self.actual_duplicates_value.config(
            text=str(
                metrics[
                    "actual_duplicates"
                ]
            )
        )

        self.duplicate_rate_value.config(
            text=(
                f"{metrics['duplicate_prevention_rate']}%"
            )
        )

        self.validation_failures_value.config(
            text=str(
                metrics[
                    "validation_failures"
                ]
            )
        )

        self.slot_conflicts_value.config(
            text=str(
                metrics[
                    "slot_conflicts"
                ]
            )
        )

        self.vehicle_exits_value.config(
            text=str(
                metrics[
                    "vehicle_exits"
                ]
            )
        )

        self.success_rate_value.config(
            text=(
                f"{metrics['entry_success_rate']}%"
            )
        )

        self.quality_status_value.config(
            text=metrics[
                "data_quality_status"
            ]
        )

        self.load_recent_events()

    # ==========================================
    # RECENT EVENTS
    # ==========================================

    def load_recent_events(
        self
    ):

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