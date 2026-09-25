# Review note: CargoMule

## Session 2026-09-25: TRL 3

Amish approved all recommendations from the TRL 2 review on 2026-09-25 ("proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them."). This session took CargoMule to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CGM-DDR-001 v0.1): ten decided items (D1 to D10) and two open items (O1, O2).
- `docs/04-calcs/01-sizing.md` (CGM-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: mass and balance, assist forces, motor and heating, loop stability, energy, braking, structure, geometry and cost, with a results table for R1 to R14. The script imports the model's `PARAMS` and reads the BOM and budget, and every quoted number carries the tag of the line that prints it.
- `cad/src/model.py`: parametric build123d model (frame with wheel arch frames and dropouts for 100 mm hubs, 12 mm deck and side boards, offset drawbar, hitch, load cell, overrun coupler, wheels, brakes, enclosure, pack, controller, board, harness, lights, stand). Exports `cad/step/` and `cad/stl/`: `cargomule-assembly`, `frame`, `drawbar-assembly`, `deck`, `enclosure`.
- `cad/src/sheets.py` and `cad/drawings/CGM-DWG-001.svg`, `.pdf`, `.png`: general arrangement, Rev P1, 1:20, "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet stays CGM-DWG-010.
- `bom/bom.csv` and `bom/bom-notes.md`: 18 lines, every line priced with a supplier type; total $969 against the $1,000 budget.
- `cad/src/concept_media.py` now builds from the model; all media refreshed (`hero.png`, `concept-blueprint.png`, `.pdf`, `.svg`, `exploded.png`, `cutaway.png`, `flow.png`, `model.glb`, `viewer.html`). Temporary `media/_views*` folders deleted.
- CGM-PRB-001, CGM-PRC-001 and CGM-REQ-001 revised to v0.3; `project.yaml` (TRL 3, budget $1,000, pitch) and `README.md` updated; PDFs rebuilt in `docs/pdf/`.

### Requirements (CGM-CAL-001, Table 5)

Eight met (six on paper, two by design), three at risk, one not met, two not verifiable at TRL 3.

| ID | Status | Value against target |
| --- | --- | --- |
| **R8 mass** | **Not met** | 43.1 kg against 40 kg (relaxed); 40.3 kg without side boards |
| **R3 hills** | **At risk** | 36.6 N felt (40 N) met; winding about 95 °C against 100 °C after 300 m on assumed motor constants; 174 °C after 1,000 m |
| **R6 braking** | **At risk** | 100 N push dry by sizing, about 120 N with wet pads; rotor rise 166 to 284 K on long descents; cut about 60 ms |
| **R7 hitch fit** | **At risk** | Axle stresses pass; thru-axles need a hitch axle per thread and length; nutted axles need adapters |
| R1, R2, R4, R9, R10, R12 | Met on paper | 0.84 m², least factor 1.6; 25.0 km; 6.2 to 6.6 N and stable; 960 mm, 2.52 m; 7.8 kg; $969 |
| R5, R14 | Met by design | 250 W, tension only, 25 km/h, no throttle; flag top 1,570 mm |
| R11, R13 | Not verifiable at TRL 3 | Datasheet items; 60 ms fault path on paper |

### Key results and changes from TRL 2

- **The TRL 2 assist filter would oscillate.** A first-order 2 Hz filter goes unstable above G = 0.5 at the softest drawbar stiffness considered. A second-order 0.7 Hz filter is stable for G = 2 to 6 (gain margin 2.9 at G = 4, 1.9 at G = 6), at the cost of about 0.47 s of assist lag. The compression cut acts on the raw signal.
- **A straight drawbar hits the bike's tyre after about 10° of yaw.** The drawbar now runs 360 mm out to the left, allowing 55.5° (about 1.3 m turn radius), and was upsized to 38 x 2.5 mm S355 for the offset.
- **Motor current.** The climb needs 24.1 A phase and 14.9 A from the pack; a controller with a lower limit would leave the rider feeling 57 to 72 N. The controller spec now states 15 A pack and 30 A phase.
- **Mass rose from about 38 kg to 43.1 kg:** realistic plywood mass, the wheel arch frames that the two-sided hub dropouts need, and the offset drawbar. A 9 mm deck failed a point-load check (15 MPa), so the deck stays 12 mm.
- **Hitch load** is 7.8 kg with the axle moved 30 mm forward, but the loading window for 3 to 10 kg is only 90 mm long.
- **Range** 25.0 km (13.9 Wh/km); mains 160 Wh per trip; braking needs 479 N from the trailer.
- **Cost** $969 after the D1 cuts (minus $50) and TRL 3 additions (plus $54).

### Decisions recorded (CGM-DDR-001)

All decided by Amish, 2026-09-25: go with recommendation. D1 budget: cost cuts, then `budget_usd` raised to $1,000 (R12 redefined). D2 battery: 36 V LiFePO4, 384 Wh; SwapCell as a later fleet variant (it would build to SwapCell interface v0.3, with the shared pack priced once outside this kit). D3 steel frame, R8 relaxed to 40 kg. D4 one hub motor in the left wheel. D5 proportional assist, selectable G = 2 to 6, default 4. D6 overrun mechanical brake plus assist cut. D7 pitch reworded to "fits most bicycles" and "a fraction of the load" (applied to `project.yaml` and `README.md`). D8 drawbar force sensing. D9 20 in wheels, hitch on the left axle end. D10 handcart mode out of scope.

### Still awaiting Amish

1. **O1, first users and region** for co-design (market traders, a trades cooperative or a community food bank). No recommendation; partners to be picked per area later.
2. **O2, road legality** of a motorized bicycle trailer in the first target country. No recommendation was made; it stays open.
3. **New: response to the R8 miss (43.1 kg).** Options: (a) relax R8 to 45 kg for the first prototype; (b) replace the plywood side boards with straps or mesh (about 40.3 kg, still just over); (c) an aluminium frame (about 5 kg lighter, about $60 more, TIG welding; reopens D3). Recommendation: (a), with (b) as a later weight option. Proposed, awaiting Amish.
4. **New: long climbs (R3).** Options: (a) keep the 250 W motor, add thermal derating and state a use limit of about 300 m of continuous 8 % climbing; (b) a larger motor, which would break the 250 W pedal-assist limit (R5). Recommendation: (a), and confirm the motor constants from a datasheet. Proposed, awaiting Amish.
5. **New: wet braking and descents (R6).** Options: (a) accept about 120 N of wet push; (b) 180 mm rotors with metallic pads (about $10 more, raises brake gain and heat capacity); (c) a higher coupler lever ratio (more stroke). Recommendation: (b). Proposed, awaiting Amish.
6. **New: highest gain setting.** G = 6 has a 5.8 dB margin at the softest stiffness, just under 6 dB. Options: keep 2 to 6, or cap at 5. Recommendation: keep 2 to 6 on paper and decide once the hitch joint stiffness is known. Proposed, awaiting Amish.

### Safety concerns

- Runaway or oscillating assist: the 0.7 Hz filter, the raw-signal compression cut, torque-mode control and a gain cap of 6 are all required.
- Braking of a 193 kg trailer: the overrun brake must work unpowered; wet pads raise the push to about 120 N; rotors on long, steep descents can rise 170 to 280 K, and the left rotor heats the motor.
- Hitch failure: secondary strap rated 3.8 kN or more, lock indicator, design load above 1,895 N.
- Load placement: the drawbar unloads with the payload center 100 mm behind the deck center; mark a loading zone.
- Motor heat on climbs longer than about 300 m at 8 %.
- 384 Wh LiFePO4 pack: BMS, 20 A fuse, closed vented steel enclosure, charging on a non-combustible surface.
- Pinch points at the 50 mm coupler stroke and the stand; tyres 22.5 mm from the side rails.
- Legal status on public roads is unknown (O2).

### Problems and notes

- `.kit/drawing.py` `project_views` fails on this model: the hidden-line projection yields one zero-length ellipse arc that the SVG exporter rejects. The kit was not changed; `cad/src/sheets.py` has an edge-by-edge copy (`safe_project_views`) that skips the one bad edge, and `cad/src/concept_media.py` uses it for `render_all`. A kit fix is suggested.
- In the exploded view the hitch (4) and load cell (5) are still small at this scale; the GA drawing and cutaway show them in context.
- Masses of bought parts, motor constants, pad friction and hitch joint stiffness are assumed catalog or handbook values; each is listed in CGM-CAL-001, Table 1.
- No TRL 4 material exists in the repo (no tests, build procedures, purchasing lists, firmware or PCB files). `build-log/README.md` is the scaffold stub and was not extended.
- The TRL 2 review listed no unchecked citations, so no web verification was run this session. The TRL 2 sources in CGM-PRB-001 are unchanged.

### Recommended next step

TRL 4 is on hold by Amish's instruction; do not start it. The next step is for Amish to decide items 3 to 6 above and, when ready, O1 and O2. For the record only, TRL 4 would need: a motor datasheet and a bench thermal run of the hub on a simulated 8 % climb; a drawbar and coupler bench rig to measure hitch joint stiffness, loop stability and the overrun brake gain dry and wet; a hitch fit survey across axle types; a test plan and lab test reports (TST, `environment: lab`); and dated build log entries.

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
