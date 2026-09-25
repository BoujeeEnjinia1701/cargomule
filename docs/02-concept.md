---
doc_id: CGM-PRC-001
title: CargoMule design precis
project: CargoMule
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, control law, first-order numbers, braking, safety, media)
---

# CargoMule design precis

CargoMule is a two-wheel, 150 kg cargo trailer that hitches to a bicycle's rear axle and pushes itself. A load cell inside the drawbar coupling measures how hard the bicycle pulls, a small controller commands a 250 W geared hub motor in one trailer wheel to push with four times that force, and the rider feels about one fifth of the trailer's resistance. When the bicycle slows, the drawbar goes into compression: the controller cuts the motor and a mechanical overrun coupler applies disc brakes on both trailer wheels. First-order estimates give about 24 km per charge of a 384 Wh LiFePO4 pack on a hilly loaded route, about 33 N of felt pull on an 8 % grade, an empty mass of about 38 kg and parts costing about $965. The mass and the cost miss their targets, by about 3 kg and $65.

![Hero render](../media/hero.png)

*Figure 1. CargoMule hitched to an ordinary bicycle with a 150 kg load, and a 1.75 m person for scale. Trailer parts are colored; the bicycle and load are grey. Massing model, not for fabrication.*

## How it works

1. **Hitch.** A universal hitch clamps under the bicycle's left rear axle end (quick release or thru-axle) and joins the drawbar through a joint that allows pitch, yaw and roll, so the bike can lean and turn freely. Nothing else attaches to the bike and there is no cable.
2. **Sense.** Near the trailer end, the drawbar passes through a sliding coupler. The coupler's bushings carry bending and the tongue load; the axial force passes through an S-type load cell, so the cell reads only pull (tension) or push (compression). A 24-bit amplifier (HX711 class) samples at 80 Hz.
3. **Decide.** The control board filters the signal below about 2 Hz to remove the pulse of each pedal stroke and road bumps, then sets motor force to a gain G times the measured pull. With G = 4 the rider supplies 1/(1 + G), or 20 %, of the force needed to move the trailer. The board also reads wheel speed from the motor's Hall sensors and a key switch.
4. **Push.** A 36 V sine-wave controller drives a 250 W geared hub motor laced into the left 20 in wheel. The right wheel is an idler. Assist stops above 25 km/h, when the trailer stands still, and whenever the drawbar is not in tension.
5. **Brake.** When the bicycle brakes, the trailer's momentum pushes the drawbar into compression. Above a small threshold (about 20 N) the controller zeroes the motor within 100 ms. Further compression slides the coupler against a preloaded spring and damper and pulls cables to mechanical disc brakes on both wheels, as in a car trailer's overrun brake. The brakes work with the electronics off or failed.
6. **Store and charge.** A 12S LiFePO4 pack (38.4 V nominal, 10 Ah, 384 Wh) with its own BMS sits in a closed steel enclosure under the front of the deck, beside the controller and control board. It charges from a 43.8 V, 4 A charger off the trailer.

Sensing force at the drawbar is what lets CargoMule fit any bicycle without wiring: it does not need to know how hard the rider pedals, only how hard the bike pulls. It also gives braking detection for free, since a pushing drawbar means the bike is slowing.

![Energy flow](../media/flow.png)

*Figure 2. Energy for one 10 km loaded round trip with 120 m of climbing and 20 stops, in Wh. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

Table 1. Main components.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Chassis frame | Welded steel box section, 30 mm, deck frame with three crossmembers, A-frame nose, dropout plates | Steel or aluminium is proposed, awaiting Amish |
| 2 | Deck and side boards | 12 mm exterior plywood deck, 1,200 x 700 mm, removable 150 mm side boards | Tie-down points on the frame |
| 3 | Drawbar | Steel tube, two sections either side of the coupler, about 1.2 m | Offset to clear the bike's rear wheel |
| 4 | Universal axle hitch | Plate under the axle end with a three-axis joint (elastomer or ball) | QR and thru-axle adapters |
| 5 | Drawbar load cell and amplifier | S-type cell, about 1 kN (100 kg) range, pinned both ends, HX711-class amplifier | Reads axial force only |
| 6 | Overrun brake coupler | Sliding coupler on bushings, preload spring, damper, cable lever | Mechanical; works with power off |
| 7 | Hub motor wheel | 36 V, 250 W geared hub in a 20 in (ETRTO 406) wheel, disc mount | Left side |
| 8 | Idler wheel | 20 in wheel with a disc hub | Right side |
| 9 | Mechanical disc brakes | Two cable calipers, 160 mm rotors | Actuated by item 6 |
| 10 | Battery and electronics enclosure | Folded steel box, about 400 x 460 x 170 mm, vented, lockable | Under the deck front |
| 11 | Battery pack | 12S1P LiFePO4, 38.4 V, 10 Ah, 384 Wh, with BMS | Option: SwapCell pack (see Key design choices) |
| 12 | Motor controller | 36 V, 15 A, sine wave, torque-mode input, IP65 | Commanded by item 13 |
| 13 | Control board | Microcontroller, load cell input, Hall speed input, key switch, status LED | Firmware is a TRL 3 sketch at most |
| 14 | Wiring harness | Keyed waterproof connectors, 20 A fuse, key switch | |
| 15 | Lights, reflectors and flag | Rear red lights powered from the pack, side reflectors, flag on a 1.15 m pole | |
| 16 | Parking stand | Drop-down leg under the nose | Holds the drawbar level when unhitched |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section on the trailer's center line, showing the pack, controller and control board in the enclosure under the deck, and the load cell and overrun coupler in the drawbar.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions are listed in CGM-REQ-001: rolling resistance coefficient 0.010, extra drag area 0.1 m², drive efficiency 75 %, charger 90 %, cell charging 96 %, 90 % usable pack energy, gain G = 4.

### Mass and balance

Table 2. Mass estimate.

| Group | Estimate |
| --- | --- |
| Frame 11 kg, deck and boards 6 kg, drawbar, hitch, load cell and coupler 5 kg | about 22 kg |
| Wheels, motor and brakes | about 8 kg |
| Enclosure, pack, controller, board, harness | about 7.5 kg |
| Lights, flag and stand | about 1.0 kg |
| **Empty trailer** | **about 38 kg (84 lb); R8 (35 kg) not met** |
| Loaded trailer, design case | about 188 kg |
| Hitch down load, payload centered | about 9 kg (axle 50 mm behind the deck center; R10 met) |

An aluminium frame would save about 5 kg and meet R8, at higher cost and with welding that fewer workshops can do.

### Forces and assist

Table 3. Drawbar forces with G = 4 (rider feels 20 %).

| Case | Trailer resistance | Motor force | Felt by rider | Motor output | Requirement |
| --- | --- | --- | --- | --- | --- |
| Flat at 18 km/h | about 20 N (rolling 18.4 N, drag 1.5 N) | about 16 N | about 4 N | about 80 W | R4 (15 N) met |
| 8 % grade at 8 km/h | about 165 N (grade 147 N, rolling 18 N) | about 132 N | about 33 N | about 290 W, about 34 N·m at the 0.258 m wheel radius | R3 force (40 N) met |
| Starting, 0.5 m/s² | about 94 N plus rolling | about 90 N | about 22 N | | |
| Same 8 % grade, no assist | about 165 N | 0 | about 165 N, about 370 W extra at 8 km/h | | Why assist is needed |

On the 8 % climb the motor gives about 290 W, above its 250 W continuous rating. Geared 250 W hubs are commonly driven to peaks of 400 to 500 W by a 15 A controller, so a 300 m climb (about 2.5 min) is plausible, but motor heating is unverified (R3). Motor current is about 10 A at 38 V, within the 15 A controller limit.

The motor drives only the left wheel, so it applies a yaw moment of about 132 N x 0.425 m, about 56 N·m, on the steepest climb. The hitch reacts about 29 N of this sideways at a 1.95 m lever, and the tyres the rest. This should be small in practice but needs checking for handling (open question).

### Energy and range

Table 4. Energy on the design route (10 km, 120 m total climbing, 20 stops from 20 km/h).

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Rolling and drag | about 55 Wh | 19.9 N over 10 km |
| Climbing | about 62 Wh | 188 kg x 9.81 m/s² x 120 m |
| Stop and start | about 16 Wh | 20 x ½ x 188 kg x (5.56 m/s)², lost to brakes |
| **Trailer work** | **about 133 Wh** | Rider about 27 Wh (20 %), motor about 106 Wh |
| Pack output | about 141 Wh | 106 / 0.75 |
| **Pack energy per km** | **about 14 Wh/km** | |
| Usable pack energy | about 346 Wh | 384 Wh x 90 % |
| **Range on the design route** | **about 24 km** | R2 (20 km) met |
| Range on flat roads, few stops | about 45 km | about 7.5 Wh/km |
| Mains energy per 10 km trip | about 163 Wh | Figure 2 |
| Charge time, empty to full | about 3 h | 10 Ah at 4 A, plus the constant-voltage phase |

### Braking

At 20 km/h the loaded trailer carries about 2.9 kJ of kinetic energy, more than the bicycle and rider (about 1.5 kJ). For the combination to slow at 3 m/s², the trailer needs about 560 N of braking force. Without trailer brakes that force would come through the hitch and push the bike's rear wheel sideways, which can jackknife the combination. The overrun coupler is sized so that 100 N of drawbar compression gives about 460 N of trailer brake force (R6), leaving the hitch push at or below 100 N. Stopping distance from 20 km/h at 3 m/s² is about 5 m plus about 5.5 m during a 1 s reaction, about 10.7 m. Brake gain, fade on long descents and behavior on gravel are TRL 3 checks.

### Cost

Table 5. Indicative parts cost from `bom/bom.csv`.

| Group | Items | Indicative cost |
| --- | --- | --- |
| Structure | 1 to 4, 16 | about $215 |
| Sensing and braking | 5, 6, 9 | about $135 |
| Drive | 7, 8, 12 | about $250 |
| Energy and control | 10, 11, 13, 14, 17 | about $310 |
| Lights and hardware | 15, 18 | about $55 |
| **Total** | | **about $965; R12 ($900) not met, about 7 % over** |

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **Force sensing at the drawbar (pitch-level, kept).** It needs no sensor on the bike, works with any bike and rider, and detects braking. Alternatives: a crank or cadence sensor on the bike (Carla Cargo's early approach; ties the trailer to one bike and needs a cable) or wheel-speed matching (Biomega Ein; cannot tell a hill from a headwind or know how hard the rider is working). Recommendation: drawbar load cell, as in the pitch.
- **Control law and gain.** Proportional assist, motor force = G x measured pull, with G = 4 by default. Options: a fixed gain; a rider-selectable gain of 2 to 6 by a switch on the trailer; or a closed loop that drives the pull toward a small set tension (near zero felt load, but a higher risk of oscillation). Recommendation: selectable fixed gain, default 4, with a stability check at TRL 3.
- **One hub motor in one wheel.** Option A: one 250 W geared hub in the left wheel (cheapest, one controller, small yaw moment). Option B: two 125 W hubs, one per wheel (symmetric push, two controllers, higher cost). Option C: a third, central drive wheel (symmetric, but adds a wheel and mass). Recommendation: A.
- **Overrun mechanical brake plus assist cut.** Option A: mechanical overrun coupler on both disc brakes (works unpowered, known from car trailers and Carla Cargo). Option B: an electrically actuated brake commanded from the load cell (lighter, but fails if the electronics fail). Option C: a brake cable from the bike's lever (not compatible with "any bicycle"). Recommendation: A.
- **Battery: 36 V LiFePO4 or a SwapCell pack.** Option A: a 12S 36 V class LiFePO4 pack, 384 Wh, about $180 (as in the scaffold; LFP is thermally more stable, which matters under a 150 kg load, and 24 km meets R2). Option B: the portfolio's SwapCell pack (48 V class, about 468 Wh, about $370, needs a CAN host heartbeat and a 48 V motor and controller). SwapCell suits fleets that already share packs, but pushes the cost further over budget. Recommendation: A, with a SwapCell receiver as a later fleet variant.
- **Frame material.** Option A: welded mild steel (cheap, repairable by most welders, about 38 kg empty, misses R8). Option B: aluminium (about 33 kg, meets R8, costs about $60 more and needs TIG welding). Option C: bolted steel angle kit (no welding, heavier). Recommendation: A for the first prototype, with R8 relaxed to 40 kg or revisited later.
- **20 in wheels and hitch on the left axle end.** Small wheels keep the deck low (420 mm) and the drawbar near level with a 700c or 26 in bike's axle; the left side keeps clear of the derailleur. Recommendation: as proposed.
- **Budget.** Parts are about $65 over the $900 budget. Options: (a) raise `budget_usd` to $1,000; (b) cut cost with salvaged 20 in wheels and brakes and a lighter enclosure to reach about $900; (c) drop the side boards and lights from the prototype (not recommended; lights are a safety item). Recommendation: try (b) first, then (a). `project.yaml` is unchanged.

## Safety

> **Safety:** CargoMule is a 190 kg moving load behind a bicycle, driven by a motor and powered by a lithium battery. Braking, hitch failure, runaway assist and battery fire are the main hazards, and each must be designed out before any ride.

- **Runaway or unintended push.** A motor that pushes when the bike slows can shove the bike into traffic or jackknife it. Assist only while the drawbar is in tension; zero motor current within 100 ms of compression above about 20 N, above 25 km/h, at standstill, on any load cell fault (open or short, out of range, stuck value, failed plausibility check against speed) and when the key is off. The controller must run in torque mode with its own current limit, so a firmware fault cannot command more than the rated force. No throttle.
- **Braking and jackknife.** The loaded trailer has about twice the kinetic energy of the bicycle and rider. Trailer brakes are mandatory above the 45 to 60 kg limits in ASTM F1975 and EN 15918, and the overrun brake must work with the power off. Long descents can overheat small rotors; this is a TRL 3 check.
- **Hitch failure.** A detached 190 kg trailer is a serious hazard to others. The hitch needs a secondary safety strap or cable, a clear locking indicator and a design load well above peak braking and pothole loads (to be calculated at TRL 3).
- **Lithium battery.** A 384 Wh LiFePO4 pack is less prone to thermal runaway than other lithium-ion chemistries, but a short circuit can still start a fire. Use a BMS with cell-level protection and low-temperature charge cutoff, a 20 A fuse at the pack, a closed steel enclosure with a vent directed away from the load, and charge on a non-combustible surface away from sleeping areas. Never charge a damaged or wet pack.
- **Mains charging.** The charger is a certified off-the-shelf unit; no mains wiring is built into the trailer.
- **Load security and tipping.** Loads must be strapped down and centered. A high or off-center load raises the center of mass and can tip the trailer in a fast turn; the hitch down load must stay positive so the drawbar does not lift.
- **Pinch points and sharp edges.** The overrun coupler slides under load and the parking stand folds; both need guards. Deburr all frame edges and fit end caps to open tube ends.
- **Visibility.** A long, wide combination is easy to misjudge; lights, reflectors and a flag are part of the design, not accessories.

## Open questions for TRL 3

- Legal status of a motorized bicycle trailer in the first target country (EU pedal-assist exclusion, US federal and state rules).
- Stability of the proportional loop: drawbar stiffness, trailer mass, filter and sample rate; does G = 4 oscillate, and is a small set tension better?
- Motor heating on a 300 m, 8 % climb at 30 °C (R3).
- Yaw effect of driving one wheel, especially on gravel or in the wet.
- Overrun brake gain, spring preload and damper rate so the coupler does not chatter on bumps or brake during normal pedaling pulses.
- Hitch design load and fit across common rear axle types (R7), plus a secondary safety strap.
- Frame stress at 150 kg with a 2 g bump factor, and the steel versus aluminium decision (R1, R8).
- Close the $65 cost gap or propose a budget change (R12).
- Freedom to operate against coupling-sensor patents such as WO2022223692A1.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
