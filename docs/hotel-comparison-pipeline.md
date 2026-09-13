\# CALL-E-010 — Hotel Comparison Pipeline



\## Purpose



CALL-E-010 converts normalized hotel call results into a recommendation-ready comparison.



The pipeline does not place calls. It operates only on normalized `HotelCallResult` objects.



\## Pipeline



```text

Normalized hotel results

&#x20;       ↓

Input and currency validation

&#x20;       ↓

Duplicate hotel detection

&#x20;       ↓

Ranking using configured weights

&#x20;       ↓

Recommendation-ready comparison object

&#x20;       ↓

Human-readable report

