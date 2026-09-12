\# CALL-E-008 — Hotel Call Execution Adapter



\## Purpose



CALL-E-008 connects the Hotel Scout domain workflow to the existing CALL-E

runtime boundary.



The adapter supports:



\- Dry-run previews.

\- Standardized hotel call goals.

\- Explicit approval checks.

\- Runtime configuration checks.

\- Controlled execution through the CALL-E CLI boundary.

\- No booking or payment actions.



\## Default behavior



The default mode is dry-run:



```python

request = HotelCallExecutionRequest(

&#x20;   preview=hotel\_call\_preview,

&#x20;   live\_call=False,

)

