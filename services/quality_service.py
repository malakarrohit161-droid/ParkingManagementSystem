from datetime import datetime

from database.db import get_connection


# ==========================================
# QUALITY EVENT TYPES
# ==========================================

VEHICLE_ADDED = "VEHICLE_ADDED"

VEHICLE_EXITED = "VEHICLE_EXITED"

DUPLICATE_ATTEMPT = "DUPLICATE_ATTEMPT"

VALIDATION_FAILED = "VALIDATION_FAILED"

SLOT_CONFLICT = "SLOT_CONFLICT"


# ==========================================
# LOG QUALITY EVENT
# ==========================================

def log_quality_event(
    event_type,
    description
):

    """
    Store a quality-related event
    inside the quality_log table.

    Examples:

    VEHICLE_ADDED
    VEHICLE_EXITED
    DUPLICATE_ATTEMPT
    VALIDATION_FAILED
    SLOT_CONFLICT
    """

    connection = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        event_time = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        cursor.execute("""
            INSERT INTO quality_log
            (
                event_type,
                description,
                event_time
            )

            VALUES (?, ?, ?)
        """, (
            event_type,
            description,
            event_time
        ))

        connection.commit()

        return True

    except Exception as error:

        print(
            "Quality logging error:",
            error
        )

        return False

    finally:

        if connection:

            connection.close()


# ==========================================
# LOG VEHICLE ADDED
# ==========================================

def log_vehicle_added(
    parking_id,
    vehicle_number,
    slot_number
):

    description = (
        f"Vehicle {vehicle_number} "
        f"successfully added with "
        f"Parking ID {parking_id} "
        f"at slot {slot_number}."
    )

    return log_quality_event(
        VEHICLE_ADDED,
        description
    )


# ==========================================
# LOG VEHICLE EXITED
# ==========================================

def log_vehicle_exited(
    parking_id,
    vehicle_number,
    slot_number
):

    description = (
        f"Vehicle {vehicle_number} "
        f"successfully exited. "
        f"Parking ID {parking_id}. "
        f"Slot {slot_number} released."
    )

    return log_quality_event(
        VEHICLE_EXITED,
        description
    )


# ==========================================
# LOG DUPLICATE ATTEMPT
# ==========================================

def log_duplicate_attempt(
    vehicle_number
):

    description = (
        f"Duplicate parking attempt "
        f"prevented for vehicle "
        f"{vehicle_number}."
    )

    return log_quality_event(
        DUPLICATE_ATTEMPT,
        description
    )


# ==========================================
# LOG VALIDATION FAILURE
# ==========================================

def log_validation_failure(
    description
):

    return log_quality_event(
        VALIDATION_FAILED,
        description
    )


# ==========================================
# LOG SLOT CONFLICT
# ==========================================

def log_slot_conflict(
    slot_number,
    description=None
):

    if description is None:

        description = (
            f"Parking slot conflict "
            f"detected for slot "
            f"{slot_number}."
        )

    return log_quality_event(
        SLOT_CONFLICT,
        description
    )


# ==========================================
# GET EVENT COUNT
# ==========================================

def get_event_count(
    event_type
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)

        FROM quality_log

        WHERE event_type = ?
    """, (
        event_type,
    ))

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ==========================================
# GET TOTAL QUALITY EVENTS
# ==========================================

def get_total_quality_events():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM quality_log
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ==========================================
# GET RECENT QUALITY EVENTS
# ==========================================

def get_recent_quality_events(
    limit=20
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            event_type,
            description,
            event_time

        FROM quality_log

        ORDER BY id DESC

        LIMIT ?
    """, (
        limit,
    ))

    events = cursor.fetchall()

    connection.close()

    return events


# ==========================================
# GET ALL QUALITY COUNTS
# ==========================================

def get_quality_counts():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            event_type,
            COUNT(*)

        FROM quality_log

        GROUP BY event_type
    """)

    rows = cursor.fetchall()

    connection.close()

    counts = {
        VEHICLE_ADDED: 0,
        VEHICLE_EXITED: 0,
        DUPLICATE_ATTEMPT: 0,
        VALIDATION_FAILED: 0,
        SLOT_CONFLICT: 0
    }

    for event_type, count in rows:

        counts[event_type] = count

    return counts