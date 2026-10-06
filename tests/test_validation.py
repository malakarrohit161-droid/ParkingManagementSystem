import unittest

from services.validation import normalize_vehicle_number


class TestVehicleNumberNormalization(unittest.TestCase):

    # ==========================================
    # LOWERCASE TO UPPERCASE
    # ==========================================

    def test_lowercase_to_uppercase(self):

        result = normalize_vehicle_number(
            "uk04ab1234"
        )

        self.assertEqual(
            result,
            "UK04AB1234"
        )

    # ==========================================
    # REMOVE SPACES
    # ==========================================

    def test_remove_spaces(self):

        result = normalize_vehicle_number(
            "UK04 AB 1234"
        )

        self.assertEqual(
            result,
            "UK04AB1234"
        )

    # ==========================================
    # REMOVE HYPHENS
    # ==========================================

    def test_remove_hyphens(self):

        result = normalize_vehicle_number(
            "UK04-AB-1234"
        )

        self.assertEqual(
            result,
            "UK04AB1234"
        )

    # ==========================================
    # REMOVE LEADING_TRAILING SPACES
    # ==========================================

    def test_leading_trailing_spaces(self):

        result = normalize_vehicle_number(
            "   UK04AB1234   "
        )

        self.assertEqual(
            result,
            "UK04AB1234"
        )

    # ==========================================
    # MIXED FORMAT
    # ==========================================

    def test_mixed_format(self):

        result = normalize_vehicle_number(
            "  uk04-ab 1234  "
        )

        self.assertEqual(
            result,
            "UK04AB1234"
        )

    # ==========================================
    # ALREADY STANDARDIZED
    # ==========================================

    def test_already_standardized(self):

        result = normalize_vehicle_number(
            "UK04AB1234"
        )

        self.assertEqual(
            result,
            "UK04AB1234"
        )

    # ==========================================
    # EMPTY VALUE
    # ==========================================

    def test_empty_value(self):

        result = normalize_vehicle_number(
            ""
        )

        self.assertEqual(
            result,
            ""
        )


if __name__ == "__main__":
    unittest.main()