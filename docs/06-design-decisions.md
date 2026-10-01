---
doc_id: CGM-DEC-001
title: CargoMule design decisions register
project: CargoMule
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the decision records, the review note and the build plan work
---

# CargoMule design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Response to the R8 miss: the constructable trailer weighs 46.2 kg against 45 kg | (a) relax R8 to 47 kg for the first prototype and weigh it at TRL 4; (b) straps or mesh in place of the plywood side boards now (about 43.9 kg); (c) find about 0.5 kg elsewhere | (a) | Side boards (build plan section 3.9) under (b); none under (a) | CGM-DDR-003, A1 |
| 2 | Where the key switch and charge port go, now that the enclosure's front face is its door | (a) enclosure right wall near the front; (b) on the door with a lead across the hinge | (a) | Enclosure drilling (section 3.10), harness | CGM-DDR-003, A2 |
| 3 | Coupler damping | (a) friction washers on the lever pivot; (b) a small hydraulic damper between the cheeks and the lever | (a) for the prototype; check for chatter at TRL 4 | Brake lever (section 3.6) | CGM-DDR-003, A3 |
| 4 | Bringing the appearance model and photoreal renders up to the constructable design | (a) update on Amish's Mac; (b) leave until TRL 4 | (a), before the repo is made public | None; media only | CGM-DDR-003, A4 |
| 5 | Finish and small parts on the renders: graphite powder coat, faced boards with badges, deck tie-down tracks, coupler gaiter, drawbar reflector | Keep the BOM's paint and plywood for the prototype, or adopt the styling | Keep the BOM for the prototype; treat the rest as finished-product styling | None for the prototype | Review note 2026-09-26, item 4 |
| 6 | Hero render composition: the trailer fills about half the frame | Accept, or add a close-up camera option to the kit renderer | Accept | None | Review note 2026-09-26, item 5 |
| 7 | First users and region for co-design | Market traders, a trades cooperative or a community food bank | None; partners to be picked per area later | Not part of the TRL 3 build | CGM-DDR-001, O1 |
| 8 | Road legality of a motorized bicycle trailer in the first target country | EU pedal-assist exclusion, US federal and state rules | None | Not part of the TRL 3 build; needed before any public road use | CGM-DDR-001, O2 |

The review note of 2026-09-26 also proposed a closed enclosure with a bottom or front access panel (item 1) and a clear guard over the load cell (item 3). Both are overtaken by CGM-DDR-003: the enclosure now has a front door and the load cell sits inside the coupler housing.

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

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D10: cost cuts then a $1,000 budget, 36 V LiFePO4 384 Wh pack, steel frame, one hub motor in the left wheel, proportional assist G = 2 to 6, overrun mechanical brake plus assist cut, pitch reworded, drawbar force sensing, 20 in wheels with the hitch on the left axle end, handcart mode out of scope | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | CGM-DDR-001 |
| 2026-09-25 | TRL 3 items D11 to D14: R8 relaxed to 45 kg with straps or mesh as a later weight option, thermal derating and a use limit for long climbs, 180 mm rotors with metallic pads, gain range kept at 2 to 6 | Amish: "i accept all your recommendations, go with them across all repos." | CGM-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; outstanding decisions go in this register, not the plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CGM-DDR-003 (Draft, open for his review) |
