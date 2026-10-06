import csv
from datetime import datetime

from services.quality_service import (
    get_quality_metrics,
    get_recent_quality_events
)


def export_quality_report(file_path):

    """
    Export TQM quality metrics and
    quality event history to a CSV file.
    """

    metrics = get_quality_metrics()

    # Get a large number of events so the
    # exported report contains the history.
    events = get_recent_quality_events(
        10000
    )

    generated_time = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    try:

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # ==================================
            # REPORT HEADER
            # ==================================

            writer.writerow([
                "TQM PARKING MANAGEMENT SYSTEM"
            ])

            writer.writerow([
                "QUALITY PERFORMANCE REPORT"
            ])

            writer.writerow([
                "Generated On",
                generated_time
            ])

            writer.writerow([])

            # ==================================
            # QUALITY METRICS
            # ==================================

            writer.writerow([
                "QUALITY PERFORMANCE METRICS"
            ])

            writer.writerow([
                "Metric",
                "Value"
            ])

            writer.writerow([
                "Successful Entries",
                metrics["successful_entries"]
            ])

            writer.writerow([
                "Vehicle Exits",
                metrics["vehicle_exits"]
            ])

            writer.writerow([
                "Duplicate Attempts Prevented",
                metrics["duplicate_attempts"]
            ])

            writer.writerow([
                "Validation Failures",
                metrics["validation_failures"]
            ])

            writer.writerow([
                "Slot Conflicts",
                metrics["slot_conflicts"]
            ])

            writer.writerow([
                "Actual Active Duplicates",
                metrics["actual_duplicates"]
            ])

            writer.writerow([
                "Duplicate Prevention Rate",
                (
                    f"{metrics['duplicate_prevention_rate']}%"
                )
            ])

            writer.writerow([
                "Entry Success Rate",
                (
                    f"{metrics['entry_success_rate']}%"
                )
            ])

            writer.writerow([
                "Data Quality Status",
                metrics["data_quality_status"]
            ])

            writer.writerow([])

            # ==================================
            # QUALITY TARGET
            # ==================================

            writer.writerow([
                "QUALITY TARGET"
            ])

            writer.writerow([
                "Target",
                "Actual Result"
            ])

            writer.writerow([
                "Active Duplicate Vehicles = 0",
                metrics["actual_duplicates"]
            ])

            writer.writerow([])

            # ==================================
            # QUALITY EVENT HISTORY
            # ==================================

            writer.writerow([
                "QUALITY EVENT HISTORY"
            ])

            writer.writerow([
                "Event Type",
                "Description",
                "Date & Time"
            ])

            for event in events:

                writer.writerow([
                    event[0],
                    event[1],
                    event[2]
                ])

        return (
            True,
            "Quality report exported successfully."
        )

    except OSError as error:

        return (
            False,
            f"Could not export report: {error}"
        )