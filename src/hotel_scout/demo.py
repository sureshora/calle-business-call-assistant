from .models import HotelCandidate, HotelSearchRequest
from .workflow import create_hotel_scout_plan, render_plan


def main() -> None:
    request = HotelSearchRequest(
        location="Chennai, Tamil Nadu",
        check_in="2026-09-20",
        check_out="2026-09-22",
        guests=2,
        rooms=1,
        budget_per_night=5000,
        currency="INR",
        required_facilities=["Wi-Fi", "Breakfast", "Parking"],
        preferences=["Good public rating", "Flexible cancellation", "Near city centre"],
    )

    candidates = [
        HotelCandidate(
            name="Candidate Hotel One",
            location="Chennai",
            phone_number="+91XXXXXXXXXX",
            website="https://example.com/hotel-one",
            public_rating=4.2,
            review_count=1250,
        ),
        HotelCandidate(
            name="Candidate Hotel Two",
            location="Chennai",
            phone_number="+91XXXXXXXXXX",
            website="https://example.com/hotel-two",
            public_rating=4.5,
            review_count=980,
        ),
        HotelCandidate(
            name="Candidate Hotel Three",
            location="Chennai",
            phone_number="+91XXXXXXXXXX",
            website="https://example.com/hotel-three",
            public_rating=4.0,
            review_count=2100,
        ),
    ]

    plan = create_hotel_scout_plan(request, candidates)
    print(render_plan(plan))


if __name__ == "__main__":
    main()
