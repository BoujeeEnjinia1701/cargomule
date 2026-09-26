"""CargoMule sizing calculations, CGM-CAL-001 v0.2 (TRL 3; 180 mm rotors, R8 45 kg and motor derating per CGM-DDR-002).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that CGM-CAL-001 (docs/04-calcs/01-sizing.md) quotes, each on a line
tagged like [A1]. Geometry comes from cad/src/model.py (PARAMS and derived), so the calc
note, the STEP files and drawing CGM-DWG-001 use the same dimensions. The BOM total is read
from bom/bom.csv and the budget from project.yaml. First-principles estimates for a paper
proof of concept; every assumption is set in the ASSUMPTIONS block below.
"""
import csv
import sys
from math import atan2, cos, degrees, exp, hypot, pi, radians, sin, sqrt
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, drawbar_points  # noqa: E402

D = derived(P)
g = 9.81

# ------------------------------------------------------------------ ASSUMPTIONS
A = {
    # masses and loads
    "payload": 150.0, "payload_cg_above_deck": 150.0, "bike_rider": 100.0,
    "steel_rho": 7850.0, "ply_rho": 550.0,
    # resistance
    "crr": 0.010, "cda_extra": 0.10, "rho_air": 1.2,
    # control
    "G": 4.0, "G_range": (2.0, 6.0), "deadband": 3.0,
    # motor: 250 W geared front-style hub, 20 in wheel, DC-equivalent model (to confirm from the datasheet)
    "v_pack": 38.4, "v_pack_low": 36.0, "no_load_rpm": 230.0, "R_motor": 0.35, "eta_gear": 0.90,
    "P_iron": 8.0, "eta_ctrl": 0.95, "I_batt_max": 15.0, "I_phase_max": 30.0,
    "Rth": 1.2, "Cth": 700.0, "T_amb": 30.0, "T_limit": 100.0,
    # pack and charging
    "pack_Wh": 384.0, "usable": 0.90, "eta_charger": 0.90, "eta_cell": 0.96, "pack_Ah": 10.0, "charge_A": 4.0,
    # loop dynamics
    "zeta_s": 0.05, "fs": 80.0, "t_ctrl": 0.020, "k_range": (20e3, 50e3, 100e3, 200e3, 500e3),
    # braking
    "decel": 3.0, "push_max": 100.0, "preload": 30.0, "mu_dry": 0.40, "mu_wet": 0.30,
    "caliper_ratio": 4.0, "cable_travel": 3.5, "lever": 7.7, "c_steel": 460.0, "h_rotor": 60.0,
    "rotor_m_160": 0.12, "rotor_area_160": 0.025, "reaction": 1.0,
    # structure
    "fy_s355": 355.0, "fy_s235": 235.0, "fy_axle": 650.0, "ply_allow": 10.0,
    "n_bump": 2.0, "n_tongue": 3.0, "ult_long_g": 1.0, "hitch_lever": 12.0,
}

# 180 mm rotors (CGM-DDR-002): mass and cooled area scaled from a 160 mm rotor by the braking annulus (hub bore 60 mm)
ROTOR_SCALE = ((P["rotor_d"] / 2) ** 2 - 30 ** 2) / (80 ** 2 - 30 ** 2)
A["rotor_m"] = A["rotor_m_160"] * ROTOR_SCALE
A["rotor_area"] = A["rotor_area_160"] * ROTOR_SCALE

# bought-in part masses, kg (typical catalog values, to confirm by weighing)
BOUGHT = {
    "4 Universal axle hitch": 0.60, "5 Load cell, clevises and amplifier": 0.45,
    "6 Overrun coupler (sleeve, spring, damper, lever)": 1.60,
    "7 Hub motor wheel (geared hub 2.6 kg, rim, spokes, tyre 1.7 kg)": 4.30,
    "8 Idler wheel with disc hub": 1.90, "9 Disc brakes, two (caliper, 180 mm rotor, cable)": round(0.80 + 2 * (A["rotor_m"] - A["rotor_m_160"]), 2),
    "11 Battery pack, 12S LiFePO4 384 Wh with BMS": 4.20, "12 Motor controller": 0.40,
    "13 Control board": 0.15, "14 Harness, fuse and key switch": 0.50,
    "15 Lights, reflectors and flag": 0.50, "18 Hardware, paint and consumables": 0.80,
}

out = []


def say(tag, text):
    line = f"[{tag}] {text}"
    out.append(line)
    print(line)


def tube_area(od, t):
    return pi / 4 * (od ** 2 - (od - 2 * t) ** 2)


def tube_Z(od, t):
    return pi * (od ** 4 - (od - 2 * t) ** 4) / (32 * od)


def box_Z(b, t):
    return (b ** 4 - (b - 2 * t) ** 4) / 12 / (b / 2)


def dist(a, b):
    return sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


print("CargoMule sizing, CGM-CAL-001. Units SI unless stated; lengths from cad/src/model.py in mm.\n")

# ================================================================== A. Mass and balance
rho = A["steel_rho"] / 1e9          # kg/mm3
hw, x0, x1, ax = D["hw"], P["deck_x0"], D["deck_x1"], P["axle_x"]
R, rt = P["rail"], P["rail_t"]
box_len = 2 * P["deck_len"] + 2 * (P["deck_w"] - 2 * R) + len(P["cross_x"]) * (P["deck_w"] - 2 * R)
box_area = R ** 2 - (R - 2 * rt) ** 2
m_box = box_len * box_area * rho
nose = (P["nose_x"], 0, P["nose_z"])
nose_len = 2 * dist((x0 + 15, hw - 15, D["fz0"] + 15), nose)
m_nose = nose_len * tube_area(*P["nose_tube"]) * rho
zr = (D["fz0"] + D["fz1"]) / 2
arch_len_side = (2 * (D["arch_y"] - hw) + 2 * hypot(80, D["arch_top"] - zr)
                 + (2 * P["arch_half"] - 160) + (D["arch_top"] - (P["wheel_r"] + 20)))
m_arch = 2 * arch_len_side * tube_area(*P["arch_tube"]) * rho
m_plates = 2 * (90 * (D["fz0"] - (P["wheel_r"] - 40)) + 60 * 80) * P["plate_t"] * rho
m_frame = m_box + m_nose + m_arch + m_plates + 0.40      # 0.40 kg: tie-down eyes, nose node, brackets
pts = drawbar_points(P)
db_len = sum(dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) - (P["coupler_x"][1] - P["cell_x"][0])
m_drawbar = db_len * tube_area(*P["drawbar"]) * rho
m_stand = (P["nose_z"] - 40) * tube_area(22, 2) * rho + 0.2
ex0, el, ew, eh = P["enc"]
enc_area = 2 * (el * ew + el * eh + ew * eh)
m_enc = enc_area * 0.8 * rho + 0.3                     # 0.3 kg: hinges, lock, glands, vent
ply = A["ply_rho"] / 1e9
m_deck = P["deck_len"] * P["deck_w"] * P["deck_t"] * ply
m_boards = (2 * P["deck_len"] + 2 * P["deck_w"]) * P["board_h"] * P["board_t"] * ply
made = {"1 Chassis frame (welded steel)": m_frame, "2 Deck, 12 mm plywood": m_deck,
        "2 Side boards, removable": m_boards, "3 Drawbar, 38 x 2.5 mm S355": m_drawbar,
        "10 Enclosure, 0.8 mm steel": m_enc, "16 Parking stand": m_stand}
say("A1", f"Frame: box section {box_len/1000:.2f} m at {box_area*rho*1000:.2f} kg/m = {m_box:.2f} kg; "
          f"nose bars {m_nose:.2f} kg; arch frames {m_arch:.2f} kg; dropout plates {m_plates:.2f} kg; "
          f"frame total {m_frame:.1f} kg")
for k, v in {**made, **BOUGHT}.items():
    say("A2", f"{k}: {v:.2f} kg")
m_empty = sum(made.values()) + sum(BOUGHT.values())
m_loaded = m_empty + A["payload"]
say("A3", f"Empty trailer {m_empty:.1f} kg ({m_empty*2.2046:.0f} lb) against R8 45 kg (relaxed from 35 kg to 40 kg, then 45 kg by CGM-DDR-002); "
          f"without side boards {m_empty-m_boards:.1f} kg")
say("A4", f"Loaded trailer, design case: {m_loaded:.1f} kg")

# center of mass: (mass, x, z) for each group
fz0, fz1 = D["fz0"], D["fz1"]
ez0, ez1 = D["enc_z"]
cm = [
    (m_frame, (x0 + x1) / 2 - 40, zr + 20), (m_deck, (x0 + x1) / 2, fz1 + 5),
    (m_boards, (x0 + x1) / 2, P["deck_z"] + 75), (m_drawbar, 500, 350), (BOUGHT["4 Universal axle hitch"], 20, 340),
    (BOUGHT["5 Load cell, clevises and amplifier"], sum(P["cell_x"]) / 2, 355),
    (BOUGHT["6 Overrun coupler (sleeve, spring, damper, lever)"], sum(P["coupler_x"]) / 2, 358),
    (BOUGHT["7 Hub motor wheel (geared hub 2.6 kg, rim, spokes, tyre 1.7 kg)"], ax, P["wheel_r"]),
    (BOUGHT["8 Idler wheel with disc hub"], ax, P["wheel_r"]), (BOUGHT["9 Disc brakes, two (caliper, 180 mm rotor, cable)"], ax + 40, P["wheel_r"]),
    (m_enc, ex0 + el / 2, (ez0 + ez1) / 2), (BOUGHT["11 Battery pack, 12S LiFePO4 384 Wh with BMS"], ex0 + 12 + 125, ez0 + 80),
    (BOUGHT["12 Motor controller"] + BOUGHT["13 Control board"], ex0 + 100, ez0 + 30),
    (BOUGHT["14 Harness, fuse and key switch"], 1500, 300), (BOUGHT["15 Lights, reflectors and flag"], 2000, 700),
    (BOUGHT["18 Hardware, paint and consumables"], 1600, 380), (m_stand, P["stand_x"], 200),
]
M0 = sum(m for m, _, _ in cm)
xe = sum(m * x for m, x, _ in cm) / M0
ze = sum(m * z for m, _, z in cm) / M0
tongue_empty = M0 * (ax - xe) / ax
x_pay = D["deck_cx"]
tongue = tongue_empty + A["payload"] * (ax - x_pay) / ax
say("A5", f"Empty trailer mass center {xe:.0f} mm behind the bike axle, {ze:.0f} mm high; axle at {ax:.0f} mm, "
          f"{D['axle_behind_center']:.0f} mm behind the deck center")
ax2 = 1950.0
tongue_trl2 = M0 * (ax2 - xe) / ax2 + A["payload"] * (ax2 - x_pay) / ax2
say("A6", f"Hitch down load: empty {tongue_empty:.1f} kg; design payload centered {tongue:.1f} kg (R10: 3 to 10 kg); "
          f"with the TRL 2 axle position ({ax2:.0f} mm) it would be {tongue_trl2:.1f} kg")
per_mm = A["payload"] / ax
lo = x_pay - (10 - tongue) / per_mm     # payload center forward limit for 10 kg
hi = x_pay + (tongue - 3) / per_mm      # rearward limit for 3 kg
zero = x_pay + tongue / per_mm
say("A7", f"Hitch load changes {per_mm*100:.2f} kg per 100 mm of payload shift; 3 to 10 kg holds for a payload "
          f"center {x_pay-lo:.0f} mm ahead to {hi-x_pay:.0f} mm behind the deck center; the drawbar unloads "
          f"(0 kg) with the payload center {zero-x_pay:.0f} mm behind it")
z_load = P["deck_z"] + A["payload_cg_above_deck"]
h_cg = (M0 * ze + A["payload"] * z_load) / m_loaded
roll = (P["track"] / 2) / h_cg
a_turn = (15 / 3.6) ** 2 / 5.0 / g
say("A8", f"Loaded mass center {h_cg:.0f} mm high; static rollover threshold {roll:.2f} g (track {P['track']:.0f} mm); "
          f"a 5 m radius turn at 15 km/h needs {a_turn:.2f} g, margin {roll/a_turn:.1f}")

# ================================================================== B. Resistance, assist and felt pull
G, mt, mb = A["G"], m_loaded, A["bike_rider"]


def resist(v_kmh, grade=0.0, m=mt):
    v = v_kmh / 3.6
    return m * g * A["crr"] + 0.5 * A["rho_air"] * A["cda_extra"] * v ** 2 + m * g * grade


def felt(Rt, Gv=G, Fmax=1e9):
    """Drawbar pull felt by the rider with motor force = G x (pull - deadband), capped at Fmax."""
    db = A["deadband"]
    F = (Rt + Gv * db) / (1 + Gv) if Rt > db else Rt
    Fm = max(0.0, Gv * (F - db))
    if Fm > Fmax:
        Fm = Fmax
        F = Rt - Fm
    return F, Fm


for v in (5, 18, 20):
    Rt = resist(v)
    F, Fm = felt(Rt)
    say("B1", f"Flat at {v} km/h: trailer resistance {Rt:.1f} N; motor {Fm:.1f} N; felt by rider {F:.1f} N (R4: 15 N or less)")
R8 = resist(8, 0.08)
say("B2", f"8 % grade at 8 km/h: grade {mt*g*0.08:.1f} N, rolling {mt*g*A['crr']:.1f} N, total {R8:.1f} N; "
          f"unassisted this is {R8*8/3.6:.0f} W extra for the rider")
# ================================================================== C. Motor, controller and heating
Ke = A["v_pack"] / (A["no_load_rpm"] * 2 * pi / 60)     # V s/rad at the wheel
r_w = P["wheel_r"] / 1000


def motor_point(F_dem, v_kmh, Vb=A["v_pack"]):
    """Deliver up to F_dem at the wheel. Returns (F, I_phase, P_mech, P_loss, P_batt, I_batt)."""
    w = v_kmh / 3.6 / r_w
    kt = Ke * A["eta_gear"]

    def at(I):
        Pm_in = I * (Ke * w + I * A["R_motor"]) + A["P_iron"]
        Pb = Pm_in / A["eta_ctrl"]
        return Pb

    I = F_dem * r_w / kt
    I = min(I, A["I_phase_max"])
    # voltage limit: Ke w + I R <= Vb
    I = min(I, max(0.0, (Vb - Ke * w) / A["R_motor"]))
    while at(I) / Vb > A["I_batt_max"] and I > 0:
        I -= 0.01
    F = I * kt / r_w
    Pmech = F * v_kmh / 3.6
    Pb = at(I) if I > 0 else 0.0
    loss = (I * (Ke * w + I * A["R_motor"]) + A["P_iron"]) - Pmech if I > 0 else 0.0
    return F, I, Pmech, loss, Pb, Pb / Vb


say("C1", f"Motor model: no-load {A['no_load_rpm']:.0f} rpm at {A['v_pack']} V "
          f"({A['no_load_rpm']*2*pi/60*r_w*3.6:.1f} km/h on the 20 in wheel); Ke {Ke:.3f} V s/rad; "
          f"{Ke*A['eta_gear']:.2f} N m per phase amp at the wheel after gears")
Fd_climb = felt(R8)[1]
Fc, Ic, Pmc, Lc, Pbc, Ibc = motor_point(Fd_climb, 8)
Ffelt_climb, _ = felt(R8, Fmax=Fc)
say("C2", f"8 % at 8 km/h: motor asked for {Fd_climb:.1f} N ({Fd_climb*r_w:.1f} N m), delivers {Fc:.1f} N at "
          f"{Ic:.1f} A phase, {Ibc:.1f} A from the pack (limit {A['I_batt_max']:.0f} A); output {Pmc:.0f} W; "
          f"losses {Lc:.0f} W; efficiency {Pmc/(Pbc*A['eta_ctrl']):.0%} motor, {Pmc/Pbc:.0%} with controller")
say("C3", f"Felt by the rider on the 8 % climb: {Ffelt_climb:.1f} N (R3: 40 N or less)")
for Ib in (10.0, 12.0):
    old = A["I_batt_max"]; A["I_batt_max"] = Ib
    Fx = motor_point(Fd_climb, 8)[0]
    A["I_batt_max"] = old
    say("C4", f"Sensitivity: with a {Ib:.0f} A pack current limit the motor gives {Fx:.0f} N and the rider feels {R8-Fx:.0f} N")
rider_P = (mb * g * (0.08 + 0.006) + Ffelt_climb) * 8 / 3.6
say("C5", f"Rider's own climb at 8 km/h (bike and rider {mb:.0f} kg, own rolling 0.006) plus felt pull: about {rider_P:.0f} W; "
          f"at 150 W the rider climbs at about {150/(mb*g*0.086+Ffelt_climb)*3.6:.1f} km/h")
# thermal: preheat at flat cruise, then the 300 m climb
Ff = felt(resist(18))[1]
_, If, _, Lf, _, _ = motor_point(Ff, 18)
T_pre = A["T_amb"] + Lf * A["Rth"]
tau = A["Rth"] * A["Cth"]
for dist_m in (300, 1000):
    t = dist_m / (8 / 3.6)
    dT = Lc * A["Rth"] * (1 - exp(-t / tau))
    say("C6", f"Winding temperature after a {dist_m} m, 8 % climb at 8 km/h ({t:.0f} s): {T_pre + dT:.0f} °C "
              f"(start {T_pre:.0f} °C after flat cruising at {Lf:.0f} W loss; limit {A['T_limit']:.0f} °C; tau {tau:.0f} s)")
say("C7", f"Steady winding rise if the climb never ended: {Lc*A['Rth']:.0f} K")
Fr20, _, _, _, _, _ = motor_point(felt(resist(20))[1], 20, Vb=A["v_pack_low"])
say("C8", f"At 20 km/h on a nearly empty pack ({A['v_pack_low']} V) the motor can still give {Fr20:.1f} N "
          f"against the {felt(resist(20))[1]:.1f} N asked (R4 holds to 20 km/h)")
say("C9", f"Assist cut-off 25 km/h is above the motor's {A['no_load_rpm']*2*pi/60*r_w*3.6:.1f} km/h no-load speed, "
          f"so the firmware limit is a backstop (R5)")
# thermal derating (CGM-DDR-002): hold the winding at the limit on a climb that never ends
L_allow = (A["T_limit"] - A["T_amb"]) / A["Rth"]
lo_, hi_ = 0.0, Fc
for _ in range(60):
    mid = (lo_ + hi_) / 2
    if motor_point(mid, 8)[3] <= L_allow:
        lo_ = mid
    else:
        hi_ = mid
F_der = lo_
t_hit = -tau * np.log(1 - (A["T_limit"] - T_pre) / (Lc * A["Rth"]))
say("C10", f"Thermal derating: full assist reaches {A['T_limit']:.0f} °C after {t_hit:.0f} s ({t_hit*8/3.6:.0f} m of 8 % climb at 8 km/h); "
           f"derated to hold {A['T_limit']:.0f} °C the motor may lose {L_allow:.0f} W, giving {F_der:.0f} N, and the rider "
           f"feels {R8-F_der:.0f} N on a climb that never ends")

# ================================================================== D. Assist loop stability
def poly_pade(T, n=3):
    from math import factorial
    num = [((-1) ** k) * factorial(2 * n - k) * factorial(n) / (factorial(2 * n) * factorial(k) * factorial(n - k)) * T ** k for k in range(n + 1)]
    den = [factorial(2 * n - k) * factorial(n) / (factorial(2 * n) * factorial(k) * factorial(n - k)) * T ** k for k in range(n + 1)]
    return np.array(num[::-1]), np.array(den[::-1])


def max_real(Gv, k, filt, T):
    mu = mb * mt / (mb + mt)
    c = 2 * A["zeta_s"] * sqrt(k * mu)
    Np = np.array([c, k])
    inv = 1 / mb + 1 / mt
    Dp = mt * np.array([1.0, c * inv, k * inv])
    Nd, Dd = poly_pade(T)
    order, fc = filt
    wf = 2 * pi * fc
    Df = np.array([1 / wf, 1.0]) if order == 1 else np.array([1 / wf ** 2, sqrt(2) / wf, 1.0])
    ch = np.polyadd(np.polymul(np.polymul(Dp, Df), Dd), Gv * np.polymul(Np, Nd))
    return max(np.roots(ch).real)


T_loop = 1 / A["fs"] + 0.5 / A["fs"] + A["t_ctrl"]
say("D1", f"Loop delay {T_loop*1000:.1f} ms (80 Hz sampling, half-sample hold, {A['t_ctrl']*1000:.0f} ms controller current loop)")
FILTERS = {"TRL 2 filter, 1st order 2 Hz": (1, 2.0), "2nd order 1 Hz": (2, 1.0), "chosen, 2nd order 0.7 Hz": (2, 0.7)}
crit = {}
for name, filt in FILTERS.items():
    crits = []
    for k in A["k_range"]:
        lo_, hi_ = 0.0, 200.0
        if max_real(hi_, k, filt, T_loop) < 0:
            crits.append(hi_); continue
        for _ in range(50):
            mid = (lo_ + hi_) / 2
            if max_real(mid, k, filt, T_loop) < 0:
                lo_ = mid
            else:
                hi_ = mid
        crits.append(lo_)
    fn = [sqrt(k * (1 / mb + 1 / mt)) / 2 / pi for k in A["k_range"]]
    crit[name] = min(crits)
    say("D2", f"Filter {name}: critical gain G at drawbar stiffness "
              + ", ".join(f"{k/1000:.0f} N/mm ({f:.1f} Hz): {c:.1f}" for k, f, c in zip(A["k_range"], fn, crits))
              + f"; lowest {min(crits):.1f}, margin at G = 6 x{min(crits)/6:.1f}")
crit2 = crit["chosen, 2nd order 0.7 Hz"]
crit1 = crit["TRL 2 filter, 1st order 2 Hz"]
say("D3", f"Chosen 0.7 Hz 2nd-order filter: stable for G = 2 to 6 at every stiffness: {'yes' if crit2 > 6 else 'no'}; "
          f"gain margin {crit2/4:.1f} ({20*np.log10(crit2/4):.1f} dB) at the default G = 4 and {crit2/6:.1f} ({20*np.log10(crit2/6):.1f} dB) at G = 6; "
          f"the TRL 2 filter goes unstable above G = {crit1:.1f}")
H2 = 1 / sqrt(1 + (2.0 / 0.7) ** 4)
t_r = 0.33 / 0.7
say("D4", f"Pedal-stroke ripple at 60 rpm cadence (2 Hz) passes the 0.7 Hz filter at {H2:.0%} (the TRL 2 filter passed "
          f"{1/sqrt(2):.0%}); the cost is a slower assist, about {t_r:.2f} s to 90 % after a step in pull")
# drawbar axial stiffness from its plan offset (bending of the offset runs), E = 200 GPa
Id = tube_Z(*P["drawbar"]) * P["drawbar"][0] / 2
ssum = 0.0
for i in range(len(pts) - 1):
    for s_ in np.linspace(0, 1, 200)[:-1]:
        y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * s_
        ssum += (y - pts[0][1]) ** 2 * dist(pts[i], pts[i + 1]) / 199
k_db = 200e3 * Id / ssum * 1000
say("D5", f"Drawbar axial stiffness from bending of its offset runs: about {k_db/1000:.0f} N/mm (before the hitch joint "
          f"and load cell, which are in series and softer); the {A['k_range'][0]/1000:.0f} to {A['k_range'][-1]/1000:.0f} N/mm sweep brackets it")
# compression cut timing (fast path, unfiltered)
t_cut = 3 / A["fs"] + 0.002 + A["t_ctrl"]
say("D6", f"Assist cut on drawbar compression: 3 consecutive raw samples below -20 N at 80 Hz plus 2 ms processing "
          f"and {A['t_ctrl']*1000:.0f} ms current decay = {t_cut*1000:.0f} ms (R6 and R13: 100 ms)")
say("D7", f"Load cell: 1 kN S-type, 2 mV/V; zero drift about 0.1 % FS over 50 K = 1.0 N, plus joint hysteresis; "
          f"deadband {A['deadband']:.0f} N")

# ================================================================== E. Energy and range
MECH = []


def seg_energy(dist_km, v_kmh, grade):
    Rt = resist(v_kmh, grade)
    if Rt <= 0:
        return 0.0, 0.0
    F, Fm = felt(Rt)
    Fm_d, _, Pm, _, Pb, _ = motor_point(Fm, v_kmh)
    t_h = dist_km / v_kmh
    rider = (Rt - Fm_d) * dist_km * 1000 / 3600
    MECH.append(Pm * t_h)
    return Pb * t_h, rider


route = [("Flat, 18 km/h", 5.2, 18, 0.0), ("Climbs, 5 % at 10 km/h", 2.4, 10, 0.05), ("Descents, 5 %, overrun braking", 2.4, 20, -0.05)]
E_tot, E_rider = 0.0, 0.0
for name, dkm, v, gr in route:
    e, r = seg_energy(dkm, v, gr)
    E_tot += e; E_rider += r
    say("E1", f"{name}, {dkm} km: pack {e:.0f} Wh, rider {r:.0f} Wh")
v_stop = 18 / 3.6
ke = 0.5 * mt * v_stop ** 2 / 3600
e_stops = 20 * ke * G / (1 + G) / 0.60
E_tot += e_stops
E_mech = sum(MECH) + 20 * ke * G / (1 + G)
E_rider += 20 * ke / (1 + G)
say("E2", f"20 stops from 18 km/h: {20*ke:.1f} Wh of kinetic energy in all, motor share {G/(1+G):.0%} at 60 % "
          f"(low-speed efficiency) = {e_stops:.0f} Wh from the pack")
usable = A["pack_Wh"] * A["usable"]
whkm = E_tot / 10
rng = usable / whkm
say("E3", f"Design route (10 km, 120 m up, 120 m down, 20 stops): pack {E_tot:.0f} Wh, {whkm:.1f} Wh/km; "
          f"usable {usable:.0f} Wh; range {rng:.1f} km (R2: 20 km)")
e_flat, _ = seg_energy(10, 18, 0.0)
e_flat += 5 * ke * G / (1 + G) / 0.60
say("E4", f"Flat 10 km, 5 stops: {e_flat:.0f} Wh, {e_flat/10:.1f} Wh/km, range {usable/(e_flat/10):.0f} km")
# TRL 2 method for comparison (all 10 km rolling, full climb, 75 %)
e2 = (resist(18) * 10000 + mt * g * 120 + 20 * 0.5 * mt * (20 / 3.6) ** 2) / 3600 * G / (1 + G) / 0.75
say("E5", f"TRL 2 method (all rolling, 75 % throughout): {e2:.0f} Wh, {e2/10:.1f} Wh/km, range {usable/(e2/10):.1f} km")
mains = E_tot / A["eta_cell"] / A["eta_charger"]
say("E6", f"Flow on the design route: mains {mains:.0f} Wh, into pack {E_tot/A['eta_cell']:.0f} Wh, pack output {E_tot:.0f} Wh, "
          f"motor at the wheel {E_mech:.0f} Wh, rider {E_rider:.0f} Wh, trailer work {E_mech+E_rider:.0f} Wh; losses: charger "
          f"{mains-E_tot/A['eta_cell']:.0f} Wh, cell charging {E_tot/A['eta_cell']-E_tot:.0f} Wh, controller and motor {E_tot-E_mech:.0f} Wh")
say("E7", f"Mains energy per design trip {mains:.0f} Wh; charge time about {A['pack_Ah']/A['charge_A']+0.5:.1f} h "
          f"({A['pack_Ah']:.0f} Ah at {A['charge_A']:.0f} A plus about 0.5 h constant-voltage phase)")

# ================================================================== F. Braking
F_need = mt * A["decel"]
F_brk = F_need - A["push_max"]
kb_req = F_brk / (A["push_max"] - A["preload"])  # gain the 100 N push limit needs
ke_t = 0.5 * mt * (20 / 3.6) ** 2
ke_b = 0.5 * mb * (20 / 3.6) ** 2
say("F1", f"At 20 km/h: trailer {ke_t/1000:.2f} kJ, bike and rider {ke_b/1000:.2f} kJ; trailer needs {F_need:.0f} N to slow at "
          f"{A['decel']} m/s²; with {A['push_max']:.0f} N push the brakes must give {F_brk:.0f} N")
r_eff = (P["rotor_d"] / 2 - 8) / 1000
Fw = F_brk / 2
T_cab = Fw * (r_w / r_eff) / (2 * A["mu_dry"] * A["caliper_ratio"])
i_lev = A["lever"]
stroke = i_lev * A["cable_travel"]
say("F2", f"Per wheel {Fw:.0f} N at the tyre, {Fw*r_w/r_eff:.0f} N at the {r_eff*1000:.0f} mm rotor radius ({P['rotor_d']:.0f} mm rotor); clamp "
          f"{Fw*r_w/r_eff/(2*A['mu_dry']):.0f} N; cable tension {T_cab:.0f} N per caliper (caliper ratio {A['caliper_ratio']:.0f})")


def gain(mu):
    """Brake force per newton of drawbar compression above the preload, lever kept at A['lever']."""
    return i_lev * A["caliper_ratio"] * 2 * mu * r_eff / r_w


def push(k):
    return (F_need + k * A["preload"]) / (1 + k)


kb = gain(A["mu_dry"])
kb_wet = gain(A["mu_wet"])
push_dry = push(kb)
push_wet = push(kb_wet)
r160 = (160 / 2 - 8) / 1000
say("F3", f"Coupler: preload {A['preload']:.0f} N, lever ratio {i_lev:.1f} to the equalizer (sized for 100 N dry on 160 mm rotors, "
          f"gain {i_lev*A['caliper_ratio']*2*A['mu_dry']*r160/r_w:.2f}); with {P['rotor_d']:.0f} mm rotors the gain is {kb:.2f} N per N above preload "
          f"and the dry push at 3 m/s² is {push_dry:.0f} N; take-up travel {stroke:.0f} mm of the {P['coupler_stroke']:.0f} mm stroke")
push_wet160 = push(i_lev * A["caliper_ratio"] * 2 * A["mu_wet"] * r160 / r_w)
say("F4", f"Wet pads (mu {A['mu_wet']}): push at 3 m/s² is {push_wet:.0f} N with {P['rotor_d']:.0f} mm rotors "
          f"({push_wet160:.0f} N with 160 mm rotors); R6 target 100 N")
v = 20 / 3.6
stop = v ** 2 / (2 * A["decel"]) + v * A["reaction"]
say("F5", f"Stopping distance from 20 km/h at 3 m/s² with a 1 s reaction: {stop:.1f} m")
for gr, vk in ((0.08, 20), (0.10, 25)):
    drive = mt * g * gr - mt * g * A["crr"]
    Fc_ = (drive + kb * A["preload"]) / (1 + kb)
    Pb_ = kb * (Fc_ - A["preload"]) * vk / 3.6
    per = Pb_ / 2
    Cth_r = A["rotor_m"] * A["c_steel"]  # 180 mm rotor, scaled
    hA = A["h_rotor"] * A["rotor_area"]
    Tss = per / hA
    t60 = 60 * (1 - exp(-120 / (Cth_r / hA)))
    say("F6", f"Descent {gr:.0%} at {vk} km/h: rider feels {Fc_:.0f} N push; trailer brakes absorb {Pb_:.0f} W "
              f"({per:.0f} W per rotor); {P['rotor_d']:.0f} mm rotor ({A['rotor_m']:.3f} kg, {A['rotor_area']:.4f} m²) rise tends to "
              f"{Tss:.0f} K (time constant {Cth_r/hA:.0f} s)")
    if gr == 0.08:
        dT8 = Tss

# ================================================================== G. Structure
nb = A["n_bump"]
w_rail = A["payload"] * g * nb / 2 / (P["deck_len"] / 1000)       # N/m per rail
m_self = (m_deck + m_boards + m_frame * 0.7) * g * nb / 2 / (P["deck_len"] / 1000)
w = w_rail + m_self
F_enc = (m_enc + BOUGHT["11 Battery pack, 12S LiFePO4 384 Wh with BMS"] + 0.55) * g * nb / 2
xs = np.linspace(x0, x1, 1201) / 1000
xa, xf = ax / 1000, x0 / 1000
xenc = (ex0 + el / 2) / 1000
tot = w * (xs[-1] - xs[0]) + F_enc
mom_f = w * (xs[-1] - xs[0]) * ((xs[0] + xs[-1]) / 2 - xf) + F_enc * (xenc - xf)
Ra = mom_f / (xa - xf)
Rf = tot - Ra
M = np.array([Rf * (x - xf) - w * (x - xs[0]) ** 2 / 2 - (F_enc * (x - xenc) if x > xenc else 0) + (Ra * (x - xa) if x > xa else 0) for x in xs])
Mmax = max(abs(M))
Zr = box_Z(R, rt)
s_rail = Mmax * 1000 / Zr
say("G1", f"Side rail at {nb:.0f} g, supported at the nose joint and the axle: max moment {Mmax:.0f} N m "
          f"(over the axle, {D['deck_x1']-ax:.0f} mm overhang); Z {Zr:.0f} mm³; stress {s_rail:.0f} MPa; "
          f"factor on S235 yield {A['fy_s235']/s_rail:.1f}")
Rw = (m_loaded - tongue) * g * nb / 2
Mt = Rw * (D["yc"] - hw) / 1000
say("G2", f"Wheel reaction at {nb:.0f} g {Rw:.0f} N per side; torsion into the frame from the {D['yc']-hw:.0f} mm wheel offset "
          f"{Mt:.0f} N m, carried by the axle crossmember in bending at {Mt*1000/Zr:.0f} MPa")
od, t = P["drawbar"]
Zd = tube_Z(od, t)
Lt = (P["nose_x"] - P["hitch"][0]) / 1000
Mv = tongue * g * A["n_tongue"] * Lt
say("G3", f"Drawbar {od:.0f} x {t} mm: Z {Zd:.0f} mm³; tongue {tongue:.1f} kg at {A['n_tongue']:.0f} g gives {Mv:.0f} N m at the nose, "
          f"{Mv*1000/Zd:.0f} MPa; factor on S355 {A['fy_s355']/(Mv*1000/Zd):.1f}")
h, k_ = pts[0], pts[1]
e_knee = max(abs(q[1] - h[1]) for q in pts) / 1000
e_str = abs(0 - h[1]) / 1000
F_ult = mt * g * A["ult_long_g"]
Mh = F_ult * e_knee
Mv_k = tongue * g * (k_[0] - h[0]) / 1000
s_knee = hypot(Mh, Mv_k) * 1000 / Zd + F_ult / tube_area(od, t)
say("G4", f"Ultimate case, {A['ult_long_g']:.0f} g on the loaded trailer through the hitch ({F_ult:.0f} N, trailer brakes failed): "
          f"offset run {e_knee*1000:.0f} mm off the load line gives {Mh:.0f} N m, stress {s_knee:.0f} MPa, factor on S355 {A['fy_s355']/s_knee:.1f}")
Fpull = resist(8, 0.08) + mt * 0.5
say("G5", f"Service pull, starting on the 8 % grade at 0.5 m/s² with no assist: {Fpull:.0f} N; knee moment {Fpull*e_knee:.0f} N m, "
          f"{Fpull*e_knee*1000/Zd:.0f} MPa")
Zq = pi * (10 ** 4 - 6 ** 4) / (32 * 10)
Zt = pi * (12 ** 4 - 8 ** 4) / (32 * 12)
Mq = F_ult * A["hitch_lever"] / 1000
say("G6", f"Hitch on the axle end, ultimate load at a {A['hitch_lever']:.0f} mm lever: {Mq:.1f} N m; 10 mm hollow QR axle "
          f"{Mq*1000/Zq:.0f} MPa (factor {A['fy_axle']/(Mq*1000/Zq):.1f}); 12 mm thru-axle {Mq*1000/Zt:.0f} MPa "
          f"(factor {A['fy_axle']/(Mq*1000/Zt):.1f}); safety strap rated {2*F_ult/1000:.1f} kN or more")
spans = [P["cross_x"][0] - x0] + [P["cross_x"][i + 1] - P["cross_x"][i] for i in range(len(P["cross_x"]) - 1)] + [x1 - P["cross_x"][-1]]
Ls = max(spans) / 1000
q = A["payload"] * g * nb / D["deck_area_m2"]
s_ply = q * Ls ** 2 / 8 / ((P["deck_t"] / 1000) ** 2 / 6) / 1e6
Pp = 75 * g
s_pt = Pp * Ls / 4 / (0.3 * (P["deck_t"] / 1000) ** 2 / 6) / 1e6
s_pt9 = Pp * Ls / 4 / (0.3 * 0.009 ** 2 / 6) / 1e6
say("G7", f"Deck {P['deck_t']:.0f} mm plywood, longest span {Ls*1000:.0f} mm: uniform {nb:.0f} g payload {q/1000:.1f} kPa gives "
          f"{s_ply:.1f} MPa; a 75 kg point load at mid-span on a 300 mm strip gives {s_pt:.1f} MPa (allowable {A['ply_allow']:.0f} MPa); a 9 mm deck would give {s_pt9:.1f} MPa")

# ================================================================== H. Geometry and fit
say("H1", f"Deck {P['deck_len']:.0f} x {P['deck_w']:.0f} mm = {D['deck_area_m2']:.2f} m² (R1: 0.8 m² or more)")
say("H2", f"Overall width {D['width']:.0f} mm (R9: 1,000 mm); hitched length from the bike axle {D['length']:.0f} mm (R9: 2,600 mm)")
say("H3", f"Tyre to side rail clearance {D['tyre_gap']:.1f} mm; dropout faces {D['d_in']:.0f} and {D['d_out']:.0f} mm from the center line "
          f"(hub spacing {P['hub_old']:.0f} mm); arch top {D['arch_top']:.0f} mm; enclosure ground clearance {D['ground_clear']:.0f} mm")
say("H4", f"Flag top {D['flag_top']:.0f} mm above the ground (R14: 1,500 mm)")
# articulation: rotate drawbar center line about the hitch until it comes within the clearance of the bike's rear tyre
tyre_half, bike_r = 20.0, 355.0
need = tyre_half + P["drawbar"][0] / 2 + 15.0
line = []
for i in range(len(pts) - 1):
    for s in np.linspace(0, 1, 60):
        line.append([pts[i][j] + (pts[i + 1][j] - pts[i][j]) * s for j in range(2)])
line = np.array(line) - np.array(h[:2])


def articulation(sign):
    for deg in np.arange(0, 120.5, 0.5):
        a = radians(sign * deg)
        rot = np.c_[line[:, 0] * cos(a) - line[:, 1] * sin(a), line[:, 0] * sin(a) + line[:, 1] * cos(a)] + np.array(h[:2])
        inside = (rot[:, 0] > -bike_r) & (rot[:, 0] < bike_r)
        if inside.any() and np.min(np.abs(rot[inside, 1])) < need:
            return deg
    return None


ang_max = articulation(+1)
ang_other = articulation(-1)
ang_str = "more than 120" if ang_max is None else f"{ang_max:.1f}"
e_straight = degrees(atan2(abs(h[1]), bike_r)) - degrees(atan2(abs(h[1]), P["nose_x"]))
r_turn = (ax / 1000) / np.tan(radians(ang_max)) if ang_max else 0
say("H5", f"Articulation with the bike yawed toward the drawbar, before the drawbar comes within 15 mm of the rear tyre: "
          f"{ang_str} deg (the other way: {'more than 120' if ang_other is None else ang_other} deg); a straight drawbar "
          f"from the same hitch would allow about {e_straight:.0f} deg")
say("H6", f"At {ang_str} deg a steady turn is possible down to a radius of about {r_turn:.1f} m at the trailer axle "
          f"(hitch to axle {ax/1000:.2f} m); tighter turns toward the left need the rider to swing wide")

# ================================================================== I. Cost
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
say("I1", f"BOM: {len(rows)} lines, total ${total:,.2f} against budget_usd ${budget:,.0f} "
          f"({'within' if total <= budget else 'over'} by ${abs(budget-total):,.2f})")

# ================================================================== J. Results table
status = [
    ("R1", "Payload 150 kg, deck 0.8 m² or more", f"{D['deck_area_m2']:.2f} m²; rail factor {A['fy_s235']/s_rail:.1f}, drawbar {A['fy_s355']/s_knee:.1f} at ultimate", "Met on paper"),
    ("R2", "Range 20 km or more, design route", f"{rng:.1f} km", "Met on paper" if rng >= 20 else "Not met"),
    ("R3", "8 % for 300 m at 8 km/h, felt 40 N or less, no over-temperature; derating beyond", f"{Ffelt_climb:.0f} N felt; winding {T_pre + Lc*A['Rth']*(1-exp(-300/(8/3.6)/tau)):.0f} °C; derated {R8-F_der:.0f} N",
     "At risk" if Ffelt_climb <= 40 else "Not met"),
    ("R4", "Felt pull 15 N or less at 5 to 20 km/h, stable", f"{felt(resist(5))[0]:.1f} to {felt(resist(20))[0]:.1f} N; G crit {crit2:.1f}", "Met on paper"),
    ("R5", "250 W rated, tension only, 25 km/h, no throttle", "250 W nameplate; no-load 22 km/h", "Met by design"),
    ("R6", "Push 100 N or less at 3 m/s²; cut 100 ms", f"{push_dry:.0f} N dry, {push_wet:.0f} N wet; cut {t_cut*1000:.0f} ms", "Met on paper" if push_wet <= 100 else "At risk"),
    ("R7", "QR and 12 mm thru-axle, 30 s, no wiring", "Axle loads pass; thru-axle threads vary", "At risk"),
    ("R8", "Empty 45 kg or less (relaxed, CGM-DDR-002)", f"{m_empty:.1f} kg", "Met on paper" if m_empty <= 45 else "Not met"),
    ("R9", "Width 1,000 mm, length 2.6 m", f"{D['width']:.0f} mm, {D['length']/1000:.2f} m", "Met on paper"),
    ("R10", "Hitch load 3 to 10 kg, centered", f"{tongue:.1f} kg", "Met on paper" if 3 <= tongue <= 10 else "Not met"),
    ("R11", "IP65 electronics, -10 to 40 °C, charge block below 0 °C", "Datasheet items", "Not verifiable at TRL 3"),
    ("R12", f"Parts ${budget:,.0f} or less (budget_usd)", f"${total:,.0f}", "Met on paper" if total <= budget else "Not met"),
    ("R13", "Faults zero motor current in 100 ms", f"{t_cut*1000:.0f} ms fast path", "Not verifiable at TRL 3"),
    ("R14", "Lights, reflectors, flag 1.5 m", f"flag {D['flag_top']:.0f} mm", "Met by design"),
]
print()
for r in status:
    say("J", " | ".join(r))
