---
doc_id: CGM-REQ-001
title: CargoMule requirements
project: CargoMule
doc_type: Requirements
version: "0.4"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. R8 relaxed to 40 kg and R12 redefined as the $1,000 budget (CGM-DDR-001); status from CGM-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R8 relaxed to 45 kg; R3 restated with thermal derating and a use limit; status from CGM-CAL-001 v0.2
---

# CargoMule requirements

These requirements are checked by calculation in CGM-CAL-001 v0.2 at TRL 3. Targets changed with Amish's decisions of 2026-09-25. Under CGM-DDR-001, R8 was relaxed from 35 kg to 40 kg for the steel frame (D3) and R12 was redefined as the $1,000 prototype budget (D1). Under CGM-DDR-002, R8 is relaxed again to 45 kg for the first prototype, and R3 is restated: the 300 m climb target stands, and beyond it the controller derates motor current to protect the winding, with the use limit stated to riders. Against the calculations, **none is missed and three are at risk (R3, R6, R7)**; nine are met on paper or by design, and two cannot be verified at TRL 3. Targets are not yet validated with users; the first users and region for co-design are still open (CGM-DDR-001, O1).

The **design load case** is 150 kg of payload centered on the deck, the trailer (about 43 kg, CGM-CAL-001) and a towing bicycle with rider of about 100 kg, on a dry paved road. The **design route** is a 10 km round trip with 120 m of climbing, 120 m of descent and 20 stops.

Table 1. Requirements, targets and status at TRL 3.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (CGM-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Carry the payload | 150 kg (330 lb) on a deck of at least 0.8 m², with tie-down points | Frame stress calculation; later proof load | Met on paper: deck 0.84 m²; least structural factor 1.6 at 2 g and the ultimate hitch case |
| R2 | Range per charge | 20 km or more on the design route in the design load case | Energy calculation; later logged ride | Met on paper: 24.9 km |
| R3 | Assist on hills | 8 % grade for 300 m at 8 km/h or more with the rider feeling 40 N or less of drawbar pull, without motor over-temperature at 30 °C. On longer continuous climbs the controller derates motor current so the winding stays at or below 100 °C; the use limit (about 300 m of continuous 8 % climbing at full assist) is stated in the rider instructions (restated, CGM-DDR-002) | Force and thermal calculation; motor datasheet at part selection | **At risk:** 36.6 N felt; winding about 95 °C against a 100 °C limit on assumed motor constants; derating starts after about 336 m [C10] |
| R4 | Near-zero added load on the flat | Steady drawbar pull felt by the rider 15 N or less at 5 to 20 km/h | Control calculation and simulation | Met on paper: 6.2 to 6.6 N; loop stable for G = 2 to 6 with the 0.7 Hz filter |
| R5 | Stay within pedal-assist limits | 250 W rated continuous motor output; assist only while the drawbar is in tension; no assist above 25 km/h; no throttle | Datasheets; controller settings | Met by design |
| R6 | Trailer brakes itself | With the combination slowing at 3 m/s², the trailer pushes the bicycle with 100 N or less; assist cut within 100 ms of drawbar compression above 20 N | Braking calculation; later bench test | **At risk:** 92 N dry and about 110 N with wet pads on 180 mm rotors with metallic pads (CGM-DDR-002); rotor heating on long descents; cut about 60 ms on paper |
| R7 | Hitch to common bicycles | Fits rear wheels with a 9 mm quick release or a 12 mm thru-axle, 130 to 148 mm spacing, 26 in to 700c; hitch and unhitch in 30 s or less; no wiring to the bike | Hitch design review; later fit survey | **At risk:** axle stresses pass; thru-axles need a hitch axle per thread pitch and length; nutted axles, some hub gears and some rear-motor e-bikes need adapters |
| R8 | Light enough to handle | Empty trailer 45 kg (99 lb) or less, including the pack, for the first prototype (relaxed from 35 kg to 40 kg by CGM-DDR-001 D3, then to 45 kg by CGM-DDR-002) | Mass estimate; later weighing | Met on paper: 43.2 kg (40.4 kg without side boards) |
| R9 | Fit bike paths and doors | Overall width 1,000 mm or less; length 2.6 m or less hitched from the bike's rear axle | Model check | Met on paper: 960 mm wide, 2.52 m long |
| R10 | Stable hitch load | Downward load on the hitch 3 to 10 kg with the design payload centered | Mass and balance estimate | Met on paper: 7.8 kg; holds only for a payload center 28 mm ahead to 62 mm behind the deck center |
| R11 | Weather and temperature | Electronics IP65; motor IP54 or better; operate −10 to 40 °C; the BMS blocks charging below 0 °C | Datasheets and design review | Not verifiable at TRL 3 |
| R12 | Affordable | Prototype parts $1,000 or less, including charger, equal to `budget_usd` (redefined, CGM-DDR-001 D1) | Priced BOM (`bom/bom.csv`) | Met on paper: $979 |
| R13 | Fail safe | Loss of the load cell signal, a reading out of range, a stuck value or a controller fault sets motor current to zero within 100 ms; the trailer stays towable as an unpowered, braked trailer | Fault tree and design review | Not verifiable at TRL 3 (60 ms fast path on paper) |
| R14 | Be seen | Rear red lights and reflectors, side reflectors, and a flag at 1.5 m or more above the ground | Design review | Met by design: flag top 1,570 mm |

## Assumptions

- Rolling resistance coefficient 0.010 for 20 x 2.15 in tyres on pavement at design load; extra drag area of the loaded trailer 0.1 m², since it rides partly in the rider's wake.
- Air density 1.2 kg/m³; gravitational acceleration 9.81 m/s².
- Drive efficiency from a motor model at each operating point (CGM-CAL-001, section C) rather than a fixed 75 %; charger efficiency 90 %; cell charging efficiency 96 % for LiFePO4.
- Usable pack energy 90 % of the nominal 384 Wh.
- 250 W and 25 km/h follow the EU pedal-assist exclusion (Regulation (EU) No 168/2013); the US federal definition allows more (under 750 W, 20 mph), so the EU limits are the tighter case. Whether a motorized trailer falls under either rule is open (CGM-DDR-001, O2).
- Brake and hitch loads follow the voluntary cycle trailer standards EN 15918 and ASTM F1975, which limit unbraked trailers to 60 kg and 45.4 kg; CargoMule exceeds both, so its brakes are required, not optional.
