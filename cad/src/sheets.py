"""CargoMule general arrangement sheet CGM-DWG-001, Rev P5 (TRL 3, constructable design).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/CGM-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from the model and PARAMS,
so they follow any parameter change. The concept sheet in media/ is CGM-DWG-010.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-09-25"
DATE_P4 = "2026-10-01"
DATE_P5 = "2026-10-02"


_NUM = r"[-+]?\d*\.?\d+(?:e[-+]?\d+)?"
_ARC = re.compile(rf"A ?({_NUM}),({_NUM}) {_NUM} [01],[01] ({_NUM},{_NUM})")


def _fix_flat_arcs(svg):
    """Replace elliptical arcs that have collapsed to a line (one radius near zero) with a straight
    line: the SVG renderer would otherwise draw them as a long stray stroke across the sheet."""
    def sub(m):
        rx, ry = abs(float(m.group(1))), abs(float(m.group(2)))
        if min(rx, ry) < 1e-3 or max(rx, ry) > 1e4 * max(min(rx, ry), 1e-12):
            return "L " + m.group(3)
        return m.group(0)
    return _ARC.sub(sub, svg)


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection (a zero-length ellipse arc) is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    eb = e.bounding_box()
                    if max(eb.size.X, eb.size.Y, eb.size.Z) > 1.2 * max(bb.size.X, bb.size.Y, bb.size.Z):
                        skipped += 1          # a degenerate edge projected to a long stray line
                        continue
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        p.write_text(_fix_flat_arcs(p.read_text()))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text):
    a = 1.4
    cx, cy = x - 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly()
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="CargoMule", title="General arrangement", dwg_no="CGM-DWG-001", rev="P5",
              author="Amish Chadha", date=DATE_P5, scale=None, theme="technical",
              material="S235 box frame, S355 drawbar; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "180 mm rotors, metallic pads (CGM-DDR-002)", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC"),
                         ("P4", "Design for construction (CGM-DDR-003)", DATE_P4, "AC"),
                         ("P5", "Key switch, charge socket, drawbar reflector", DATE_P5, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    ax, x0, x1 = P["axle_x"], P["deck_x0"], D["deck_x1"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zg = Z(0)
    L += [ext(X(0), Z(P['hitch'][2]) - 2, X(0), Z(1000) - 2), ext(X(ax), Z(P['wheel_r']), X(ax), Z(1000) - 2)]
    L += dim_h(X(0), X(ax), Z(1000), f"{ax:,.0f} axle to axle")
    L += [ext(X(x0), Z(P['deck_z']) - 1, X(x0), Z(bb.max.Z) - 3), ext(X(x1), Z(P['deck_z']) - 1, X(x1), Z(bb.max.Z) - 3)]
    L += dim_h(X(x0), X(x1), Z(bb.max.Z) - 2, f"{P['deck_len']:,.0f} deck")
    L += [ext(X(x1) + 1, Z(P['deck_z']), X(bb.max.X) + 9, Z(P['deck_z']))]
    L += dim_v(X(bb.max.X) + 7, Z(P["deck_z"]), zg, f"{P['deck_z']:.0f} deck")
    L += [ext(X(0) - 1, Z(P['hitch'][2]), x - 9, Z(P['hitch'][2]))]
    L += dim_v(x - 10, Z(P["hitch"][2]), zg, f"{P['hitch'][2]:.0f} hitch")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    xt1, xt2 = Xt(bb.max.X) + 8, Xt(bb.max.X) + 17
    L += [ext(Xt(ax), Yt(D['yc']), xt1 + 1, Yt(D['yc'])), ext(Xt(ax), Yt(-D['yc']), xt1 + 1, Yt(-D['yc']))]
    L += dim_v(xt1, Yt(D["yc"]), Yt(-D["yc"]), f"{P['track']:.0f} track")
    L.append(_t(Xt(bb.min.X) + 2, Yt(-360) + 10, "offset drawbar run, 360 off center line", 2.0, 400, MUTED, "start"))

    # right view (from +X, looking forward): Y to the right
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    L += [ext(Yr(-D['d_out']), Zr(P['wheel_r']), Yr(-D['d_out']), Zr(0) + 12),
          ext(Yr(-D['d_in']), Zr(P['wheel_r']), Yr(-D['d_in']), Zr(0) + 12)]
    L += dim_h(Yr(-D["d_out"]), Yr(-D["d_in"]), Zr(0) + 10, f"{P['hub_old']:.0f} hub")
    L += dim_v(x + w + 9, Zr(D["arch_top"]), Zr(0), f"{D['arch_top']:.0f} arch")

    s._layers += L
    s.add_svg(views["iso"], 276, 42, 140, 86, label="Isometric view", sublabel="Not to scale")
    cx0, cx1 = P["cell_x"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Wheels 20 in (ETRTO 406), 100 mm hubs; dropout faces {D['d_in']:.0f} and {D['d_out']:.0f} off center",
        f"Disc brakes both wheels, {P['rotor_d']:.0f} rotors, metallic pads",
        f"Deck {P['deck_len']:.0f} x {P['deck_w']:.0f} x {P['deck_t']:.0f} plywood at Z {P['deck_z']:.0f}; axle {D['axle_behind_center']:.0f} behind deck center",
        f"Frame {P['rail']:.0f} x {P['rail']:.0f} x {P['rail_t']} box; drawbar {P['drawbar'][0]:.0f} x {P['drawbar'][1]} tube",
        f"Hitch point X 0, Y {P['hitch'][1]:.0f}, Z {P['hitch'][2]:.0f} (bike left axle end)",
        f"Coupler housing X {P['housing'][2]:.0f} to {P['coupler_x'][1]:.0f}; load cell inside, X {cx0:.0f} to {cx1:.0f}",
        f"Coupler stroke {P['coupler_stroke']:.0f}; brake lever {D['lever_ratio']:.1f} to 1",
        f"Enclosure {P['enc'][1]:.0f} x {P['enc'][2]:.0f} x {P['enc'][3]:.0f}, X {P['enc'][0]:.0f}, door at front",
        f"Key switch (19 hole) and charge socket (24 hole) in enclosure right wall, X {P['enc'][0] + P['key_hole'][0]:.0f} and {P['enc'][0] + P['port_hole'][0]:.0f}",
        f"Ground clearance {D['ground_clear']:.0f} under enclosure; tyre to rail {D['tyre_gap']:.1f}",
        "Empty about 46 kg; hitch load about 7.5 kg (CGM-CAL-001)",
        "Third-angle; front view from -Y; X rearward from bike axle",
    ], x=276, y=144, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "CGM-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
