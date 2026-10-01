"""CargoMule prototype build plan pictures (CGM-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
(one sheet, joint or step by number: python cad/src/build_plan_media.py sheet 101 | joint 3 | step 7)
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CGM-DWG-101 to 111        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import drawing  # noqa: E402
from sheets import safe_project_views  # noqa: E402
from model import PARAMS as P, build_components, derived, box, fuse  # noqa: E402

# The hidden-line projection of some of these parts yields degenerate edges that the SVG
# exporter rejects; use the edge-by-edge projection from sheets.py (the kit is unchanged).
drawing.project_views = safe_project_views

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
_C = None


def C():
    global _C
    if _C is None:
        _C = build_components(P)
    return _C


def S(*ks):
    return fuse([C()[k].shape for k in ks])


COL = {"housing": "#0F766E", "frame": "#475569", "bush": "#F59E0B", "drawbar": "#334155", "cell": "#2563EB",
       "rod": "#7C3AED", "cage": "#0E7490", "lever": "#B45309", "stand": "#A16207", "motor": "#1F2937",
       "idler": "#4B5563", "brakes": "#DC2626", "cables": "#111827", "enc": "#94A3B8", "door": "#64748B",
       "ctrl": "#115E59", "harness": "#111827", "deck": "#B7925A", "boards": "#D6B98C", "fit": "#9CA3AF",
       "lights": "#F59E0B", "pack": "#C2410C", "hitch": "#D4A017", "pin": "#111827", "dropout": "#64748B"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def ground(x0=700, x1=2650, w=700):
    return part("Floor", box(x0, x1, -w, w, -3, 0), "#E5E7EB")


# ----------------------------------------------------------------- named components, in build order
def made():
    return {
        "housing": part("Coupler housing", S("housing"), COL["housing"]),
        "frame": part("Chassis frame", S("rails", "nose_bars", "dropouts", "arches"), COL["frame"]),
        "bushings": part("Bushings (2)", S("bushings"), COL["bush"]),
        "drawbar": part("Drawbar, rod end and overload pin", S("drawbar", "rod_end", "opin"), COL["drawbar"]),
        "cartridge": part("Load cell, pull rod, spring and spring cage", S("cell", "pull_rod", "spring", "cage"), COL["cell"]),
        "end_cap": part("End cap", S("end_cap"), COL["cage"]),
        "lever": part("Brake lever", S("lever", "lever_bolt"), COL["lever"]),
        "stand": part("Parking stand", S("stand", "stand_bolt"), COL["stand"]),
        "motor": part("Hub motor wheel and torque arm", S("motor_wheel", "torque_arm"), COL["motor"]),
        "idler": part("Idler wheel", S("idler_wheel"), COL["idler"]),
        "brakes": part("Disc brakes (rotors, calipers)", S("brakes"), COL["brakes"]),
        "cables": part("Brake cables and splitter", S("brake_cables", "splitter"), COL["cables"]),
        "enclosure": part("Enclosure and door", S("enclosure", "door", "enc_bolts"), COL["enc"]),
        "ctrl": part("Controller and control board", S("controller", "board"), COL["ctrl"]),
        "harness": part("Wiring harness", S("harness"), COL["harness"]),
        "deck": part("Plywood deck", S("deck"), COL["deck"]),
        "boards": part("Side and end boards, corner pieces, brackets", S("board_l", "board_r", "board_f", "board_b", "corners", "brackets"), COL["boards"]),
        "lights": part("Lights, reflectors and flag", S("lights", "flag", "pole_clips"), COL["lights"]),
        "pack": part("Battery pack", S("pack"), COL["pack"]),
        "hitch": part("Axle hitch and locking pin", S("hitch", "hitch_pin"), COL["hitch"]),
    }


ORDER = ["housing", "frame", "bushings", "drawbar", "cartridge", "end_cap", "lever", "stand", "motor", "idler",
         "brakes", "cables", "enclosure", "ctrl", "harness", "deck", "boards", "lights", "pack", "hitch"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"housing": (-80, 0, -420), "frame": (0, 0, 0), "bushings": (-360, 0, -720), "drawbar": (-560, 0, -420),
           "cartridge": (-60, 0, -720), "end_cap": (150, 0, -720), "lever": (300, 0, -640), "stand": (-620, 0, -760),
           "motor": (800, -150, 0), "idler": (800, 250, 120), "brakes": (820, 0, -520), "cables": (0, 0, -1060),
           "enclosure": (300, 0, -560), "ctrl": (300, 0, -860), "harness": (40, 0, -1320), "deck": (0, 0, 360),
           "boards": (0, 0, 660), "lights": (1150, 0, 420), "pack": (720, 0, -860), "hitch": (-760, 0, -220)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "CargoMule prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the left and above; the bicycle would be at the left",
                       elev=20, azim=-105, size=(13, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="CargoMule", date=DATE)
    zc = D["zc"]
    hx0, hx1 = P["housing"][2], P["housing"][3]
    out = []

    def want(n):
        return only is None or str(n) in only

    if want(101):
        out.append(bv.component_sheet(
            Part("Coupler housing", S("housing"), COL["housing"]), [M["frame"], M["drawbar"], M["lever"], M["stand"]],
            dwg_no="CGM-DWG-101", title="CargoMule coupler housing: making sketch",
            material="Steel tube 60.3 x 2.0 mm; plates 4 and 5 mm; S235", view_shape=b.Pos(-hx0, 0, -zc) * S("housing"),
            inset_view=(22, -125),
            notes=["Tube 60.3 x 2.0 mm, 370 mm long. Measure along it from the front end.",
                   "Bore must take the 56.3 mm bushings and spring cage as a sliding",
                   "  fit: hone or file out any weld bead inside.",
                   "Window 70 x 24 mm in the right side, 105 to 175 mm from the front:",
                   "  the clevis pin goes in through it. Deburr; fit a rubber cover.",
                   "Flange ring 80 mm OD x 6 mm on the rear end, flush; four M5",
                   "  tapped holes on a 66 mm circle at 45 degrees from the top.",
                   "Fork on top at the front: two 5 x 17 mm tines 12.8 mm apart,",
                   "  112 mm long, 72 mm of it ahead of the tube; a 5 mm plate closes",
                   "  the slot's front end. This end is the overload stop.",
                   "Stand clevis under the front: two 5 mm plates 25 mm apart,",
                   "  10 to 40 mm from the front, 10 mm hole 46 mm below the axis.",
                   "Lever cheeks under the rear: two 4 mm plates 16 mm apart; 8 mm",
                   "  pivot hole 106 mm below the axis, 23 mm behind the rear end.",
                   "Cable stop tab 5 mm across the cheeks' rear ends, 6 mm hole",
                   "  120 mm below the axis.",
                   "Check: a 38 mm bar slides end to end with the bushings in."],
            **base))

    if want(102):
        cc = S("cage", "end_cap")
        out.append(bv.component_sheet(
            Part("Spring cage and end cap", cc, COL["cage"]), [part("Load cell and pull rod", S("cell", "pull_rod", "rod_end"), "#9CA3AF"), M["lever"], M["drawbar"]],
            dwg_no="CGM-DWG-102", title="CargoMule spring cage and end cap: making sketch",
            material="Steel tube 56.3 x 1.5 mm; plate 3 and 6 mm", view_shape=b.Pos(-P["bulkhead_x"], 0, -zc) * cc,
            inset_view=(20, -120),
            notes=["Spring cage: tube 56.3 x 1.5 mm, 105 mm long, a sliding fit in",
                   "  the housing bore.",
                   "Bulkhead: 6 mm disc welded inside the cage's front end, 12.5 mm",
                   "  centre hole for the pull rod and an 8 mm hole for the load",
                   "  cell cable, 18 mm right of and 15 mm above the centre.",
                   "Ring: 80 mm OD x 3 mm, welded on the cage's rear end, four",
                   "  5.5 mm holes on a 66 mm circle to match the housing flange.",
                   "End cap: 80 mm OD x 6 mm disc, the same four holes, a 12.5 mm",
                   "  centre hole for the pull rod's tail and an 8 mm cable hole",
                   "  lined up with the bulkhead's (fit a small cable gland).",
                   "The ring is clamped between the housing flange and the end cap",
                   "  by four M5 screws; the rod's pull is carried by the bulkhead,",
                   "  the cage and the ring.",
                   "Check: the cage slides fully home by hand."],
            **base))

    if want(103):
        fr = S("rails", "nose_bars", "arches")
        out.append(bv.component_sheet(
            Part("Chassis frame", fr, COL["frame"]), [M["housing"], M["motor"], M["idler"], M["drawbar"]],
            dwg_no="CGM-DWG-103", title="CargoMule chassis frame: making sketch (weldment)",
            material="Steel box 30 x 30 x 1.5; tube 28 x 1.5 and 25 x 1.5; S235",
            inset_view=(25, -125),
            notes=["Positions from the front face of the front end rail, and from",
                   "  the centre line. Weld on a flat table; check diagonals.",
                   "Side rails: two 30 x 30 x 1.5 box, 1,200 mm, ends capped.",
                   "End rails and crossmembers: five 640 mm lengths between the",
                   "  side rails; crossmember centres at 300, 620 and 950 mm.",
                   "Nose bars: 28 x 1.5 tube from the front rail's face, 15 mm in",
                   "  from each side, to the coupler housing's sides, 320 mm from",
                   "  its front end. Fishmouth the ends to sit on the housing.",
                   "Arch frames: 25 x 1.5 tube; outriggers at 320 and 920 mm,",
                   "  117.5 mm out from each side rail; a hoop over each tyre,",
                   "  top 546 mm above the ground; a strut down at 620 mm.",
                   "Rivet nuts M6 in the rail tops for the deck (16) and in the",
                   "  crossmember bottoms at 300 and 620 mm, 100 mm each side",
                   "  (enclosure, 4); M5 in the rear rail face (lights, 4).",
                   "Tie-down eyes on the side rails at 150 mm from each end.",
                   "Dropout plates: see CGM-DWG-104. Paint after welding."],
            **base))

    if want(104):
        dro = S("dropouts")
        left_inner = dro & box(P["axle_x"] - 60, P["axle_x"] + 140, -351, -344, 200, 380)
        out.append(bv.component_sheet(
            Part("Inner dropout plate", left_inner, COL["dropout"]), [part("Frame", S("rails", "arches"), "#D1D5DB")],
            dwg_no="CGM-DWG-104", title="CargoMule dropout plates (make 4): making sketch",
            material="Steel plate 5 mm, S235", view_shape=b.Pos(-P["axle_x"], 0, -P["wheel_r"]) * left_inner,
            inset_view=(-30, 60),
            notes=["Inner plates (2): 170 x 80 mm at axle height with a 90 mm",
                   "  wide upper part up to the side rail, 160 mm tall in all.",
                   "  The axle sits 45 mm from the plate's front edge.",
                   "Axle slot 10.2 mm wide, 40 mm deep up from the bottom edge,",
                   "  round-ended at the axle centre. File it to fit the axle flats.",
                   "Caliper tab: two 6.5 mm holes 100 mm behind the axle, 18 mm",
                   "  above and below it; check against the adapter you buy.",
                   "Torque arm hole: 6.5 mm, 60 mm above the axle (left plate;",
                   "  drill both so they match).",
                   "Outer plates (2): 60 x 80 mm, the same slot, welded to the",
                   "  arch strut's foot.",
                   "Weld the inner plates under the side rails with their inner",
                   "  faces 350 mm from the centre line; outer plates' inner faces",
                   "  450 mm: the 100 mm hub fits between, axles in line.",
                   "Check: a straight 10 mm bar drops into all four slots at once."],
            **base))

    if want(105):
        bar = S("drawbar")
        out.append(bv.component_sheet(
            Part("Drawbar", bar, COL["drawbar"]), [M["housing"], M["frame"], M["hitch"]],
            dwg_no="CGM-DWG-105", title="CargoMule drawbar: making sketch",
            material="S355 steel tube 38 x 2.5 mm", inset_view=(30, -125),
            notes=["Cut 1,320 mm of 38 x 2.5 S355 tube (trim to 1,305 after bending).",
                   "Three bends, 115 mm centre-line radius, in a tube bender with",
                   "  a 38 mm die. From the hitch end: 90 mm straight, bend 85",
                   "  degrees; 338 mm straight, bend 67 degrees the same way;",
                   "  237 mm straight, bend 67 degrees back; 198 mm straight.",
                   "The bends lie almost flat: the straight rear part sits 16 mm",
                   "  higher than the hitch end. Check on a table with a packer.",
                   "The rear 198 mm must be straight and round to slide in the",
                   "  bushings: no dents, file off any weld spatter.",
                   "Rear end: weld in a 33 mm plug, 15 mm long, tapped M10.",
                   "Overload pin hole: 12.2 mm, straight down through both walls,",
                   "  155 mm from the rear end, square to the last bend's plane.",
                   "Hitch end: 6.2 mm locking pin hole, 30 mm from the end.",
                   "Check: the rear end slides through a 38.2 mm ring gauge."],
            **base))

    if want(106):
        lv = S("lever")
        out.append(bv.component_sheet(
            Part("Brake lever", lv, COL["lever"]), [M["housing"], M["cartridge"], M["end_cap"]],
            dwg_no="CGM-DWG-106", title="CargoMule brake lever: making sketch",
            material="Steel flat bar 20 x 6 mm", view_shape=b.Pos(-P["pivot"][0], 0, -P["pivot"][1]) * lv,
            inset_view=(10, 60),
            notes=["Cut 138 mm of 20 x 6 mm flat bar; round both ends.",
                   "Pivot hole 8.2 mm, 20 mm from the bottom end.",
                   "Cable hole 5 mm, 6 mm from the bottom end: 13.8 mm below",
                   "  the pivot.",
                   "The pull rod's tail pushes the lever's face 106 mm above the",
                   "  pivot, so the cable end moves 7.7 times less and pulls 7.7",
                   "  times harder than the rod.",
                   "Fit: between the housing's cheeks on an M8 bolt with two",
                   "  spring washers each side, set so the lever swings with a",
                   "  light drag (this is the coupler's damping).",
                   "At rest the rod's tail is 2 mm short of the lever.",
                   "Check: the lever swings freely through 30 degrees."],
            **base))

    if want(107):
        dk = S("deck")
        out.append(bv.component_sheet(
            Part("Deck", dk, COL["deck"]), [M["frame"], M["boards"]],
            dwg_no="CGM-DWG-107", title="CargoMule deck: making sketch",
            material="Exterior plywood 12 mm", inset_view=(30, -125),
            notes=["Cut 1,200 x 700 mm from 12 mm exterior plywood, square.",
                   "Drill 16 countersunk 6.5 mm holes over the rivet nuts in the",
                   "  frame: drill through the deck into the nuts' centres with",
                   "  the deck clamped in place.",
                   "Side rails: 15 mm in from each long edge, at 200, 600 and",
                   "  1,000 mm from the front edge (these also hold the brackets).",
                   "End rails: 15 mm in from the ends, 150 mm each side of centre.",
                   "Crossmembers at 300, 620 and 950 mm: 200 mm each side.",
                   "Seal every edge and hole with exterior sealer before fitting.",
                   "Mark the loading zone: payload centre between 32 mm ahead",
                   "  and 57 mm behind the deck centre (CGM-CAL-001).",
                   "Check: lies flat on the frame with every hole over a nut."],
            **base))

    if want(108):
        bd = S("board_l", "board_f")
        out.append(bv.component_sheet(
            Part("Side and end boards", bd, COL["boards"]), [M["deck"], M["frame"]],
            dwg_no="CGM-DWG-108", title="CargoMule side and end boards: making sketch",
            material="Exterior plywood 9 mm", inset_view=(30, -125),
            notes=["Side boards (2): 1,200 x 150 x 9 mm.",
                   "End boards (2): 682 x 150 x 9 mm; they sit between the side",
                   "  boards (drawn: the left side board and the front board).",
                   "Hand slots are optional; seal all edges.",
                   "Holes, 6.5 mm, 15 mm up from the bottom edge, where the",
                   "  brackets go: side boards at 200, 600 and 1,000 mm; end",
                   "  boards 150 mm each side of centre.",
                   "Corner holes, 6.5 mm, at 50 and 100 mm up: 15 mm from each",
                   "  end of the side boards, 11 mm from each end of the end boards.",
                   "The boards stand on the deck with their outer faces flush with",
                   "  its edges.",
                   "The left side board also carries the two flag pole clips",
                   "  (position on CGM-DWG-109).",
                   "Check: each board stands square with the deck's edge."],
            **base))

    if want(109):
        corner = S("corners") & box(P["deck_x0"] - 10, P["deck_x0"] + 40, -360, -310, 400, 600)
        brk = S("brackets") & box(P["deck_x0"] + 170, P["deck_x0"] + 230, -360, -300, 400, 470)
        both = corner + brk
        reg = (P["deck_x0"] - 10, P["deck_x0"] + 260, -365, -250, 405, 580)
        out.append(bv.component_sheet(
            Part("Corner piece and board bracket", both, COL["fit"]),
            [part("Boards", S("board_l", "board_f") & box(*reg), "#D1D5DB"), part("Deck", S("deck") & box(*reg), "#E5E7EB")],
            view_shape=corner + b.Pos(-150, 0, 0) * brk,
            dwg_no="CGM-DWG-109", title="CargoMule corner pieces (4) and board brackets (10): making sketch",
            material="Aluminium angle 30 x 30 x 3 mm", inset_view=(30, 40),
            notes=["Corner pieces (4): 150 mm of 30 x 30 x 3 aluminium angle;",
                   "  one leg covers the end of the side board and the end board's",
                   "  face, the other the side board's face.",
                   "  Two 6.5 mm holes in each leg at 50 and 100 mm up, drilled",
                   "  through the boards' corner holes with the piece clamped on.",
                   "Board brackets (10): 40 mm of the same angle; one 6.5 mm hole",
                   "  in each leg, 15 mm from the corner, centred.",
                   "Fit: bracket flat leg on the deck, bolted down through the deck",
                   "  into a frame rivet nut; upright leg on the board's inside",
                   "  face with an M6 bolt and wing nut. Corner pieces: M6 bolts",
                   "  with wing nuts through both boards.",
                   "To take a board off: undo its wing nuts and lift it.",
                   "Flag pole: 12 mm pole in two clips on the left board's inside",
                   "  face, 30 mm behind the front board, at 40 and 120 mm up.",
                   "Deburr every cut edge."],
            **base))

    if want(110):
        en = S("enclosure", "door")
        out.append(bv.component_sheet(
            Part("Enclosure and door", en, COL["enc"]), [M["frame"], M["pack"], M["ctrl"]],
            dwg_no="CGM-DWG-110", title="CargoMule battery enclosure and door: making sketch",
            material="Galvanized steel sheet 0.8 mm", view_shape=b.Pos(-P["enc"][0], 0, -D["enc_z"][0]) * en,
            inset_view=(-25, -125),
            notes=["Box 350 long x 300 wide x 170 tall, folded from 0.8 mm",
                   "  galvanized sheet, seams riveted and sealed. Closed top.",
                   "Front face (toward the drawbar): door opening 280 x 163 mm,",
                   "  centred, from the floor up; the pack slides out through it.",
                   "Door: 292 x 166 mm with 11 mm folded sides, hinged along its",
                   "  bottom edge, a keyed lock at the top, a foam gasket.",
                   "Top: four 6.5 mm holes 15 and 335 mm from the front face,",
                   "  100 mm each side of centre, with a 1.5 mm steel doubler strip",
                   "  inside under each pair.",
                   "Vent low on the rear face, pointing down and away from the load;",
                   "  cable glands on the left, right and rear faces.",
                   "Fit: four M6 bolts from inside, up into the rivet nuts in the",
                   "  crossmembers, with large washers.",
                   "Check: the pack slides in and out with the door open."],
            **base))

    if want(111):
        st = S("stand")
        out.append(bv.component_sheet(
            Part("Parking stand", st, COL["stand"]), [M["housing"], M["drawbar"]],
            dwg_no="CGM-DWG-111", title="CargoMule parking stand: making sketch",
            material="Steel tube 25 x 2 mm; plate 6 mm", view_shape=b.Pos(-P["stand_x"], 0, 0) * st,
            inset_view=(15, -125),
            notes=["Leg: 316 mm of 25 x 2 mm steel tube.",
                   "Cross hole 10.2 mm, 12 mm from the top end.",
                   "Foot: 80 x 60 x 6 mm plate welded square on the bottom end.",
                   "Fit: in the clevis under the coupler housing's front on an",
                   "  M10 bolt with a nyloc nut, snug so it stays where it is put.",
                   "Down, it holds the housing's axis 356 mm above the ground,",
                   "  level with a bicycle's rear axle.",
                   "Up, it folds back under the housing and is held by a rubber",
                   "  strap. Fold it up before riding.",
                   "Check: down, the trailer stands level and does not rock."],
            **base))
    return out


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & box(x0, x1, y0, y1, z0, z1)


def joints(only=None):
    out = []
    zc = D["zc"]
    ax, wr = P["axle_x"], P["wheel_r"]

    def want(n):
        return only is None or str(n) in only

    def J(n, parts, title, sub, **kw):
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    if want(1):
        bx = (860, 1330, 0, 40, 225, 410)
        J(1, [part("Coupler housing (cut open)", win(S("housing"), *bx), COL["housing"]),
              part("Bushings", win(S("bushings"), *bx), COL["bush"]),
              part("Drawbar", win(S("drawbar"), *bx), COL["drawbar"]),
              part("Rod end and clevis pin", win(S("rod_end", "clevis_pin"), *bx), COL["rod"]),
              part("Load cell and clevis", win(S("cell"), *bx), COL["cell"]),
              part("Pull rod, washer and nut", win(S("pull_rod"), *bx), "#7C3AED"),
              part("Spring", win(S("spring"), *bx), "#F97316"),
              part("Spring cage and end cap", win(S("cage", "end_cap"), *bx), COL["cage"]),
              part("Brake lever", win(S("lever"), *bx), COL["lever"])],
          "inside the coupler (cut on the centre line)",
          "Seen from the left. Pull goes drawbar, load cell, pull rod, bulkhead; push slides it all back against the spring",
          elev=8, azim=-90, size=(11, 5.5))
    if want(2):
        bx = (790, 935, -40, 40, 300, 410)
        J(2, [part("Coupler housing front, fork and stop plate", win(S("housing"), *bx), COL["housing"]),
              part("Drawbar", win(S("drawbar"), *bx), COL["drawbar"]),
              part("Overload pin (M12 shoulder bolt)", win(S("opin"), *bx), COL["pin"]),
              part("Front bushing", win(S("bushings"), *bx), COL["bush"]),
              part("Stand leg in its clevis", win(S("stand", "stand_bolt"), *bx), COL["stand"])],
          "fork, overload pin and stand clevis",
          "Seen from above, front left. The pin rides in the slot; it sits 0.5 mm behind the closed end, which stops an overload",
          elev=55, azim=-150)
    if want(3):
        bx = (960, 1080, 0, 40, 320, 395)
        J(3, [part("Coupler housing, side window", win(S("housing"), *bx), COL["housing"]),
              part("Rod end eye (behind the near clevis plate)", win(S("rod_end"), *bx), COL["rod"]),
              part("Load cell clevis plate", win(S("cell"), *bx), COL["cell"]),
              part("Clevis pin (M8 bolt), in through the window", win(S("clevis_pin"), *bx), COL["pin"])],
          "clevis pin through the side window",
          "Seen from the right. The window lets the pin in after both halves are in the housing",
          elev=12, azim=80)
    if want(4):
        bx = (1180, 1330, -30, 30, 215, 400)
        J(4, [part("Housing rear, flange and cheeks", win(S("housing"), *bx), COL["housing"]),
              part("End cap", win(S("end_cap"), *bx), COL["cage"]),
              part("Pull rod tail", win(S("pull_rod"), *bx), "#7C3AED"),
              part("Brake lever", win(S("lever"), *bx), COL["lever"]),
              part("Pivot bolt and friction washers", win(S("lever_bolt"), *bx), COL["pin"]),
              part("Brake cable", win(S("brake_cables"), *bx), COL["cables"])],
          "brake lever under the housing's rear",
          "Seen from behind and to the left. The rod's tail pushes the lever's top; the bottom pulls the cable through the stop tab",
          elev=12, azim=-25)
    if want(5):
        bx = (1150, 1340, -360, 360, 300, 420)
        J(5, [part("Coupler housing", win(S("housing"), *bx), COL["housing"]),
              part("Nose bars (fishmouthed onto the housing)", win(S("nose_bars"), *bx), COL["frame"]),
              part("Front end rail and side rails", win(S("rails"), *bx), "#94A3B8")],
          "A-frame nose: nose bars, front rail and coupler housing",
          "Seen from above and the front left. Every joint is a full weld",
          elev=50, azim=-145)
    if want(6):
        bx = (ax - 100, ax + 150, -400, -320, 180, 400)
        J(6, [part("Inner dropout plate and caliper tab", win(S("dropouts"), *bx), COL["dropout"]),
              part("Side rail", win(S("rails"), *bx), "#94A3B8"),
              part("Hub motor, axle and nut", win(S("motor_wheel"), *bx), COL["motor"]),
              part("Torque arm and M6 bolt", win(S("torque_arm"), *bx), COL["fit"]),
              part("Rotor and caliper", win(S("brakes"), *bx), COL["brakes"]),
              part("Brake cable", win(S("brake_cables"), *bx), COL["cables"])],
          "left inner dropout: axle, torque arm and caliper",
          "Seen from the inside of the trailer. The torque arm stops the motor's axle turning in its slot",
          elev=10, azim=75)
    if want(7):
        bx = (ax - 80, ax + 80, -500, -440, 200, 330)
        J(7, [part("Outer dropout plate", win(S("dropouts"), *bx), COL["dropout"]),
              part("Arch strut", win(S("arches"), *bx), COL["frame"]),
              part("Axle end and nut", win(S("motor_wheel"), *bx), COL["motor"]),
              part("Motor cable (clipped to the strut)", win(S("harness"), *bx), COL["harness"])],
          "left outer dropout on the arch strut",
          "Seen from outside. The plate is welded to the strut's foot; the axle nut sits on its outer face",
          elev=10, azim=-100)
    if want(8):
        bx = (1565, 1645, 100, 170, 330, 415)
        J(8, [part("Crossmember (cut) with rivet nut", win(S("rails"), *bx), "#475569"),
              part("Enclosure top and front wall (cut)", win(S("enclosure"), *bx), "#CBD5E1"),
              part("Door", win(S("door"), *bx), "#64748B"),
              part("M6 bolt and washer, from inside", win(S("enc_bolts"), *bx), COL["pin"])],
          "enclosure hung under a crossmember",
          "Cut through the front right bolt, seen from the left. The bolt goes up from inside the box into a rivet nut",
          elev=8, azim=-75)
    if want(9):
        x0 = P["deck_x0"]
        bx = (x0 - 10, x0 + 240, -365, -250, 370, 580)
        J(9, [part("Corner piece", win(S("corners"), *bx), COL["fit"]),
              part("Board bracket", win(S("brackets"), *bx), "#6B7280"),
              part("Left side board", win(S("board_l"), *bx), COL["boards"]),
              part("Front board", win(S("board_f"), *bx), "#C8A878"),
              part("Deck", win(S("deck"), *bx), COL["deck"]),
              part("Side rail", win(S("rails"), *bx), "#94A3B8")],
          "front left corner: boards, corner piece and bracket",
          "Seen from above and outside the front left corner. Wing nuts on the inside let the boards come off",
          elev=72, azim=-150)
    if want(10):
        import build123d as b  # noqa: F401
        bx = (-40, 140, -260, -70, 290, 400)
        J(10, [part("Axle hitch (bought)", win(S("hitch"), *bx), COL["hitch"]),
               part("Locking pin", win(S("hitch_pin"), *bx), COL["pin"]),
               part("Drawbar front end", win(S("drawbar"), *bx), COL["drawbar"])],
           "hitch arm into the drawbar",
           "Seen from above and behind. The arm goes 60 mm into the tube; the locking pin goes through both",
           elev=45, azim=-40)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []
    fl = [ground()]

    def want(n):
        return only is None or str(n) in only

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    fr, ho = M["frame"], M["housing"]
    front = box(600, 1460, -400, 400, 150, 450)
    frf = part("Chassis frame (front part shown)", S("rails", "nose_bars") & front, COL["frame"])
    base = [frf, ho]
    st(1, base, [mv(part("Front bushing", S("bushings") & box(870, 910, -40, 40, 300, 420), COL["bush"]), (-160, 0, 0)),
                 mv(part("Rear bushing", S("bushings") & box(930, 970, -40, 40, 300, 420), COL["bush"]), (520, 0, 0))],
       "bushings into the coupler housing",
       "Front bushing in from the front, rear bushing in from the rear end; press flush to their marks",
       elev=18, azim=-125, label_done=False)
    b1 = base + [M["bushings"]]
    st(2, b1, [mv(part("Drawbar with rod end", S("drawbar", "rod_end"), COL["drawbar"]), (-380, 0, 0)),
               mv(part("Overload pin", S("opin"), COL["pin"]), (0, 0, 160))],
       "drawbar in from the front, then the overload pin",
       "Slide the straight end through both bushings; drop the pin through the slot and the drawbar, nut underneath",
       elev=22, azim=-125, label_done=False)
    drc = part("Drawbar (rear part shown)", S("drawbar", "rod_end", "opin") & box(650, 1500, -120, 120, 250, 450), COL["drawbar"])
    b2 = b1 + [drc]
    st(3, b2, [mv(part("Load cell, pull rod, spring and spring cage", S("cell", "pull_rod", "spring", "cage"), COL["cell"]), (380, 0, 0)),
               mv(M["end_cap"], (520, 0, 0))],
       "load cell cartridge in from the rear, then the end cap",
       "Cartridge built on the bench; slide it in until the clevis meets the rod end; four M5 screws through cap and ring",
       elev=20, azim=-60, label_done=False)
    b3 = b2 + [M["cartridge"], M["end_cap"]]
    st(4, b3, [mv(part("Clevis pin (M8 bolt)", S("clevis_pin"), COL["pin"]), (0, 140, 0))],
       "clevis pin through the side window",
       "Seen from the right. Line up the eye and clevis through the window; bolt and nyloc nut; fit the window cover",
       elev=15, azim=60, label_done=False)
    b4 = b3
    st(5, b4, [mv(M["lever"], (0, -120, 0))], "brake lever onto its cheeks",
       "M8 bolt with two spring washers each side; set a light drag",
       elev=10, azim=-140, label_done=False)
    st(6, b4 + [M["lever"]], [mv(M["stand"], (0, -150, -60))], "parking stand into its clevis",
       "M10 bolt and nyloc nut, snug; stand down from here on", elev=15, azim=-120, label_done=False)
    b6 = [fr, ho, M["bushings"], M["drawbar"], M["cartridge"], M["end_cap"], M["lever"], M["stand"]]
    st(7, b6, [mv(M["motor"], (0, -260, -120)), mv(M["idler"], (0, 260, -120))],
       "wheels into the dropouts",
       "Motor wheel on the left with its torque arm on the inside face; idler on the right; axle nuts to the maker's torque",
       elev=18, azim=-60, label_done=False)
    b7 = b6 + [M["motor"], M["idler"]]
    zone = box(P["axle_x"] - 150, P["axle_x"] + 200, -480, -300, 150, 420)
    st(8, [part("Frame at the left wheel", S("rails", "dropouts", "arches") & zone, COL["frame"]),
           part("Hub motor wheel", S("motor_wheel", "torque_arm") & zone, COL["motor"])],
       [part("Rotor (fitted at the bench)", S("brakes") & zone & box(P["axle_x"] - 100, P["axle_x"] + 79, -400, -300, 150, 420), "#F59E0B"),
        mv(part("Caliper on its adapter", S("brakes") & box(P["axle_x"] + 70, P["axle_x"] + 130, -400, -340, 200, 300), COL["brakes"]), (0, 0, -110))],
       "calipers onto the dropout tabs",
       "Left wheel, seen from below and inside. Adapter and caliper on two M6 bolts with threadlocker; the right wheel is the same",
       elev=-65, azim=60, label_done=True)
    b8 = b7 + [M["brakes"]]
    st(9, b8, [mv(M["cables"], (0, 0, -150))], "brake cables and splitter",
       "Lever to splitter under the left rail, then one cable to each caliper; clip along the rails",
       elev=-35, azim=-60, label_done=False)
    b9 = b8 + [M["cables"]]
    st(10, b9, [mv(M["enclosure"], (0, 0, -170))], "enclosure under the crossmembers",
       "Four M6 bolts from inside, up into the rivet nuts, large washers", elev=-25, azim=-120, label_done=False)
    b10 = b9 + [M["enclosure"]]
    st(11, b10, [mv(M["ctrl"], (-260, 0, 0)), mv(M["harness"], (0, 0, -140))],
       "controller, control board and harness",
       "Controller and board on the enclosure floor; motor, load cell and light cables through glands. No pack yet",
       elev=-25, azim=-120, label_done=False)
    b11 = b10 + [M["ctrl"], M["harness"]]
    st(12, b11, [mv(M["deck"], (0, 0, 260))], "deck onto the frame",
       "Six M6 countersunk bolts into the crossmembers' rivet nuts; the ten edge bolts go in with the brackets", elev=25, azim=-125, label_done=False)
    b12 = b11 + [M["deck"]]
    st(13, b12, [mv(M["boards"], (0, 0, 300))], "boards, corner pieces and brackets",
       "Brackets bolted down through the deck; boards on with M6 bolts and wing nuts", elev=25, azim=-125, label_done=False)
    b13 = b12 + [M["boards"]]
    st(14, b13, [mv(M["lights"], (250, 0, 250))], "lights, reflectors and flag",
       "Rear lights on M5 screws into the rear rail; reflectors on the side rails; pole in its two clips",
       elev=22, azim=-125, label_done=False)
    b14 = b13 + [M["lights"]]
    st(15, [p for p in b14 if p.name not in ("Plywood deck", "Side and end boards, corner pieces, brackets", "Lights, reflectors and flag")],
       [mv(M["pack"], (-300, 0, 0))], "battery pack into the enclosure",
       "Only after safety stop S3. Slide it in through the front door, strap it down, plug in, lock the door",
       elev=-20, azim=-130, label_done=False)
    b15 = b14 + [M["pack"]]
    st(16, b15, [mv(M["hitch"], (0, -200, 120))], "hitch onto the bicycle and into the drawbar",
       "Hitch plate under the bike's left axle end (bike not drawn); arm into the drawbar, locking pin, safety strap",
       elev=25, azim=-130, label_done=False)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] in ("sheet", "joint", "step"):
        fn = {"sheet": sheets, "joint": joints, "step": steps}[args[0]]
        print(fn(set(args[1:])))
        sys.exit(0)
    what = args or ["overview", "sheets", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps}
    for w in what:
        print(w, "->", fns[w]())
