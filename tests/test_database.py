import sqlite3
import unittest


class TestDatabaseIntegrity(unittest.TestCase):

    def setUp(self):

        # Temporary in-memory database.
        # Real parking.db is NOT affected.
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("PRAGMA foreign_keys = ON")

        self.cursor = self.connection.cursor()

        # ------------------------------------------
        # Parking Slots
        # ------------------------------------------

        self.cursor.execute("""
            CREATE TABLE parking_slots (
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

        # ------------------------------------------
        # Parking Records
        # ------------------------------------------

        self.cursor.execute("""
            CREATE TABLE parking_records (
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

                FOREIGN KEY (slot_number)
                    REFERENCES parking_slots(slot_number)
            )
        """)

        # ------------------------------------------
        # Active Vehicle Unique Constraint
        # ------------------------------------------

        self.cursor.execute("""
            CREATE UNIQUE INDEX
            idx_unique_active_vehicle

            ON parking_records(vehicle_number)

            WHERE status = 'Parked'
        """)

        # ------------------------------------------
        # Test Slots
        # ------------------------------------------

        self.cursor.execute("""
            INSERT INTO parking_slots
            (
                slot_number,
                slot_type,
                status
            )
            VALUES
            (
                'A01',
                'Car',
                'Available'
            )
        """)

        self.cursor.execute("""
            INSERT INTO parking_slots
            (
                slot_number,
                slot_type,
                status
            )
            VALUES
            (
                'A02',
                'Car',
                'Available'
            )
        """)

        self.connection.commit()

    def tearDown(self):

        self.connection.close()

    # ==========================================
    # HELPER
    # ==========================================

    def insert_record(
        self,
        parking_id,
        vehicle_number,
        slot_number,
        status="Parked"
    ):

        self.cursor.execute("""
            INSERT INTO parking_records
            (
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            parking_id,
            vehicle_number,
            "Test User",
            "9876543210",
            "Car",
            slot_number,
            "2026-10-06 10:00:00",
            None,
            status
        ))

    # ==========================================
    # TEST 1
    # NORMAL VEHICLE ENTRY
    # ==========================================

    def test_valid_vehicle_entry(self):

        self.insert_record(
            "P001",
            "UK04AB1234",
            "A01"
        )

        self.connection.commit()

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM parking_records
        """)

        count = self.cursor.fetchone()[0]

        self.assertEqual(
            count,
            1
        )

    # ==========================================
    # TEST 2
    # DUPLICATE PARKING ID
    # ==========================================

    def test_duplicate_parking_id_rejected(self):

        self.insert_record(
            "P001",
            "UK04AB1234",
            "A01"
        )

        with self.assertRaises(
            sqlite3.IntegrityError
        ):

            self.insert_record(
                "P001",
                "UK04CD5678",
                "A02"
            )

    # ==========================================
    # TEST 3
    # DUPLICATE ACTIVE VEHICLE
    # ==========================================

    def test_duplicate_active_vehicle_rejected(self):

        self.insert_record(
            "P001",
            "UK04AB1234",
            "A01",
            "Parked"
        )

        with self.assertRaises(
            sqlite3.IntegrityError
        ):

            self.insert_record(
                "P002",
                "UK04AB1234",
                "A02",
                "Parked"
            )

    # ==========================================
    # TEST 4
    # SAME VEHICLE AFTER EXIT
    # ==========================================

    def test_same_vehicle_allowed_after_exit(self):

        self.insert_record(
            "P001",
            "UK04AB1234",
            "A01",
            "Exited"
        )

        self.insert_record(
            "P002",
            "UK04AB1234",
            "A02",
            "Parked"
        )

        self.connection.commit()

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM parking_records
            WHERE vehicle_number = ?
        """, (
            "UK04AB1234",
        ))

        count = self.cursor.fetchone()[0]

        self.assertEqual(
            count,
            2
        )

    # ==========================================
    # TEST 5
    # INVALID STATUS
    # ==========================================

    def test_invalid_parking_status_rejected(self):

        with self.assertRaises(
            sqlite3.IntegrityError
        ):

            self.insert_record(
                "P001",
                "UK04AB1234",
                "A01",
                "InvalidStatus"
            )

    # ==========================================
    # TEST 6
    # INVALID SLOT FOREIGN KEY
    # ==========================================

    def test_invalid_slot_rejected(self):

        with self.assertRaises(
            sqlite3.IntegrityError
        ):

            self.insert_record(
                "P001",
                "UK04AB1234",
                "Z99",
                "Parked"
            )


if __name__ == "__main__":
    unittest.main()