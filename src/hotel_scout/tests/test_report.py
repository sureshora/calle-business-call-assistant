import unittest

from src.hotel_scout.comparison import compare_hotel_results
from src.hotel_scout.models import HotelCallResult, HotelSearchRequest
from src.hotel_scout.report import (
    render_compact_result,
    render_hotel_comparison,
)


class ReportTests(unittest.TestCase):
    def setUp(self):
        request = HotelSearchRequest(
            location="Chennai",
            check_in="2026-09-20",
            check_out="2026-09-22",
            guests=2,
            rooms=1,
            currency="INR",
            required_facilities=["Wi-Fi"],
        )

        result = HotelCallResult(
            hotel_name="Hotel A",
            availability="Available",
            price_per_night=4200,
            total_price=8400,
            currency="INR",
            requested_facilities=["Wi-Fi"],
            public_rating=4.2,
            status="completed",
        )

        self.comparison = compare_hotel_results(request, [result])
        self.result = result

    def test_report_contains_request_and_recommendation(self):
        report = render_hotel_comparison(self.comparison)

        self.assertIn("SEARCH REQUEST", report)
        self.assertIn("Hotel A", report)
        self.assertIn("RECOMMENDATION", report)
        self.assertIn("Recommended hotel: Hotel A", report)

    def test_report_preserves_missing_values(self):
        report = render_hotel_comparison(self.comparison)

        self.assertIn("Taxes included: Not confirmed", report)
        self.assertIn("Breakfast included: Not confirmed", report)

    def test_compact_result_contains_core_fields(self):
        text = render_compact_result(self.result)

        self.assertIn("Hotel A", text)
        self.assertIn("Available", text)
        self.assertIn("4,200.00 INR", text)


if __name__ == "__main__":
    unittest.main()