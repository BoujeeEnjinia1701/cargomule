"""CargoMule concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X points rearward from the towing bicycle's rear axle (X = 0) toward the
trailer, Y is across the trailer, Z is up, ground at Z = 0. The towing bicycle and the load are
grey context parts shown only in the hero render; trailer parts are colored and numbered to
match bom/bom.csv.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Torus, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

# ---------------- main parameters (concept values, see CGM-PRC-001) ----------------
WHEEL_R = 258.0            # 20 x 2.15 in tyre (ETRTO 406), outer radius
TYRE_W = 55.0
DECK_X0, DECK_X1 = 1300.0, 2500.0   # deck front and rear (1,200 mm long)
DECK_W = 700.0             # deck width
DECK_Z = 420.0             # deck top height
AXLE_X = 1950.0            # trailer axle, 50 mm behind deck center so the drawbar carries a light down load
TRACK = 850.0              # wheel center to wheel center
HITCH = (0.0, -95.0, 340.0)  # on the bicycle's left rear axle end
NOSE = (1180.0, 0.0, 360.0)  # drawbar meets the A-frame nose


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def tube(a, b, r):
    """Round bar between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def wheel(cx, cy, cz, r, w, spokes=16):
    tyre = Pos(cx, cy, cz) * Rot(90, 0, 0) * Torus(r - w / 2, w / 2)
    rim = Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(r - w + 8, 20) - Cylinder(r - w - 6, 22))
    hub = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(22, 70)
    sp = None
    for k in range(spokes):
        t = math.radians(k * 360 / spokes)
        s = tube((cx, cy, cz), (cx + (r - w - 2) * math.cos(t), cy, cz + (r - w - 2) * math.sin(t)), 1.8)
        sp = s if sp is None else sp + s
    return tyre + rim + hub + sp


# ---------------- 1 chassis frame: rectangular deck frame, A-frame nose, dropout plates ----------------
RAIL = 30.0
FZ0, FZ1 = DECK_Z - 12 - RAIL, DECK_Z - 12        # frame under a 12 mm deck
hw = DECK_W / 2
frame = (box(DECK_X0, DECK_X1, -hw, -hw + RAIL, FZ0, FZ1) + box(DECK_X0, DECK_X1, hw - RAIL, hw, FZ0, FZ1)
         + box(DECK_X0, DECK_X0 + RAIL, -hw, hw, FZ0, FZ1) + box(DECK_X1 - RAIL, DECK_X1, -hw, hw, FZ0, FZ1))
for x in (1600.0, AXLE_X, 2250.0):
    frame = frame + box(x - RAIL / 2, x + RAIL / 2, -hw, hw, FZ0, FZ1)
# A-frame nose: two bars from the front corners to the nose
frame = frame + tube((DECK_X0 + 15, -hw + 15, FZ0 + 15), NOSE, 14) + tube((DECK_X0 + 15, hw - 15, FZ0 + 15), NOSE, 14)
# axle stubs and dropout plates outboard of the side rails
for s in (-1, 1):
    frame = frame + box(AXLE_X - 60, AXLE_X + 60, s * hw - 4, s * hw + 4, WHEEL_R - 30, FZ1)
    frame = frame + tube((AXLE_X, s * hw, WHEEL_R), (AXLE_X, s * (TRACK / 2 - 30), WHEEL_R), 8)

# ---------------- 2 deck and side boards ----------------
deck = box(DECK_X0, DECK_X1, -hw, hw, DECK_Z - 12, DECK_Z)
deck = deck + box(DECK_X0, DECK_X1, -hw, -hw + 12, DECK_Z, DECK_Z + 150) + box(DECK_X0, DECK_X1, hw - 12, hw, DECK_Z, DECK_Z + 150)
deck = deck + box(DECK_X1 - 12, DECK_X1, -hw, hw, DECK_Z, DECK_Z + 150) + box(DECK_X0, DECK_X0 + 12, -hw, hw, DECK_Z, DECK_Z + 150)

# ---------------- drawbar chain, hitch to nose ----------------
P_LC0 = lerp(HITCH, NOSE, 0.60)   # load cell starts
P_LC1 = lerp(HITCH, NOSE, 0.68)   # load cell ends, overrun coupler starts
P_OR1 = lerp(HITCH, NOSE, 0.88)   # overrun coupler ends
P_H1 = lerp(HITCH, NOSE, 0.05)
drawbar = tube(P_H1, P_LC0, 16) + tube(P_OR1, NOSE, 16)                          # 3 drawbar tube, two sections
hitch = (Pos(*HITCH) * Rot(90, 0, 0) * Cylinder(32, 14)                            # 4 axle plate
         + Pos(HITCH[0], HITCH[1] - 12, HITCH[2]) * Cylinder(20, 30)               # articulating joint body
         + tube((HITCH[0], HITCH[1] - 12, HITCH[2]), P_H1, 18))
dvec = Vector(*NOSE) - Vector(*HITCH)
load_cell = Solid.make_cylinder(24, (Vector(*P_LC1) - Vector(*P_LC0)).length, Plane(origin=Vector(*P_LC0), z_dir=dvec.normalized()))
load_cell = load_cell + Pos(*lerp(P_LC0, P_LC1, 0.5)) * Box(40, 40, 60)  # S-type body and gland
overrun = Solid.make_cylinder(28, (Vector(*P_OR1) - Vector(*P_LC1)).length, Plane(origin=Vector(*P_LC1), z_dir=dvec.normalized()))
overrun = overrun + Pos(*lerp(P_LC1, P_OR1, 0.55)) * Pos(0, 0, 38) * Box(90, 30, 30)  # damper and cable lever

# ---------------- wheels, motor, brakes ----------------
yL, yR = -TRACK / 2, TRACK / 2
motor_wheel = wheel(AXLE_X, yL, WHEEL_R, WHEEL_R, TYRE_W) + Pos(AXLE_X, yL, WHEEL_R) * Rot(90, 0, 0) * Cylinder(78, 60)
idler_wheel = wheel(AXLE_X, yR, WHEEL_R, WHEEL_R, TYRE_W)
brakes = None
for y, s in ((yL, 1), (yR, -1)):
    rotor = Pos(AXLE_X, y + s * 50, WHEEL_R) * Rot(90, 0, 0) * (Cylinder(80, 3) - Cylinder(30, 4))
    caliper = Pos(AXLE_X - 70, y + s * 50, WHEEL_R + 45) * Box(40, 26, 50)
    b = rotor + caliper
    brakes = b if brakes is None else brakes + b

# ---------------- under-deck enclosure with pack, controller and control board ----------------
EX0, EX1 = 1360.0, 1580.0 + 180.0          # between front crossmember and axle zone
EZ0, EZ1 = 200.0, FZ0
enc = box(EX0, EX1, -230, 230, EZ0, EZ1) - box(EX0 + 4, EX1 - 4, -226, 226, EZ0 + 4, EZ1 + 1)
pack = box(EX0 + 20, EX0 + 20 + 250, -85, 85, EZ0 + 8, EZ0 + 8 + 150)     # 12S LFP, about 250 x 170 x 150
controller = box(EX0 + 300, EX0 + 300 + 110, 20, 90, EZ0 + 8, EZ0 + 8 + 45)
board = box(EX0 + 300, EX0 + 300 + 90, 120, 180, EZ0 + 8, EZ0 + 8 + 30)
# harness: enclosure to motor, to load cell, to lights
harness = (tube((EX1 - 10, -150, EZ0 + 30), (AXLE_X - 90, -hw + 40, EZ0 + 30), 5)
           + tube((AXLE_X - 90, -hw + 40, EZ0 + 30), (AXLE_X, yL + 40, WHEEL_R), 5)
           + tube((EX0 + 10, 0, EZ0 + 60), (NOSE[0] - 20, 0, NOSE[2] - 25), 5)
           + tube((NOSE[0] - 20, 0, NOSE[2] - 25), lerp(P_LC0, P_LC1, 0.5), 5)
           + tube((EX1 - 10, 150, EZ0 + 30), (DECK_X1 - 40, 150, FZ0 - 8), 5))

# ---------------- 15 lights, reflectors and flag; 16 parking stand ----------------
lights = (box(DECK_X1 + 2, DECK_X1 + 22, -hw + 30, -hw + 130, FZ0, FZ1) + box(DECK_X1 + 2, DECK_X1 + 22, hw - 130, hw - 30, FZ0, FZ1)
          + box(DECK_X0 + 400, DECK_X0 + 480, -hw - 4, -hw, FZ0, FZ1) + box(DECK_X0 + 400, DECK_X0 + 480, hw, hw + 4, FZ0, FZ1)
          + tube((DECK_X1 - 30, -hw + 20, DECK_Z), (DECK_X1 - 30, -hw + 20, DECK_Z + 1150), 6)
          + box(DECK_X1 - 30, DECK_X1 + 220, -hw + 17, -hw + 23, DECK_Z + 1000, DECK_Z + 1150))
STAND_X = NOSE[0] - 120
stand = tube((STAND_X, 0, NOSE[2] - 12), (STAND_X, 0, 25), 11) + box(STAND_X - 50, STAND_X + 50, -35, 35, 0, 25)

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
crates = None
for (x, y, h) in ((1480, -170, 300), (1480, 170, 300), (1860, -170, 300), (1860, 170, 300), (2260, 0, 250)):
    c = box(x - 170, x + 170, y - 155, y + 155, DECK_Z, DECK_Z + h) if x < 2200 else box(x - 180, x + 180, -300, 300, DECK_Z, DECK_Z + h)
    crates = c if crates is None else crates + c

ACC = "#0F766E"
parts = [
    Part("Chassis frame, welded steel", frame, "#475569", 1, (0, 0, 0)),
    Part("Deck and side boards", deck, "#B7925A", 2, (0, 0, 480)),
    Part("Drawbar", drawbar, "#334155", 3, (-50, -250, -550)),
    Part("Universal axle hitch", hitch, "#D4A017", 4, (-300, -700, -700)),
    Part("Drawbar load cell and amplifier", load_cell, ACC, 5, (-350, -450, -1000)),
    Part("Overrun brake coupler", overrun, "#7C3AED", 6, (-50, -200, -1150)),
    Part("Hub motor wheel, 250 W geared", motor_wheel, "#1F2937", 7, (0, -750, 0)),
    Part("Idler wheel", idler_wheel, "#4B5563", 8, (0, 650, 0)),
    Part("Mechanical disc brakes (pair)", brakes, "#DC2626", 9, (300, 0, -450)),
    Part("Battery and electronics enclosure", enc, "#94A3B8", 10, (0, 0, -650)),
    Part("36 V LiFePO4 pack, 384 Wh", pack, "#C2410C", 11, (0, -350, -1150)),
    Part("Motor controller", controller, "#115E59", 12, (100, 150, -1150)),
    Part("Control board (MCU)", board, "#2563EB", 13, (100, 500, -1100)),
    Part("Wiring harness, fuse and key switch", harness, "#111827", 14, (500, 250, -800)),
    Part("Lights, reflectors and flag", lights, "#F59E0B", 15, (500, 0, 450)),
    Part("Parking stand", stand, "#A16207", 16, (-300, 0, -1350)),
]
context = [Part("Towing bicycle", bicycle, "#9CA3AF", None), Part("150 kg load", crates, "#B0B7C0", None)]

render_all(
    parts, project="CargoMule", title="Electric-assist cargo trailer concept", dwg_no="CGM-DWG-010",
    key_figures=["150 kg payload on a 1,200 x 700 mm deck",
                 "Drawbar load cell; rider feels about 20 % of trailer pull",
                 "250 W geared hub, 36 V 384 Wh LiFePO4 (proposed)",
                 "About 24 km per charge, hilly loaded route (estimate)",
                 "Overrun disc brakes both wheels; about 38 kg empty (est.)",
                 "About 2.5 m long, 910 mm wide; parts about $965 (est.)"],
    context=context, cut_exclude=("Lights, reflectors and flag",),
    flow={"title": "energy for a 10 km loaded round trip with 120 m of climbing, Wh (all values are estimates)",
          "unit": "Wh",
          "stages": [("Mains to charger", 163), ("Into pack", 147), ("Pack output", 141),
                     ("Motor at wheel", 106), ("Trailer work", "133 Wh, 27 Wh by rider")],
          "losses": [(0, "Charger (10 %)", 16), (1, "Cell charge (4 %)", 6), (2, "Controller, motor (25 %)", 35)]},
)
