"""CargoMule parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    cargomule-assembly.step / .stl   whole trailer, hitched position
    frame.step / .stl                welded chassis with dropouts and wheel arch frames
    drawbar-assembly.step / .stl     hitch, offset drawbar, load cell and overrun coupler
    deck.step / .stl                 plywood deck and removable side boards
    enclosure.step / .stl            battery and electronics enclosure

Axes: X points rearward from the towing bicycle's rear axle (x = 0) toward the trailer,
Y is across the trailer (the hitch is on the bike's left, -Y), Z is up with the ground at
z = 0. Main dimensions and interfaces only: wheel size, track and hub spacing, dropouts,
deck, drawbar line, hitch point, load cell and coupler axis, enclosure envelope. Not
fabrication detail; not for fabrication. The same PARAMS feed docs/04-calcs/sizing.py
(CGM-CAL-001) and the drawing CGM-DWG-001 (cad/src/sheets.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # wheels: 20 x 2.15 in (ETRTO 406), front-style hubs with 100 mm over-locknut spacing
    "wheel_r": 258.0, "tyre_w": 55.0, "hub_old": 100.0, "rotor_d": 180.0,
    # rotor_d: 180 mm rotors with metallic pads (CGM-DDR-002), was 160 mm
    "track": 800.0,                  # wheel center to wheel center
    "axle_x": 1920.0,                # 20 mm behind the deck center (tongue load, CGM-CAL-001 section A)
    # deck and chassis
    "deck_x0": 1300.0, "deck_len": 1200.0, "deck_w": 700.0,
    "deck_z": 420.0,                 # deck top above ground
    "deck_t": 12.0, "board_h": 150.0, "board_t": 9.0,
    "rail": 30.0, "rail_t": 1.5,     # 30 x 30 x 1.5 mm steel box section
    "cross_x": (1600.0, 1920.0, 2250.0),
    "nose_x": 1180.0, "nose_z": 360.0,
    "nose_tube": (28.0, 1.5),        # A-frame nose bars, OD and wall
    "arch_tube": (25.0, 1.5),        # wheel arch frame (carries the outer dropout)
    "arch_half": 300.0, "arch_gap": 30.0,
    "plate_t": 5.0,                  # dropout plates
    # hitch and offset drawbar
    "hitch": (0.0, -95.0, 340.0),    # on the bicycle's left rear axle end
    "knees": ((30.0, -360.0, 342.0), (550.0, -360.0, 348.0)),  # outward run that clears the bike's rear tyre
    "straight_x": 800.0,             # drawbar runs straight along X, on the center line, from here to the nose
    "drawbar": (38.0, 2.5),          # OD and wall, S355 tube
    "cell_x": (840.0, 950.0),        # S-type load cell with clevises, on the coupler axis
    "coupler_x": (950.0, 1150.0),    # overrun coupler body
    "coupler_stroke": 50.0,
    # enclosure (0.8 mm galvanized steel, under the deck front)
    "enc": (1340.0, 320.0, 300.0, 170.0),   # x0, length, width, height
    "pack": (250.0, 170.0, 150.0),
    # stand, lights and flag
    "stand_x": 1200.0, "flag_h": 1150.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
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
        "length": x1 + 22.0,                                  # rear lights stand 22 mm proud
        "tyre_gap": yc - p["tyre_w"] / 2 - hw,                # tyre to side rail
        "arch_top": 2 * p["wheel_r"] + p["arch_gap"],
        "enc_x": (enc[0], enc[0] + enc[1]), "enc_z": (fz0 - enc[3], fz0),
        "ground_clear": fz0 - enc[3],
        "flag_top": p["deck_z"] + p["flag_h"],
        "axle_behind_center": p["axle_x"] - (x0 + x1) / 2,
    }


def drawbar_points(p=PARAMS):
    """Center line of the drawbar from the hitch joint to the nose (plan offset at the knee)."""
    s = (p["straight_x"], 0.0, p["nose_z"] - 6.0)
    n = (p["nose_x"], 0.0, p["nose_z"])
    return [p["hitch"], *p["knees"], s, n]


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


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def wheel(cx, cy, cz, r, w, spokes=16):
    b = _b3d()
    tyre = b.Pos(cx, cy, cz) * b.Rot(90, 0, 0) * b.Torus(r - w / 2, w / 2)
    rim = b.Pos(cx, cy, cz) * b.Rot(90, 0, 0) * (b.Cylinder(r - w + 8, 20) - b.Cylinder(r - w - 6, 22))
    hub = b.Pos(cx, cy, cz) * b.Rot(90, 0, 0) * b.Cylinder(22, 90)
    sp = fuse(tube((cx, cy, cz), (cx + (r - w - 2) * math.cos(math.radians(k * 360 / spokes)), cy,
                                  cz + (r - w - 2) * math.sin(math.radians(k * 360 / spokes))), 1.8)
              for k in range(spokes))
    return tyre + rim + hub + sp


# ---------------------------------------------------------------- parts
def build_parts(p=PARAMS):
    """Return {name: solid} for the main trailer parts (BOM items 1 to 16)."""
    b = _b3d()
    D = derived(p)
    x0, x1, hw, R = p["deck_x0"], D["deck_x1"], D["hw"], p["rail"]
    fz0, fz1, ax, wr = D["fz0"], D["fz1"], p["axle_x"], p["wheel_r"]
    parts = {}

    # 1 chassis frame: perimeter, three crossmembers, A-frame nose, dropouts, wheel arch frames
    fr = [box(x0, x1, -hw, -hw + R, fz0, fz1), box(x0, x1, hw - R, hw, fz0, fz1),
          box(x0, x0 + R, -hw, hw, fz0, fz1), box(x1 - R, x1, -hw, hw, fz0, fz1)]
    fr += [box(x - R / 2, x + R / 2, -hw, hw, fz0, fz1) for x in p["cross_x"]]
    nr = p["nose_tube"][0] / 2
    nose = (p["nose_x"], 0.0, p["nose_z"])
    fr += [tube((x0 + 15, s * (hw - 15), fz0 + 15), nose, nr) for s in (-1, 1)]
    fr.append(b.Pos(*nose) * b.Sphere(nr + 4))
    ar = p["arch_tube"][0] / 2
    for s in (-1, 1):
        # inner dropout: plate under the side rail, face on the hub's inner locknut
        yi = s * (D["d_in"] - p["plate_t"] / 2)
        fr.append(box(ax - 45, ax + 45, yi - p["plate_t"] / 2, yi + p["plate_t"] / 2, wr - 40, fz0))
        # arch frame: outriggers from the rail, a hoop over the tyre and a strut down to the outer dropout
        ya = s * D["arch_y"]
        xa, xb = ax - p["arch_half"], ax + p["arch_half"]
        zt = D["arch_top"]
        zr = (fz0 + fz1) / 2
        fr += [tube((xa, s * hw, zr), (xa, ya, zr), ar), tube((xb, s * hw, zr), (xb, ya, zr), ar),
               tube((xa, ya, zr), (xa + 80, ya, zt), ar), tube((xa + 80, ya, zt), (xb - 80, ya, zt), ar),
               tube((xb - 80, ya, zt), (xb, ya, zr), ar), tube((ax, ya, zt), (ax, ya, wr + 20), ar)]
        yo = s * (D["d_out"] + p["plate_t"] / 2)
        fr.append(box(ax - 30, ax + 30, yo - p["plate_t"] / 2, yo + p["plate_t"] / 2, wr - 40, wr + 40))
        # tie-down eyes on the side rails
        fr += [b.Pos(x, s * (hw + 6), fz0 + 15) * b.Rot(0, 90, 0) * b.Torus(9, 3) for x in (x0 + 150, x1 - 150)]
    parts["frame"] = fuse(fr)

    # 2 deck and removable side boards
    bt, bh = p["board_t"], p["board_h"]
    parts["deck"] = fuse([box(x0, x1, -hw, hw, fz1, p["deck_z"]),
                          box(x0, x1, -hw, -hw + bt, p["deck_z"], p["deck_z"] + bh),
                          box(x0, x1, hw - bt, hw, p["deck_z"], p["deck_z"] + bh),
                          box(x1 - bt, x1, -hw + bt, hw - bt, p["deck_z"], p["deck_z"] + bh),
                          box(x0, x0 + bt, -hw + bt, hw - bt, p["deck_z"], p["deck_z"] + bh)])

    # 3 drawbar: hitch end, knee, straight coupler section on the center line (two sections)
    pts = drawbar_points(p)
    dr = p["drawbar"][0] / 2
    h, k, k2, s_, n = pts
    c0, c1 = p["cell_x"]
    k0, k1 = p["coupler_x"]
    zc = lambda x: s_[2] + (n[2] - s_[2]) * (x - s_[0]) / (n[0] - s_[0])
    hitch_end = (h[0] + 20, h[1] - 60, h[2] + 1)
    parts["drawbar"] = fuse([tube(hitch_end, k, dr), b.Pos(*k) * b.Sphere(dr), tube(k, k2, dr),
                             b.Pos(*k2) * b.Sphere(dr), tube(k2, s_, dr),
                             b.Pos(*s_) * b.Sphere(dr), tube(s_, (c0, 0, zc(c0)), dr),
                             tube((k1, 0, zc(k1)), n, dr)])

    # 4 universal axle hitch: plate under the axle end, three-axis joint, short arm to the drawbar
    parts["hitch"] = fuse([b.Pos(*h) * b.Rot(90, 0, 0) * b.Cylinder(32, 14),
                           b.Pos(h[0] + 8, h[1] - 30, h[2]) * b.Sphere(20),
                           tube((h[0] + 8, h[1] - 30, h[2]), hitch_end, 17)])

    # 5 S-type load cell between clevises, on the coupler axis
    parts["load_cell"] = fuse([tube((c0, 0, zc(c0)), (c1, 0, zc(c1)), 12),
                               box(c0 + 30, c1 - 30, -25, 25, zc(c0) - 30, zc(c0) + 30)])

    # 6 overrun coupler: sliding sleeve on bushings, spring and damper housing, cable lever
    parts["coupler"] = fuse([tube((k0, 0, zc(k0)), (k1, 0, zc(k1)), 27),
                             box(k0 + 60, k0 + 170, -15, 15, zc(k0) + 25, zc(k0) + 55),
                             box(k1 - 50, k1 - 20, -40, 40, zc(k1) - 45, zc(k1) - 20)])

    # 7 hub motor wheel (left, -Y) and 8 idler wheel (right, +Y)
    yL, yR = -D["yc"], D["yc"]
    parts["motor_wheel"] = wheel(ax, yL, wr, wr, p["tyre_w"]) + b.Pos(ax, yL, wr) * b.Rot(90, 0, 0) * b.Cylinder(78, 60)
    parts["idler_wheel"] = wheel(ax, yR, wr, wr, p["tyre_w"])

    # 9 disc brakes, rotors inboard beside the inner dropouts, calipers behind the axle
    rr = p["rotor_d"] / 2
    br = []
    for s in (-1, 1):
        y = s * (D["d_in"] + 15)
        br.append(b.Pos(ax, y, wr) * b.Rot(90, 0, 0) * (b.Cylinder(rr, 2) - b.Cylinder(30, 3)))
        br.append(box(ax + rr - 25, ax + rr + 20, y - 14, y + 14, wr - 25, wr + 25))
    parts["brakes"] = fuse(br)

    # 10 enclosure (open-top shell for the section views), 11 pack, 12 controller, 13 control board
    ex0, el, ew, eh = p["enc"]
    ez0, ez1 = D["enc_z"]
    parts["enclosure"] = (box(ex0, ex0 + el, -ew / 2, ew / 2, ez0, ez1)
                          - box(ex0 + 3, ex0 + el - 3, -ew / 2 + 3, ew / 2 - 3, ez0 + 3, ez1 + 1))
    pl, pw, ph = p["pack"]
    parts["pack"] = box(ex0 + 12, ex0 + 12 + pl, -ew / 2 + 12, -ew / 2 + 12 + pw, ez0 + 4, ez0 + 4 + ph)
    parts["controller"] = box(ex0 + 12, ex0 + 132, 45, 115, ez0 + 4, ez0 + 49)
    parts["board"] = box(ex0 + 150, ex0 + 240, 60, 120, ez0 + 4, ez0 + 34)

    # 14 harness: enclosure to motor, to load cell, to lights
    parts["harness"] = fuse([tube((ex0 + el - 5, -100, ez0 + 30), (ax - 120, -hw + 40, ez0 + 30), 5),
                             tube((ax - 120, -hw + 40, ez0 + 30), (ax, yL + 45, wr), 5),
                             tube((ex0 + 5, 0, ez0 + 60), (p["nose_x"] - 20, 0, p["nose_z"] - 25), 5),
                             tube((p["nose_x"] - 20, 0, p["nose_z"] - 25), ((c0 + c1) / 2, 0, zc(c0) - 30), 5),
                             tube((ex0 + el - 5, 100, ez0 + 30), (x1 - 40, 100, fz0 - 8), 5)])

    # 15 lights, reflectors and flag (pole at the front left corner)
    parts["lights"] = fuse([box(x1 + 2, x1 + 22, -hw + 30, -hw + 130, fz0, fz1),
                            box(x1 + 2, x1 + 22, hw - 130, hw - 30, fz0, fz1),
                            box(x0 + 400, x0 + 480, -hw - 4, -hw, fz0, fz1),
                            box(x0 + 400, x0 + 480, hw, hw + 4, fz0, fz1),
                            tube((x0 + 30, -hw + 20, p["deck_z"]), (x0 + 30, -hw + 20, D["flag_top"]), 6),
                            box(x0 + 30, x0 + 250, -hw + 17, -hw + 23, D["flag_top"] - 150, D["flag_top"])])

    # 16 parking stand under the nose
    sx = p["stand_x"]
    parts["stand"] = tube((sx, 0, p["nose_z"] - 15), (sx, 0, 25), 11) + box(sx - 50, sx + 50, -35, 35, 0, 25)
    return parts


def assembly(p=PARAMS):
    b = _b3d()
    return b.Compound(children=list(build_parts(p).values()))


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    groups = {
        "cargomule-assembly": list(parts.values()),
        "frame": [parts["frame"]],
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
    print("exported:", ", ".join(groups))
