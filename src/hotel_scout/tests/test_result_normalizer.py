import unittest

from src.hotel_scout.result_normalizer import (
    normalize_hotel_call_result,
)


class HotelResultNormalizerTests(unittest.TestCase):
    def test_normalizes_structured_result(self):
        raw = {
            "status": "completed",
            "availability": "Available",
            "room_type": "Deluxe Room",
            "price_per_night": "₹4,500",
            "total_price": "₹9,000",
            "currency": "INR",
            "taxes_included": "yes",
            "breakfast_included": "No",
            "breakfast_cost": "₹500",
            "facilities": "Wi-Fi, Parking, Pool",
            "cancellation_policy": "Free cancellation until 24 hours before check-in",
            "additional_charges": "No mandatory charges",
            "rating": "4.3",
            "review_count": "1,245",
        }

        result = normalize_hotel_call_result(
            "Example Hotel",
            raw,
            evidence=["Hotel representative confirmed the price."],
        )

        self.assertEqual(result.hotel_name, "Example Hotel")
        self.assertEqual(result.availability, "Available")
        self.assertEqual(result.room_type, "Deluxe Room")
        self.assertEqual(result.price_per_night, 4500.0)
        self.assertEqual(result.total_price, 9000.0)
        self.assertEqual(result.currency, "INR")
        self.assertTrue(result.taxes_included)
        self.assertFalse(result.breakfast_included)
        self.assertEqual(result.breakfast_cost, 500.0)
        self.assertEqual(
            result.requested_facilities,
            ["Wi-Fi", "Parking", "Pool"],
        )
        self.assertEqual(result.public_rating, 4.3)
        self.assertEqual(result.review_count, 1245)
        self.assertEqual(
            result.evidence,
            ["Hotel representative confirmed the price."],
        )

    def test_missing_values_are_not_invented(self):
        result = normalize_hotel_call_result(
            "Incomplete Hotel",
            {
                "status": "completed",
                "availability": "Unknown",
            },
        )

        self.assertEqual(result.hotel_name, "Incomplete Hotel")
        self.assertEqual(result.availability, "Unknown")
        self.assertIsNone(result.price_per_night)
        self.assertIsNone(result.total_price)
        self.assertIsNone(result.public_rating)
        self.assertIsNone(result.review_count)
        self.assertEqual(result.requested_facilities, [])

    def test_list_facilities_are_preserved(self):
        result = normalize_hotel_call_result(
            "List Hotel",
            {
                "facilities": ["Wi-Fi", "Breakfast", "Parking"],
            },
        )

        self.assertEqual(
            result.requested_facilities,
            ["Wi-Fi", "Breakfast", "Parking"],
        )

    def test_custom_evidence_overrides_raw_evidence(self):
        result = normalize_hotel_call_result(
            "Evidence Hotel",
            {
                "evidence": ["Raw evidence"],
            },
            evidence=["Verified evidence"],
        )

        self.assertEqual(result.evidence, ["Verified evidence"])


if __name__ == "__main__":
    unittest.main()