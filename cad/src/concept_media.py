"""CargoMule concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the trailer parts from cad/src/model.py (PARAMS), adds a grey towing bicycle and a grey
150 kg load as hero context, and renders the media set with .kit/concept.py. Trailer parts are
colored and numbered to match bom/bom.csv. Figures quoted on the sheet and in the flow diagram
come from docs/04-calcs/sizing.py (CGM-CAL-001). Not for fabrication.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Pos  # noqa: E402
from concept import Part, render_all  # noqa: E402
from model import PARAMS as P, build_parts, derived, tube, wheel  # noqa: E402
import drawing  # noqa: E402
from sheets import safe_project_views  # noqa: E402

# The hidden-line projection of this model yields one zero-length ellipse arc that the SVG
# exporter rejects; use the edge-by-edge projection from sheets.py (the kit is unchanged).
drawing.project_views = safe_project_views

D = derived(P)
m = build_parts()

# ---------------- context: towing bicycle and a 150 kg load (grey, hero only) ----------------
BW = 355.0
bike_wheels = wheel(0, 0, BW, BW, 40, 24) + wheel(-1100, 0, BW, BW, 40, 24)
BB = (-430.0, 0.0, 290.0); ST = (-225.0, 0.0, 815.0); HB = (-1030.0, 0.0, 690.0); HT = (-975.0, 0.0, 840.0)
bike = (tube(BB, ST, 14) + tube(ST, HT, 14) + tube(BB, HB, 16) + tube(HB, HT, 18)
        + tube(BB, (0, 45, BW), 9) + tube(BB, (0, -45, BW), 9) + tube(ST, (0, 45, BW), 8) + tube(ST, (0, -45, BW), 8)
        + tube(HB, (-1100, 50, BW), 11) + tube(HB, (-1100, -50, BW), 11)
        + tube(HT, (-950, 0, 960), 12) + tube((-950, -300, 960), (-950, 300, 960), 11)
        + Pos(-200, 0, 925) * Box(260, 150, 55) + tube((-215, 0, 850), (-205, 0, 900), 13))
bicycle = bike_wheels + bike
dz = P["deck_z"]
crates = None
for (x, y, hgt) in ((1480, -165, 300), (1480, 165, 300), (1830, -165, 300), (1830, 165, 300), (2230, 0, 250)):
    wy = 155 if x < 2200 else 300
    c = Pos(x, y, dz + hgt / 2) * Box(340 if x < 2200 else 360, 2 * wy, hgt)
    crates = c if crates is None else crates + c

ACC = "#0F766E"
parts = [
    Part("Chassis frame, welded steel", m["frame"], "#475569", 1, (0, 0, 0)),
    Part("Deck and side boards", m["deck"], "#B7925A", 2, (0, 0, 520)),
    Part("Drawbar, offset", m["drawbar"], "#334155", 3, (-50, -250, -550)),
    Part("Universal axle hitch", m["hitch"], "#D4A017", 4, (-300, -700, -700)),
    Part("Drawbar load cell and amplifier", m["load_cell"], ACC, 5, (-350, -450, -1000)),
    Part("Overrun brake coupler", m["coupler"], "#7C3AED", 6, (-50, -200, -1150)),
    Part("Hub motor wheel, 250 W geared", m["motor_wheel"], "#1F2937", 7, (300, -800, 380)),
    Part("Idler wheel", m["idler_wheel"], "#4B5563", 8, (0, 650, 0)),
    Part("Mechanical disc brakes (pair)", m["brakes"], "#DC2626", 9, (350, 0, -450)),
    Part("Battery and electronics enclosure", m["enclosure"], "#94A3B8", 10, (300, 0, -700)),
    Part("36 V LiFePO4 pack, 384 Wh", m["pack"], "#C2410C", 11, (150, -350, -1200)),
    Part("Motor controller", m["controller"], "#115E59", 12, (150, 250, -1050)),
    Part("Control board (MCU)", m["board"], "#2563EB", 13, (250, 550, -1000)),
    Part("Wiring harness, fuse and key switch", m["harness"], "#111827", 14, (500, 250, -800)),
    Part("Lights, reflectors and flag", m["lights"], "#F59E0B", 15, (500, 0, 450)),
    Part("Parking stand", m["stand"], "#A16207", 16, (-500, 0, -1300)),
]
context = [Part("Towing bicycle", bicycle, "#9CA3AF", None), Part("150 kg load", crates, "#B0B7C0", None)]

render_all(
    parts, project="CargoMule", title="Electric-assist cargo trailer concept", dwg_no="CGM-DWG-010",
    date="2026-10-01",
    key_figures=["150 kg payload on a 1,200 x 700 mm deck",
                 "Drawbar load cell, G = 4: about 7 N felt on the flat",
                 "8 % climb: about 39 N felt; 250 W hub, 36 V 384 Wh LFP",
                 "About 24.5 km per charge, hilly loaded route (CGM-CAL-001)",
                 "Overrun 180 mm disc brakes, both wheels; about 46 kg empty",
                 "2.55 m long, 972 mm wide; parts about $997"],
    context=context, cut_exclude=("Lights, reflectors and flag",),
    flow={"title": "energy for a 10 km loaded round trip with 120 m of climbing, Wh (estimates, CGM-CAL-001)",
          "unit": "Wh",
          "stages": [("Mains to charger", 163), ("Into pack", 147), ("Pack output", 141),
                     ("Motor at wheel", 92), ("Trailer work", "121 Wh, 29 Wh by rider")],
          "losses": [(0, "Charger (10 %)", 16), (1, "Cell charge (4 %)", 6), (2, "Controller, motor (35 %)", 49)]},
)
