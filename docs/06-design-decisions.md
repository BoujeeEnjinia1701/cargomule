---
doc_id: CGM-DEC-001
title: CargoMule design decisions register
project: CargoMule
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the decision records, the review note and the build plan work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for all eight open decisions on 2026-10-02; moved to decisions made; R8 fallback line in value engineering updated; 2026-09-26 review note items 1 to 3 closed"
---

# CargoMule design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The S-type load cell fits the 56.3 mm housing bore: body no more than 54 mm across its diagonal (about 51 x 13 x 61 mm assumed), M10 threads at both ends | The cell lives inside the coupler housing | CGM-DDR-003, P1 |
| 2 | The hub motor: 100 mm spacing, 10 mm axle flats, disc mount, shell no more than 156 mm across within 16 mm of the disc-side locknut, cable exit on the non-disc side, torque arm in the kit | Sets the slot width, the caliper clearance and the cable route | CGM-DDR-003, P9, P10 |
| 3 | The caliper's post-mount adapter for a 180 mm rotor: hole spacing on the dropout tab | The tab's two holes are drilled to suit | CGM-DDR-003, P9 |
| 4 | The hitch's arm is 32 mm or less and takes the 6 mm locking pin; the hitch fits the bicycle's axle type | The arm goes 60 mm into the drawbar's 33 mm bore | CGM-DDR-003, P7; R7 |
| 5 | The preload spring: about 30 N installed, free length about 96 mm, OD 40 mm or less, solid length under 40 mm | It sets the brake's onset and must not go solid within the 50 mm stroke | CGM-CAL-001, F3 |
| 6 | Motor constants (winding, resistance, thermal) from the datasheet | They decide whether R3 holds (decided under CGM-DDR-002; part selection is TRL 4) | CGM-DDR-002, D12 |
| 7 | Rivet nuts rated for 1.5 mm wall box section | They carry the deck, the enclosure and the lights | CGM-DDR-003, P8, P11 |

## Value engineering

Value-engineering target: USD 1,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 997 (USD 3 under the target).

Main cost drivers (CGM-CAL-001, I1): the battery pack (line 11, $180), the hub motor wheel (line 7, $160), the chassis frame (line 1, $95), the deck and side boards (line 2, $77) and the overrun brake coupler (line 6, $58). The parts added to make the design buildable added $18 (CGM-DDR-003).

Savings worth trying:

- Salvaged 20 in wheels and brakes and a lighter enclosure, which the TRL 3 review estimated could bring the parts to about $900.
- Straps or mesh in place of the plywood side boards (about 43.9 kg), the fallback if the weighed prototype is over the 47 kg cap of R8 (CGM-DDR-003, A1).
- A SwapCell receiver in the fleet variant, which would price the shared pack once and leave it out of this kit (CGM-DDR-001, D2).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D10: cost cuts then a $1,000 budget, 36 V LiFePO4 384 Wh pack, steel frame, one hub motor in the left wheel, proportional assist G = 2 to 6, overrun mechanical brake plus assist cut, pitch reworded, drawbar force sensing, 20 in wheels with the hitch on the left axle end, handcart mode out of scope | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | CGM-DDR-001 |
| 2026-09-25 | TRL 3 items D11 to D14: R8 relaxed to 45 kg with straps or mesh as a later weight option, thermal derating and a use limit for long climbs, 180 mm rotors with metallic pads, gain range kept at 2 to 6 | Amish: "i accept all your recommendations, go with them across all repos." | CGM-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; outstanding decisions go in this register, not the plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CGM-DDR-003 (Draft; Table 3 accepted on 2026-10-02) |
| 2026-10-02 | R8 set to 47 kg as a hard cap for the first prototype only, not a new target; the trailer is weighed at TRL 4, and straps or mesh side boards are the fallback if it weighs more than 47 kg | Amish: "i approve your recommendations for all 555 open decisions." | CGM-DDR-003, A1 |
| 2026-10-02 | Key switch and charge port on the enclosure's right wall near the front, so no lead flexes across the door hinge | Amish: "i approve your recommendations for all 555 open decisions." | CGM-DDR-003, A2 |
| 2026-10-02 | Coupler damping: friction washers on the lever pivot for the prototype; a rough-road chatter check is a pass condition at TRL 4, and the small hydraulic damper is fitted if the brake chatters or grabs | Amish: "i approve your recommendations for all 555 open decisions." | CGM-DDR-003, A3 |
| 2026-10-02 | Appearance model and photoreal renders to be updated to the constructable design on Amish's Mac before the repo is made public | Amish: "i approve your recommendations for all 555 open decisions." | CGM-DDR-003, A4 |
| 2026-10-02 | Keep the BOM's paint and sealed plywood for the prototype; the powder coat, faced boards, badges, tie-down tracks and gaiter are labeled as finished-product styling in the renders; the drawbar reflector is to be added to the BOM | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, item 4 |
| 2026-10-02 | Hero render composition accepted as it is; a kit close-up camera only if a load cell detail shot is wanted | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, item 5 |
| 2026-10-02 | First users chosen by one rule: a group moving 50 to 150 kg loads on short, repeated urban trips by bicycle or hand cart on paved, hilly routes. First candidate type to approach: a community food bank's local delivery or pantry runs; market traders are the second choice | Amish: "i approve your recommendations for all 555 open decisions." | CGM-DDR-001, O1 |
| 2026-10-02 | Until a written legal check exists for the first partner's country, the trailer is for private ground only; the EU pedal-assist limits (250 W, assist only under pull, cut at 25 km/h, no throttle) stay the design rule as the strictest common case | Amish: "i approve your recommendations for all 555 open decisions." | CGM-DDR-001, O2 |

The review note of 2026-09-26 also proposed a closed enclosure with a bottom or front access panel (item 1), controls on the enclosure's front face (item 2) and a clear guard over the load cell with an enclosure window (item 3). Items 1 and 3 are closed: CGM-DDR-003 overtook them (the enclosure has a front door, P8, and the load cell sits inside the coupler housing, P1). Item 2 is closed by the 2026-10-02 decision on CGM-DDR-003, A2.
