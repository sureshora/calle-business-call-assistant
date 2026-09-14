"""CALL-E-012 interactive Streamlit UI for CALL-E Hotel Scout.

Run from the repository root:
    streamlit run src/hotel_scout/streamlit_app.py

The UI defaults to a deterministic dry-run. Live CALL-E execution is deliberately
kept behind an explicit approval gate and is not enabled by default.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import streamlit as st

# Make the src-layout package importable when Streamlit launches this file directly.
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hotel_scout.approval import CallApproval
from hotel_scout.models import HotelCandidate, HotelSearchRequest
from hotel_scout.orchestrator import (
    build_orchestration_plan,
    execute_orchestration,
    render_call_preview,
)


st.set_page_config(
    page_title="CALL-E Hotel Scout",
    page_icon="☎️",
    layout="wide",
)

st.title("☎️ CALL-E Hotel Scout")
st.caption("Live hotel comparison through a safe, inspectable phone-call workflow")

with st.sidebar:
    st.header("Execution settings")
    mode = st.radio(
        "Mode",
        ["Demo dry-run", "Live CALL-E"],
        index=0,
        help="Dry-run is deterministic and never contacts a hotel.",
    )
    st.warning(
        "Live mode can create real-world side effects. Use only authorized numbers "
        "and approve the exact preview before calling."
    )

    st.header("Safety boundary")
    st.markdown(
        "- No reservation or booking\n"
        "- No payment collection\n"
        "- No OTPs or passwords\n"
        "- No unsupported availability claims\n"
        "- Missing values remain unavailable"
    )

st.subheader("1. Search requirements")
left, right = st.columns(2)
with left:
    location = st.text_input("Location", "Chennai")
    check_in = st.date_input("Check-in")
    check_out = st.date_input("Check-out")
    guests = st.number_input("Guests", min_value=1, value=2, step=1)
    rooms = st.number_input("Rooms", min_value=1, value=1, step=1)
with right:
    budget = st.number_input(
        "Budget per night (INR)", min_value=0.0, value=5000.0, step=500.0
    )
    facilities_text = st.text_input(
        "Required facilities", "Wi-Fi, breakfast, parking"
    )
    preferences_text = st.text_area(
        "Preferences", "Good value, flexible cancellation, family-friendly"
    )

st.subheader("2. Hotel candidates")
st.caption("Enter up to three hotels. Phone numbers are required for a live call.")

candidate_columns = st.columns(3)
candidate_inputs: list[dict[str, Any]] = []
for index, column in enumerate(candidate_columns, start=1):
    with column:
        st.markdown(f"**Hotel {index}**")
        name = st.text_input("Hotel name", f"Hotel {chr(64 + index)}", key=f"name_{index}")
        hotel_location = st.text_input(
            "Hotel location", location, key=f"location_{index}"
        )
        phone = st.text_input(
            "Phone number",
            f"+91000000000{index}",
            key=f"phone_{index}",
            help="Use international format, for example +919876543210.",
        )
        rating = st.number_input(
            "Public rating",
            min_value=0.0,
            max_value=5.0,
            value=float(4.0 - (index - 1) * 0.2),
            step=0.1,
            key=f"rating_{index}",
        )
        candidate_inputs.append(
            {
                "name": name,
                "location": hotel_location,
                "phone_number": phone,
                "public_rating": rating,
            }
        )

request = HotelSearchRequest(
    location=location,
    check_in=check_in.isoformat(),
    check_out=check_out.isoformat(),
    guests=int(guests),
    rooms=int(rooms),
    budget_per_night=budget if budget > 0 else None,
    required_facilities=[item.strip() for item in facilities_text.split(",") if item.strip()],
    preferences=[line.strip() for line in preferences_text.splitlines() if line.strip()],
)

candidates = [HotelCandidate(**candidate) for candidate in candidate_inputs]

if "plan" not in st.session_state:
    st.session_state.plan = None
if "result" not in st.session_state:
    st.session_state.result = None

if st.button("Generate call preview", type="primary", use_container_width=True):
    try:
        st.session_state.plan = build_orchestration_plan(request, candidates)
        st.session_state.result = None
        st.success("Call plan generated. Review it before execution.")
    except Exception as exc:  # Streamlit should show user-friendly validation errors.
        st.error(str(exc))

plan = st.session_state.plan
if plan is not None:
    st.subheader("3. CALL-E call preview")
    st.info("No live call has been made. Review every recipient, question, and safety limit.")
    st.code(render_call_preview(plan), language="text")

    st.subheader("4. Approval and execution")
    approved = st.checkbox(
        "I reviewed the hotel names, phone numbers, questions, and safety restrictions.",
        value=False,
    )
    approver = st.text_input("Approver name or email", "", disabled=not approved)
    approval_note = st.text_area(
        "Approval note",
        "Approved after reviewing the generated call preview.",
        disabled=not approved,
    )

    if mode == "Demo dry-run":
        st.success("Demo dry-run selected: no phone number will be contacted.")
    else:
        st.error("Live CALL-E mode selected. Explicit approval is mandatory.")

    if st.button("Execute Hotel Scout", use_container_width=True):
        if not approved:
            st.error("Execution blocked: explicit approval is required.")
        elif not approver.strip():
            st.error("Execution blocked: enter the approving user.")
        else:
            approval = CallApproval(
                approved=True,
                approved_by=approver.strip(),
                approval_note=approval_note.strip(),
            )
            try:
                # The demo mode uses deterministic simulated responses. This makes
                # the UI repeatable for judging and video recording.
                if mode == "Demo dry-run":
                    def demo_provider(preview):
                        index = next(
                            i for i, item in enumerate(plan.previews)
                            if item.hotel_name == preview.hotel_name
                        )
                        samples = [
                            {
                                "status": "completed",
                                "availability": "available",
                                "room_type": "Deluxe Room",
                                "price_per_night": 4200,
                                "total_price": 8400,
                                "currency": "INR",
                                "taxes_included": False,
                                "breakfast_included": True,
                                "requested_facilities": ["Wi-Fi", "breakfast", "parking"],
                                "cancellation_policy": "Free cancellation up to 24 hours before check-in.",
                                "additional_charges": "GST extra.",
                                "evidence": ["Simulated demo response for Hotel A."],
                            },
                            {
                                "status": "completed",
                                "availability": "available",
                                "room_type": "Superior Room",
                                "price_per_night": 5100,
                                "total_price": 10200,
                                "currency": "INR",
                                "taxes_included": True,
                                "breakfast_included": False,
                                "breakfast_cost": 450,
                                "requested_facilities": ["Wi-Fi", "parking"],
                                "cancellation_policy": "Free cancellation up to 48 hours before check-in.",
                                "additional_charges": "No mandatory additional charges reported.",
                                "evidence": ["Simulated demo response for Hotel B."],
                            },
                            {
                                "status": "completed",
                                "availability": "not confirmed",
                                "room_type": None,
                                "price_per_night": None,
                                "total_price": None,
                                "currency": "INR",
                                "taxes_included": None,
                                "breakfast_included": None,
                                "requested_facilities": [],
                                "cancellation_policy": None,
                                "additional_charges": None,
                                "evidence": ["Simulated response with unavailable values for Hotel C."],
                            },
                        ]
                        return samples[index]

                    result = execute_orchestration(
                        plan,
                        approval=approval,
                        live_call=False,
                        raw_result_provider=demo_provider,
                    )
                else:
                    st.warning(
                        "Live execution requires a configured CALL-E runtime. "
                        "The UI will use the existing runtime boundary."
                    )
                    result = execute_orchestration(
                        plan,
                        approval=approval,
                        live_call=True,
                    )
                st.session_state.result = result
                st.success("Hotel Scout execution completed.")
            except Exception as exc:
                st.error(f"Execution failed: {exc}")

result = st.session_state.result
if result is not None:
    st.subheader("5. Comparison and recommendation")
    st.metric("Recommended hotel", result.recommended_hotel or "Not available")
    st.text(result.report)

    with st.expander("Normalized result details"):
        for item in result.results:
            st.markdown(f"**{item.hotel_name}**")
            st.json({
                "availability": item.availability,
                "room_type": item.room_type,
                "price_per_night": item.price_per_night,
                "total_price": item.total_price,
                "currency": item.currency,
                "taxes_included": item.taxes_included,
                "breakfast_included": item.breakfast_included,
                "breakfast_cost": item.breakfast_cost,
                "requested_facilities": item.requested_facilities,
                "cancellation_policy": item.cancellation_policy,
                "additional_charges": item.additional_charges,
                "status": item.status,
                "evidence": item.evidence,
            })

    with st.expander("Machine-readable comparison"):
        st.code(json.dumps(result.comparison.__dict__, default=str, indent=2), language="json")

st.divider()
st.caption(
    "CALL-E Hotel Scout is a comparison assistant. It does not book rooms, collect payments, "
    "or make binding commitments."
)
