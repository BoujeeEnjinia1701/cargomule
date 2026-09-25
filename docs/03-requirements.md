---
doc_id: CGM-REQ-001
title: CargoMule requirements
project: CargoMule
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
---

# CargoMule requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3. Status is judged against the first-order estimates in CGM-PRC-001; **four requirements are not met or at risk** (R7, R8, R12 and the thermal part of R3).

The **design load case** is 150 kg of payload centered on the deck, a trailer of about 38 kg (estimate) and a towing bicycle with rider of about 100 kg, on a dry paved road. The **design route** is a 10 km round trip with 120 m of total climbing and 20 stops.

Table 1. Requirements, targets and concept status.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Carry the payload | 150 kg (330 lb) on a deck of at least 0.8 m², with tie-down points | Frame stress calculation; later proof load | Deck 0.84 m²; frame strength unverified |
| R2 | Range per charge | 20 km or more on the design route in the design load case | Energy calculation; later logged ride | Met: about 24 km (estimate) |
| R3 | Assist on hills | 8 % grade for 300 m at 8 km/h or more with the rider feeling 40 N or less of drawbar pull, without motor over-temperature at 30 °C | Force and thermal calculation | Force met (about 33 N); thermal **unverified**, motor near 290 W against a 250 W rating |
| R4 | Near-zero added load on the flat | Steady drawbar pull felt by the rider 15 N or less at 5 to 20 km/h | Control calculation and simulation | Met on paper (about 4 N); loop stability unverified |
| R5 | Stay within pedal-assist limits | 250 W rated continuous motor output; assist only while the drawbar is in tension; no assist above 25 km/h; no throttle | Datasheets; controller settings | Met by design |
| R6 | Trailer brakes itself | With the combination slowing at 3 m/s², the trailer pushes the bicycle with 100 N or less; assist cut within 100 ms of drawbar compression above 20 N | Braking calculation; later bench test | By design (overrun brake); gain unverified |
| R7 | Hitch to common bicycles | Fits rear wheels with a 9 mm quick release or a 12 mm thru-axle, 130 to 148 mm spacing, 26 in to 700c; hitch and unhitch in 30 s or less; no wiring to the bike | Hitch design review; later fit survey | **At risk:** nutted axles, some hub gears and some rear-motor e-bikes need adapters, so "any bicycle" is not met |
| R8 | Light enough to handle | Empty trailer 35 kg (77 lb) or less, including the pack | Mass estimate; later weighing | **Not met:** about 38 kg with a steel frame (estimate) |
| R9 | Fit bike paths and doors | Overall width 1,000 mm or less; length 2.6 m or less hitched from the bike's rear axle | Model check | Met: about 910 mm wide, about 2.5 m long |
| R10 | Stable hitch load | Downward load on the hitch 3 to 10 kg with the design payload centered | Mass and balance estimate | Met: about 9 kg (estimate); off-center loads unverified |
| R11 | Weather and temperature | Electronics IP65; motor IP54 or better; operate −10 to 40 °C; the BMS blocks charging below 0 °C | Datasheets and design review | By design; unverified |
| R12 | Affordable | Prototype parts $900 or less, including charger | Priced BOM (`bom/bom.csv`) | **Not met:** about $965 (indicative), about 7 % over |
| R13 | Fail safe | Loss of the load cell signal, a reading out of range, a stuck value or a controller fault sets motor current to zero within 100 ms; the trailer stays towable as an unpowered, braked trailer | Fault tree and design review | By design; unverified |
| R14 | Be seen | Rear red lights and reflectors, side reflectors, and a flag at 1.5 m or more above the ground | Design review | Met by design |

## Assumptions

- Rolling resistance coefficient 0.010 for 20 x 2.15 in tyres on pavement at design load; extra drag area of the loaded trailer 0.1 m², since it rides partly in the rider's wake.
- Air density 1.2 kg/m³; gravitational acceleration 9.81 m/s².
- Motor, gear and controller efficiency 75 %; charger efficiency 90 %; cell charging efficiency 96 % for LiFePO4.
- Usable pack energy 90 % of the nominal 384 Wh.
- 250 W and 25 km/h follow the EU pedal-assist exclusion (Regulation (EU) No 168/2013); the US federal definition allows more (under 750 W, 20 mph), so the EU limits are the tighter case.
- Brake and hitch loads follow the voluntary cycle trailer standards EN 15918 and ASTM F1975, which limit unbraked trailers to 60 kg and 45.4 kg; CargoMule exceeds both, so its brakes are required, not optional.
