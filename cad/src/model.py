"""CargoMule parametric model (build123d), TRL 3, constructable design (CGM-DDR-003).

Run from the repo root:  python cad/src/model.py [--check]
Exports STEP and STL into cad/step and cad/stl and prints the constructability checks
(--check prints the checks only and exits non-zero if any fails):
    cargomule-assembly.step / .stl   whole trailer, hitched position
    frame.step / .stl                welded chassis with the coupler housing, dropouts and wheel arch frames
    drawbar-assembly.step / .stl     hitch, bent drawbar, load cell, pull rod, spring and brake lever
    deck.step / .stl                 plywood deck, removable side boards and their fittings
    enclosure.step / .stl            battery and electronics enclosure with its door

Axes: X points rearward from the towing bicycle's rear axle (x = 0) toward the trailer,
Y is across the trailer (the hitch is on the bike's left, -Y), Z is up with the ground at
z = 0. Every component is modelled as it is made: hollow tube and box section, plates with
their holes and slots, and the fixings that hold each part to the next. The same PARAMS feed
docs/04-calcs/sizing.py (CGM-CAL-001), the drawing CGM-DWG-001 (cad/src/sheets.py) and the
build plan pictures (cad/src/build_plan_media.py). Not for fabrication before TRL 4.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # wheels: 20 x 2.15 in (ETRTO 406), front-style hubs with 100 mm over-locknut spacing
    "wheel_r": 258.0, "tyre_w": 55.0, "hub_old": 100.0, "rotor_d": 180.0,
    # rotor_d: 180 mm rotors with metallic pads (CGM-DDR-002), was 160 mm
    "track": 800.0,                  # wheel center to wheel center
    "axle_x": 1920.0,                # 20 mm behind the deck center (tongue load, CGM-CAL-001 section A)
    "axle_d": 10.0, "slot_w": 10.2,  # axle across the flats and the dropout slot width
    # deck and chassis
    "deck_x0": 1300.0, "deck_len": 1200.0, "deck_w": 700.0,
    "deck_z": 420.0,                 # deck top above ground
    "deck_t": 12.0, "board_h": 150.0, "board_t": 9.0,
    "rail": 30.0, "rail_t": 1.5,     # 30 x 30 x 1.5 mm steel box section
    "cross_x": (1600.0, 1920.0, 2250.0),
    "nose_x": 1200.0, "nose_z": 356.0,   # where the A-frame nose bars meet the coupler housing
    "nose_tube": (28.0, 1.5),        # A-frame nose bars, OD and wall
    "arch_tube": (25.0, 1.5),        # wheel arch frame (carries the outer dropout)
    "arch_half": 300.0, "arch_gap": 30.0,
    "plate_t": 5.0,                  # dropout plates
    "inner_plate_x": (-45.0, 125.0), # inner dropout plate, from the axle; the rear part is the caliper tab
    "outer_plate_x": (-30.0, 30.0),
    # hitch and bent drawbar
    "hitch": (0.0, -95.0, 340.0),    # on the bicycle's left rear axle end
    "hitch_joint": (10.0, -130.0, 340.0),
    "knees": ((30.0, -360.0, 342.0), (550.0, -360.0, 348.0)),  # outward run that clears the bike's rear tyre
    "straight_x": 700.0,             # drawbar runs straight along X, on the center line, from here back
    "bend_r": 115.0,                 # centre-line bend radius of the three drawbar bends
    "drawbar": (38.0, 2.5),          # OD and wall, S355 tube
    "drawbar_end": 975.0,            # rear end of the drawbar tube inside the coupler housing, at rest
    "pin_x": 820.0, "pin_d": 12.0,   # anti-rotation and overload pin on the drawbar
    # overrun coupler and load cell, on the center line at z = nose_z
    "housing": (60.3, 2.0, 880.0, 1250.0),       # OD, wall, front end, rear end
    "bush_front": (880.0, 905.0), "bush_rear": (940.0, 965.0),
    "eye_x": 995.0,                              # rod end eye on the drawbar end: the clevis pin
    "window": (985.0, 1055.0),                   # access window in the housing's right side for the clevis pin
    "cell": (13.0, 51.0, 61.0),                  # S-type cell thickness (Y), height (Z), length (X)
    "bulkhead_x": 1145.0, "cap_t": 6.0, "ring_t": 3.0, "flange_d": 80.0,
    "rod_d": 10.0,
    "coupler_stroke": 50.0,
    "pivot": (1273.0, 250.0),        # brake lever pivot (x, z)
    "lever_arms": (106.0, 13.8),     # upper (rod) arm and lower (cable) arm: 7.7 to 1
    # enclosure (0.8 mm galvanized steel, hung under the crossmembers at 1600 and 1920)
    "enc": (1585.0, 350.0, 300.0, 170.0),   # x0, length, width, height
    "enc_wall": 0.8,
    "pack": (250.0, 170.0, 150.0),
    # stand, lights and flag
    "stand_x": 905.0, "flag_h": 1150.0,
}

# derived positions the scripts quote
P = PARAMS
P["cell_x"] = (P["eye_x"] + 30.0, P["eye_x"] + 30.0 + P["cell"][2])
P["coupler_x"] = (P["housing"][2], P["housing"][3] + P["ring_t"] + P["cap_t"])


@dataclass
class Comp:
    name: str
    shape: object
    bom: int
    kind: str     # made, bought, fixing


def derived(p=PARAMS):
    """Dimensions the calc note and drawings quote, computed from PARAMS."""
    fz1 = p["deck_z"] - p["deck_t"]
    fz0 = fz1 - p["rail"]
    hw = p["deck_w"] / 2
    yc = p["track"] / 2
    d_in, d_out = yc - p["hub_old"] / 2, yc + p["hub_old"] / 2          # dropout inner faces
    arch_y = d_out + p["plate_t"] + p["arch_tube"][0] / 2
    x0, x1 = p["deck_x0"], p["deck_x0"] + p["deck_len"]
    enc = p["enc"]
    return {
        "fz0": fz0, "fz1": fz1, "hw": hw, "yc": yc, "d_in": d_in, "d_out": d_out, "arch_y": arch_y,
        "deck_x1": x1, "deck_cx": (x0 + x1) / 2, "deck_area_m2": p["deck_len"] * p["deck_w"] / 1e6,
        "width": 2 * (arch_y + p["arch_tube"][0] / 2),
        "length": x1 + 20.0,                                  # rear lights stand 20 mm proud
        "tyre_gap": yc - p["tyre_w"] / 2 - hw,                # tyre to side rail
        "arch_top": 2 * p["wheel_r"] + p["arch_gap"],
        "enc_x": (enc[0], enc[0] + enc[1]), "enc_z": (fz0 - enc[3], fz0),
        "ground_clear": fz0 - enc[3],
        "flag_top": p["deck_z"] + p["flag_h"],
        "axle_behind_center": p["axle_x"] - (x0 + x1) / 2,
        "zc": p["nose_z"],
        "lever_ratio": p["lever_arms"][0] / p["lever_arms"][1],
    }


def drawbar_points(p=PARAMS):
    """Corner points of the drawbar centre line from the hitch to its rear end (bends are
    radiused at bend_r between these corners)."""
    zc = p["nose_z"]
    return [p["hitch"], *p["knees"], (p["straight_x"], 0.0, zc), (p["drawbar_end"], 0.0, zc)]


# ---------------------------------------------------------------- geometry helpers
def _b3d():
    import build123d as b
    return b


def box(x0, x1, y0, y1, z0, z1):
    b = _b3d()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def tube(a, c, r):
    b = _b3d()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def hollow(a, c, r, t):
    return tube(a, c, r) - tube(a, c, r - t)


def xcyl(x0, x1, y, z, r):
    return tube((x0, y, z), (x1, y, z), r)


def ycyl(y0, y1, x, z, r):
    return tube((x, y0, z), (x, y1, z), r)


def zcyl(z0, z1, x, y, r):
    return tube((x, y, z0), (x, y, z1), r)


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def rhs(x0, x1, y0, y1, z0, z1, t, axis, capped=False):
    """Hollow rectangular section running along axis 'x' or 'y', open at both ends or (capped)
    closed by welded end plates."""
    outer = box(x0, x1, y0, y1, z0, z1)
    e = -t if capped else 1
    if axis == "x":
        inner = box(x0 - e, x1 + e, y0 + t, y1 - t, z0 + t, z1 - t)
    else:
        inner = box(x0 + t, x1 - t, y0 - 1, y1 + 1, z0 + t, z1 - t)
    return outer - inner


def polyline_tube(pts, r):
    """A cable or wire run: straight pieces with rounded joints."""
    b = _b3d()
    segs = [tube(pts[i], pts[i + 1], r) for i in range(len(pts) - 1)]
    segs += [b.Pos(*q) * b.Sphere(r) for q in pts[1:-1]]
    return fuse(segs)


def wheel(cx, cy, cz, r, w, spokes=16):
    """Tyre, rim and a single plane of spokes (the hub is added separately)."""
    b = _b3d()
    tyre = b.Pos(cx, cy, cz) * b.Rot(90, 0, 0) * b.Torus(r - w / 2, w / 2)
    rim = b.Pos(cx, cy, cz) * b.Rot(90, 0, 0) * (b.Cylinder(r - w + 8, 20) - b.Cylinder(r - w - 6, 22))
    sp = fuse(tube((cx + 21 * math.cos(math.radians(k * 360 / spokes)), cy, cz + 21 * math.sin(math.radians(k * 360 / spokes))),
                   (cx + (r - w - 5) * math.cos(math.radians(k * 360 / spokes)), cy,
                    cz + (r - w - 5) * math.sin(math.radians(k * 360 / spokes))), 1.8)
              for k in range(spokes))
    return tyre + rim + sp


# ---------------------------------------------------------------- components
def build_components(p=PARAMS):
    """Every component as a Comp, keyed by a short name."""
    b = _b3d()
    D = derived(p)
    C = {}

    def add(key, name, shape, bom, kind):
        C[key] = Comp(name, shape, bom, kind)

    x0, x1, hw, R, rt = p["deck_x0"], D["deck_x1"], D["hw"], p["rail"], p["rail_t"]
    fz0, fz1, ax, wr = D["fz0"], D["fz1"], p["axle_x"], p["wheel_r"]
    zr = (fz0 + fz1) / 2
    zc = D["zc"]
    hod, ht, hx0, hx1 = p["housing"]
    hr, hri = hod / 2, hod / 2 - ht

    # ---------------- 1 chassis frame: hollow box perimeter and crossmembers, nose bars, dropouts, arch frames
    rails = [rhs(x0, x1, -hw, -hw + R, fz0, fz1, rt, "x", True), rhs(x0, x1, hw - R, hw, fz0, fz1, rt, "x", True),
             rhs(x0, x0 + R, -hw + R, hw - R, fz0, fz1, rt, "y"), rhs(x1 - R, x1, -hw + R, hw - R, fz0, fz1, rt, "y")]
    rails += [rhs(x - R / 2, x + R / 2, -hw + R, hw - R, fz0, fz1, rt, "y") for x in p["cross_x"]]
    rails = fuse(rails)
    for x in p["cross_x"][:2]:                        # rivet-nut holes for the enclosure bolts
        for y in (-100.0, 100.0):
            rails -= zcyl(fz0 - 1, fz0 + rt + 1, x, y, 3.0)
    add("rails", "Perimeter rails and crossmembers", rails, 1, "made")

    nr, nt = p["nose_tube"][0] / 2, p["nose_tube"][1]
    nb = []
    for s in (-1, 1):
        a = (x0 + 20, s * (hw - 15), fz0 + 15)
        c = (p["nose_x"], s * 18.0, zc)
        u = [c[i] - a[i] for i in range(3)]
        L = math.sqrt(sum(v * v for v in u))
        a2 = tuple(a[i] - u[i] / L * 40 for i in range(3))
        bar = hollow(a2, c, nr, nt) - box(x0, x0 + 200, -hw - 50, hw + 50, fz0 - 100, fz1 + 100)
        bar = bar - xcyl(hx0 - 10, hx1 + 10, 0, zc, hr)
        nb.append(bar)
    add("nose_bars", "A-frame nose bars (2)", fuse(nb), 1, "made")

    sw, pt = p["slot_w"], p["plate_t"]
    dro, arch = [], []
    ar, at = p["arch_tube"][0] / 2, p["arch_tube"][1]
    for s in (-1, 1):
        yi0, yi1 = sorted((s * (D["d_in"] - pt), s * D["d_in"]))
        ix0, ix1 = p["inner_plate_x"]
        plate = box(ax + ix0, ax + ix1, yi0, yi1, wr - 40, wr + 40) + box(ax + ix0, ax - ix0, yi0, yi1, wr + 40, fz0)
        plate -= box(ax - sw / 2, ax + sw / 2, yi0 - 1, yi1 + 1, wr - 41, wr) + ycyl(yi0 - 1, yi1 + 1, ax, wr, sw / 2)
        for dz in (-18.0, 18.0):                      # two 6.5 mm holes for the caliper adapter
            plate -= ycyl(yi0 - 1, yi1 + 1, ax + 100, wr + dz, 3.25)
        plate -= ycyl(yi0 - 1, yi1 + 1, ax, wr + 60, 3.25)  # torque arm bolt hole
        dro.append(plate)
        yo0, yo1 = sorted((s * D["d_out"], s * (D["d_out"] + pt)))
        ox0, ox1 = p["outer_plate_x"]
        op = box(ax + ox0, ax + ox1, yo0, yo1, wr - 40, wr + 40)
        op -= box(ax - sw / 2, ax + sw / 2, yo0 - 1, yo1 + 1, wr - 41, wr) + ycyl(yo0 - 1, yo1 + 1, ax, wr, sw / 2)
        dro.append(op)
        ya = s * D["arch_y"]
        xa, xb = ax - p["arch_half"], ax + p["arch_half"]
        zt = D["arch_top"]
        segs = [((xa, s * hw, zr), (xa, ya, zr)), ((xb, s * hw, zr), (xb, ya, zr)),
                ((xa, ya, zr), (xa + 80, ya, zt)), ((xa + 80, ya, zt), (xb - 80, ya, zt)),
                ((xb - 80, ya, zt), (xb, ya, zr)), ((ax, ya, zt), (ax, ya, wr + 20))]
        arch += [hollow(a, c, ar, at) for a, c in segs]
        arch += [b.Pos(*q) * b.Sphere(ar) for q in ((xa, ya, zr), (xb, ya, zr), (xa + 80, ya, zt), (xb - 80, ya, zt))]
        # tie-down eyes welded to the side rails
        arch += [b.Pos(x, s * (hw + 6), fz0 + 15) * b.Rot(0, 90, 0) * b.Torus(9, 3) for x in (x0 + 150, x1 - 150)]
    add("dropouts", "Dropout plates (4)", fuse(dro), 1, "made")
    add("arches", "Wheel arch frames and tie-down eyes", fuse(arch), 1, "made")

    # ---------------- 6 coupler housing (welded into the frame nose) and its fittings
    hous = xcyl(hx0, hx1, 0, zc, hr) - xcyl(hx0 - 1, hx1 + 1, 0, zc, hri)
    fl = p["flange_d"] / 2
    hous += xcyl(hx1 - 6, hx1, 0, zc, fl) - xcyl(hx1 - 7, hx1 + 1, 0, zc, hri)
    w0, w1 = p["window"]
    hous -= box(w0, w1, 15, 35, zc - 12, zc + 12)                 # clevis pin access window, right side
    # slotted fork on the top front (anti-rotation, and its closed front end is the overload stop),
    # stand clevis under the front, lever cheeks under the rear
    pr = p["pin_d"] / 2
    sf = p["pin_x"] - pr - 0.5                                    # front stop face, 0.5 mm ahead of the pin
    for s in (-1, 1):
        y0_, y1_ = sorted((s * (pr + 0.4), s * (pr + 5.4)))
        hous += box(sf - 5, 920, y0_, y1_, 385.0, zc + 46) - xcyl(hx0, 921, 0, zc, hri)
        y0_, y1_ = sorted((s * 12.5, s * 17.5))
        clev = box(890, 920, y0_, y1_, 300, 331) - ycyl(y0_ - 1, y1_ + 1, p["stand_x"], 310, 5.0)
        hous += clev - xcyl(hx0, hx1, 0, zc, hri)
        y0_, y1_ = sorted((s * 8.0, s * 12.0))
        px, pz = p["pivot"]
        cheek = box(px - 60, hx1 - 8, y0_, y1_, 241, 329) + box(hx1 - 8, px + 20, y0_, y1_, 241, 315) + box(px + 20, px + 35, y0_, y1_, 241, 262)
        cheek -= ycyl(y0_ - 1, y1_ + 1, px, pz, 4.0)
        hous += cheek - xcyl(hx0, hx1, 0, zc, hri)
    hous += box(sf - 5, sf, -(pr + 5.4), pr + 5.4, 385.0, zc + 46) - xcyl(hx0, 921, 0, zc, hri)   # stop plate
    px, pz = p["pivot"]
    hous += box(px + 35, px + 40, -12, 12, 228, 262) - xcyl(px + 34, px + 41, 0, pz - p["lever_arms"][1], 3.0)   # cable stop tab
    add("housing", "Coupler housing with fork, stand clevis and lever cheeks", hous, 6, "made")
    bf, br_ = p["bush_front"], p["bush_rear"]
    dr = p["drawbar"][0] / 2
    bush = (xcyl(bf[0], bf[1], 0, zc, hri) - xcyl(bf[0] - 1, bf[1] + 1, 0, zc, dr)) + \
           (xcyl(br_[0], br_[1], 0, zc, hri) - xcyl(br_[0] - 1, br_[1] + 1, 0, zc, dr))
    add("bushings", "Bushings (2)", bush, 6, "bought")
    # spring cage: tube with the bulkhead welded in its front end and a ring on its rear end that is
    # clamped between the housing flange and the end cap; the end cap is a bolted plate
    bh, rt_, ct_ = p["bulkhead_x"], p["ring_t"], p["cap_t"]
    cage_r = hri - 1.5
    cage = xcyl(bh, hx1, 0, zc, hri) - xcyl(bh + 6, hx1 + 1, 0, zc, cage_r)
    cage += xcyl(hx1, hx1 + rt_, 0, zc, fl) - xcyl(hx1 - 1, hx1 + rt_ + 1, 0, zc, cage_r)
    cage -= xcyl(bh - 1, bh + 7, 0, zc, 6.25) + tube((bh - 1, 18, zc + 15), (bh + 7, 18, zc + 15), 4.0)
    cap = xcyl(hx1 + rt_, hx1 + rt_ + ct_, 0, zc, fl)
    cap -= xcyl(hx1, hx1 + 20, 0, zc, 6.25) + tube((hx1, 18, zc + 15), (hx1 + 20, 18, zc + 15), 4.0)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        hole = xcyl(hx1 - 7, hx1 + 20, (fl - 7) * math.cos(a), zc + (fl - 7) * math.sin(a), 2.75)
        cap -= hole
        cage -= hole
    add("cage", "Spring cage with bulkhead", cage, 6, "made")
    add("end_cap", "End cap", cap, 6, "made")

    # ---------------- 3 drawbar: one bent tube, welded end plug, anti-rotation pin
    J = p["hitch_joint"]
    k1 = p["knees"][0]
    u = [k1[i] - J[i] for i in range(3)]
    Lu = math.sqrt(sum(v * v for v in u))
    u = [v / Lu for v in u]
    start = tuple(J[i] + 35 * u[i] for i in range(3))
    pts = [start, *p["knees"], (p["straight_x"], 0.0, zc), (p["drawbar_end"], 0.0, zc)]
    path = b.FilletPolyline(*pts, radius=p["bend_r"])
    pl = b.Plane(origin=start, z_dir=u)
    prof = pl * b.Circle(dr).face() - pl * b.Circle(dr - p["drawbar"][1]).face()
    bar = b.sweep(prof, path)
    lockhole = tube(tuple(J[i] + 65 * u[i] + (0, 0, -30)[i] for i in range(3)), tuple(J[i] + 65 * u[i] + (0, 0, 30)[i] for i in range(3)), 3.0)
    bar = bar - lockhole
    ce = p["drawbar_end"]
    plug = xcyl(ce - 15, ce, 0, zc, dr - p["drawbar"][1])
    bar = bar - zcyl(zc - 25, zc + 25, p["pin_x"], 0, pr)
    add("drawbar", "Drawbar with end plug", bar + plug, 3, "made")
    opin = zcyl(zc - dr - 8, 398.0, p["pin_x"], 0, pr) + zcyl(zc - dr - 16, zc - dr - 8, p["pin_x"], 0, 9.5)
    add("opin", "Overload pin (M12 shoulder bolt and nut)", opin, 3, "fixing")

    # ---------------- 4 hitch (bought): axle plate, three-axis joint, arm into the drawbar bore
    h = p["hitch"]
    hit = ycyl(h[1] - 7, h[1] + 7, h[0], h[2], 32) + ycyl(J[1] - 15, h[1] - 7, J[0], J[2], 20)
    hit += tube(J, tuple(J[i] + 95 * u[i] for i in range(3)), 16.0)
    hit -= lockhole
    lockp = tube(tuple(J[i] + 65 * u[i] + (0, 0, -24)[i] for i in range(3)), tuple(J[i] + 65 * u[i] + (0, 0, 24)[i] for i in range(3)), 3.0)
    add("hitch", "Universal axle hitch", hit, 4, "bought")
    add("hitch_pin", "Hitch locking pin", lockp, 4, "bought")

    # ---------------- 5 load cell: rod end on the drawbar, clevis and pin, S-type cell; pull rod, spring
    ex_ = p["eye_x"]
    reye = xcyl(ce, ex_ - 12, 0, zc, 5.0) + (ycyl(-7, 7, ex_, zc, 14.0) - ycyl(-8, 8, ex_, zc, 4.0))
    add("rod_end", "Rod end (spherical eye)", reye, 5, "bought")
    clev = xcyl(ex_ + 20, ex_ + 30, 0, zc, 14.0)
    for s in (-1, 1):
        y0_, y1_ = sorted((s * 7.5, s * 12.5))
        clev += box(ex_ - 14, ex_ + 20, y0_, y1_, zc - 14, zc + 14) - ycyl(y0_ - 1, y1_ + 1, ex_, zc, 4.0)
    ct, ch, cln = p["cell"]
    cx0 = ex_ + 30.0
    cell = clev + box(cx0, cx0 + cln, -ct / 2, ct / 2, zc - ch / 2, zc + ch / 2)
    add("cell", "S-type load cell with its clevis", cell, 5, "bought")
    cpin = ycyl(-16, 16, ex_, zc, 4.0) + ycyl(12.5, 17, ex_, zc, 6.5) + ycyl(-17, -12.5, ex_, zc, 6.5)
    add("clevis_pin", "Clevis pin (M8 bolt and nut)", cpin, 5, "fixing")
    rod_end = hx1 + rt_ + ct_ + 2.0
    rod = xcyl(cx0 + cln, rod_end, 0, zc, p["rod_d"] / 2)
    rod += xcyl(bh + 6, bh + 9, 0, zc, 20.0) + xcyl(bh + 9, bh + 17, 0, zc, 8.5)
    add("pull_rod", "Pull rod, spring seat washer and nut", rod, 6, "bought")
    spring = xcyl(bh + 9, hx1, 0, zc, 20.0) - xcyl(bh + 8, hx1 + 1, 0, zc, 17.0)
    add("spring", "Preload spring", spring, 6, "bought")

    # ---------------- brake lever, pivot bolt and brake cables
    px, pz = p["pivot"]
    ua, la = p["lever_arms"]
    lev = box(px - 10, px + 10, -3, 3, pz - la - 6, pz + ua + 12) - ycyl(-4, 4, px, pz, 4.0) - ycyl(-4, 4, px, pz - la, 2.5)
    add("lever", "Brake lever", lev, 6, "made")
    add("lever_bolt", "Lever pivot bolt and friction washers", ycyl(-15, 15, px, pz, 4.0) + ycyl(-8, -3, px, pz, 7.0) + ycyl(3, 8, px, pz, 7.0), 6, "fixing")

    # ---------------- 7 and 8 wheels, hubs, axles; torque arm on the motor side
    yL, yR = -D["yc"], D["yc"]
    for key, nm, yw, bomn in (("motor_wheel", "Hub motor wheel", yL, 7), ("idler_wheel", "Idler wheel", yR, 8)):
        s = -1 if yw < 0 else 1
        w = wheel(ax, yw, wr, wr, p["tyre_w"])
        hub = ycyl(s * D["d_in"], s * D["d_out"], ax, wr, 22.0)
        if key == "motor_wheel":
            hub += ycyl(s * (D["d_in"] + 16), s * (D["d_in"] + 84), ax, wr, 78.0)
        axle = ycyl(s * (D["d_in"] - pt - 12), s * (D["d_out"] + pt + 12), ax, wr, p["axle_d"] / 2)
        nuts = ycyl(s * (D["d_out"] + pt), s * (D["d_out"] + pt + 8), ax, wr, 8.5)
        nuts += ycyl(s * (D["d_in"] - pt - (5 if key == "motor_wheel" else 0)), s * (D["d_in"] - pt - (13 if key == "motor_wheel" else 8)), ax, wr, 8.5)
        add(key, nm, w + hub + axle + nuts, bomn, "bought")
    # torque arm: 5 mm plate on the inboard face of the left inner dropout, slotted over the axle flats
    yt0, yt1 = sorted((-(D["d_in"] - pt), -(D["d_in"] - pt - 5)))
    ta = box(ax - 12, ax + 12, yt0, yt1, wr - 14, wr + 72) - ycyl(yt0 - 1, yt1 + 1, ax, wr, p["axle_d"] / 2) - ycyl(yt0 - 1, yt1 + 1, ax, wr + 60, 3.25)
    ta += ycyl(yt0 - 10, yt0 - 5, ax, wr + 60, 5.0) + ycyl(yt0 - 5, yt1, ax, wr + 60, 3.0) + ycyl(yt1, yt1 + 7, ax, wr + 60, 5.0)
    add("torque_arm", "Torque arm and M6 bolt", ta, 7, "bought")

    # ---------------- 9 disc brakes: rotors on the hubs, calipers on adapters on the inner dropout tabs
    rr = p["rotor_d"] / 2
    br = []
    for s in (-1, 1):
        y = s * (D["d_in"] + 15)
        br.append(ycyl(y - 1, y + 1, ax, wr, rr) - ycyl(y - 2, y + 2, ax, wr, 22.0))
        yc0, yc1 = sorted((s * D["d_in"], s * (D["d_in"] + 30)))
        cal = box(ax + 80, ax + 120, yc0, yc1, wr - 25, wr + 25)
        ys0, ys1 = sorted((s * (D["d_in"] + 12), s * (D["d_in"] + 18)))
        cal -= box(ax + 79, ax + 93, ys0, ys1, wr - 26, wr + 26)
        br.append(cal)
    add("brakes", "Disc brakes (rotors and calipers)", fuse(br), 9, "bought")
    # brake cables: lever to a splitter under the left rail, then one cable to each caliper
    zL = 236.2
    spl = box(1500, 1540, -hw + 6, -hw + 24, fz0 - 16, fz0)
    add("splitter", "Brake cable splitter", spl, 9, "bought")
    cab = polyline_tube([(px + 10, 0, zL), (px + 100, 0, zL + 20), (1480, -hw + 15, fz0 - 9), (1500, -hw + 15, fz0 - 9)], 2.5)
    for s in (-1, 1):
        pts_c = [(1540, -hw + 15, fz0 - 9)]
        if s > 0:
            pts_c += [(1550, 0, fz0 - 9), (1555, hw - 15, fz0 - 9)]
        pts_c += [(ax - 90, s * (hw - 15), fz0 - 9), (ax + 140, s * (D["d_in"] - 18), 330.0),
                  (ax + 140, s * (D["d_in"] + 15), 300.0), (ax + 100, s * (D["d_in"] + 15), wr + 27.5)]
        cab += polyline_tube(pts_c, 2.5)
    add("brake_cables", "Brake cables (3)", cab, 9, "bought")

    # ---------------- 2 deck, removable side boards, corner angles, board brackets, deck bolts
    dz, bt, bhh = p["deck_z"], p["board_t"], p["board_h"]
    deck = box(x0, x1, -hw, hw, fz1, dz)
    holes = [(x0 + d, sy * (hw - 15)) for d in (200.0, 600.0, 1000.0) for sy in (-1, 1)]
    holes += [(x0 + 15, sy * 150.0) for sy in (-1, 1)] + [(x1 - 15, sy * 150.0) for sy in (-1, 1)]
    holes += [(x, sy * 200.0) for x in p["cross_x"] for sy in (-1, 1)]
    for hx, hy in holes:                              # 16 countersunk holes over the rivet nuts
        deck -= zcyl(fz1 - 1, dz + 1, hx, hy, 3.25)
    add("deck", "Plywood deck", deck, 2, "made")
    boards = {"board_l": box(x0, x1, -hw, -hw + bt, dz, dz + bhh), "board_r": box(x0, x1, hw - bt, hw, dz, dz + bhh),
              "board_f": box(x0, x0 + bt, -hw + bt, hw - bt, dz, dz + bhh), "board_b": box(x1 - bt, x1, -hw + bt, hw - bt, dz, dz + bhh)}
    for sy, k in ((-1, "board_l"), (1, "board_r")):
        for x in (x0 + 200, (x0 + x1) / 2, x1 - 200):
            boards[k] -= ycyl(-hw - 1, hw + 1, x, dz + 15, 3.25)
        for x in (x0 + 15, x1 - 15):
            for z in (dz + 50, dz + 100):
                boards[k] -= ycyl(-hw - 1, hw + 1, x, z, 3.25)
    for k in ("board_f", "board_b"):
        for y in (-150.0, 150.0):
            boards[k] -= xcyl(x0 - 1, x1 + 1, y, dz + 15, 3.25)
        for y in (-(hw - 20), hw - 20):
            for z in (dz + 50, dz + 100):
                boards[k] -= xcyl(x0 - 1, x1 + 1, y, z, 3.25)
    for k, sh in boards.items():
        add(k, {"board_l": "Left side board", "board_r": "Right side board", "board_f": "Front board", "board_b": "Rear board"}[k], sh, 2, "made")
    corners, brk = [], []
    for sx, xe in ((-1, x0), (1, x1)):
        for sy in (-1, 1):
            xa_, xb_ = sorted((xe, xe - sx * 3))
            ya_, yb_ = sorted((sy * hw, sy * (hw - 30)))
            xl0, xl1 = sorted((xe, xe + sx * 3))
            ya2, yb2 = sorted((sy * (hw - 30), sy * (hw + 3)))
            leg1 = box(xl0, xl1, ya2, yb2, dz, dz + bhh)
            xa2, xb2 = sorted((xe, xe - sx * 30))
            ya3, yb3 = sorted((sy * hw, sy * (hw + 3)))
            leg2 = box(xa2, xb2, ya3, yb3, dz, dz + bhh)
            corners.append(leg1 + leg2)
    add("corners", "Corner angles (4)", fuse(corners), 2, "made")
    bxs = (x0 + 200, (x0 + x1) / 2, x1 - 200)
    for sy in (-1, 1):
        for x in bxs:
            yb0, yb1 = sorted((sy * (hw - bt), sy * (hw - bt - 3)))
            yf0, yf1 = sorted((sy * (hw - bt), sy * (hw - bt - 30)))
            brk.append(box(x - 20, x + 20, yb0, yb1, dz, dz + 30) + box(x - 20, x + 20, yf0, yf1, dz, dz + 3))
    for sx, xe in ((1, x0 + bt), (-1, x1 - bt)):
        for y in (-150.0, 150.0):
            xb0, xb1 = sorted((xe, xe + sx * 3))
            xf0, xf1 = sorted((xe, xe + sx * 30))
            brk.append(box(xb0, xb1, y - 20, y + 20, dz, dz + 30) + box(xf0, xf1, y - 20, y + 20, dz, dz + 3))
    add("brackets", "Board brackets (10)", fuse(brk), 2, "made")

    # ---------------- 10 enclosure: closed folded box, front door, four bolts up into the crossmembers
    ex0, el, ew, eh = p["enc"]
    ez0, ez1 = D["enc_z"]
    wt = p["enc_wall"]
    shell = box(ex0, ex0 + el, -ew / 2, ew / 2, ez0, ez1) - box(ex0 + wt, ex0 + el - wt, -ew / 2 + wt, ew / 2 - wt, ez0 + wt, ez1 - wt)
    shell -= box(ex0 - 1, ex0 + wt + 1, -140, 140, ez0 + wt, ez0 + 164)
    for x in p["cross_x"][:2]:
        for y in (-100.0, 100.0):
            shell -= zcyl(ez1 - wt - 1, ez1 + 1, x, y, 3.0)
    add("enclosure", "Enclosure body", shell, 10, "made")
    door = box(ex0 - 0.8, ex0, -146, 146, ez0 + 2, ez0 + 168) + box(ex0 - 12, ex0 - 0.8, -146, -145.2, ez0 + 2, ez0 + 168) \
        + box(ex0 - 12, ex0 - 0.8, 145.2, 146, ez0 + 2, ez0 + 168)
    add("door", "Enclosure door", door, 10, "made")
    eb = []
    for x in p["cross_x"][:2]:
        for y in (-100.0, 100.0):
            eb.append(zcyl(ez1 - wt - 5, ez1 - wt, x, y, 6.5) + zcyl(ez1 - wt, ez1 + 6, x, y, 3.0))
    add("enc_bolts", "Enclosure bolts (4)", fuse(eb), 18, "fixing")
    pl_, pw, ph = p["pack"]
    fz = ez0 + wt
    add("pack", "Battery pack", box(ex0 + 6, ex0 + 6 + pl_, -136, -136 + pw, fz, fz + ph), 11, "bought")
    add("controller", "Motor controller", box(ex0 + 30, ex0 + 150, 50, 120, fz, fz + 45), 12, "bought")
    add("board", "Control board", box(ex0 + 180, ex0 + 270, 55, 125, fz, fz + 30), 13, "bought")

    # ---------------- 14 harness: motor cable up the arch, cell cable from the end cap, light cables
    zs = fz0 - 9
    hrn = polyline_tube([(ex0 + 200, -ew / 2, ez0 + 120), (ex0 + 200, -hw + 30, zs), (ax - p["arch_half"] + 22, -hw + 30, zs),
                         (ax - p["arch_half"] + 22, -D["arch_y"] - 20, zs + 5), (ax - p["arch_half"] + 100, -D["arch_y"] - 20, D["arch_top"] - 2),
                         (ax, -D["arch_y"] - 20, D["arch_top"] - 2), (ax, -D["arch_y"] - 20, wr + 30), (ax, -D["d_out"] - pt - 12, wr + 14)], 4.0)
    hrn += polyline_tube([(hx1 + p["ring_t"] + p["cap_t"], 18, zc + 15), (hx1 + 16, 30, zc + 6), (hx1 + 50, 30, zc - 6), (1500, 60, 330), (ex0 - 30, ew / 2 + 20, 320),
                          (ex0 + 40, ew / 2 + 20, 320), (ex0 + 40, ew / 2, 320)], 3.0)
    for s in (-1, 1):
        hrn += polyline_tube([(ex0 + el, s * 60, ez0 + 120), (ex0 + el + 40, s * 60, zs), (x1 - 60, s * 270, zs),
                              (x1 + 10, s * 270, fz0 - 3)], 3.0)
    add("harness", "Wiring harness", hrn, 14, "bought")

    # ---------------- 15 lights, reflectors, flag pole in two clips
    lt = [box(x1, x1 + 20, min(s * 220, s * 320), max(s * 220, s * 320), fz0, fz1) for s in (-1, 1)]
    lt += [box(x0 + 400, x0 + 480, -hw - 4, -hw, fz0, fz1), box(x0 + 400, x0 + 480, hw, hw + 4, fz0, fz1)]
    add("lights", "Rear lights and side reflectors", fuse(lt), 15, "bought")
    fy = -hw + bt + 8
    flag = zcyl(dz, D["flag_top"], x0 + 30, fy, 6.0) + box(x0 + 30, x0 + 250, fy - 3, fy + 3, D["flag_top"] - 150, D["flag_top"])
    add("flag", "Flag and pole", flag, 15, "bought")
    clips = fuse([zcyl(z, z + 15, x0 + 30, fy, 8.0) - zcyl(z - 1, z + 16, x0 + 30, fy, 6.0) for z in (dz + 40, dz + 120)])
    add("pole_clips", "Pole clips (2)", clips, 15, "bought")

    # ---------------- 16 parking stand: leg pivoted in the clevis under the housing
    sx = p["stand_x"]
    leg = zcyl(6, 322, sx, 0, 12.5) - zcyl(5, 323, sx, 0, 10.5) - ycyl(-13, 13, sx, 310, 5.0)
    leg += box(sx - 40, sx + 40, -30, 30, 0, 6)
    add("stand", "Parking stand leg and foot", leg, 16, "made")
    add("stand_bolt", "Stand pivot bolt", ycyl(-22, 22, sx, 310, 5.0), 16, "fixing")
    return C


GROUPS = {
    # concept-media groups (BOM items 1 to 16), as in the TRL 3 model
    "frame": ("rails", "nose_bars", "dropouts", "arches"),
    "deck": ("deck", "board_l", "board_r", "board_f", "board_b", "corners", "brackets"),
    "drawbar": ("drawbar", "opin"),
    "hitch": ("hitch", "hitch_pin"),
    "load_cell": ("cell", "rod_end", "clevis_pin"),
    "coupler": ("housing", "bushings", "cage", "end_cap", "pull_rod", "spring", "lever", "lever_bolt"),
    "motor_wheel": ("motor_wheel", "torque_arm"),
    "idler_wheel": ("idler_wheel",),
    "brakes": ("brakes", "splitter", "brake_cables"),
    "enclosure": ("enclosure", "door", "enc_bolts"),
    "pack": ("pack",),
    "controller": ("controller",),
    "board": ("board",),
    "harness": ("harness",),
    "lights": ("lights", "flag", "pole_clips"),
    "stand": ("stand", "stand_bolt"),
}


def build_parts(p=PARAMS, C=None):
    """Return {name: solid} for the main trailer parts (BOM items 1 to 16)."""
    C = C or build_components(p)
    return {g: fuse([C[k].shape for k in ks]) for g, ks in GROUPS.items()}


def assembly(p=PARAMS):
    b = _b3d()
    return b.Compound(children=list(build_parts(p).values()))


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def _gap(a, b_):
    return a.distance_to(b_)


def checks(p=PARAMS, C=None):
    """Pairs that must touch or keep a clearance. Returns (description, overlap mm3, gap mm, expectation, ok)."""
    b = _b3d()
    C = C or build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    D = derived(p)
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = _gap(a, b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    frame = S("rails") + S("nose_bars") + S("dropouts") + S("arches")
    wheels = S("motor_wheel") + S("idler_wheel")
    # frame weldment
    chk("Nose bars on the front end rail", S("nose_bars"), S("rails"), "touch")
    chk("Nose bars on the coupler housing", S("nose_bars"), S("housing"), "touch")
    chk("Coupler housing clear of the front end rail", S("housing"), S("rails"), 10.0)
    chk("Dropout plates on the rails and arch frames", S("dropouts"), S("rails") + S("arches"), "touch")
    # deck and boards
    chk("Deck on the frame", S("deck"), S("rails"), "touch")
    for k in ("board_l", "board_r", "board_f", "board_b"):
        chk(f"{C[k].name} on the deck", S(k), S("deck"), "touch")
    chk("Corner angles on the boards", S("corners"), S("board_l") + S("board_r") + S("board_f") + S("board_b"), "touch")
    chk("Board brackets on the deck", S("brackets"), S("deck"), "touch")
    chk("Board brackets on the boards", S("brackets"), S("board_l") + S("board_r") + S("board_f") + S("board_b"), "touch")
    chk("Flag pole on the deck", S("flag"), S("deck"), "touch")
    chk("Pole clips on the left board", S("pole_clips"), S("board_l"), "touch")
    chk("Pole clips round the pole", S("pole_clips"), S("flag"), "touch")
    chk("Rear lights on the rear rail", S("lights"), S("rails"), "touch")
    # drawbar, coupler and cell
    chk("Drawbar in the front and rear bushings", S("drawbar"), S("bushings"), "touch")
    chk("Bushings in the housing", S("bushings"), S("housing"), "touch")
    chk("Drawbar clear of the housing bore and fork", S("drawbar"), S("housing"), 0.3)
    chk("Overload pin through the drawbar", S("opin"), S("drawbar"), "touch")
    chk("Overload pin clear between the fork tines", S("opin"), S("housing") - box(p["pin_x"] - 30, p["pin_x"] - p["pin_d"] / 2, -20, 20, 384, 410), 0.3)
    chk("Overload stop: pin 0.5 mm behind the slot's closed front end", S("opin"),
        S("housing") & box(p["pin_x"] - 30, p["pin_x"] - p["pin_d"] / 2, -20, 20, 384, 410), 0.45)
    chk("Rod end on the drawbar end plug", S("rod_end"), S("drawbar"), "touch")
    chk("Rod end eye clear between the clevis plates", S("rod_end"), S("cell"), 0.3)
    chk("Clevis pin through the clevis plates", S("clevis_pin"), S("cell"), "touch")
    chk("Clevis pin through the rod end eye", S("clevis_pin"), S("rod_end"), "touch")
    chk("Clevis pin head inside the side window at rest", S("clevis_pin"), S("housing"), 2.0)
    chk("Clevis pin head inside the side window at full stroke", b.Pos(p["coupler_stroke"], 0, 0) * S("clevis_pin"), S("housing"), 2.0)
    chk("Load cell and clevis clear of the housing bore", S("cell") + S("rod_end"), S("housing") + S("cage"), 1.0)
    chk("Pull rod on the load cell", S("pull_rod"), S("cell"), "touch")
    chk("Pull rod head on the cage bulkhead", S("pull_rod"), S("cage"), "touch")
    chk("Pull rod clear of the housing and end cap", S("pull_rod"), S("housing") + S("end_cap"), 1.0)
    chk("Spring between the rod head and the end cap", S("spring"), S("pull_rod") + S("end_cap"), "touch")
    chk("Spring clear of the cage bore", S("spring"), S("cage"), 0.5)
    chk("Spring cage sliding fit in the housing bore", S("cage"), S("housing"), "touch")
    chk("End cap on the cage ring", S("end_cap"), S("cage"), "touch")
    chk("Rod tail 2 mm short of the lever at rest", S("pull_rod"), S("lever"), 1.5)
    chk("Lever clear of the cheeks", S("lever"), S("housing"), 1.0)
    chk("Lever clear of the end cap and flange", S("lever"), S("end_cap"), 2.0)
    chk("Lever pivot bolt through the cheeks", S("lever_bolt"), S("housing"), "touch")
    chk("Lever on its pivot bolt", S("lever"), S("lever_bolt"), "touch")
    chk("Anti-rotation pin between the fork tines", S("drawbar"), S("housing") - b.Pos(0, 0, 0) * box(860, 1300, -40, 40, 300, 384), 0.1)
    chk("Hitch arm in the drawbar bore", S("hitch"), S("drawbar"), 0.4)
    chk("Drawbar clear of the frame", S("drawbar"), frame, 20.0)
    chk("Stand leg in its clevis", S("stand"), S("housing"), "touch")
    chk("Stand pivot bolt through the clevis and leg", S("stand_bolt"), S("stand") + S("housing"), "touch")
    # the coupler at full stroke: drawbar, cell and pull rod moved 50 mm rearward
    st = b.Pos(p["coupler_stroke"], 0, 0)
    moved = st * (S("drawbar") + S("opin") + S("cell") + S("rod_end") + S("pull_rod"))
    chk("Full stroke: overload pin short of the housing front", st * S("opin"),
        S("housing") - box(870, 1400, -40, 40, 290, 383) - box(780, 930, -12, 12, 384.5, 410), 3.0)
    chk("Full stroke: cell clear of the bulkhead", st * S("cell"), S("cage"), 5.0)
    chk("Full stroke: rod tail under the front rail", st * S("pull_rod"), S("rails"), 10.0)
    chk("Full stroke: moving parts clear of the enclosure", moved, S("enclosure") + S("door"), 10.0)
    chk("Brake cables clear of the enclosure and door", S("brake_cables"), S("enclosure") + S("door"), 5.0)
    # wheels, dropouts, brakes
    chk("Hubs between the dropout plates", wheels, S("dropouts"), "touch")
    chk("Tyres clear of the side rails and deck", wheels, S("rails") + S("deck") + S("board_l") + S("board_r"), 20.0)
    tyres = fuse([b.Pos(p["axle_x"], sy * D["yc"], p["wheel_r"]) * b.Rot(90, 0, 0) * b.Torus(p["wheel_r"] - p["tyre_w"] / 2, p["tyre_w"] / 2) for sy in (-1, 1)])
    chk("Tyres clear of the arch frames", tyres, S("arches"), 15.0)
    chk("Calipers on the inner dropout tabs", S("brakes"), S("dropouts"), "touch")
    chk("Rotors on the hubs", S("brakes"), wheels, "touch")
    chk("Calipers clear of the motor shell", S("brakes") - ycyl(-370, -360, p["axle_x"], p["wheel_r"], 91), S("motor_wheel"), 1.5)
    chk("Torque arm on the inner dropout", S("torque_arm"), S("dropouts"), "touch")
    # enclosure
    chk("Enclosure on the crossmembers", S("enclosure"), S("rails"), "touch")
    chk("Enclosure bolts up into the crossmembers", S("enc_bolts"), S("rails"), "touch")
    chk("Door on the enclosure", S("door"), S("enclosure"), "touch")
    for k in ("pack", "controller", "board"):
        chk(f"{C[k].name} on the enclosure floor", S(k), S("enclosure"), "touch")
    chk("Pack clear of the controller", S("pack"), S("controller") + S("board"), 5.0)
    chk("Pack clear of the enclosure bolts", S("pack"), S("enc_bolts"), 3.0)
    chk("Enclosure clear of the wheels and brakes", S("enclosure"), wheels + S("brakes"), 20.0)
    # cables
    chk("Brake cables clear of the tyres and spokes", S("brake_cables"), wheels, 5.0)
    chk("Brake cables clear of the rotors", S("brake_cables") - box(1950, 2100, -400, 400, 250, 320), S("brakes"), 5.0)
    chk("Harness clear of the wheels", S("harness"), S("motor_wheel") - ycyl(-470, -440, p["axle_x"], p["wheel_r"], 20) + S("idler_wheel"), 5.0)
    chk("Harness clear of the rotors and calipers", S("harness"), S("brakes"), 5.0)
    chk("Harness clear of the drawbar and lever", S("harness"), S("drawbar") + S("opin") + S("lever"), 5.0)
    bb = fuse([c.shape for c in C.values()]).bounding_box()
    rows.append(("Overall width 1,000 mm or less (R9)", 0.0, 1000.0 - bb.size.Y, 0.0, bb.size.Y <= 1000.0))
    return rows


def print_checks(p=PARAMS, C=None):
    rows = checks(p, C)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    parts = build_parts(C=C)
    groups = {
        "cargomule-assembly": list(parts.values()),
        "frame": [parts["frame"], C["housing"].shape],
        "drawbar-assembly": [parts[k] for k in ("hitch", "drawbar", "load_cell", "coupler")],
        "deck": [parts["deck"]],
        "enclosure": [parts["enclosure"]],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
    bb = Compound(children=list(parts.values())).bounding_box()
    D = derived()
    print(f"assembly bounding box: X {bb.min.X:.0f} to {bb.max.X:.0f}, Y {bb.min.Y:.0f} to {bb.max.Y:.0f}, "
          f"Z {bb.min.Z:.0f} to {bb.max.Z:.0f} mm")
    print(f"overall width {bb.size.Y:.0f} mm (derived {D['width']:.0f}); length from bike axle "
          f"{bb.max.X:.0f} mm (derived {D['length']:.0f})")
    print(f"lever ratio {D['lever_ratio']:.2f}; coupler housing {P['housing'][2]:.0f} to {P['housing'][3]:.0f} mm; "
          f"load cell {P['cell_x'][0]:.1f} to {P['cell_x'][1]:.1f} mm")
    print("exported:", ", ".join(groups))
    print_checks(C=C)
