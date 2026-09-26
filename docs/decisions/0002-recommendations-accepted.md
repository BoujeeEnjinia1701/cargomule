---
doc_id: CGM-DDR-002
title: CargoMule TRL 3 recommendations accepted
project: CargoMule
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of the TRL 3 review recommendations and what changed in the repo
---

# 0002: TRL 3 recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items D11 to D14; items O1 and O2 remain proposed

## Context

The TRL 3 review note (`docs/REVIEW.md`, session 2026-09-25, TRL 3) listed four new items as "Proposed, awaiting Amish", each with options and a recommendation: the response to the R8 mass miss, long climbs (R3), wet braking and descents (R6) and the highest gain setting. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Each of those items is therefore decided in favor of its recommendation. Where the recommendation named one of several options, that option is the decision. Items with no recommendation stay open. TRL 4 remains on hold by Amish's instruction, so any part of a recommendation that needs building, testing, measuring or purchasing is recorded as decided but on hold.

## Decision

*Table 1. Newly decided items.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D11 | Response to the R8 miss (43.1 kg against 40 kg) | Option (a): relax R8 to 45 kg for the first prototype, keeping the steel frame; option (b), straps or mesh in place of the plywood side boards, is kept as a later weight option. Decided by Amish, 2026-09-25: go with recommendation. | CGM-REQ-001 v0.4: R8 target 45 kg (99 lb). CGM-CAL-001 v0.2: 43.2 kg, R8 met on paper (was not met). CGM-PRC-001 v0.4 updated. |
| D12 | Long climbs (R3) | Option (a): keep the 250 W motor, add thermal derating and state a use limit of about 300 m of continuous 8 % climbing; confirm the motor constants from a datasheet. Decided by Amish, 2026-09-25: go with recommendation. | CGM-REQ-001 v0.4: R3 restated with the derating rule and the stated use limit. CGM-CAL-001 v0.2 adds [C10]: full assist reaches 100 °C after about 336 m; derated, the motor gives about 57 N and the rider feels up to about 114 N on a climb that never ends. CGM-PRC-001 v0.4 adds the firmware rule to "How it works" and Safety. The datasheet check comes with motor selection, which is TRL 4 purchasing: decided, on hold. R3 stays at risk. |
| D13 | Wet braking and descents (R6) | Option (b): 180 mm rotors with metallic pads, about $10 more. Decided by Amish, 2026-09-25: go with recommendation. | `cad/src/model.py`: `rotor_d` 160 to 180 mm; STEP and STL re-exported; drawing CGM-DWG-001 to Rev P2. `bom/bom.csv` item 9: $20 to $25 per wheel; total $969 to $979. CGM-CAL-001 v0.2: brake gain 6.9 to 7.8 with the 7.7:1 lever kept; push 100 to 92 N dry and 119 to 110 N wet; rotor rise on an 8 % descent 166 to 129 K. R6 improves but stays at risk in the wet. |
| D14 | Highest gain setting | Keep G = 2 to 6 on paper and decide the top setting once the hitch joint stiffness is known. Decided by Amish, 2026-09-25: go with recommendation. | No design change. Measuring the hitch joint stiffness is TRL 4 work: decided, on hold. CGM-CAL-001 v0.2 and CGM-PRC-001 v0.4 note the decision. |

The TRL 2 review items were already decided in CGM-DDR-001 (D1 to D10); CGM-DDR-001 is revised to v0.2 only to point its R8 note to D11.

*Table 2. Items that remain open (no recommendation was made).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First users and region for co-design: market traders, a trades cooperative or a community food bank | Proposed, awaiting Amish (co-design partners to be picked per area later) |
| O2 | Legal status of a motorized bicycle trailer on public roads and bike lanes in the first target country | Proposed, awaiting Amish; no recommendation was made and none is made here |

## Consequences

- `project.yaml`: `budget_usd` stays $1,000; the $979 BOM is within it (R12 met on paper). Pitch and problem are unchanged. `trl` and `trl_target` stay 3.
- Requirement status (CGM-CAL-001 v0.2): 9 met (7 on paper, 2 by design), 3 at risk (R3, R6, R7), 0 not met, 2 not verifiable at TRL 3. Before this record: 8 met, 3 at risk, 1 not met (R8), 2 not verifiable.
- Decided but on hold for TRL 4: the motor datasheet and bench thermal check (D12) and the hitch joint stiffness measurement that settles the top gain setting (D14).
- No cross-repo action arises from these items.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building, testing or purchasing.
