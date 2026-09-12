\# CALL-E-009 — Hotel Call Result Normalization



\## Purpose



CALL-E-009 converts structured or partially structured CALL-E responses into

the common `HotelCallResult` model used by Hotel Scout.



\## Supported fields



The normalizer handles:



\- Call status.

\- Availability.

\- Room type.

\- Price per night.

\- Total price.

\- Currency.

\- Tax inclusion.

\- Breakfast inclusion.

\- Breakfast cost.

\- Requested facilities.

\- Cancellation policy.

\- Additional charges.

\- Public rating.

\- Review count.

\- Evidence.



\## Example



```python

raw\_result = {

&#x20;   "status": "completed",

&#x20;   "availability": "Available",

&#x20;   "room\_type": "Deluxe Room",

&#x20;   "price\_per\_night": "₹4,500",

&#x20;   "total\_price": "₹9,000",

&#x20;   "currency": "INR",

&#x20;   "taxes\_included": "yes",

&#x20;   "breakfast\_included": "no",

&#x20;   "facilities": "Wi-Fi, Parking, Pool",

&#x20;   "rating": "4.3",

&#x20;   "review\_count": "1,245",

}



result = normalize\_hotel\_call\_result(

&#x20;   "Example Hotel",

&#x20;   raw\_result,

)

