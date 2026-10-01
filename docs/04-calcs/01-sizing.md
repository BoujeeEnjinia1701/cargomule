---
doc_id: CGM-CAL-001
title: CargoMule sizing calculations
project: CargoMule
doc_type: Calculation
version: "0.4"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (mass and balance, assist forces, motor and heating, loop stability, energy, braking, structure, geometry, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). 180 mm rotors with metallic pads, R8 relaxed to 45 kg, thermal derating check [C10], results table updated
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (CGM-DDR-003). Made-part masses from the model's volumes; coupler, enclosure and fixings added; R8 now not met at 46.2 kg; drawbar moment taken at the coupler's front bushing; all figures rerun
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
---

# CargoMule sizing calculations

On paper, CargoMule meets eight of its fourteen requirements, has three at risk, misses one and has two that cannot be verified at TRL 3. Version 0.3 reruns every figure for the constructable design of CGM-DDR-003: the made parts' masses now come from the model's own volumes, and the coupler, enclosure, fixings and board fittings that make the design buildable are counted. The empty trailer rises from 43.2 kg to 46.2 kg, so **R8 (45 kg) is not met**; the response is proposed to Amish in CGM-DDR-003 (A1). Version 0.2 applied Amish's decisions of 2026-09-25 (CGM-DDR-002): R8 relaxed to 45 kg, 180 mm rotors with metallic pads, and a thermal derating rule with a stated use limit. The three at risk are the hill climb (R3), where the motor delivers the force but its winding reaches about 96 °C against a 100 °C limit after the 300 m design climb, on assumed motor constants; braking (R6), where the push is 93 N dry but about 111 N with wet pads; and hitch fit (R7). The calculations also changed three parts of the TRL 2 concept: the assist filter (the TRL 2 filter was unstable), the drawbar shape (a straight drawbar clears the bike's tyre only up to about 10°) and the deck thickness. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They are not a substitute for the braking, hitch and structural tests of EN 15918 or ASTM F1975, or for electrical safety checks on the battery and controller. Nothing may be ridden or towed on the strength of this note. See CGM-PRC-001, Safety.

## Scope and method

The note checks every requirement in CGM-REQ-001 v0.5 against the design in CGM-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and derived dimensions, and builds the model's components to take the volumes of the made steel parts, so the deck, frame, drawbar, wheel and enclosure dimensions used here are the ones in the STEP files and in drawing CGM-DWG-001. The script also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design load case is 150 kg of payload centered on the deck, the trailer's own mass and a towing bicycle with rider of 100 kg, on a dry paved road. The design route is a 10 km round trip with 120 m of climbing, 120 m of descent and 20 stops.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Masses | Steel 7,850 kg/m³, plywood 550 kg/m³, aluminium 2,700 kg/m³; made steel parts from the model's volumes, plywood from its sizes; bought parts from typical catalog values (Table 2) | To confirm by weighing parts |
| Resistance | Rolling coefficient 0.010 for 20 x 2.15 in tyres; extra drag area 0.10 m²; air 1.2 kg/m³ | Handbook ranges; the trailer rides partly in the rider's wake |
| Control | Motor force = G x (pull minus a 3 N deadband); G = 4 default, 2 to 6 selectable (CGM-DDR-001, D5) | Deadband covers load cell zero drift and joint hysteresis [D7] |
| Motor | 250 W geared front-style hub, 20 in wheel; DC-equivalent model with no-load speed 230 rpm at 38.4 V, winding resistance 0.35 Ω, gear efficiency 90 %, 8 W iron and friction loss | Typical small geared hubs; to confirm from the datasheet |
| Controller | 15 A pack current limit, 30 A phase current limit, 95 % efficient, 20 ms current-loop response | Typical 36 V sine-wave controller settings |
| Motor heating | One thermal mass: 1.2 K/W winding to air, 700 J/K; 30 °C air; 100 °C limit (a margin below the usual 120 to 130 °C winding class, to protect the nylon gears and Hall sensors) | Assumed; no datasheet values yet |
| Pack | 384 Wh, 90 % usable; cell charging 96 %; charger 90 % | As at TRL 2 |
| Loop | Bike and rider 100 kg; drawbar stiffness swept 20 to 500 N/mm; structural damping ratio 0.05; 80 Hz sampling | Stiffness of the hitch joint is not known, so it is swept |
| Brakes | Metallic pads, friction 0.40 dry, 0.30 wet; caliper clamp 4 x cable tension; rotor effective radius 82 mm on a 180 mm rotor (72 mm on the earlier 160 mm rotor); rotor 0.157 kg, 0.033 m² cooled at 60 W/m²K, scaled from a 0.12 kg, 0.025 m² 160 mm rotor by braking annulus area; coupler lever kept at 7.7:1 | Typical cable disc brakes; to confirm |
| Structure | S235 frame (yield 235 MPa), S355 drawbar (355 MPa), axle steel 650 MPa, plywood 10 MPa allowable; 2 g bump on the deck, 3 g on the tongue; ultimate case 1 g of the loaded trailer through the hitch | Screening values, not a fatigue analysis |

## A. Mass and balance (R8, R10)

The frame, from the model's volumes, is about 13.0 kg: the 30 x 30 x 1.5 mm box section rails and crossmembers 7.55 kg, nose bars 0.53 kg, the wheel arch frames that carry the outer dropouts with the tie-down eyes 2.74 kg, and the dropout plates with their caliper tabs 1.93 kg, plus 0.25 kg of weld metal, rivet nuts and end caps [A1].

*Table 2. Mass by part [A2], [A3].*

| Part | Mass |
| --- | --- |
| 1 Chassis frame | 13.01 kg |
| 2 Deck, 12 mm plywood; removable 9 mm side boards; aluminium corner pieces and brackets | 5.54; 2.82; 0.49 kg |
| 3 Drawbar, 38 x 2.5 mm, bent | 2.95 kg |
| 4 Hitch; 5 load cell, rod end, clevis and amplifier | 0.60; 0.45 kg |
| 6 Coupler housing, spring cage, end cap and brake lever (steel); coupler internals | 2.53; 0.40 kg |
| 7 Hub motor wheel; torque arm; 8 idler wheel | 4.30; 0.10; 1.90 kg |
| 9 Two disc brakes, 180 mm rotors; cable splitter and third cable | 0.87; 0.12 kg |
| 10 Enclosure and door, 0.8 mm steel; 11 pack; 12 controller; 13 board; 14 harness | 3.03; 4.20; 0.40; 0.15; 0.50 kg |
| 15 Lights and flag; 16 stand; 18 hardware and paint | 0.50; 0.58; 0.80 kg |
| **Empty trailer** | **46.2 kg (102 lb)** |

- **R8 is not met:** 46.2 kg against the 45 kg target that Amish set on 2026-09-25 (CGM-DDR-002); the target was 35 kg at TRL 2 and 40 kg under CGM-DDR-001 [A3]. Version 0.2 gave 43.2 kg. The 3.0 kg rise comes from designing the parts the concept only estimated: the coupler (2.9 kg in all, against 1.6 kg), the dropout plates' caliper tabs, the board fittings, a larger enclosure with a door, the torque arm and the brake cable splitter (CGM-DDR-003). Without the side boards the trailer weighs 43.4 kg. The response (relax R8 for the prototype, take the straps or mesh option now, or find mass elsewhere) is proposed to Amish in CGM-DDR-003, A1.
- **Loaded mass** in the design case is 196.2 kg [A4].
- **Hitch down load.** The empty trailer's mass center is 1,675 mm behind the bike axle and 362 mm high [A5]; it moved 33 mm rearward because the enclosure now hangs between the crossmembers at 1,600 and 1,920 mm. With the axle 20 mm behind the deck center, the hitch carries 5.9 kg empty and 7.5 kg with the payload centered [A6]. R10 (3 to 10 kg) is met. The axle moved forward 30 mm from the TRL 2 layout, which would give 10.4 kg with this mass breakdown [A6].
- **Payload placement.** The hitch load changes by 7.8 kg per 100 mm of payload shift. It stays within 3 to 10 kg only while the payload center sits between 32 mm ahead of and 57 mm behind the deck center, and the drawbar unloads completely with the payload center 96 mm behind it [A7]. This is inherent in a two-wheel trailer carrying four times its own mass, and it needs a clear loading mark on the deck.
- **Tipping.** The loaded mass center is 521 mm high, giving a static rollover threshold of 0.77 g on the 800 mm track; a 5 m radius turn at 15 km/h needs 0.35 g, a margin of 2.2 [A8].

## B. Resistance and felt pull (R4)

- **Flat.** The loaded trailer's resistance is 19.4 N at 5 km/h, 20.8 N at 18 km/h and 21.1 N at 20 km/h. With G = 4 and the 3 N deadband, the rider feels 6.3 to 6.6 N [B1]. R4 (15 N or less) is met. The deadband adds about 2.4 N to the 4 N quoted at TRL 2.
- **8 % climb.** At 8 km/h the trailer needs 173.6 N (154.0 N grade, 19.3 N rolling). Unassisted, that is 386 W on top of the rider's own climb [B2].

## C. Motor, controller and heating (R3, R5)

The motor model has a no-load speed of 230 rpm at 38.4 V, which is 22.4 km/h on the 20 in wheel, and gives 1.43 N·m per phase ampere at the wheel [C1].

- **Force on the climb.** On 8 % at 8 km/h the motor is asked for 136.4 N (35.2 N·m) and, at the 15.0 A pack limit, delivers 134.9 N at 24.3 A phase current. Output is 300 W, losses 247 W: the motor runs at about 55 % efficiency at this low speed and high torque [C2]. The rider feels 38.7 N [C3], within R3's 40 N but with only 1.3 N to spare.
- **Current limit sensitivity.** The result depends on the controller settings. With a 12 A pack limit the rider would feel 59 N, and with 10 A, 74 N [C4]. A controller with a 15 A battery limit and at least a 25 A phase limit is therefore part of the design.
- **The rider's own climb.** Even with assist, the rider must lift their own bike and body: about 273 W in all at 8 km/h. A rider giving 150 W climbs at about 4.4 km/h, at which the felt pull is about the same [C5]. R3's 8 km/h is reached only by a fit rider; the felt pull target is met at any speed.
- **Heating.** After flat cruising the winding sits at about 52 °C. The 300 m design climb takes 135 s and brings it to about 96 °C against the 100 °C limit; a 1,000 m climb would reach about 175 °C [C6]. The steady rise, if the climb never ended, is 297 K [C7]. **R3 is at risk:** the force is met with 1.3 N to spare, and the thermal margin is 4 K on assumed motor constants.
- **Thermal derating (CGM-DDR-002).** Amish decided to keep the 250 W motor, add thermal derating and state a use limit. At full assist the winding reaches 100 °C after about 149 s, or 331 m of 8 % climbing at 8 km/h. From there the firmware must reduce motor current so the winding stays at or below 100 °C: with 58 W of allowed loss the motor gives about 57 N, and the rider's felt pull rises toward about 117 N on a climb that never ends [C10]. The stated use limit is therefore about 300 m of continuous 8 % climbing with full assist; beyond it the assist fades rather than stops. The motor constants still need a datasheet, which comes with part selection at TRL 4 (on hold).
- **Top of the speed range.** At 20 km/h on a nearly empty pack (36.0 V) the motor can still give the 14.5 N asked [C8], so R4 holds to 20 km/h. The 25 km/h assist cut-off in R5 sits above the motor's 22.4 km/h no-load speed, so the firmware limit is a backstop [C9]. R5 is met by design: the motor is rated 250 W continuous, the peak output of about 300 W on climbs is within the usual rating convention for pedelec motors, and there is no throttle.

## D. Assist loop stability (R4, R6, R13)

The drawbar, hitch joint and load cell form a spring between two masses (bike and rider, 100 kg; loaded trailer, 196 kg). The controller feeds the measured pull back as motor force through a filter and a delay of 38.8 ms (80 Hz sampling, half-sample hold, 20 ms controller current loop) [D1]. The script finds the critical gain, above which the loop oscillates, from the roots of the closed-loop characteristic polynomial (third-order Padé model of the delay).

*Table 3. Critical gain G by filter and drawbar stiffness [D2].*

| Filter | 20 N/mm | 50 N/mm | 100 N/mm | 200 N/mm | 500 N/mm |
| --- | --- | --- | --- | --- | --- |
| TRL 2: 1st order, 2 Hz | 0.5 | 0.8 | 1.5 | 3.9 | 8.1 |
| 2nd order, 1 Hz | 5.4 | 12.2 | 15.2 | 16.8 | 17.7 |
| **Chosen: 2nd order, 0.7 Hz** | **11.7** | **19.7** | **22.7** | **24.2** | **25.1** |

- **The TRL 2 filter would oscillate.** With a first-order 2 Hz low-pass the loop goes unstable above G = 0.5 at the softest stiffness, far below the default G = 4 [D3].
- **Chosen filter.** A second-order (Butterworth) 0.7 Hz low-pass is stable for G = 2 to 6 at every stiffness swept. Its gain margin is 2.9 (9.3 dB) at the default G = 4 and 2.0 (5.8 dB) at G = 6 [D3]. The G = 6 setting is just under the usual 6 dB margin at the softest stiffness. Amish decided on 2026-09-25 to keep 2 to 6 on paper and to settle the top setting once the hitch joint stiffness is measured, which is TRL 4 work and on hold (CGM-DDR-002).
- **Cost of the filter.** The pedal-stroke ripple at 60 rpm cadence (2 Hz) passes at 12 %, against 71 % for the TRL 2 filter, but the assist takes about 0.47 s to reach 90 % after a step in pull [D4]. When pulling away, the rider carries most of the trailer for about half a second.
- **Stiffness.** Bending of the drawbar's offset runs alone gives an axial stiffness of about 169 N/mm; the hitch joint and load cell are in series with it and softer, so the 20 to 500 N/mm sweep brackets the real value [D5].
- **Compression cut.** The assist cut must not wait for the filter. A fast path on the raw signal (three consecutive samples below -20 N at 80 Hz, 2 ms processing, 20 ms current decay) zeroes the motor in about 60 ms, within the 100 ms of R6 and R13 [D6].
- **Load cell.** A 1 kN S-type cell at 2 mV/V drifts about 1.0 N over 50 K; the 3 N deadband covers this plus joint hysteresis [D7]. The cell needs a mechanical overload stop, since the ultimate hitch load (section G) is about twice its range. In the constructable design the overload pin through the drawbar rests 0.5 mm behind the closed end of the slot on the coupler housing, so a pull beyond the cell's travel bears on the housing (CGM-DDR-003, P2).

## E. Energy and range (R2)

The TRL 2 estimate charged rolling resistance over the whole route and assumed 75 % drive efficiency throughout. This version splits the route and uses the motor model's efficiency at each speed.

*Table 4. Energy on the design route [E1] to [E3].*

| Segment | Pack energy | Rider energy |
| --- | --- | --- |
| Flat, 5.2 km at 18 km/h | 27 Wh | 9 Wh |
| Climbs, 2.4 km at 5 % and 10 km/h | 96 Wh | 17 Wh |
| Descents, 2.4 km at 5 % (gravity exceeds rolling; the overrun brake holds speed) | 0 Wh | 0 Wh |
| 20 stops from 18 km/h (13.6 Wh of kinetic energy, 80 % from the motor at 60 %) | 18 Wh | |
| **Design route** | **141 Wh, 14.1 Wh/km** | |

- **Range** on the design route is 24.5 km from 346 Wh usable [E3]. R2 (20 km) is met. On flat roads with few stops the pack gives about 5.7 Wh/km and 61 km [E4]. The TRL 2 method gives 14.8 Wh/km and 23.4 km [E5], close to this result, so the TRL 2 claim of about 24 km stands.
- **Energy flow** for Figure 2 of the precis: mains 163 Wh, into the pack 147 Wh, pack output 141 Wh, motor at the wheel 92 Wh, rider 29 Wh, trailer work 121 Wh; losses 16 Wh in the charger, 6 Wh in cell charging and 49 Wh in the controller and motor [E6].
- **Charging** takes about 3.0 h: 10 Ah at 4 A plus about 0.5 h of constant-voltage charging [E7].

## F. Braking (R6)

- **Need.** At 20 km/h the loaded trailer carries 3.03 kJ, about twice the bicycle and rider's 1.54 kJ. To slow at 3 m/s² it needs 589 N; with the bike taking no more than 100 N of push, the trailer brakes must give 489 N [F1].
- **Brakes.** Amish decided on 2026-09-25 to fit 180 mm rotors with metallic pads (CGM-DDR-002; v0.1 used 160 mm rotors). The 489 N is 244 N per tyre, 769 N at the 82 mm rotor radius and 961 N of pad clamp, which needs 240 N of cable tension per caliper [F2]. This is well within the range of cable disc brakes.
- **Coupler.** The 30 N preload spring and the 7.7:1 lever are kept; in the constructable design the lever pulls one cable to a splitter that feeds both calipers (CGM-DDR-003, P4). That lever was sized to give 100 N of push dry on 160 mm rotors (gain 6.88); with 180 mm rotors the gain rises to 7.83 N per newton of compression above the preload, and the dry push at 3 m/s² is 93 N. Taking up pad clearance and cable stretch uses 27 mm of the 50 mm stroke [F3].
- **R6 is still at risk.** With wet pads (friction 0.30) the push is about 111 N, against 121 N with 160 mm rotors and the 100 N target [F4]. Closing the rest of the gap would need a higher lever ratio (more stroke) or wet-weather pad data. The 100 ms assist cut is met on paper (section D). Stopping distance from 20 km/h at 3 m/s² with a 1 s reaction is 10.7 m [F5].
- **Descents.** On 8 % at 20 km/h the overrun brake settles with the rider feeling about 42 N of push, while the trailer brakes absorb 516 W, 258 W per rotor; the rotor's temperature rise tends to about 131 K with a 37 s time constant. On 10 % at 25 km/h this becomes 441 W per rotor and about 225 K [F6]. Long, steep descents still risk pad fade and heat flowing into the hub motor, which carries the left rotor; a descent speed limit is still needed.

## G. Structure (R1, hitch safety)

- **Side rails.** At a 2 g bump the rails see 230 N·m over the axle, where the deck overhangs by 580 mm, giving 149 MPa in the 30 x 30 x 1.5 mm box, a factor of 1.6 on S235 yield [G1]. This passes as a screen; fatigue at the welded dropouts is not assessed.
- **Wheel offset.** Each wheel reacts 1,852 N at 2 g, 50 mm outboard of the side rail; the 93 N·m of torsion is carried by the axle crossmember at 60 MPa [G2].
- **Drawbar.** The 38 x 2.5 mm S355 tube carries the tongue load at 3 g as 193 N·m where the coupler's front bushing holds it, 83 MPa, a factor of 4.3 [G3]. (Version 0.2 took the moment at the old nose point, 300 mm further back: 271 N·m and a factor of 3.0.) In the ultimate case (1 g of the loaded trailer, 1,925 N, through the hitch, as when the bike stops against an obstacle with the trailer brakes failed), the offset run 265 mm off the load line sees 510 N·m and 227 MPa, a factor of 1.6 [G4]. In service, pulling away up the 8 % grade without assist gives 31 MPa [G5]. The TRL 2 drawbar (32 x 2 mm, straight) was upsized when the offset was added.
- **Hitch on the axle end.** At the ultimate load and a 12 mm lever, a 10 mm hollow quick-release axle sees 270 MPa (factor 2.4) and a 12 mm thru-axle 170 MPa (factor 3.8). The secondary safety strap should be rated 3.9 kN or more [G6].
- **Deck.** The 12 mm plywood deck spans at most 330 mm between crossmembers. A uniform 2 g payload (3.5 kPa) gives 2.0 MPa, and a 75 kg point load at mid-span on a 300 mm strip gives 8.4 MPa against 10 MPa allowable. A 9 mm deck would give 15.0 MPa for the point load [G7], so the deck stays at 12 mm.

R1 is met on paper: the deck is 0.84 m² and every member passes the screen with a factor of 1.6 or more.

## H. Geometry and fit (R1, R7, R9, R14)

- **Deck** 1,200 x 700 mm, 0.84 m² [H1].
- **Size.** Overall width 960 mm over the arch frames, 972 mm over the motor cable clipped outside the left arch, and hitched length 2,520 mm from the bike's rear axle [H2]; R9 (1,000 mm and 2.6 m) is met. The hitch plate adds 32 mm ahead of the axle, for 2,552 mm overall on drawing CGM-DWG-001.
- **Wheel installation.** The tyre clears the side rail by 22.5 mm. The 100 mm hubs sit between dropout faces 350 and 450 mm from the center line, the outer dropout hanging from an arch frame whose top is 546 mm above the ground. The enclosure has 208 mm of ground clearance [H3].
- **Flag** top at 1,570 mm [H4]; R14 is met.
- **Articulation.** A straight drawbar from the left axle end would touch the bike's rear tyre after only about 10° of yaw. The drawbar now runs out 360 mm to the left of the center line before turning in, which allows 55.5° with the bike yawed toward the drawbar and 105.5° the other way [H5]. At 55.5° a steady turn is possible down to about 1.3 m radius at the trailer axle; tighter left turns need the rider to swing wide [H6].
- **R7 is at risk.** The axle loads pass (section G), but a thru-axle hitch needs a matching hitch axle for each thread pitch and length (M12 x 1.0, 1.5 or 1.75 and several lengths), and nutted axles, some hub gears and some rear-motor e-bikes need adapters. Hitch and unhitch time (30 s) is not verifiable on paper.

## I. Cost (R12)

The BOM has 18 lines totalling $997 (the estimated cost of the constructable design) against the $1,000 value-engineering target `budget_usd`, $3 under it [I1]. The 180 mm rotors and metallic pads added $10 to the $969 of v0.1, and the parts that make the design buildable added $18 (board fittings, coupler parts, rivet nuts; CGM-DDR-003). R12, redefined against the $1,000 value-engineering target by CGM-DDR-001 D1 (a hypothetical control target, not a limit), is within the target with almost no margin.

## J. Results against every requirement

*Table 5. Requirement status from this note [J].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R8 | Light enough to handle | 46.2 kg empty (43.4 kg without side boards) | 45 kg or less (relaxed, CGM-DDR-002) | **Not met** (response proposed, CGM-DDR-003 A1) |
| R3 | Assist on hills | 38.7 N felt; winding 96 °C after 300 m; derating holds 100 °C beyond about 331 m | 40 N or less; no over-temperature (100 °C) | **At risk** (4 K thermal margin on assumed constants) |
| R6 | Trailer brakes itself | 93 N push dry, 111 N wet; cut 60 ms | 100 N or less; 100 ms | **At risk** (wet pads, fade on long descents) |
| R7 | Hitch to common bicycles | Axle stresses pass; thru-axle threads vary | QR and 12 mm thru-axle, 30 s, no wiring | **At risk** |
| R1 | Carry the payload | 0.84 m²; least structural factor 1.6 | 150 kg on 0.8 m² or more | Met on paper |
| R2 | Range per charge | 24.5 km | 20 km or more | Met on paper |
| R4 | Near-zero added load on the flat | 6.3 to 6.6 N; stable, G crit 11.7 | 15 N or less at 5 to 20 km/h | Met on paper |
| R9 | Fit bike paths and doors | 960 mm wide (972 mm over the motor cable), 2.52 m long | 1,000 mm; 2.6 m | Met on paper |
| R10 | Stable hitch load | 7.5 kg centered | 3 to 10 kg | Met on paper (narrow loading window) |
| R12 | Affordable | $997 | $1,000 value-engineering target (redefined) | Within the value-engineering target ($3 under) |
| R5 | Stay within pedal-assist limits | 250 W rated; tension only; 25 km/h; no throttle | As stated | Met by design |
| R14 | Be seen | Flag top 1,570 mm; lights and reflectors | 1,500 mm or more | Met by design |
| R11 | Weather and temperature | Datasheet items (IP65, IP54, BMS charge block) | As stated | Not verifiable at TRL 3 |
| R13 | Fail safe | 60 ms fast path on paper | 100 ms | Not verifiable at TRL 3 |

Counts: 8 met (6 on paper, 2 by design), 3 at risk, 1 not met (R8), 2 not verifiable at TRL 3. In v0.1, R8 was not met at 43.1 kg against 40 kg; in v0.2 it was met at 43.2 kg against 45 kg.

## Checks against the TRL 2 figures

| TRL 2 claim (CGM-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| Empty mass about 38 kg | 46.2 kg (constructable design) | Precis corrected |
| Felt pull about 4 N flat, 33 N on 8 % | 6.3 to 6.6 N, 38.7 N (with the 3 N deadband) | Precis corrected |
| Motor about 290 W, 34 N·m, about 10 A | 300 W, 35.2 N·m asked, 24.3 A phase, 15.0 A pack | Precis corrected |
| Filter about 2 Hz | Unstable at G = 4; 0.7 Hz second order | Precis corrected |
| About 14 Wh/km, 24 km range, about 45 km flat | 14.1 Wh/km, 24.5 km, 61 km flat | Precis corrected |
| Mains about 163 Wh per trip | 163 Wh | Precis and Figure 2 corrected |
| Braking about 560 N; 460 N from the trailer | 589 N; 489 N (heavier trailer) | Precis corrected |
| Hitch load about 9 kg | 7.5 kg (axle moved forward 30 mm) | Precis corrected |
| About 910 mm wide, 2.5 m long | 960 mm (arch frames), 972 mm over the motor cable, 2.52 m | Precis corrected |
| Cost about $965 | $997 (180 mm rotors of CGM-DDR-002; fittings of CGM-DDR-003) | Precis corrected |
