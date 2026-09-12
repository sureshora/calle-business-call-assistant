from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class HotelSearchRequest:
    location: str
    check_in: str
    check_out: str
    guests: int = 1
    rooms: int = 1
    budget_per_night: Optional[float] = None
    currency: str = "INR"
    required_facilities: List[str] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.location.strip(): errors.append("Location is required.")
        if not self.check_in.strip(): errors.append("Check-in date is required.")
        if not self.check_out.strip(): errors.append("Check-out date is required.")
        if self.guests < 1: errors.append("Guests must be at least 1.")
        if self.rooms < 1: errors.append("Rooms must be at least 1.")
        if self.budget_per_night is not None and self.budget_per_night <= 0:
            errors.append("Budget per night must be greater than zero.")
        return errors


@dataclass
class HotelCandidate:
    name: str
    location: str
    phone_number: Optional[str] = None
    website: Optional[str] = None
    public_rating: Optional[float] = None
    review_count: Optional[int] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class HotelCallPreview:
    hotel_name: str
    phone_number: Optional[str]
    purpose: str
    questions: List[str]
    expected_information: List[str]
    approval_required: bool = True
    live_call_enabled: bool = False


@dataclass
class HotelCallResult:
    hotel_name: str
    availability: Optional[str] = None
    room_type: Optional[str] = None
    price_per_night: Optional[float] = None
    total_price: Optional[float] = None
    currency: str = "INR"
    taxes_included: Optional[bool] = None
    breakfast_included: Optional[bool] = None
    breakfast_cost: Optional[float] = None
    requested_facilities: List[str] = field(default_factory=list)
    cancellation_policy: Optional[str] = None
    additional_charges: Optional[str] = None
    public_rating: Optional[float] = None
    review_count: Optional[int] = None
    evidence: List[str] = field(default_factory=list)
    status: str = "not_called"


@dataclass
class RankedHotel:
    hotel_name: str
    total_score: float
    value_score: float
    availability_score: float
    rating_score: float
    facilities_score: float
    explanation: str


@dataclass
class HotelScoutPlan:
    request: HotelSearchRequest
    candidates: List[HotelCandidate]
    call_previews: List[HotelCallPreview]
    ranking_weights: dict
    live_calls_allowed: bool = False
