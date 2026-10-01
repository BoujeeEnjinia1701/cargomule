---
doc_id: CGM-DDR-003
title: CargoMule design for construction
project: CargoMule
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; they are open for his review. The items in Table 3 change a requirement status or the product's appearance and are Proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo's build plan to show how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of CargoMule (CGM-DDR-002) was a massing model: it showed what the trailer does and carried the right main dimensions, but many of its parts could not be made, fixed or assembled as drawn. Checking it with build123d found parts that overlapped (the calipers ran into the hub motor, the harness ran through the coupler, load cell, stand and enclosure), parts with no fixing (deck, boards, enclosure, lights, flag, stand) and a load path that could not work (a load cell on pinned ends carrying the drawbar's bending). Working out the assembly order found three more problems that an overlap check cannot see (P3, P4 and P8 below).

The changes keep what CargoMule does: the same deck, wheels, track, hitch point and drawbar route, the same proportional assist sensed at the drawbar, the same mechanical overrun brake on both wheels with the same 30 N preload, 50 mm stroke and 7.7 to 1 lever, the same 384 Wh pack, motor and controller. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 73 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must not touch keep the stated clearance, and the coupler's moving parts are checked again at full stroke. All 73 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The load cell sat in the drawbar line on pinned clevises, between the drawbar and a separate sliding coupler. A pinned link cannot carry the drawbar's bending or the 7.5 kg tongue load, so the drawbar would fold at the cell; the coupler's force path was not defined. | The drawbar's straight rear end is the coupler's sliding member: it runs in two acetal bushings in a 60.3 x 2.0 mm steel housing welded into the frame nose, so the bushings carry bending and the tongue load. Inside the housing, in series: a rod end on the drawbar's end plug, a clevis pin, the S-type cell, an M10 pull rod and a nut and washer that bear on the bulkhead of a spring cage. A 30 N preload spring sits behind the nut. Pull goes drawbar, cell, rod, bulkhead, cage, housing. Push above 30 N slides the drawbar, cell and rod back against the spring, and the rod's tail pushes the brake lever. | The cell sees only axial force, in both directions, as the concept intended (it reads true push up to the brake's onset, so the 20 N compression cut still works). The concept's preload, stroke and lever ratio are unchanged. |
| P2 | No overload stop could be built in the concept's layout, and nothing stopped the offset drawbar rolling in a round sleeve. | A slotted fork welded on top of the housing's front end, its front end closed by a plate. An M12 shoulder bolt through the drawbar rides in the slot: it stops the drawbar turning, and it sits 0.5 mm behind the closed end, so a pull beyond the cell's travel bears on the housing instead of the cell. | One part does both jobs. A 12 mm pin keeps the bending stress about 180 MPa at the 1.9 kN ultimate pull. |
| P3 | The cell string could not be put into the housing: a collar on the drawbar was wider than the bushing bore and the bulkhead was welded in. | The spring, pull rod, cell and spring cage form a cartridge that goes in from the rear and is held by a ring clamped under a bolted end cap. The drawbar goes in from the front carrying its rod end. The two are joined by an M8 clevis pin put in through a 70 x 24 mm window in the housing's right side, closed by a rubber cover. | Every part can be fitted and taken out with hand tools, in one order. The window is behind the bushings, where the housing carries no drawbar bending. |
| P4 | The brake lever and damper were boxes with no pivot or cable path; the hydraulic damper had no mounting. | A 20 x 6 mm lever pivoted on an M8 bolt between two 4 mm cheeks under the housing's rear, 106 mm above and 13.8 mm below the pivot (7.7 to 1). The rod's tail pushes its top; its bottom pulls one cable through a stop tab to a splitter under the left rail, then one cable to each caliper. Damping comes from spring washers on the pivot (friction), which the concept allowed as an alternative to a small hydraulic damper. | A cable splitter replaces the equalizer bar and needs no mounting of its own. See A3 for the damping choice. |
| P5 | The drawbar's corners were sharp with balls at the knees; its straight section started 800 mm from the hitch, leaving too little straight tube for the coupler. | One 38 x 2.5 mm S355 tube with three 115 mm radius bends made in a tube bender; the straight rear part starts at 700 mm (centre line corner) so 198 mm of straight tube runs in the bushings. The hitch end's knee positions are unchanged, so the 55.5 degree articulation (CGM-CAL-001 H5) is unchanged. | A bent tube can be made by any fabricator with a bender. The drawbar is 0.1 kg heavier. |
| P6 | The nose bars met in a solid ball; they started inside the front rail. | The nose bars run from the front rail's face to the sides of the coupler housing, fishmouthed onto it, 320 mm behind its front end. | The housing is the nose: one welded joint replaces a part that could not be made. |
| P7 | The hitch arm (34 mm) was larger than the drawbar's 33 mm bore. | Hitch arm 32 mm, 60 mm into the bore, with a 6 mm locking pin through both. | A sliding fit with 0.5 mm clearance. |
| P8 | The enclosure was an open box touching one crossmember with no fixing. Its lid was on top, against the frame, so it could not open, and the pack could not come out. | The box is 350 mm long (was 320) and centred under the crossmembers at 1,600 and 1,920 mm, held by four M6 bolts from inside into rivet nuts in the crossmembers. A front door, hinged along its bottom edge with a keyed lock, opens toward the drawbar; the pack slides out forward under the deck. | The box hangs from two crossmembers with a 15 mm bolt edge distance. The forward path is the only one clear of the wheels and rotors. The box's mass center moves 260 mm rearward. |
| P9 | The calipers overlapped the hub motor's shell (caliper body from 65 mm radius against a 78 mm shell) and had nothing to mount to. | Each inner dropout plate extends rearward as a tab; the caliper's post-mount adapter bolts to it with two M6 bolts and the caliper body sits 80 to 120 mm from the axle, 2 mm clear of the motor shell. The rotor sits 15 mm inside the hub's locknut face. | Standard bicycle parts and dimensions. |
| P10 | The dropout plates had no axle slots; the motor's torque (about 35 N m on the climb) had nothing to react it but the axle flats. | 10.2 mm slots, 40 mm deep from the bottom edge, in all four plates. A bought torque arm on the left inner plate's inside face, bolted to the plate with one M6 bolt. | The wheels drop in from below. Hub motor makers call for a torque arm in steel dropouts. |
| P11 | The deck and boards had no fixing. | Sixteen M6 countersunk bolts through the deck into rivet nuts in the rail tops. The boards are held by four aluminium angle corner pieces and ten aluminium angle brackets with M6 wing nuts, so they still come off by hand. | Rivet nuts put threads in closed box section without welding nuts inside. |
| P12 | The flag pole stood on the deck with no fixing. Rear lights floated 2 mm behind the rear rail. | The pole sits in two clips on the left board's inside face. The lights bolt to the rear rail with M5 screws into rivet nuts. | |
| P13 | The parking stand's top had nothing to attach to. | The stand leg pivots on an M10 bolt in a clevis under the housing's front end and folds back under the housing. | |
| P14 | The harness was drawn through the coupler, load cell, stand and enclosure. | Rerouted. The motor cable runs from the axle's outer end up the arch strut and along the arch frame, clipped outside it, to the left rail and the enclosure. The cell cable leaves through a gland in the end cap. The light cables run under the deck. | The motor cable outside the left arch makes the trailer 972 mm wide over the cable (960 mm over the frame); R9 (1,000 mm) is still met. |
| P15 | Rails and tubes were solid. | Rails, crossmembers, nose bars and arch frames are modelled as hollow sections with capped ends where open ends would face forward or rearward. | Needed for the fixings and for honest masses. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Empty trailer 46.2 kg (was 43.2 kg) [A3]: frame 13.0 kg from the model (dropout tabs, eyes), coupler 2.9 kg in all (was 1.6 kg), board fittings 0.5 kg, enclosure 3.0 kg, torque arm and splitter 0.2 kg. R8 (45 kg) is **not met**; see A1. | The concept's masses were estimates for parts that had not been designed. |
| Balance | Hitch load 7.5 kg with the payload centred (was 7.8 kg) [A6]; loading window 32 mm ahead to 57 mm behind the deck centre [A7]. R10 still met. | Enclosure moved rearward; coupler heavier. |
| Performance | Felt pull on the 8 % climb 38.7 N (was 36.6 N, R3 target 40 N) [C3]; range 24.5 km (was 24.9 km) [E3]; push 93 N dry and 111 N wet (was 92 N and 110 N) [F3], [F4]. Statuses unchanged: R3 and R6 at risk, R2 met. | The trailer is 3 kg heavier. |
| Structure | Drawbar factor 4.3 at the coupler's front bushing [G3] (was 3.0, quoted at the nose); ultimate case 1.6 unchanged [G4]. | The drawbar is now held by the bushing, 320 mm ahead of the old nose point. |
| Cost | BOM lines 2, 5, 6, 7, 9, 10, 15, 16 and 18 respecified; total $997 (was $979) within the unchanged $1,000 `budget_usd` [I1]. | Fittings, rivet nuts, coupler parts. |
| Drawing | CGM-DWG-001 Rev P4; making sketches CGM-DWG-101 to 111 added. | Follows the model. |
| Documents | CGM-CAL-001 v0.3, CGM-PRC-001 v0.5, CGM-REQ-001 v0.5. R8 changes from met to not met; no other requirement changes status. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The constructable trailer weighs 46.2 kg, 1.2 kg over R8's 45 kg. | (a) relax R8 to 47 kg for the first prototype and weigh it at TRL 4; (b) take the later weight option of CGM-DDR-002 now: straps or mesh in place of the plywood side boards (about 43.9 kg); (c) look for mass elsewhere (4 mm dropout plates, a shorter housing with a stiffer spring), about 0.5 kg. | (a). The boards are part of what the trailer offers; the margin is small and the estimate is on catalogue masses. |
| A2 | The key switch and charge port. The renders of 2026-09-26 put them on the enclosure's front face, which is now the door. | (a) on the enclosure's right wall near the front, reached under the deck edge; (b) on the door, with a flexible lead across the hinge. | (a): no cable flexes at the hinge. |
| A3 | Friction damping on the lever pivot in place of a small hydraulic damper (the concept allowed either). | (a) friction washers for the prototype; (b) a small hydraulic damper between the cheeks and the lever. | (a), and check at TRL 4 that the coupler does not chatter on rough roads; (b) fits later without other changes. |
| A4 | The photoreal renders and the appearance model (`cad/src/product_model.py`) show the concept's coupler, load cell guard, top-opening enclosure with an inspection window and the old harness. | (a) update the appearance model and renders on Amish's Mac to this design; (b) leave them until TRL 4. | (a), before the repo is made public. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CGM-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status (CGM-CAL-001 v0.3): one not met (R8), three at risk (R3, R6, R7), eight met on paper or by design, two not verifiable at TRL 3.
- The renders `media/render-*.png`, `media/card.png` and `media/social-preview.png` and the appearance model still show the concept; they are made on Amish's Mac (A4).
- The parts to confirm when bought (load cell size, hub motor axle and cable exit, caliper adapter, spring) are listed in the design decisions register, CGM-DEC-001.
