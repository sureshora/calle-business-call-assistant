import unittest

from src.hotel_scout.comparison import compare_hotel_results
from src.hotel_scout.models import HotelCallResult, HotelSearchRequest


def make_request() -> HotelSearchRequest:
    return HotelSearchRequest(
        location="Chennai",
        check_in="2026-09-20",
        check_out="2026-09-22",
        guests=2,
        rooms=1,
        currency="INR",
        required_facilities=["Wi-Fi", "Breakfast"],
    )


def make_result(
    name: str,
    *,
    price: float = 4000,
    currency: str = "INR",
) -> HotelCallResult:
    return HotelCallResult(
        hotel_name=name,
        availability="Available",
        price_per_night=price,
        currency=currency,
        requested_facilities=["Wi-Fi", "Breakfast"],
        public_rating=4.0,
        status="completed",
    )


class ComparisonTests(unittest.TestCase):
    def test_results_are_ranked(self):
        comparison = compare_hotel_results(
            make_request(),
            [
                make_result("Hotel A", price=5000),
                make_result("Hotel B", price=4000),
            ],
        )

        self.assertEqual(comparison.recommended_hotel, "Hotel B")
        self.assertEqual(len(comparison.rankings), 2)

    def test_duplicate_hotels_are_rejected(self):
        with self.assertRaises(ValueError):
            compare_hotel_results(
                make_request(),
                [
                    make_result("Hotel A"),
                    make_result("hotel a"),
                ],
            )

    def test_empty_results_are_rejected(self):
        with self.assertRaises(ValueError):
            compare_hotel_results(make_request(), [])

    def test_more_than_three_results_are_rejected(self):
        results = [
            make_result("Hotel A"),
            make_result("Hotel B"),
            make_result("Hotel C"),
            make_result("Hotel D"),
        ]

        with self.assertRaises(ValueError):
            compare_hotel_results(make_request(), results)

    def test_mixed_currencies_are_rejected(self):
        with self.assertRaises(ValueError):
            compare_hotel_results(
                make_request(),
                [
                    make_result("Hotel A", currency="INR"),
                    make_result("Hotel B", currency="USD"),
                ],
            )

    def test_weights_must_sum_to_one(self):
        with self.assertRaises(ValueError):
            compare_hotel_results(
                make_request(),
                [make_result("Hotel A")],
                weights={
                    "value": 0.50,
                    "availability": 0.30,
                    "rating": 0.20,
                    "facilities": 0.20,
                },
            )

    def test_missing_values_do_not_crash_comparison(self):
        result = HotelCallResult(
            hotel_name="Hotel A",
            currency="INR",
            status="completed",
        )

        comparison = compare_hotel_results(make_request(), [result])

        self.assertEqual(comparison.recommended_hotel, "Hotel A")
        self.assertEqual(comparison.rankings[0].total_score, 10.0)


if __name__ == "__main__":
    unittest.main()