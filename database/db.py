import sqlite3
import os


# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

DATABASE_PATH = os.path.join(
    DATA_DIR,
    "parking.db"
)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # ======================================
    # PARKING SLOTS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            slot_number TEXT
                UNIQUE
                NOT NULL,

            slot_type TEXT
                NOT NULL,

            status TEXT
                NOT NULL
                DEFAULT 'Available'
                CHECK(
                    status IN (
                        'Available',
                        'Occupied'
                    )
                )
        )
    """)

    # ======================================
    # PARKING RECORDS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            parking_id TEXT
                UNIQUE
                NOT NULL,

            vehicle_number TEXT
                NOT NULL,

            owner_name TEXT
                NOT NULL,

            phone TEXT
                NOT NULL,

            vehicle_type TEXT
                NOT NULL,

            slot_number TEXT
                NOT NULL,

            entry_time TEXT
                NOT NULL,

            exit_time TEXT,

            status TEXT
                NOT NULL
                DEFAULT 'Parked'
                CHECK(
                    status IN (
                        'Parked',
                        'Exited'
                    )
                ),

            FOREIGN KEY (
                slot_number
            )
            REFERENCES parking_slots(
                slot_number
            )
        )
    """)

    # ======================================
    # QUALITY LOG TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event_type TEXT
                NOT NULL,

            description TEXT
                NOT NULL,

            event_time TEXT
                NOT NULL
        )
    """)

    # ======================================
    # DATABASE-LEVEL DUPLICATE PREVENTION
    # ======================================
    #
    # A vehicle may appear multiple times in
    # parking history after exiting.
    #
    # But only ONE record for that vehicle
    # may have status = 'Parked'.
    #
    # Example allowed:
    #
    # UK04AB1234 -> Exited
    # UK04AB1234 -> Exited
    # UK04AB1234 -> Parked
    #
    # Example NOT allowed:
    #
    # UK04AB1234 -> Parked
    # UK04AB1234 -> Parked
    #
    # ======================================

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_unique_active_vehicle

        ON parking_records(
            vehicle_number
        )

        WHERE status = 'Parked'
    """)

    connection.commit()
    connection.close()

    print(
        "Database tables and quality "
        "constraints created successfully."
    )


# ==========================================
# INITIALIZE PARKING SLOTS
# ==========================================

def initialize_parking_slots():

    connection = get_connection()
    cursor = connection.cursor()

    # ======================================
    # CAR SLOTS
    # A01 - A20
    # ======================================

    for number in range(
        1,
        21
    ):

        slot_number = (
            f"A{number:02d}"
        )

        cursor.execute("""
            INSERT OR IGNORE
            INTO parking_slots
            (
                slot_number,
                slot_type,
                status
            )

            VALUES (?, ?, ?)
        """, (
            slot_number,
            "Car",
            "Available"
        ))

    # ======================================
    # BIKE SLOTS
    # B01 - B20
    # ======================================

    for number in range(
        1,
        21
    ):

        slot_number = (
            f"B{number:02d}"
        )

        cursor.execute("""
            INSERT OR IGNORE
            INTO parking_slots
            (
                slot_number,
                slot_type,
                status
            )

            VALUES (?, ?, ?)
        """, (
            slot_number,
            "Bike",
            "Available"
        ))

    connection.commit()
    connection.close()

    print(
        "Parking slots initialized "
        "successfully."
    )


# ==========================================
# DATABASE SETUP
# ==========================================

if __name__ == "__main__":

    create_tables()

    initialize_parking_slots()

    print(
        "Database setup completed "
        "successfully."
    )