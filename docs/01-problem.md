---
doc_id: CGM-PRB-001
title: CargoMule problem statement
project: CargoMule
doc_type: Problem statement
version: "0.5"
status: Draft
date: '2026-10-01'
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Pitch wording "most bicycles" and $1,000 budget per CGM-DDR-001; open questions linked to the decision record
- version: "0.4"
  date: '2026-09-26'
  author: Amish Chadha
  change: Stronger sources
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
---

# CargoMule problem statement

Small businesses and households need to move 100 to 150 kg loads a few kilometers at a time, but a mainstream cargo e-bike lists at about $2,400, the few electric-assist trailers on the market cost as much or more, and an ordinary bicycle cannot pull that weight up a hill. CargoMule aims to turn the bicycle a person already owns into a 150 kg load carrier for well under the price of a cargo e-bike.

## The problem

Short urban and suburban trips with heavy loads (a market stall's stock, tools and materials for a trade job, a week of groceries for a large household, a delivery round) are usually made by car or van. A bicycle with a cargo trailer can do many of these trips, but the rider becomes the limit:

1. **Hills.** On level ground most people can pull about 137 kg (300 lb) on a trailer at modest speed, but a 2 % grade already triples the effort and a 4 % grade needs very low gearing ([Bikes At Work](https://www.bikesatwork.com/blog/how-much-weight-can-a-bicycle-carry)). A first-order estimate for CargoMule's design load (about 188 kg of loaded trailer) on an 8 % grade is about 165 N of extra pull, or about 370 W at 8 km/h on top of the rider's own climb. That is beyond most riders.
2. **Cost of the alternatives.** A mainstream electric longtail such as the RadWagon 5 lists at $2,399 ([Rad Power Bikes](https://www.radpowerbikes.com/products/radwagon-electric-cargo-bike)). Commercial electric-assist trailers exist but are priced for businesses (see Prior work).
3. **Braking.** A heavy trailer without its own brakes pushes the bicycle when it slows. Voluntary trailer standards set low limits for unbraked trailers: 60 kg in EN 15918 and 45.4 kg (100 lb) in ASTM F1975 ([Wikipedia summary of both standards](https://en.wikipedia.org/wiki/Bicycle_trailer); [EN 15918 catalog entry](https://standards.iteh.ai/catalog/standards/cen/e11b5f02-592a-45fb-9a47-3d8c2c11275d/en-15918-2011a2-2017)). A 150 kg trailer therefore needs its own brakes.

CargoMule is an electric-assist cargo trailer that hitches to most bicycles with no wiring to the bike. A load cell in the drawbar measures how hard the bicycle is pulling and the trailer's hub motor pushes in proportion, so the rider feels a fraction of the trailer's load on the flat and on hills.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Market trader or street vendor | Move 80 to 150 kg of stock and a stall between storage and market | Early starts, mixed roads, curbs, parking at the stall |
| Tradesperson (gardener, painter, bike mechanic) | Carry tools and materials to jobs within about 10 km | Daily use, loads vary through the day, hills |
| Household without a car | Weekly shopping, moving furniture, bulk goods | Occasional use, stored in a shed or hallway |
| Community group, food bank or repair café | Pick up and deliver donations; share the trailer among members | Several riders and bikes; must hitch quickly to any bike |
| Local workshop or maker | Build and repair the trailer from common parts | Hand tools, a welder in some cases, e-bike parts suppliers |

### Operating environment

- **Roads:** paved streets, bike lanes and compacted gravel paths, with curbs, drop kerbs and grades up to about 8 % on short climbs (10 % occasionally).
- **Loads:** 100 to 150 kg of payload on the deck; towing bicycle and rider about 90 to 110 kg.
- **Speed:** 10 to 20 km/h cruising; assisted speed limited to 25 km/h in line with pedelec rules.
- **Climate:** −10 to 40 °C, rain, road spray and winter salt in some regions.
- **Charging:** household mains at home or at the business; charged overnight.

## Constraints

- Garage-buildable prototype, with a $1,000 USD value-engineering target for parts (`project.yaml`, a hypothetical control target, not a limit; raised from $900 by CGM-DDR-001, D1).
- Hitches to most bicycles with no change to the bike and no wiring to it: bikes with a quick-release or thru-axle rear wheel first, with adapters for others (see CGM-REQ-001, R7).
- Assist within e-bike limits: 250 W rated power and assist to 25 km/h at most, matching the EU pedal-assist exclusion in Regulation (EU) No 168/2013 ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32013R0168)) and within the US federal low-speed electric bicycle definition of under 750 W and 20 mph ([15 U.S.C. 2085](https://www.law.cornell.edu/uscode/text/15/2085)). Whether a motorized trailer falls under these rules is an open question.
- The trailer must brake itself so it never pushes the bicycle hard when slowing.
- Generic, replaceable parts (e-bike hub motor, controller, disc brakes, 20 in wheels) so a local bike shop can repair it.

## Out of scope

- A complete cargo bicycle or tricycle (see FlatTrike).
- Carrying people or children.
- Handcart or walk-behind mode (kept out of scope by CGM-DDR-001, D10).
- Designing the battery cells or BMS (a bought-in 36 V LiFePO4 pack, CGM-DDR-001 D2; a SwapCell receiver is a later fleet variant).
- Road registration or type approval.

## Prior work

- **Carla Cargo (Germany).** A heavy-duty trailer with an optional 250 W hub motor, 150 kg payload in its original version and an overrun brake with dual discs ([New Atlas](https://newatlas.com/carla-cargo-bike-trailer/43044/)). Its current eCARLA carries up to 200 kg, uses a Bafang hub motor and a 720 Wh LiFePO4 pack, assists to 25 km/h and starts at €6,490 ([Carla Cargo](https://www.carlacargo.de/products/ecarla)). The early version sensed pedaling through a crank sensor fitted to the towing bike, which ties the trailer to one bike.
- **Biomega Ein.** A single-wheel electric trailer with a 250 W hub motor that detects the bike's motion from its own wheel speed and pushes in proportion; about $1,428 planned retail ([New Atlas](https://newatlas.com/bicycles/biomega-ein-electric-bicycle-trailer/)). It is a light-load design.
- **Roland PAXXTER e.** A box trailer with two 125 W, 36 V hub motors, a 180 Wh pack and a pedal sensor, sold at about €3,300 ([Notebookcheck](https://www.notebookcheck.net/Roland-PAXXTER-e-Bicycle-Trailer-launches-as-new-cargo-bike-kit.763538.0.html)).
- **Brake-controlling couplings.** A Brüggli patent application describes a trailer coupling that senses relative movement between two housing parts to control the trailer's brakes ([WO2022223692A1](https://patents.google.com/patent/WO2022223692A1/en)), and a German utility model covers a bicycle trailer coupling for an overrun brake ([DE202010010674U1](https://patents.google.com/patent/DE202010010674U1/en)). These confirm that sensing at the coupling works for braking. CargoMule uses a load cell at the coupling for propulsion as well, and a freedom-to-operate check is needed before release.
- **Unpowered heavy trailers.** Commercial cargo trailers carry 14 to 140 kg ([Wikipedia](https://en.wikipedia.org/wiki/Bicycle_trailer)), and heavy-haul builders show 137 kg is a practical unassisted limit on level ground ([Bikes At Work](https://www.bikesatwork.com/blog/how-much-weight-can-a-bicycle-carry)).

The gap CargoMule addresses is an open, garage-buildable design that senses pull force at the drawbar, so it needs no sensor or wiring on the towing bike, carries 150 kg with its own brakes, and costs a fraction of a commercial electric trailer.

## Open questions

- Is a motorized bicycle trailer legal on public roads and bike lanes in the first target country, and under which category? Carla Cargo's sale in Germany suggests a path in the EU; US state rules need checking. Proposed, awaiting Amish (CGM-DDR-001, O2).
- Which users first: a market trader group, a trades cooperative, or a community food bank? Proposed, awaiting Amish (CGM-DDR-001, O1); co-design partners are to be picked per area later.
- Is 150 kg the right payload, or do most target loads fall under 100 kg, which would allow a lighter trailer?
- How many target bikes have a quick-release or thru-axle rear wheel, and what share need a nutted-axle or hub-gear adapter?

## User research and co-design

- [ ] Identify two or three target users (trader, tradesperson, community group) and record their typical loads, routes and storage space
- [ ] Ride typical routes with a loaded unpowered trailer and log grades and speeds
- [ ] Validate payload, range and cost assumptions with users
- [ ] Revise requirements (REQ) from findings before freezing the design
