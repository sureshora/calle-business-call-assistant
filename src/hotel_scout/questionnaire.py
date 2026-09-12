from typing import List

from .models import HotelCandidate, HotelSearchRequest, HotelCallPreview


STANDARD_HOTEL_QUESTIONS: List[str] = [
    "Do you have availability for the requested dates and number of guests?",
    "Which room categories are available?",
    "What is the price per night for the suitable room?",
    "What is the total price for the complete stay?",
    "Are taxes and mandatory fees included in the quoted price?",
    "Is breakfast included? If not, what is the breakfast cost per person?",
    "Do you provide the requested facilities and services?",
    "What is the cancellation and modification policy?",
    "Are there any deposits, resort fees, service charges, or other mandatory costs?",
    "What are the check-in and check-out times and requirements?",
    "Can you provide the official website or direct booking link?",
]

EXPECTED_INFORMATION: List[str] = [
    "Availability confirmation",
    "Available room category",
    "Price per night",
    "Total stay price",
    "Tax and fee treatment",
    "Breakfast inclusion and cost",
    "Facilities confirmation",
    "Cancellation policy",
    "Additional charges or deposit",
    "Check-in and check-out information",
    "Official contact or booking link",
]


def build_call_purpose(request: HotelSearchRequest, hotel: HotelCandidate) -> str:
    return (
        f"Verify live accommodation availability and pricing at {hotel.name} "
        f"for {request.guests} guest(s), {request.rooms} room(s), "
        f"from {request.check_in} to {request.check_out}. "
        "Do not make a reservation or collect payment."
    )


def build_hotel_call_preview(request: HotelSearchRequest, hotel: HotelCandidate) -> HotelCallPreview:
    return HotelCallPreview(
        hotel_name=hotel.name,
        phone_number=hotel.phone_number,
        purpose=build_call_purpose(request, hotel),
        questions=list(STANDARD_HOTEL_QUESTIONS),
        expected_information=list(EXPECTED_INFORMATION),
    )
