# Standardized Hotel Call Questionnaire

The same questions must be used for each candidate hotel so that results are comparable.

## Opening

> Hello. I am calling on behalf of a customer who is comparing hotel options. May I ask a few questions about availability and rates? This is an information inquiry only; no booking or payment will be made during this call.

## Questions

1. Do you have availability for **[guests]** from **[check-in date]** to **[check-out date]**?
2. What room categories are available for those dates?
3. What is the price per night for the requested room?
4. What is the total price for the complete stay?
5. Does that total include taxes and mandatory fees?
6. Is breakfast included? If not, what is the additional cost?
7. Are the requested facilities available, such as parking, Wi-Fi, air conditioning, or hot water?
8. What is the cancellation policy?
9. Are there any additional mandatory charges, deposits, or check-in requirements?
10. Can you provide a direct contact number or booking link for the customer to follow up?

## Closing

> Thank you. I am only collecting information and will not make a reservation during this call.

## Extraction rules

- Preserve the hotel's original currency and amount.
- Store nightly price and complete-stay price separately.
- Never compare tax-inclusive and tax-exclusive prices as if they were equivalent.
- Record whether each answer was confirmed, unclear, unavailable, or not asked.
- If the hotel offers multiple rooms, retain the room category associated with each price.
- Do not infer facilities from silence.
- A verbal quote is an inquiry result, not a booking confirmation.