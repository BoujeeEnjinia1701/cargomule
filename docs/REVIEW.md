# Review note: CargoMule

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch)

### What was done

- `docs/01-problem.md` (CGM-PRB-001 v0.2): problem with sourced figures (cargo e-bike prices, unassisted trailer limits, unbraked trailer limits), users, operating environment, constraints, out of scope, prior work with inline sources (Carla Cargo, Biomega Ein, Roland PAXXTER e, coupling-sensor patents), open questions, and a new co-design checklist.
- `docs/03-requirements.md` (CGM-REQ-001 v0.2): 14 measurable requirements (R1 to R14) with targets, verification and a status column against the concept estimates, a design load case and a design route.
- `docs/02-concept.md` (CGM-PRC-001 v0.2): how it works, 16 numbered components, control law, mass and balance, drawbar forces, energy and range, braking, cost, design choices with options, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the trailer (frame, deck, drawbar, hitch, load cell, overrun coupler, motor and idler wheels, brakes, enclosure, pack, controller, control board, harness, lights and flag, stand), with a grey towing bicycle and a grey 150 kg load as hero context and the 1.75 m scale figure.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` (callouts 1 to 16), `cutaway.png`, `flow.png` (energy per 10 km loaded trip, estimates), `model.glb` and `viewer.html`. Temporary `media/_views*` folders removed.
- `bom/bom.csv`: 18 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` updated to say so.
- `README.md`: hero image and links line inserted before "Problem"; Concept, Key components and Safety sections updated to match the precis.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Payload and deck | 150 kg on 1,200 x 700 mm (0.84 m²) | R1: frame strength unverified |
| Empty trailer mass | about 38 kg (steel frame) | **R8 (35 kg) not met** |
| Pull felt on the flat, G = 4 | about 4 N of about 20 N | R4 met on paper |
| Pull felt on 8 % at 8 km/h | about 33 N of about 165 N; motor about 290 W, 34 N·m | R3 force met; **thermal unverified** |
| Pack energy on the design route | about 14 Wh/km | |
| Range per charge, 384 Wh LiFePO4 | about 24 km hilly and loaded, about 45 km flat | R2 (20 km) met |
| Braking force needed at 3 m/s² | about 560 N from the trailer; overrun brake sized for about 460 N at 100 N push | R6 by design; gain unverified |
| Hitch down load | about 9 kg, payload centered | R10 met |
| Size | about 2.5 m long hitched, about 910 mm wide | R9 met |
| Parts cost | about $965 including charger | **R12 ($900) not met, about 7 % over** |

Requirements not met or at risk:

- **R8 (mass) not met:** about 38 kg against 35 kg with a steel frame; aluminium would give about 33 kg.
- **R12 (cost) not met:** about $965 against $900.
- **R7 (hitch to common bikes) at risk:** the hitch covers quick-release and 12 mm thru-axle wheels; nutted axles, some hub gears and some rear-motor e-bikes need adapters. The pitch's "fits any bicycle" is therefore stronger than the concept supports.
- **R3 (hills) thermal part unverified:** the motor runs at about 290 W against a 250 W continuous rating on the design climb.
- **R4 and R6 unverified:** the proportional loop's stability and the overrun brake gain are TRL 3 calculations.

### Proposed, awaiting Amish

1. **Budget.** Parts are about $65 over. Options: (a) raise `budget_usd` to $1,000; (b) cut cost with salvaged 20 in wheels and brakes and a lighter enclosure to reach about $900; (c) drop side boards and lights from the prototype (not recommended; lights are safety items). Recommendation: (b), then (a) if needed. `project.yaml` is unchanged.
2. **Battery.** Option A: 36 V class LiFePO4, 384 Wh, about $180 (scaffold choice, meets R2, more thermally stable under a load). Option B: the portfolio's SwapCell pack (48 V class, about 468 Wh, about $370, CAN host heartbeat, 48 V drive), which suits shared fleets but adds about $190. Recommendation: A, with a SwapCell variant later for fleets.
3. **Frame material.** Welded steel (cheap, local, about 38 kg, misses R8), aluminium (about 33 kg, about $60 more, TIG welding) or a bolted steel kit. Recommendation: steel for the first prototype and relax R8 to 40 kg, or revisit.
4. **Drive layout.** One 250 W hub in the left wheel (recommended), two 125 W hubs, or a third central drive wheel.
5. **Control law.** Proportional assist with a selectable fixed gain, default G = 4 (recommended), versus a closed loop to a small set tension.
6. **Brakes.** Mechanical overrun coupler on both disc brakes plus electronic assist cut (recommended), versus an electrically actuated brake or a cable from the bike's lever.
7. **Pitch wording.** "Fits any bicycle" and "almost no added load" are strong: the hitch fits most quick-release and thru-axle bikes, and the rider feels about 4 N on the flat but about 33 N on an 8 % climb. Options: keep the pitch as an aim, or soften to "fits most bicycles" and "a fraction of the load". Recommendation: soften at the next pitch review. `project.yaml` pitch and problem are unchanged; the sourced numbers support the problem statement as written.
8. **First users and region** for co-design (market traders, a trades cooperative or a community food bank).
9. **Handcart mode** left out of scope for now.

### Safety concerns

- Unintended push or runaway assist, which can shove the bike into traffic or jackknife it: assist only in tension, cut within 100 ms on compression, standstill, overspeed or any sensor fault; controller in torque mode with its own current limit; no throttle.
- Braking of a 188 kg trailer, well above the 45 to 60 kg unbraked limits in ASTM F1975 and EN 15918: the overrun brake is mandatory and must work unpowered; rotor heating on long descents is unchecked.
- Hitch failure: a secondary safety strap and a clear lock indicator are required; hitch design loads are not yet calculated.
- 384 Wh LiFePO4 pack: BMS, fuse, closed vented enclosure, charging on a non-combustible surface.
- Load tipping, pinch points at the sliding coupler and stand, and visibility of a long combination.
- Legal status of a motorized trailer on public roads is unknown in every target country.

### Problems and notes

- The kit renderer's labels for the orthographic views read "Front view" and "Right view"; for this trailer the "Front view" is the side elevation. This comes from `.kit/drawing.py` and was not changed.
- In the exploded view the hitch (4) and load cell (5) are small, so their callouts nearly cover them; the precis and cutaway show them in context.
- The cutaway cuts on the trailer center line, so the left-offset hitch and most of the load cell are cut away; the pack, controller, board and overrun coupler show clearly.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- While stopping a stale render of this repo, a `pkill -f concept_media.py` command was run that could also have stopped concept renders for other repos running in parallel in the same overnight batch. Those repos' media should be checked for completeness.

### Recommended next step

Review this note and the media, then decide items 1 to 3 and 7. If approved, run `/advance-trl3` to check the assist loop stability, motor heating, overrun brake gain, hitch loads and frame stress by calculation, and produce the parametric model and drawing sheet.
