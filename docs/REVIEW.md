# Review note: CargoMule

## Session 2026-10-02: open decisions decided by Amish

Amish wrote on 2026-10-02: "i approve your recommendations for all 555 open decisions." Every open decision in this repo's register was decided as recommended and moved to "Decisions made" in `docs/06-design-decisions.md`, dated 2026-10-02.

### Decisions recorded

8 decisions recorded (register items 1 to 8). The register's "Open decisions" section now reads: "None. All open decisions were decided on 2026-10-02."

### Documents changed

- `docs/06-design-decisions.md` v0.3
- `docs/decisions/0003-design-for-construction.md` v0.3
- `docs/decisions/0001-trl2-review-decisions.md` v0.3
- `docs/decisions/0002-recommendations-accepted.md` v0.2
- `docs/03-requirements.md` v0.7
- `docs/04-calcs/01-sizing.md` v0.5
- `docs/02-concept.md` v0.7
- `docs/01-problem.md` v0.6
- `docs/05-build-plan.md` v0.2
- `README.md` (safety note; not a controlled document)

PDFs re-rendered with `python3 .kit/render.py`. The CAD model, BOM quantities and prices, and pictures were not changed.

### Follow-up actions to carry approved decisions into the design

1. Decision 1 (calculations): Change the R8 target in `docs/04-calcs/sizing.py` (line A3 and the status table) from 45 kg to the 47 kg prototype cap so that a rerun reproduces CGM-CAL-001 v0.5, which was edited by hand.
2. Decision 2 (model): Add the key switch and charge port holes to the enclosure's right wall near the front in `cad/src/model.py`, with the harness route to them, and rerun the constructability checks.
3. Decision 2 (drawings): Regenerate the enclosure making sketch and CGM-DWG-001 with the key switch and charge port holes.
4. Decision 2 (build plan pictures and renders): Regenerate the build plan pictures of the enclosure and harness steps and add the drilling of the two holes to the enclosure step text of CGM-BLD-001.
5. Decision 3 (documents): When TRL 4 is opened, write the rough-road chatter check of the coupler into the test plan as a pass condition, with fitting the small hydraulic damper as the response to chatter or grabbing.
6. Decision 4 (build plan pictures and renders): Update `cad/src/product_model.py` to the constructable design and regenerate `media/render-*.png`, `media/card.png` and `media/social-preview.png` on Amish's Mac before the repo is made public; show the key switch and charge port on the enclosure's right wall.
7. Decision 5 (BOM): Add a drawbar reflector to `bom/bom.csv` and `bom/bom-notes.md` (price and mass), then rerun the cost and mass lines of CGM-CAL-001.
8. Decision 5 (build plan pictures and renders): Caption the renders so that the powder coat, faced boards, badges, tie-down tracks and gaiter read as finished-product styling, not the prototype's paint and plywood.

### Points found in the review

- Item 1, option (b) gives about 43.9 kg without plywood boards, while R8's status row in CGM-REQ-001 v0.5 gives 43.4 kg without side boards; the two figures should be reconciled (the difference may be the straps or mesh).
- REVIEW.md 2026-09-26 appearance items 1 to 3 (closed enclosure, controls on the front face, load cell guard and enclosure window) are not in the register. Items 1 and 3 appear superseded by CGM-DDR-003 (P1 and P8) and item 2 is replaced by register item 2; they should be closed explicitly.
- R8 has been relaxed from 35 to 40 to 45 kg and is now proposed at 47 kg; the requirement may need restating as a prototype cap with a separate product target.
- Descent speed limit: CGM-CAL-001 says a descent speed limit is still needed (225 K rotor rise on 10 % at 25 km/h), but it is not in the open decisions register.
- CGM-DDR-003 Table 1 (the changes made for construction) was not itself an open decision in the register, so the record stays Draft and Table 1 is still open for Amish's review; only Table 3 was accepted on 2026-10-02.
- Flag 2 above is now handled in the register: the 2026-09-26 appearance items 1 to 3 are recorded as closed under "Decisions made".

TRL 4 remains on hold by Amish's instruction.

## Session 2026-10-01: kit 1.7.0, design for construction and prototype build plan

Following Amish's 2026-09-30 instruction ("If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations") and the build plan format he approved for FieldNode, with outstanding decisions kept out of the plan and in a separate register.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced by `.kit/CLAUDE.md`.
- Constructability review of the TRL 3 model with build123d (overlaps, contacts, fixings, assembly order, process). `cad/src/model.py` rewritten as a constructable model with `build_components()` and 73 checks (`python cad/src/model.py --check`), all passing.
- `docs/decisions/0003-design-for-construction.md` (CGM-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `cad/src/build_plan_media.py`: overview, eleven making sketches (`cad/drawings/CGM-DWG-101` to `111`), ten joint close-ups and sixteen assembly step pictures in `docs/05-build-plan/`.
- `docs/05-build-plan.md` (CGM-BLD-001 v0.1) and `docs/06-design-decisions.md` (CGM-DEC-001 v0.1).
- Calculations rerun: `docs/04-calcs/sizing.py` now takes made-part masses from the model's volumes; CGM-CAL-001 v0.3, CGM-REQ-001 v0.5, CGM-PRC-001 v0.5. `bom/bom.csv` and `bom/bom-notes.md` updated ($997).
- CGM-DWG-001 Rev P4 regenerated; `cad/src/sheets.py` now repairs collapsed elliptical arcs in the projected views, which drew a stray line across the sheet. STEP and STL re-exported; concept media regenerated.
- `project.yaml`: `design_state: constructable`; DDR-003, the build plan, the register, the overview picture and the media script added to `trl_evidence`. README: links line and a "Building the prototype" section.

### Design changes made for construction (CGM-DDR-003)

1. Load cell moved inside a coupler housing welded into the frame nose; the drawbar slides in two bushings that carry its bending and tongue load; pull goes through a rod end, clevis pin, cell and pull rod to a spring cage's bulkhead.
2. Overload stop and anti-rotation: a slotted fork on the housing with a closed front end; an M12 pin through the drawbar rests 0.5 mm behind it.
3. Assembly order: spring, rod and cell go in from the rear as a cartridge under a bolted end cap; the clevis pin goes in through a 70 x 24 mm side window with a rubber cover.
4. Brake lever: 20 x 6 mm lever, 7.7 to 1, on a bolt between cheeks under the housing; friction washers in place of a hydraulic damper; one cable to a splitter, then one to each caliper.
5. Drawbar: one tube with three 115 mm radius bends; straight rear part from 700 mm; welded end plug.
6. Nose: nose bars fishmouthed onto the coupler housing (the concept's solid ball removed).
7. Hitch arm 32 mm into the drawbar's 33 mm bore with a locking pin.
8. Enclosure: 350 mm long, bolted up into the crossmembers at 1,600 and 1,920 mm, front door hinged at the bottom with a lock; the pack slides out forward.
9. Calipers on post-mount adapters on rearward tabs of the inner dropout plates, clear of the motor shell.
10. Axle slots in all four dropouts; a torque arm on the left inner dropout.
11. Deck on 16 M6 bolts into rivet nuts; boards held by aluminium corner pieces and brackets with wing nuts.
12. Flag pole in two clips; rear lights bolted to the rear rail.
13. Parking stand pivoted in a clevis under the housing.
14. Harness rerouted (motor cable along the left arch frame; cell cable out of the end cap; light cables under the deck).
15. Rails and tubes modelled hollow with capped ends.

### Key results (CGM-CAL-001 v0.3)

- **R8 not met:** 46.2 kg against 45 kg (43.2 kg before); the coupler, fixings and fittings add 3.0 kg. Proposed, awaiting Amish (register item 1).
- R3 still at risk: 38.7 N felt (was 36.6 N, target 40 N); winding 96 °C. R6 still at risk: 93 N dry, 111 N wet. R7 at risk.
- Range 24.5 km; hitch load 7.5 kg (window 32 mm ahead to 57 mm behind the deck centre); drawbar factor 4.3 at the front bushing; width 960 mm (972 mm over the motor cable); BOM $997 against $1,000.

### Proposed, awaiting Amish

See `docs/06-design-decisions.md`: R8 response (recommend relaxing to 47 kg for the prototype), key switch and charge port position (recommend the enclosure's right wall), coupler damping (recommend friction washers for the prototype), updating the appearance model and renders, render styling and composition (from 2026-09-26), and O1 and O2 (no recommendation).

### Stale media (made on Amish's Mac, not regenerated here)

`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png` and `media/social-preview.png` show the concept's coupler, load cell guard, top-opening enclosure with a window and harness, so they are stale. `cad/src/product_model.py` still builds from `build_parts()` (same group names) but its appearance parts follow the concept.

### Safety

The coupler adds pinch points at the fork slot, the side window and the lever cheeks; the build plan has safety stops for welding, tube bending, the battery, first motor power, hitching and the first loaded roll (private ground only). The overload pin now protects the load cell. No change to the safety case.

### Problems and notes

- `.kit/drawing.py` `project_views` still fails on this model's degenerate edges; the repo keeps its own `safe_project_views` in `cad/src/sheets.py`, now also repairing collapsed arcs. A kit fix is suggested.
- In `.kit/build_views.py` sketches, the "Front view" label is the side elevation for this trailer (kit naming), as noted on 2026-09-25.

### Recommended next step

Amish reviews CGM-DDR-003 and decides register items 1 to 4. TRL 4 (building to this plan) stays on hold.

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to "fix the weaker sources." Links in the README sections Concept rationale to What sparked the idea were checked; the three uncited country rows were rewritten or replaced with cited rows, and trade-press price sources were replaced with the manufacturer's page.

| Item | Old source | New source |
| --- | --- | --- |
| Netherlands row | None (uncited claim about cargo-bike habit and bridges) | KiM Netherlands Institute for Transport Policy Analysis, *Cycling Facts 2023* (1.3 bicycles per person, 28 % of journeys, cargo bikes 2 % of new e-bike sales); row rewritten to match |
| Kenya and East Africa row | None | Replaced by Uganda and East Africa, citing the World Bank case study by Malmberg Calvo (1994), SSATP Working Paper 12 (bicycle traders with about 100 kg loads pushing up hills) |
| Colombia and Andean cities row | None | Replaced by Colombia (Bogotá), citing the Secretaría Distrital de Movilidad's 2023 mobility survey release (886,655 daily bicycle trips, 7 %) |
| United States row, cargo e-bike price | The Inertia (review) and Notebookcheck (trade press) | Rad Power Bikes RadWagon 5 product page ($2,399); the unverified $4,999 Tern figure removed |
| India row | Street Vendors Act only; uncited claim about daily hand-cart and bicycle use | Uncited clause removed; row now states only what the Act supports |
| CGM-PRB-001 cost of alternatives | The Inertia and Notebookcheck | Rad Power Bikes product page; CGM-PRB-001 v0.3 to v0.4 |

Kept and re-checked: European Environment Agency transport indicator, WHO ambient air quality fact sheet, and the 2013 CycleLogistics baseline study (Reiter and Wrighton, FGM-AMOR, EU IEE grant IEE/10/277), which is the primary report (hosted by cargobike.jetzt). Kept but not re-fetched this session: Carla Cargo's own eCARLA page, India Code (Street Vendors Act, 2014) and Cornell LII (15 U.S.C. 2085). No budget change.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now decided by Amish, 2026-09-25: go with recommendation, and recorded in `docs/decisions/0002-recommendations-accepted.md` (CGM-DDR-002 v0.1). TRL stays at 3; TRL 4 remains on hold.

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| D11 | R8 relaxed to 45 kg for the first prototype; straps or mesh side boards kept as a later weight option | R8 40 kg; 43.1 kg, not met | R8 45 kg; 43.2 kg, met on paper |
| D12 | Keep the 250 W motor, add thermal derating and state a use limit of about 300 m of continuous 8 % climbing; confirm motor constants from a datasheet | R3 at risk; derating only suggested | R3 restated with the derating rule and use limit; derating starts after about 336 m [C10]; felt pull rises toward about 114 N on an endless climb; datasheet check on hold (TRL 4 part selection); R3 still at risk |
| D13 | 180 mm rotors with metallic pads | 160 mm rotors; push 100 N dry, 119 N wet; rotor rise 166 K on 8 %; BOM $969 | 180 mm rotors; push 92 N dry, 110 N wet; rotor rise 129 K; BOM $979; R6 still at risk in the wet |
| D14 | Keep G = 2 to 6 on paper; set the top gain once hitch joint stiffness is known | Open | Decided; the stiffness measurement is TRL 4, on hold; no design change |

Files changed:

- `cad/src/model.py`: `rotor_d` 160 to 180 mm; `cad/step/` and `cad/stl/` re-exported.
- `cad/src/sheets.py` and `cad/drawings/CGM-DWG-001.svg`, `.pdf`, `.png`: Rev P1 to P2 (rotor note and revision row).
- `bom/bom.csv` item 9: $20 to $25 per wheel, 180 mm rotors, metallic pads; `bom/bom-notes.md` updated. Total $969 to $979; `budget_usd` stays $1,000.
- `docs/04-calcs/sizing.py` and `01-sizing.md`: CGM-CAL-001 v0.1 to v0.2 (rotor mass and area scaled, lever kept at 7.7:1, brake gain 6.9 to 7.8, new [C10] derating check, R8 at 45 kg, results table).
- CGM-REQ-001 v0.3 to v0.4 (R8 45 kg, R3 restated); CGM-PRC-001 v0.3 to v0.4; CGM-DDR-001 v0.1 to v0.2 (R8 note points to DDR-002); new CGM-DDR-002 v0.1. CGM-PRB-001 unchanged at v0.3.
- `project.yaml`: DDR-002 added to `trl_evidence`; budget, pitch and problem unchanged; `trl: 3`, `trl_target: 3`.
- `README.md`: new sections Concept rationale, Burning platform, Where it could be used and What sparked the idea (the 2013 CycleLogistics baseline study); Concept paragraph and key components updated.
- `cad/src/concept_media.py` key figures ($979, 180 mm brakes); all media, drawings and `docs/pdf/` regenerated with the designmolecule.com footer. Temporary `media/_views*` folders deleted.

### Requirement status (CGM-CAL-001 v0.2)

Nine met (seven on paper, two by design), three at risk, none not met, two not verifiable at TRL 3.

| ID | Status | Value against target |
| --- | --- | --- |
| **R3 hills** | **At risk** | 36.6 N felt (40 N); winding about 95 °C against 100 °C after 300 m on assumed constants; derating beyond about 336 m |
| **R6 braking** | **At risk** | 92 N push dry, about 110 N wet (100 N); cut about 60 ms |
| **R7 hitch fit** | **At risk** | Axle stresses pass; thru-axle threads vary; nutted axles need adapters |
| R1, R2, R4, R8, R9, R10, R12 | Met on paper | 0.84 m², factor 1.6; 24.9 km; 6.2 to 6.6 N; 43.2 kg (45 kg); 960 mm, 2.52 m; 7.8 kg; $979 |
| R5, R14 | Met by design | 250 W, tension only, 25 km/h, no throttle; flag top 1,570 mm |
| R11, R13 | Not verifiable at TRL 3 | Datasheet items; 60 ms fault path on paper |

### Still awaiting Amish

1. **O1, first users and region** for co-design. No recommendation; Proposed, awaiting Amish.
2. **O2, road legality** of a motorized bicycle trailer in the first target country. No recommendation; Proposed, awaiting Amish.

### Cross-repo actions

None. The four decisions affect CargoMule only. (The SwapCell fleet variant under CGM-DDR-001, D2 is unchanged and not designed at TRL 3.)

### Safety

The safety sections stay in the README, precis and calculation note. New points: the motor derating means assist fades near the top of long climbs, so riders must be warned of the use limit; wet braking still gives about 110 N of push; descents still need a speed limit.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Decided but on hold: the motor datasheet and bench thermal check (D12) and the hitch joint stiffness measurement that settles the top gain setting (D14). No tests, build procedures, purchasing lists, firmware or PCB files were created.

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

Update: items 3 to 6 were decided by Amish, 2026-09-25: go with recommendation (CGM-DDR-002). See the session above.

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

Update: all items below that carried a recommendation were decided by Amish, 2026-09-25: go with recommendation (CGM-DDR-001). Item 8 had none and stays open (O1).

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

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was added

`cad/src/product_model.py` exposes `product_parts()` (80 parts: 60 shell, 9 internal, 2 accessory, 9 context), `TITLE` and `RENDER_VIEWS` (hero, exploded, and a detail view of the trailer alone from the drawbar side). It reuses PARAMS, derived(), drawbar_points() and build_parts() from `cad/src/model.py`; the chassis frame, drawbar and harness are the model.py solids, and every other part keeps the model.py position and main dimensions. It adds:

- Deck and boards: rounded plywood deck with two aluminium tie-down tracks; off-white side and end boards with hand slots, aluminium corner caps, teal trim bands and a raised CARGOMULE badge on each side.
- Drawbar load cell: S-shaped cell body in the model.py envelope, pinned clevises, gauge plugs and cable, under a clear polycarbonate guard with teal end rings.
- Overrun coupler: sleeve, rubber gaiter over the sliding end, filleted damper housing, brake lever and equalizer, bolts and brake cables to the calipers.
- Hitch: filleted axle plate and nut, joint with a ribbed rubber boot, arm, locking pin with a green lock indicator, and the secondary safety strap to the bicycle's chainstay.
- Wheels and brakes: tyres, rims and laced spokes as separate parts; the 250 W hub motor shell with spoke flanges, a teal cover ring, bolts and cable exit; the idler hub; slotted 180 mm rotors and calipers.
- Enclosure: closed, filleted galvanized box with a parting seam, louvre vents, screws, cable glands, a warning label, a clear inspection window onto the pack, and on its front face the key switch, the knurled assist gain dial with its 2 to 6 scale, a lit green status light and a capped charge port. Inside: the pack with its label, a finned controller and the control board with components.
- Lights and stand: lit red rear lights in black housings, amber side and drawbar reflectors, a fabric safety flag on its pole, and the stand leg with a rubber foot.
- Accessory: the off-trailer charger and lead (BOM 17), shown in the exploded view only.
- Context (not in the BOM): a simple bicycle whose rear axle sits at the hitch height (340 mm), the shared clay mannequin in the "ride" pose placed from its landmarks so the feet meet the pedals, the seat meets the saddle and the hands meet the grips, and a small strapped load of a crate and two cartons.

`README.md` now shows `media/render-hero.png` and links `media/render-exploded.png`; the orchestrator produces both files. Matplotlib self-check previews were made in `/tmp/cargomule-prod/` (outside the repo).

### Differences from model.py (Proposed, awaiting Amish)

1. **Closed enclosure with a parting seam.** model.py draws an open-top box so the section views show the pack; BOM line 10 calls for a lockable lid. The appearance model closes the box and shows a seam 28 mm below the top, but the top sits against the frame rails, so a top lid could not open in place. Proposed, awaiting Amish. Recommendation: specify a bolted bottom or front access panel (or a removable box on slides) at the next design step, and keep the lock on the key switch.
2. **Controls on the enclosure front face.** The key switch, gain dial, status light and charge port are placed on the face toward the drawbar, where the rider can reach them at a stop. The concept does not yet say where they go. Proposed, awaiting Amish. Recommendation: accept this location.
3. **Clear guard over the load cell and an inspection window on the enclosure.** Neither is in the BOM. The guard shields the cell and its cable from spray and stones; the window lets the render show the pack. Proposed, awaiting Amish. Recommendation: adopt the guard (a short polycarbonate tube, a few dollars under BOM line 5), and treat the enclosure window as render-only: a plain steel side is cheaper, keeps the pack out of the sun and keeps the enclosure robust.
4. **Finish and small parts.** Graphite powder coat for the frame (BOM line 1 says painted), off-white faced side boards with hand slots and name badges (BOM line 2 says sealed plywood), deck tie-down tracks in place of loose eyes on the deck, a rubber gaiter on the coupler and a drawbar reflector. Proposed, awaiting Amish. Recommendation: keep the plywood and paint of the BOM for the prototype; treat the faced boards, tracks and badges as finished-product styling.
5. **Hero composition.** With the bicycle and rider in the scene the trailer fills about half of the hero frame. The views cannot frame a single subsystem, so the "detail" view shows the trailer alone from the front left, with the load cell, coupler and hitch nearest the camera. Proposed, awaiting Amish. Recommendation: accept; if a tighter shot of the load cell is wanted, add a close-up camera option to the kit renderer rather than changing the model.

### Status

This is an appearance model only: no tolerances, no fabrication detail, nothing past TRL 3. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold. model.py, the BOM and the other documents were not edited.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.
