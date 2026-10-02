---
doc_id: CGM-DDR-001
title: CargoMule TRL 2 review decisions
project: CargoMule
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). The R8 response is now decided; see CGM-DDR-002
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "O1 and O2 decided by Amish on 2026-10-02 as recommended (CGM-DEC-001, items 7 and 8)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D10; items O1 and O2 remained proposed at this record and were decided by Amish on 2026-10-02, as recommended in the design decisions register (CGM-DEC-001, items 7 and 8): "i approve your recommendations for all 555 open decisions."

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis CGM-PRC-001 v0.2 listed further key design choices, each with options. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. Items without a recommendation stay open. The same instruction approved three portfolio-wide decisions: SwapCell interface v0.3 adds a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles; shared SwapCell packs are priced once and excluded from each dependent kit budget; and community designs pick co-design partners per area later.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in CGM-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Budget | Cut cost first (salvaged or budget 20 in idler wheel, budget disc calipers, a smaller and lighter enclosure), then raise `budget_usd` to $1,000 because the cuts alone do not reach $900. The redefined budget is carried into R12 as a $1,000 target. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Battery | Option A: a 12S 36 V class LiFePO4 pack, 384 Wh, rather than a SwapCell pack. A SwapCell receiver stays a later fleet variant. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Frame material | Welded mild steel for the first prototype, with R8 relaxed from 35 kg to 40 kg. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Drive layout | Option A: one 250 W geared hub motor in the left wheel, with a plain idler wheel on the right. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Control law | Proportional assist with a rider-selectable fixed gain of 2 to 6, default G = 4, rather than a closed loop to a set tension. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Brakes | Option A: a mechanical overrun coupler on disc brakes on both wheels, plus an electronic assist cut, rather than an electrically actuated brake or a cable from the bike's lever. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Pitch wording | Soften "fits any bicycle" to "fits most bicycles" and "almost no added load" to "a fraction of the load" in `project.yaml` and `README.md`. The problem line is unchanged. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | Force sensing | Sense pull force with a load cell at the drawbar (pitch-level choice kept), rather than a crank sensor on the bike or wheel-speed matching. Decided by Amish, 2026-09-25: go with recommendation. |
| D9 | Wheels and hitch side | 20 in (ETRTO 406) wheels and a hitch on the bicycle's left axle end, as proposed. Decided by Amish, 2026-09-25: go with recommendation. |
| D10 | Handcart mode | Stays out of scope for now. Decided by Amish, 2026-09-25: go with recommendation. |

*Table 2. Items left open at this record (no recommendation was made here); decided on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First users and region for co-design: market traders, a trades cooperative or a community food bank | Proposed, awaiting Amish (co-design partners to be picked per area later, as Amish directed for community designs) Decided by Amish, 2026-10-02 (CGM-DEC-001, item 7): first users chosen by one rule, a group moving 50 to 150 kg loads on short, repeated urban trips on paved, hilly routes; first candidate type to approach, a community food bank's local delivery or pantry runs. |
| O2 | Legal status of a motorized bicycle trailer on public roads and bike lanes in the first target country (EU pedal-assist exclusion, US federal and state rules) | Proposed, awaiting Amish; no recommendation was made and none is made here Decided by Amish, 2026-10-02 (CGM-DEC-001, item 8): private ground only until a written legal check exists for the first partner's country; the EU pedal-assist limits stay the design rule. |

## Consequences

- `project.yaml`: `budget_usd` is $1,000 and the pitch reads "fits most bicycles" and "a fraction of the load". `README.md` matches.
- CGM-PRB-001, CGM-PRC-001 and CGM-REQ-001 are revised to v0.3. R8 is relaxed to 40 kg and R12 is redefined as $1,000 (the budget). No other requirement target changes. The key design choices in the precis are no longer "proposed".
- The BOM carries the D1 cost cuts: idler wheel $30 (was $55), disc calipers $20 each (were $30) and a 0.8 mm, 320 x 300 x 170 mm enclosure at $25 (was $30). The TRL 3 total is $969 (CGM-CAL-001, I1).
- The SwapCell fleet variant under D2 is not designed at TRL 3. If it is taken up, it would build to SwapCell interface v0.3 (wake without CAN, charge while discharging, vehicle latch vibration rating), and the shared pack would be priced once in the SwapCell repo and left out of the CargoMule kit budget.
- TRL 3 calculations (CGM-CAL-001 v0.1) showed that R8 was still not met at 40 kg with the steel frame (about 43 kg). Decided by Amish, 2026-09-25: go with recommendation. R8 is relaxed to 45 kg for the first prototype, recorded in CGM-DDR-002 with the other TRL 3 review items.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
