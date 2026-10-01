# BOM notes

- Item numbers 1 to 16 match the callouts in `media/exploded.png`. Items 17 (charger) and 18 (hardware) have no callout.
- Costs are indicative 2026 small-quantity prices in USD for a TRL 3 paper design, not quotes. Suppliers are given by type; no supplier has been selected.
- Item 9 is priced per wheel (quantity 2).
- Estimated cost is $997 against the $1,000 value-engineering target `budget_usd` in `project.yaml` (a hypothetical control target, not a limit; $3 under), checked by `docs/04-calcs/sizing.py` (CGM-CAL-001, I1).
- Amish decided on 2026-09-25 to cut cost first and then raise the budget from $900 to $1,000 (CGM-DDR-001, D1). The cuts are on items 8 (idler wheel, $55 to $30), 9 (calipers, $30 to $20 each) and 10 (smaller 0.8 mm enclosure, $30 to $25), saving $50. TRL 3 sizing added $54 (arch frames on item 1, repriced plywood on item 2, the larger offset drawbar on item 3, a 3.8 kN strap on item 4, an overload stop on item 5 and the 7.7:1 lever on item 6).
- Amish accepted the TRL 3 recommendations on 2026-09-25 (CGM-DDR-002). Item 9 moved to 180 mm rotors with metallic pads, $20 to $25 per wheel, so the total rose from $969 to $979. The target stays $1,000.
- On 2026-10-01 the design was made constructable (CGM-DDR-003, open for Amish's review). Items 2 (aluminium corner pieces and board brackets, +$10), 5 (threaded cell ends, rod end and clevis in place of pinned clevises, -$5), 6 (housing, spring cage, pull rod, lever, cable splitter, +$8) and 18 (rivet nuts, +$5) were repriced, and items 1, 3, 7, 9, 10, 15 and 16 respecified at the same price. The total rose from $979 to $997. The target stays $1,000.
- Masses in the notes column come from CGM-CAL-001, section A.
