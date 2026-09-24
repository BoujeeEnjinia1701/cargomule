# CargoMule

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mobility and Logistics · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $900 USD · **Difficulty:** 3 of 5

Electric-assist cargo trailer that fits any bicycle. A load cell in the drawbar measures pull force and the trailer's hub motor pushes in proportion, so the rider feels almost no added load.

## Problem

Small businesses and households need to move 100 to 150 kg loads short distances, but cargo e-bikes are costly and ordinary bikes cannot pull that weight up hills.

## Concept

Electric-assist cargo trailer that fits any bicycle. A load cell in the drawbar measures pull force and the trailer's hub motor pushes in proportion, so the rider feels almost no added load.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Welded steel or aluminum trailer frame
- 250 W rear hub motor wheel
- Drawbar load cell with HX711 amplifier
- Motor controller
- 36 V LiFePO4 pack
- Microcontroller
- Hydraulic or mechanical disc brake
- Universal hitch

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Check local rules for electrically assisted trailers. The controller must cut assist whenever the drawbar goes into compression during braking. Contains a lithium battery pack. Use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CGM-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CGM-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
