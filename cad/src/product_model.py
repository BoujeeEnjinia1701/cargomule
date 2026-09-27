"""CargoMule product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: graphite chassis with rounded plywood deck, off-white
side boards with hand slots, aluminium corner caps and a raised name badge; the drawbar load cell
in its pinned clevises under a clear polycarbonate guard; the overrun coupler with a rubber gaiter,
damper housing and brake lever; a detailed axle hitch with its lock indicator and safety strap;
the 250 W hub motor with a teal cover ring and cable exit; slotted brake rotors and calipers; a
closed galvanized enclosure with a parting seam, vents, screws, key switch, gain dial, lit status
light, charge port and an inspection window onto the pack; lit rear lights, reflectors and a
fabric safety flag. Context is a simple bicycle with the shared clay mannequin riding it and a
small strapped load on the deck.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived(), drawbar_points() and
build_parts() in model.py. Axes as model.py: X rearward from the bicycle's rear axle (x = 0),
Y across (hitch and motor on the -Y side, the bicycle's left), Z up with the ground at z = 0.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RectangleRounded, RegularPolygon, Rot,
                       SlotOverall, Sphere, Text, Torus, extrude, fillet)
from model import PARAMS, derived, drawbar_points, build_parts, box, tube, fuse

TITLE = "CargoMule: electric-assist cargo trailer for most bicycles"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 20, "az": -38,
     "note": "Product render from the rear left and above (about 20 deg elevation); loaded trailer in the "
             "foreground with the hub motor wheel nearest, drawbar running forward to the hitch on the "
             "bicycle's left rear axle, rider in the saddle"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -125,
     "note": "Exploded view from the front left and above (about 28 deg elevation): side boards and deck, "
             "chassis, hub motor and idler wheels, disc brakes, enclosure with pack, controller and control "
             "board, drawbar with load cell and overrun coupler, hitch, stand, lights, flag and charger"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 16, "az": -150,
     "note": "Detail from the front left and above (about 16 deg elevation), without the bicycle and rider: "
             "drawbar load cell behind its clear guard and the overrun coupler at lower left, hitch at the "
             "drawbar tip, enclosure window onto the pack, hub motor wheel at right"},
]

# Colours (restrained product palette; kit accent)
C_FRAME = "#3B4452"        # graphite powder coat
C_DRAW = "#2F3642"
C_BOARD = "#E6E8EB"        # off-white HPL-faced side boards
C_PLY = "#C9A574"
C_ACCENT = "#0F766E"
C_ALU = "#B8BEC6"
C_STEEL = "#9AA1AA"
C_GALV = "#AEB6BF"
C_BLACK = "#1F2329"
C_RUBBER = "#2B2F36"
C_TYRE = "#25282D"
C_RIM = "#8F979F"
C_MOTOR = "#30363F"
C_CELL = "#C7CCD2"
C_PACK = "#1E3A5F"
C_PCB = "#166534"
C_CHIP = "#111827"
C_RED_LIT = "#EF4444"
C_AMBER = "#F59E0B"
C_GREEN_LIT = "#22C55E"
C_FLAG = "#F97316"
C_GUARD = "#DCEBF5"
C_BIKE = "#C4C9D0"
C_CLAY = "#9CA3AF"
C_BOXES = "#C8A57A"
FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

# Context bicycle (appearance only; it is not part of the trailer)
BIKE_R = 340.0             # wheel radius, so the rear axle sits at the hitch height (PARAMS["hitch"] z)
BIKE_WB = 1080.0           # wheelbase
BIKE_BB = (-430.0, 285.0)  # bottom bracket x, z
RIDER_H = 1750.0


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _rbox(x0, x1, y0, y1, z0, z1, r_vert=0.0, r_top=0.0, r_all=0.0):
    """Box with optional vertical edge, top edge or all-edge fillets."""
    s = box(x0, x1, y0, y1, z0, z1)
    if r_all:
        return _fillet_try(s, s.edges(), [r_all, r_all * 0.6, r_all * 0.3])
    if r_vert:
        s = _fillet_try(s, s.edges().filter_by(Axis.Z), [r_vert, r_vert * 0.6, r_vert * 0.3])
    if r_top:
        s = _fillet_try(s, s.faces().sort_by(Axis.Z)[-1].edges(), [r_top, r_top * 0.6, r_top * 0.3])
    return s


def _cyl_y(x, y, z, r, w):
    """Cylinder with its axis along Y, centred at (x, y, z)."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, w)


def _cyl_x(x, y, z, r, w):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, w)


def _text(s, size, plane, depth=1.0):
    return plane * extrude(Text(s, font_size=size, font_path=FONT), amount=depth)


def _wheel(cx, cy, cz, r, w, spokes, hub_r, flange_dy, rim_w=20.0):
    """Wheel as separate tyre, rim and spoke solids. Spokes run from hub flanges at +/- flange_dy."""
    tyre = Pos(cx, cy, cz) * Rot(90, 0, 0) * Torus(r - w / 2, w / 2)
    rim = _cyl_y(cx, cy, cz, r - w + 8, rim_w) - _cyl_y(cx, cy, cz, r - w - 6, rim_w + 2)
    rim = _fillet_try(rim, rim.edges(), [2.0, 1.0])
    rr = r - w - 4
    sp = []
    for k in range(spokes):
        a = math.radians(k * 360.0 / spokes)
        dy = flange_dy if k % 2 else -flange_dy
        a0 = a + math.radians(12 if k % 2 else -12)        # tangential lacing look
        p0 = (cx + hub_r * math.cos(a0), cy + dy, cz + hub_r * math.sin(a0))
        p1 = (cx + rr * math.cos(a), cy, cz + rr * math.sin(a))
        sp.append(tube(p0, p1, 1.8))
    return tyre, rim, fuse(sp)


def _bicycle():
    """Context bicycle: frame, fork, bar and stem, saddle, cranks and pedals, chainring, tyres, rims."""
    rax, fax = 0.0, -BIKE_WB
    az_ = BIKE_R
    bbx, bbz = BIKE_BB
    st = math.radians(73.0)
    seat = (bbx + 707 * math.cos(st), 0.0, bbz + 707 * math.sin(st))
    st_top = (bbx + 540 * math.cos(st), 0.0, bbz + 540 * math.sin(st))
    ht_top, ht_bot = (-930.0, 0.0, 790.0), (-968.0, 0.0, 660.0)
    bb = (bbx, 0.0, bbz)
    fr = [tube(bb, st_top, 16), tube(st_top, ht_top, 15), tube(bb, ht_bot, 18),
          tube((ht_bot[0] + 3, 0, ht_bot[2] - 20), (ht_top[0] - 2, 0, ht_top[2] + 20), 19)]
    for s in (-1, 1):
        fr += [tube(bb, (rax, s * 62, az_), 9), tube(st_top, (rax, s * 62, az_), 8),
               tube((ht_bot[0], s * 15, ht_bot[2] - 20), (fax, s * 52, az_), 12)]
    fr.append(Pos(*bb) * Rot(90, 0, 0) * Cylinder(22, 76))
    frame = fuse(fr)
    frame = frame + tube(st_top, (seat[0] - 15, 0, seat[2] - 55), 13)                    # seat post
    # stem and bar (bar centre on the rider's grip line)
    hx, hz = BIKE_BAR
    frame = frame + tube((ht_top[0] - 2, 0, ht_top[2] + 15), (hx - 20, 0, hz - 40), 14)
    frame = frame + tube((hx - 20, 0, hz - 40), (hx, 0, hz), 14)
    frame = frame + tube((hx, -260, hz), (hx, 260, hz), 11)
    grips = fuse([tube((hx, s * 120, hz), (hx, s * 250, hz), 16) for s in (-1, 1)])
    saddle = Pos(seat[0] + 10, 0, seat[2] - 22) * Box(250, 140, 44)
    saddle = saddle & (Pos(seat[0] + 10, 0, seat[2] - 22) * Rot(0, 0, 0) *
                       (Pos(40, 0, 0) * Cylinder(90, 44) + Pos(-60, 0, 0) * Box(140, 60, 44)))
    saddle = _fillet_try(saddle, saddle.edges(), [10.0, 6.0, 3.0])
    # drivetrain on the right (+Y) side: chainring, cranks and pedals (left pedal up, right down)
    ring = _cyl_y(bbx, 48, bbz, 92, 4) - _cyl_y(bbx, 48, bbz, 60, 6)
    cranks = [tube((bbx, -44, bbz), (bbx, -62, bbz + 170), 9), tube((bbx, 56, bbz), (bbx, 62, bbz - 170), 9)]
    pedals = [box(bbx - 50, bbx + 50, -110, -66, bbz + 160, bbz + 180),
              box(bbx - 50, bbx + 50, 66, 110, bbz - 180, bbz - 160)]
    drive = fuse([ring] + cranks + [tube((bbx + 92 * 0.2, 50, bbz + 90), (rax, 50, az_ + 40), 3),
                                    tube((bbx + 92 * 0.2, 50, bbz - 90), (rax, 50, az_ - 40), 3),
                                    _cyl_y(rax, 50, az_, 42, 4)])
    tyres, rims = [], []
    for x in (rax, fax):
        t, r, s = _wheel(x, 0.0, az_, BIKE_R, 45.0, 28, 24.0, 28.0, rim_w=18.0)
        tyres.append(t)
        rims.append(r + s + _cyl_y(x, 0, az_, 20, 100))
    return frame, saddle, grips, drive, fuse(pedals), fuse(tyres), fuse(rims)


# Rider placement: the "ride" landmarks put the bottom bracket, pedals, seat and grips on the bike.
def _rider_frame():
    from context_parts import mannequin_landmarks
    lm = mannequin_landmarks(RIDER_H, "ride")
    # the figure faces -Y; turn it -90 deg about Z so it faces -X (forward on the bicycle)
    rot = lambda p: (p[1], -p[0], p[2])
    bbm = rot(lm["bb"])
    shift = (BIKE_BB[0] - bbm[0], -bbm[1], BIKE_BB[1] - bbm[2])
    hands = [rot(h) for h in lm["hands"]]
    bar = (hands[0][0] + shift[0], hands[0][2] + shift[2])
    return lm, shift, bar


_LM, _RIDER_SHIFT, BIKE_BAR = _rider_frame()


def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    x0, x1, hw, R = P["deck_x0"], D["deck_x1"], D["hw"], P["rail"]
    fz0, fz1, ax, wr = D["fz0"], D["fz1"], P["axle_x"], P["wheel_r"]
    dz, bt, bh = P["deck_z"], P["board_t"], P["board_h"]
    yL, yR = -D["yc"], D["yc"]

    # ---------------------------------------------------------------- 1 chassis frame (as model.py)
    E_FRAME = (0, 0, -80)
    add("Chassis frame, powder coated", m["frame"], C_FRAME, "painted", 1, "shell", E_FRAME)
    caps = []
    for s in (-1, 1):
        for xx in (x0, x1):                             # black end caps on the side rail ends
            caps.append(box(xx - 3 if xx == x0 else xx, xx if xx == x0 else xx + 3,
                            s * hw - (R if s > 0 else 0) + 2, s * hw + (R if s < 0 else 0) - 2, fz0 + 2, fz1 - 2))
    add("Rail end caps", fuse(caps), C_BLACK, "plastic", 18, "shell", E_FRAME)

    # ---------------------------------------------------------------- 2 deck, boards, trim
    E_DECK = (0, 0, 620)
    deck = _rbox(x0, x1, -hw, hw, fz1, dz, r_vert=6.0)
    deck = _fillet_try(deck, deck.faces().sort_by(Axis.Z)[-1].edges(), [2.0, 1.0])
    add("Plywood deck, sealed", deck, C_PLY, "wood", 2, "shell", E_DECK)
    tracks = fuse([box(x0 + 60, x1 - 60, s * (hw - 70) - 12, s * (hw - 70) + 12, dz, dz + 2.5) for s in (-1, 1)])
    for s in (-1, 1):
        for xx in range(int(x0 + 100), int(x1 - 60), 100):
            tracks -= Pos(xx, s * (hw - 70), dz + 2.5) * extrude(SlotOverall(14, 7), amount=-2.0)
    add("Deck tie-down tracks", tracks, C_ALU, "metal", 2, "shell", E_DECK)

    E_BOARD_Z = 900
    zb0, zb1 = dz, dz + bh
    slot = lambda x, y: Pos(x, y, zb1 - 45) * Rot(90, 0, 0) * extrude(SlotOverall(130, 34), amount=40, both=True)
    for s, nm in ((-1, "left"), (1, "right")):
        b = _rbox(x0, x1, s * hw - (bt if s > 0 else 0), s * hw + (bt if s < 0 else 0), zb0, zb1, r_top=3.0)
        for xx in (x0 + 170, x1 - 170):
            b -= slot(xx, s * hw)
        add(f"Side board, {nm}", b, C_BOARD, "painted", 2, "shell", (0, s * 260, E_BOARD_Z))
    for xx, nm, dx in ((x0, "front", -220), (x1 - bt, "rear", 220)):
        b = _rbox(xx, xx + bt, -hw + bt, hw - bt, zb0, zb1, r_top=3.0)
        b -= Pos(xx + bt / 2, 0, zb1 - 45) * Rot(0, 90, 0) * Rot(0, 0, 90) * extrude(SlotOverall(130, 34), amount=40, both=True)
        add(f"End board, {nm}", b, C_BOARD, "painted", 2, "shell", (dx, 0, E_BOARD_Z))
    # aluminium corner caps and a teal trim band with the raised name badge
    cc = []
    for sx, xx in ((-1, x0), (1, x1)):
        for sy in (-1, 1):
            cc.append(box(xx - 60 if sx > 0 else xx - 3, xx + 3 if sx > 0 else xx + 60,
                          sy * hw - 3 if sy > 0 else sy * hw, sy * hw if sy > 0 else sy * hw + 3,
                          zb0 - 4, zb1 + 3))
            cc.append(box(xx - 3 if sx < 0 else xx, xx if sx < 0 else xx + 3,
                          sy * hw - 60 if sy > 0 else sy * hw, sy * hw if sy > 0 else sy * hw + 60,
                          zb0 - 4, zb1 + 3))
    add("Board corner caps", fuse(cc), C_ALU, "metal", 2, "shell", (0, 0, E_BOARD_Z + 220))
    xm = (x0 + x1) / 2
    for sy, nm in ((-1, "left"), (1, "right")):
        yo = sy * hw
        band = box(x0 + 330, x1 - 330, min(yo, yo + sy * 1.2), max(yo, yo + sy * 1.2), zb0 + 22, zb0 + 40)
        add(f"Accent trim band, {nm}", band, C_ACCENT, "painted", 2, "shell", (0, sy * 260, E_BOARD_Z))
        pl_ = Plane(origin=(xm, yo, zb0 + 88), x_dir=(-sy, 0, 0), z_dir=(0, sy, 0))
        add(f"Name badge, {nm}", _text("CARGOMULE", 44, pl_, 1.2), "#2F3642", "plastic", 2, "shell",
            (0, sy * 260, E_BOARD_Z))

    # ---------------------------------------------------------------- 3 drawbar (as model.py) and end detail
    pts = drawbar_points(P)
    h, k, k2, s_, n = pts
    c0, c1 = P["cell_x"]
    k0, k1 = P["coupler_x"]
    zc = lambda x: s_[2] + (n[2] - s_[2]) * (x - s_[0]) / (n[0] - s_[0])
    E_BAR = (-60, -260, -380)
    add("Drawbar, powder coated", m["drawbar"], C_DRAW, "painted", 3, "shell", E_BAR)
    ref = box(k[0] + 200, k[0] + 300, k[1] - 20.5, k[1] - 17.0, k[2] - 12, k[2] + 12)   # on the outer face
    add("Drawbar reflector strip", ref, C_AMBER, "plastic", 15, "shell", E_BAR)

    # ---------------------------------------------------------------- 4 hitch: axle plate, joint with boot, lock, strap
    E_HITCH = (-200, -520, -380)
    hitch_end = (h[0] + 20, h[1] - 60, h[2] + 1)
    plate = _cyl_y(h[0], h[1], h[2], 32, 14)
    plate = _fillet_try(plate, plate.edges(), [3.0, 1.5])
    plate += Pos(h[0] + 22, h[1], h[2] - 30) * Box(40, 14, 44)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Y), [4.0, 2.0])
    add("Hitch axle plate", plate, C_STEEL, "metal", 4, "shell", E_HITCH)
    add("Hitch axle nut", Pos(h[0], h[1] + 11, h[2]) * Rot(90, 0, 0) * extrude(RegularPolygon(12, 6), amount=8),
        C_ALU, "metal", 4, "shell", E_HITCH)
    jc = (h[0] + 8, h[1] - 30, h[2])
    boot = Pos(*jc) * Sphere(21)
    for i in range(-2, 3):
        boot -= Pos(jc[0], jc[1] + i * 7, jc[2]) * Rot(90, 0, 0) * (Cylinder(30, 1.6) - Cylinder(19.5, 2))
    add("Hitch joint boot (EPDM)", boot, C_RUBBER, "rubber", 4, "shell", E_HITCH)
    arm = tube(jc, hitch_end, 17)
    arm += Pos(*hitch_end) * Sphere(17)
    add("Hitch arm", arm, C_STEEL, "metal", 4, "shell", E_HITCH)
    pin = _cyl_x(hitch_end[0] - 4, hitch_end[1] + 14, hitch_end[2] + 20, 4, 60)
    pin += Pos(hitch_end[0] - 36, hitch_end[1] + 14, hitch_end[2] + 20) * Sphere(9)
    add("Locking pin", pin, C_ALU, "metal", 4, "shell", E_HITCH)
    add("Lock indicator (green when locked)",
        _cyl_x(hitch_end[0] + 28, hitch_end[1] + 14, hitch_end[2] + 20, 7, 6), C_GREEN_LIT, "plastic", 4, "shell", E_HITCH)
    # secondary safety strap: from the hitch arm around the bicycle's left chainstay
    sa = (hitch_end[0] + 60, hitch_end[1] - 80, hitch_end[2] + 1)
    strap = fuse([tube(hitch_end, (hitch_end[0] - 40, -64, h[2] - 8), 6),
                  tube((hitch_end[0] - 40, -64, h[2] - 8), (-160, -52, 320), 6),
                  Pos(-160, -52, 320) * Rot(0, 0, 0) * Sphere(9)])
    add("Safety strap (fabric)", strap, C_BLACK, "fabric", 4, "shell", (-200, -520, -380))

    # ---------------------------------------------------------------- 5 load cell, clevises, clear guard
    E_CELL = (0, -420, -560)
    cz = zc((c0 + c1) / 2)
    cell = box(c0 + 30, c1 - 30, -22, 22, cz - 32, cz + 32)
    cell -= box(c0 + 30 - 1, c0 + 30 + 34, -30, 30, cz - 2, cz + 6)        # the S shape: two opposed slots
    cell -= box(c1 - 30 - 34, c1 - 30 + 1, -30, 30, cz - 6, cz + 2)
    cell = _fillet_try(cell, cell.edges().filter_by(Axis.Y), [1.5, 0.8])
    cell += _cyl_y((c0 + c1) / 2, 0, cz + 14, 4.5, 50)                        # gauge window plugs
    add("S-type load cell", cell, C_CELL, "metal", 5, "internal", E_CELL)
    clev = []
    for xa, xb in ((c0, c0 + 30), (c1 - 30, c1)):
        cl = box(xa, xb, -18, 18, cz - 36 if xa == c0 else cz - 36, cz + 36) - box(xa + (8 if xa == c0 else -1), xb - (-1 if xa == c0 else 8), -8, 8, cz - 40, cz + 40)
        cl = _fillet_try(cl, cl.edges().filter_by(Axis.Y), [3.0, 1.5])
        clev.append(cl)
        clev.append(_cyl_y((xa + xb) / 2, 0, cz, 5, 48))                     # clevis pins
    clev.append(tube((c0 - 6, 0, zc(c0 - 6)), (c0, 0, zc(c0)), 14))
    clev.append(tube((c1, 0, zc(c1)), (c1 + 6, 0, zc(c1 + 6)), 14))
    add("Load cell clevises and pins", fuse(clev), C_STEEL, "metal", 5, "internal", E_CELL)
    add("Load cell cable", fuse([tube((c1 - 34, 22, cz + 10), (c1 - 20, 34, cz + 10), 3.5),
                                  tube((c1 - 20, 34, cz + 10), (k0 + 40, 32, zc(k0 + 40) - 10), 3.5)]),
        C_BLACK, "rubber", 5, "internal", E_CELL)
    gr = 44.0
    guard = _cyl_x((c0 + c1) / 2, 0, cz, gr, c1 - c0 + 12) - _cyl_x((c0 + c1) / 2, 0, cz, gr - 2.5, c1 - c0 + 16)
    add("Load cell guard, clear polycarbonate", guard, C_GUARD, "clear", 5, "shell", (0, -420, -380))
    rings = fuse([_cyl_x(x, 0, zc(x), gr + 2, 10) - _cyl_x(x, 0, zc(x), 20.5, 12) for x in (c0 - 1, c1 + 1)])
    add("Guard end rings", rings, C_ACCENT, "plastic", 5, "shell", (0, -420, -380))

    # ---------------------------------------------------------------- 6 overrun coupler
    E_CPL = (0, -140, -700)
    sleeve = tube((k0 + 60, 0, zc(k0 + 60)), (k1, 0, zc(k1)), 27)
    add("Coupler sleeve", sleeve, C_DRAW, "painted", 6, "shell", E_CPL)
    gait = None
    for i in range(7):
        xa = k0 + 4 + i * 8
        r_ = 30 if i % 2 == 0 else 25
        g = tube((xa, 0, zc(xa)), (xa + 8, 0, zc(xa + 8)), r_)
        gait = g if gait is None else gait + g
    add("Coupler gaiter (rubber)", gait, C_RUBBER, "rubber", 6, "shell", E_CPL)
    damp = _rbox(k0 + 60, k0 + 170, -15, 15, zc(k0) + 25, zc(k0) + 55, r_all=6.0)
    add("Damper housing", damp, C_ALU, "metal", 6, "shell", E_CPL)
    lever = _rbox(k1 - 50, k1 - 20, -40, 40, zc(k1) - 45, zc(k1) - 20, r_all=4.0)
    add("Brake lever and equalizer", lever, C_STEEL, "metal", 6, "shell", E_CPL)
    cables = fuse([tube((k1 - 35, s * 40, zc(k1) - 32), (x0 + 200, s * 200, fz0 - 6), 3.0) for s in (-1, 1)]
                  + [tube((x0 + 200, s * 200, fz0 - 6), (ax - 40, s * (D["d_in"] - 10), wr + 30), 3.0) for s in (-1, 1)])
    add("Brake cables", cables, C_BLACK, "rubber", 6, "shell", E_CPL)
    add("Coupler bolts", fuse([_cyl_y(x, 0, zc(x), 6, 64) for x in (k0 + 80, k1 - 10)]), C_ALU, "metal", 18, "shell", E_CPL)

    # ---------------------------------------------------------------- 7 hub motor wheel, 8 idler wheel
    E_MW = (0, -620, 0)
    t, r_, sp = _wheel(ax, yL, wr, wr, P["tyre_w"], 16, 70.0, 22.0)
    add("Hub motor wheel tyre", t, C_TYRE, "rubber", 7, "shell", E_MW)
    add("Hub motor wheel rim", r_, C_RIM, "metal", 7, "shell", E_MW)
    add("Hub motor wheel spokes", sp, C_ALU, "metal", 7, "shell", E_MW)
    mot = _cyl_y(ax, yL, wr, 78, 60)
    mot = _fillet_try(mot, mot.edges(), [10.0, 6.0, 3.0])
    for s in (-1, 1):                                                   # spoke flanges
        mot += _cyl_y(ax, yL + s * 22, wr, 82, 4)
    add("Hub motor shell, 250 W geared", mot, C_MOTOR, "painted", 7, "shell", E_MW)
    cover = _cyl_y(ax, yL - 31, wr, 56, 3) - _cyl_y(ax, yL - 31, wr, 20, 5)
    add("Hub motor cover ring", cover, C_ACCENT, "painted", 7, "shell", E_MW)
    bolts = fuse([_cyl_y(ax + 66 * math.cos(math.radians(a)), yL - 31, wr + 66 * math.sin(math.radians(a)), 3.2, 3)
                  for a in range(15, 360, 60)])
    bolts += _cyl_y(ax, yL, wr, 7, P["hub_old"] + 30)                   # axle ends
    bolts += Pos(ax, yL - P["hub_old"] / 2 - 12, wr) * Rot(90, 0, 0) * extrude(RegularPolygon(10, 6), amount=10, both=True)
    add("Hub motor bolts and axle", bolts, C_ALU, "metal", 7, "shell", E_MW)
    add("Hub motor cable", fuse([tube((ax, yL + 50, wr), (ax - 60, yL + 60, wr + 70), 4),
                                  tube((ax - 60, yL + 60, wr + 70), (ax - 120, -hw + 40, fz0 - 20), 4)]),
        C_BLACK, "rubber", 7, "shell", E_MW)
    E_IW = (0, 480, 0)
    t, r_, sp = _wheel(ax, yR, wr, wr, P["tyre_w"], 16, 28.0, 30.0)
    add("Idler wheel tyre", t, C_TYRE, "rubber", 8, "shell", E_IW)
    add("Idler wheel rim", r_, C_RIM, "metal", 8, "shell", E_IW)
    add("Idler wheel spokes", sp, C_ALU, "metal", 8, "shell", E_IW)
    hub = _cyl_y(ax, yR, wr, 18, P["hub_old"] - 4)
    for s in (-1, 1):
        hub += _cyl_y(ax, yR + s * 30, wr, 30, 4)
    hub += _cyl_y(ax, yR, wr, 7, P["hub_old"] + 30)
    hub += Pos(ax, yR + P["hub_old"] / 2 + 12, wr) * Rot(90, 0, 0) * extrude(RegularPolygon(10, 6), amount=10, both=True)
    add("Idler hub", hub, C_ALU, "metal", 8, "shell", E_IW)

    # ---------------------------------------------------------------- 9 disc brakes: slotted rotors, calipers
    rr = P["rotor_d"] / 2
    rot_s, cal_s = [], []
    for s in (-1, 1):
        y = s * (D["d_in"] + 15)
        rt = _cyl_y(ax, y, wr, rr, 2) - _cyl_y(ax, y, wr, 30, 3)
        for kk in range(6):
            a = math.radians(kk * 60 + 30)
            rt -= Pos(ax + 62 * math.cos(a), y, wr + 62 * math.sin(a)) * Rot(90, 0, 0) * Rot(0, 0, -math.degrees(a) + 90) * \
                extrude(SlotOverall(26, 9), amount=4, both=True)
        rot_s.append(rt)
        cal = _rbox(ax + rr - 25, ax + rr + 20, y - 14, y + 14, wr - 25, wr + 25, r_all=5.0)
        cal_s.append(cal)
    E_BRK = (260, 0, -300)
    add("Brake rotors, 180 mm", fuse(rot_s), C_STEEL, "metal", 9, "shell", E_BRK)
    add("Brake calipers", fuse(cal_s), C_BLACK, "painted", 9, "shell", E_BRK)

    # ---------------------------------------------------------------- 10 enclosure: closed, vents, window, controls
    ex0, el, ew, eh = P["enc"]
    ez0, ez1 = D["enc_z"]
    ex1 = ex0 + el
    E_ENC = (0, 0, -520)
    enc = _rbox(ex0, ex1, -ew / 2, ew / 2, ez0, ez1, r_vert=10.0)
    enc = _fillet_try(enc, enc.faces().sort_by(Axis.Z)[0].edges(), [6.0, 3.0])
    enc -= _rbox(ex0 + 3, ex1 - 3, -ew / 2 + 3, ew / 2 - 3, ez0 + 3, ez1 - 3, r_vert=7.0)
    seam_z = ez1 - 28
    enc -= _rbox(ex0 - 2, ex1 + 2, -ew / 2 - 2, ew / 2 + 2, seam_z - 0.8, seam_z + 0.8, r_vert=12.0) - \
        _rbox(ex0 + 0.8, ex1 - 0.8, -ew / 2 + 0.8, ew / 2 - 0.8, seam_z - 2, seam_z + 2, r_vert=9.2)
    for i in range(6):                                               # louvre vents on the +Y side
        enc -= box(ex0 + 70 + i * 32, ex0 + 86 + i * 32, ew / 2 - 5, ew / 2 + 1, ez0 + 40, ez0 + 110)
    win = (ex0 + 30, ex0 + 250, ez0 + 40, ez0 + 130)                 # inspection window on the -Y side
    enc -= box(win[0], win[1], -ew / 2 - 1, -ew / 2 + 5, win[2], win[3])
    for (yy, zz, rr_) in ((-90, 335, 11), (-20, 330, 13), (40, 335, 4.5), (100, 325, 13)):
        enc -= _cyl_x(ex0, yy, zz - (ez1 - 378), rr_, 8)
    add("Enclosure, galvanized steel", enc, C_GALV, "metal", 10, "shell", E_ENC)
    glass = box(win[0] - 8, win[1] + 8, -ew / 2 - 1.5, -ew / 2, win[2] - 8, win[3] + 8)
    glass = _fillet_try(glass, glass.edges().filter_by(Axis.Y), [6.0, 3.0])
    add("Enclosure window, clear polycarbonate", glass, C_GUARD, "clear", 10, "shell", (0, -160, -520))
    screws = []
    for yy in (-ew / 2 + 18, ew / 2 - 18):
        for zz in (ez0 + 18, ez1 - 12):
            screws.append(_cyl_x(ex0 - 1, yy, zz, 4.5, 2.5))
    for xx in (ex0 + 18, ex1 - 18):
        for zz in (ez0 + 18, ez1 - 12):
            screws.append(Pos(xx, -ew / 2 - 1, zz) * Rot(90, 0, 0) * Cylinder(4.5, 2.5))
            screws.append(Pos(xx, ew / 2 + 1, zz) * Rot(90, 0, 0) * Cylinder(4.5, 2.5))
    add("Enclosure screws", fuse(screws), C_ALU, "metal", 18, "shell", E_ENC)
    dzs = ez1 - 378
    key = _cyl_x(ex0 - 5, -90, 335 + dzs, 13, 12) + box(ex0 - 12, ex0 - 9, -90 - 2, -90 + 2, 335 + dzs - 8, 335 + dzs + 8)
    add("Key switch", key, C_ALU, "metal", 14, "shell", E_ENC)
    knob = _cyl_x(ex0 - 10, -20, 330 + dzs, 16, 18)
    knob = _fillet_try(knob, knob.faces().sort_by(Axis.X)[0].edges(), [3.0, 1.5])
    for kk in range(12):                                             # knurl flutes
        a = math.radians(kk * 30)
        knob -= _cyl_x(ex0 - 10, -20 + 16.5 * math.cos(a), 330 + dzs + 16.5 * math.sin(a), 1.6, 20)
    add("Assist gain dial (G 2 to 6)", knob, C_BLACK, "rubber", 13, "shell", E_ENC)
    ptr = box(ex0 - 20, ex0 - 18.5, -21.5, -18.5, 330 + dzs + 4, 330 + dzs + 14)
    dots = fuse([_cyl_x(ex0 - 0.6, -20 + 26 * math.cos(math.radians(a)), 330 + dzs + 26 * math.sin(math.radians(a)), 2.0, 1.2)
                 for a in (-30, 15, 60, 105, 150)])
    add("Gain dial pointer and scale", ptr + dots, C_ACCENT, "plastic", 13, "shell", E_ENC)
    led = _cyl_x(ex0 - 2.5, 40, 335 + dzs, 4.2, 5)
    led = _fillet_try(led, led.faces().sort_by(Axis.X)[0].edges(), [2.0, 1.2, 0.6])
    add("Status light (lit)", led, C_GREEN_LIT, "emissive", 13, "shell", E_ENC)
    port = _cyl_x(ex0 - 6, 100, 325 + dzs, 14, 12) - _cyl_x(ex0 - 12, 100, 325 + dzs, 9, 6)
    port += _cyl_x(ex0 - 6, 100, 325 + dzs, 4, 6)
    add("Charge port with cap", port, C_BLACK, "rubber", 14, "shell", E_ENC)
    glands = fuse([_cyl_x(ex1 + 6, yy, ez0 + 30, 9, 12) for yy in (-100, 100)] + [_cyl_x(ex0 - 6, 0, ez0 + 60, 9, 12)])
    add("Cable glands", glands, C_BLACK, "plastic", 14, "shell", E_ENC)
    lab = box(ex0 + 30, ex0 + 250, -ew / 2 - 0.8, -ew / 2, ez0 + 140, ez0 + 158)
    add("Enclosure warning label", lab, C_AMBER, "paper", 10, "shell", E_ENC)

    # ---------------------------------------------------------------- 11 pack, 12 controller, 13 board (inside)
    pl, pw, ph = P["pack"]
    pk = _rbox(ex0 + 12, ex0 + 12 + pl, -ew / 2 + 12, -ew / 2 + 12 + pw, ez0 + 4, ez0 + 4 + ph, r_all=6.0)
    add("LiFePO4 pack, 384 Wh", pk, C_PACK, "plastic", 11, "internal", (0, -380, -1000))
    plab = box(ex0 + 40, ex0 + 12 + pl - 28, -ew / 2 + 11.4, -ew / 2 + 12, ez0 + 50, ez0 + 110)
    add("Pack label", plab, "#F3F4F6", "paper", 11, "internal", (0, -380, -1000))
    ctl = _rbox(ex0 + 12, ex0 + 132, 45, 115, ez0 + 4, ez0 + 40, r_vert=4.0)
    for i in range(7):
        ctl += box(ex0 + 18 + i * 16, ex0 + 24 + i * 16, 47, 113, ez0 + 40, ez0 + 49)
    add("Motor controller, finned", ctl, "#6B7280", "metal", 12, "internal", (0, 240, -900))
    bx0, bx1 = ex0 + 150, ex0 + 240
    pcb = box(bx0, bx1, 60, 120, ez0 + 4, ez0 + 6)
    add("Control board PCB", pcb, C_PCB, "plastic", 13, "internal", (0, 380, -820))
    comps = fuse([box(bx0 + 10, bx0 + 30, 70, 90, ez0 + 6, ez0 + 9), box(bx0 + 40, bx0 + 55, 75, 85, ez0 + 6, ez0 + 8),
                  box(bx1 - 20, bx1 - 5, 95, 115, ez0 + 6, ez0 + 18), box(bx0 + 10, bx0 + 40, 100, 115, ez0 + 6, ez0 + 30)])
    add("Control board components", comps, C_CHIP, "plastic", 13, "internal", (0, 380, -820))

    # ---------------------------------------------------------------- 14 harness (as model.py)
    add("Wiring harness", m["harness"], C_BLACK, "rubber", 14, "internal", (0, 0, -700))

    # ---------------------------------------------------------------- 15 lights, reflectors, flag
    E_LT = (360, 0, 300)
    lh, lens = [], []
    for s in (-1, 1):
        ya, yb = sorted((s * (hw - 30), s * (hw - 130)))
        hsg = _rbox(x1 + 2, x1 + 22, ya, yb, fz0 - 4, fz1 + 4, r_all=4.0)
        lh.append(hsg)
        lens.append(_rbox(x1 + 21, x1 + 24, ya + 8, yb - 8, fz0 + 2, fz1 - 2, r_all=1.0))
    add("Rear light housings", fuse(lh), C_BLACK, "plastic", 15, "shell", E_LT)
    add("Rear lights (lit)", fuse(lens), C_RED_LIT, "emissive", 15, "shell", E_LT)
    refl = fuse([_rbox(x0 + 400, x0 + 480, -hw - 4, -hw, fz0 + 3, fz1 - 3, r_all=1.2),
                 _rbox(x0 + 400, x0 + 480, hw, hw + 4, fz0 + 3, fz1 - 3, r_all=1.2)])
    add("Side reflectors", refl, C_AMBER, "plastic", 15, "shell", (0, 0, -80))
    E_FLAG = (-320, -560, 700)
    fp = (x0 + 30, -hw + 20)
    pole = tube((fp[0], fp[1], dz), (fp[0], fp[1], D["flag_top"]), 6) + Pos(fp[0], fp[1], D["flag_top"]) * Sphere(9)
    pole += Pos(fp[0], fp[1], dz + 20) * Cylinder(14, 40)
    add("Flag pole", pole, C_BLACK, "plastic", 15, "shell", E_FLAG)
    ft = D["flag_top"]
    flag = extrude(Plane.XZ * Pos(0, 0) * RectangleRounded(220, 150, 6), amount=1.5)
    flag = Pos(fp[0] + 118, fp[1] + 0.75, ft - 85) * flag
    add("Safety flag (fabric)", flag, C_FLAG, "fabric", 15, "shell", E_FLAG)

    # ---------------------------------------------------------------- 16 parking stand
    sx = P["stand_x"]
    E_ST = (-160, 0, -450)
    leg = tube((sx, 0, P["nose_z"] - 15), (sx, 0, 25), 11) + _cyl_y(sx, 0, P["nose_z"] - 40, 16, 40)
    add("Parking stand leg", leg, C_FRAME, "painted", 16, "shell", E_ST)
    foot = _rbox(sx - 50, sx + 50, -35, 35, 0, 25, r_all=6.0)
    add("Parking stand foot (rubber)", foot, C_RUBBER, "rubber", 16, "shell", E_ST)

    # ---------------------------------------------------------------- 17 charger (accessory, off the trailer)
    chg = _rbox(1350, 1560, -1150, -1060, 0, 60, r_all=8.0)
    add("Charger, 43.8 V 4 A", chg, C_BLACK, "plastic", 17, "accessory", (0, 0, 0))
    add("Charger lead", fuse([tube((1350, -1105, 30), (1250, -1105, 30), 4), tube((1250, -1105, 30), (1180, -1000, 10), 4)]),
        C_RUBBER, "rubber", 17, "accessory", (0, 0, 0))

    # ---------------------------------------------------------------- context: load, bicycle, rider
    crate = _rbox(x0 + 120, x0 + 520, -250, 250, dz + 2.5, dz + 300, r_all=10.0)
    crate -= _rbox(x0 + 140, x0 + 500, -230, 230, dz + 20, dz + 320, r_vert=8.0)
    for xx in (x0 + 120, x0 + 520):
        crate -= Pos(xx, 0, dz + 250) * Rot(0, 90, 0) * Rot(0, 0, 90) * extrude(SlotOverall(110, 30), amount=30, both=True)
    add("Crate (load)", crate, "#A7AFB9", "plastic", None, "context", (0, 0, 0))
    boxes = _rbox(x0 + 620, x0 + 980, -260, 60, dz + 2.5, dz + 260, r_all=3.0)
    boxes += _rbox(x0 + 640, x0 + 940, 90, 290, dz + 2.5, dz + 200, r_all=3.0)
    add("Cartons (load)", boxes, C_BOXES, "paper", None, "context", (0, 0, 0))
    strap = box(x0 + 790, x0 + 830, -hw + 70 - 12, -hw + 70 + 12, dz + 2.5, dz + 262) + \
        box(x0 + 790, x0 + 830, -hw + 70, 60, dz + 260, dz + 263) + \
        box(x0 + 790, x0 + 830, 60, 63, dz + 2.5, dz + 263)
    add("Load strap (fabric)", strap, C_ACCENT, "fabric", None, "context", (0, 0, 0))

    frame, saddle, grips, drive, pedals, tyres, rims = _bicycle()
    add("Bicycle frame (context)", frame, C_BIKE, "painted", None, "context", (0, 0, 0))
    add("Bicycle saddle and grips (context)", saddle + grips, C_RUBBER, "rubber", None, "context", (0, 0, 0))
    add("Bicycle drivetrain (context)", drive + pedals, "#6B7280", "metal", None, "context", (0, 0, 0))
    add("Bicycle tyres (context)", tyres, C_TYRE, "rubber", None, "context", (0, 0, 0))
    add("Bicycle rims and spokes (context)", rims, C_RIM, "metal", None, "context", (0, 0, 0))

    from context_parts import mannequin
    rider = Pos(*_RIDER_SHIFT) * Rot(0, 0, -90) * mannequin(RIDER_H, "ride")
    add("Rider, 1.75 m mannequin (scale)", rider, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:40s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.1f} cm3")
