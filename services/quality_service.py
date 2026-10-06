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


# ==========================================
# ACTUAL ACTIVE DUPLICATE VEHICLES
# ==========================================

def get_actual_duplicate_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM
        (
            SELECT vehicle_number
            FROM parking_records
            WHERE status = 'Parked'
            GROUP BY vehicle_number
            HAVING COUNT(*) > 1
        )
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ==========================================
# DUPLICATE PREVENTION RATE
# ==========================================

def get_duplicate_prevention_rate():

    duplicate_attempts = (
        get_event_count(
            DUPLICATE_ATTEMPT
        )
    )

    actual_duplicates = (
        get_actual_duplicate_count()
    )

    if duplicate_attempts == 0:

        if actual_duplicates == 0:
            return 100.0

        return 0.0

    prevented = (
        duplicate_attempts
        - actual_duplicates
    )

    if prevented < 0:
        prevented = 0

    rate = (
        prevented
        / duplicate_attempts
    ) * 100

    return round(
        rate,
        2
    )


# ==========================================
# ENTRY SUCCESS RATE
# ==========================================

def get_entry_success_rate():

    successful_entries = (
        get_event_count(
            VEHICLE_ADDED
        )
    )

    duplicate_attempts = (
        get_event_count(
            DUPLICATE_ATTEMPT
        )
    )

    validation_failures = (
        get_event_count(
            VALIDATION_FAILED
        )
    )

    slot_conflicts = (
        get_event_count(
            SLOT_CONFLICT
        )
    )

    total_attempts = (
        successful_entries
        + duplicate_attempts
        + validation_failures
        + slot_conflicts
    )

    if total_attempts == 0:
        return 0.0

    rate = (
        successful_entries
        / total_attempts
    ) * 100

    return round(
        rate,
        2
    )


# ==========================================
# DATA QUALITY STATUS
# ==========================================

def get_data_quality_status():

    actual_duplicates = (
        get_actual_duplicate_count()
    )

    if actual_duplicates == 0:

        return "PASS"

    return "ATTENTION REQUIRED"


# ==========================================
# COMPLETE QUALITY METRICS
# ==========================================

def get_quality_metrics():

    counts = get_quality_counts()

    return {

        "successful_entries":
            counts.get(
                VEHICLE_ADDED,
                0
            ),

        "vehicle_exits":
            counts.get(
                VEHICLE_EXITED,
                0
            ),

        "duplicate_attempts":
            counts.get(
                DUPLICATE_ATTEMPT,
                0
            ),

        "validation_failures":
            counts.get(
                VALIDATION_FAILED,
                0
            ),

        "slot_conflicts":
            counts.get(
                SLOT_CONFLICT,
                0
            ),

        "actual_duplicates":
            get_actual_duplicate_count(),

        "duplicate_prevention_rate":
            get_duplicate_prevention_rate(),

        "entry_success_rate":
            get_entry_success_rate(),

        "data_quality_status":
            get_data_quality_status()
    }