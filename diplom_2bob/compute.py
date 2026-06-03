# -*- coding: utf-8 -*-
"""
II BOB. HISOBIY QISM — barcha hisob-kitoblar va grafiklar.
Sulfat-ammoniy ishlab chiqarish (saturator) jarayonini boshqarish tizimi.
Hech qanday tashqi paket ishlatilmaydi (faqat math + plotlib).
"""
import math
import json
from plotlib import Plot, Canvas, text_width

MEDIA = "media"

# Ranglar
RED = (200, 30, 30)
BLUE = (30, 70, 200)
GREEN = (20, 140, 60)
ORANGE = (220, 130, 0)
PURPLE = (150, 40, 160)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)

# ===========================================================================
# 1. OB'EKT MODELI PARAMETRLARI (eksperimental razgon egri chizig'idan)
# ===========================================================================
# Boshqariluvchi kattalik y  — saturatordagi ona eritmaning kislotaliligi
#   (erkin H2SO4 konsentratsiyasi), o'lchov shkalasining % da.
# Rostlovchi ta'sir mu — sulfat kislota sarfini rostlovchi klapan holati, %.

K_ob = 1.6     # ob'ekt kuchaytirish koeff., %/%
T_ob = 320.0   # ob'ekt vaqt doimiysi, s
tau = 45.0     # transport (sof) kechikish, s

# Ijro mexanizmi (rostlovchi klapan + ijro mexanizmi)
K_im = 1.0
T_im = 12.0    # s

# O'lchov (datchik-uzatgich)
K_d = 1.0
T_d = 13.0     # s

# Plantning to'liq kuchaytirishi (regulyatorsiz)
K0 = K_ob * K_im * K_d            # = 1.6
# Plant: W0(s) = K0 * e^{-tau s} / [(T_ob s+1)(T_im s+1)(T_d s+1)]
T_list = [T_ob, T_im, T_d]


def plant_freq(w):
    """Plant W0(jw) ni qaytaradi (regulyatorsiz, kechikish bilan). (re, im)."""
    mag = K0
    ph = -w * tau
    for T in T_list:
        mag /= math.sqrt(1.0 + (w * T) ** 2)
        ph += -math.atan(w * T)
    return mag * math.cos(ph), mag * math.sin(ph), mag, ph


def pi_freq(w, Kp, Ti):
    """PI-regulyator W_p(jw)."""
    re = Kp
    im = -Kp / (w * Ti)
    mag = math.hypot(re, im)
    ph = math.atan2(im, re)
    return re, im, mag, ph


def open_loop(w, Kp, Ti):
    """Ochiq kontur L(jw) = W_p * W0."""
    pr, pi_, pm, pph = plant_freq(w)
    rr, ri, rm, rph = pi_freq(w, Kp, Ti)
    mag = pm * rm
    ph = pph + rph
    return mag * math.cos(ph), mag * math.sin(ph), mag, ph


# ===========================================================================
# 2. ZIEGLER–NICHOLS (chegaraviy kuchaytirish usuli) — plant bo'yicha
# ===========================================================================
def find_phase_cross_plant():
    """Plant fazasi -180 grad bo'ladigan chastota (wu) va |W0(jwu)|."""
    lo, hi = 1e-4, 1.0
    target = -math.pi
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        _, _, _, ph = plant_freq(mid)
        if ph > target:   # faza yetarlicha manfiy emas -> chastotani oshiramiz
            lo = mid
        else:
            hi = mid
    wu = math.sqrt(lo * hi)
    _, _, mag, _ = plant_freq(wu)
    return wu, mag


wu, mag_u = find_phase_cross_plant()
Ku = 1.0 / mag_u                 # chegaraviy (kritik) kuchaytirish
Pu = 2 * math.pi / wu            # chegaraviy tebranish davri, s

# Ziegler–Nichols PI sozlamalari
Kp_zn = 0.45 * Ku
Ti_zn = Pu / 1.2


# ===========================================================================
# 3. PI ni faza zapasi ~45 grad bo'lishi uchun aniqlashtirish
# ===========================================================================
def gain_crossover(Kp, Ti):
    """|L(jw)|=1 bo'ladigan wc va o'sha yerdagi faza (grad)."""
    lo, hi = 1e-4, 1.0
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        _, _, mag, _ = open_loop(mid, Kp, Ti)
        if mag > 1.0:
            lo = mid
        else:
            hi = mid
    wc = math.sqrt(lo * hi)
    _, _, _, ph = open_loop(wc, Kp, Ti)
    pm = 180.0 + math.degrees(ph)
    return wc, pm


# Ti ni Ziegler-Nichols dan olamiz, Kp ni faza zapasi 45 grad ga sozlaymiz
Ti = Ti_zn
target_pm = 45.0
lo, hi = 0.05, Kp_zn * 2
for _ in range(120):
    mid = 0.5 * (lo + hi)
    wc, pm = gain_crossover(mid, Ti)
    if pm > target_pm:     # zapas katta -> Kp ni oshirsa bo'ladi
        lo = mid
    else:
        hi = mid
Kp = 0.5 * (lo + hi)
wc, PM = gain_crossover(Kp, Ti)


# ===========================================================================
# 4. OCHIQ KONTUR ZAPASLARI (amplituda va faza zapasi)
# ===========================================================================
def find_phase_cross_open(Kp, Ti):
    """L(jw) fazasi -180 grad: w_pi va |L|."""
    lo, hi = 1e-4, 1.0
    target = -math.pi
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        _, _, _, ph = open_loop(mid, Kp, Ti)
        if ph > target:
            lo = mid
        else:
            hi = mid
    w_pi = math.sqrt(lo * hi)
    _, _, mag, _ = open_loop(w_pi, Kp, Ti)
    return w_pi, mag


w_pi, mag_at_pi = find_phase_cross_open(Kp, Ti)
GM = 1.0 / mag_at_pi                 # amplituda zapasi (martalab)
GM_dB = 20 * math.log10(GM)


# ===========================================================================
# 5. YOPIQ KONTUR O'TISH JARAYONI (vaqt sohasida simulyatsiya)
# ===========================================================================
def simulate_closed(Kp, Ti, Tend=2500.0, dt=0.25, setpoint=1.0):
    n = int(Tend / dt)
    ndelay = int(round(tau / dt))
    ubuf = [0.0] * (ndelay + 1)
    x1 = x2 = x3 = 0.0      # uchta apdoq (T_ob, T_im, T_d)
    I = 0.0
    e_prev = 0.0
    ts, ys, us = [], [], []
    for k in range(n + 1):
        t = k * dt
        y = K_d * x3 if False else x3   # chiqish (datchik chiqishi ham y ga normalangan)
        e = setpoint - y
        I += e * dt
        u = Kp * (e + I / Ti)
        # kechikish buferi
        ubuf.append(u)
        u_del = ubuf[-(ndelay + 1)]
        # plant: u_del -> [K_ob/(T_ob s+1)] -> [K_im/(T_im s+1)] -> [K_d/(T_d s+1)]
        dx1 = (K_ob * u_del - x1) / T_ob
        dx2 = (K_im * x1 - x2) / T_im
        dx3 = (K_d * x2 - x3) / T_d
        x1 += dx1 * dt
        x2 += dx2 * dt
        x3 += dx3 * dt
        ts.append(t); ys.append(y); us.append(u)
        e_prev = e
        if len(ubuf) > 4 * (ndelay + 1):
            ubuf = ubuf[-(ndelay + 1):]
    return ts, ys, us


ts, ys, us = simulate_closed(Kp, Ti)
y_ss = ys[-1]
y_max = max(ys)
t_max = ts[ys.index(y_max)]
overshoot = (y_max - y_ss) / y_ss * 100.0

# O'rnatilish vaqti (5% koridor)
band = 0.05 * y_ss
t_set = ts[-1]
for i in range(len(ys) - 1, -1, -1):
    if abs(ys[i] - y_ss) > band:
        t_set = ts[i + 1] if i + 1 < len(ts) else ts[i]
        break

# Ko'tarilish vaqti (0 -> birinchi marta y_ss ga yetishi)
t_rise = ts[-1]
for i in range(len(ys)):
    if ys[i] >= y_ss:
        t_rise = ts[i]
        break

# So'ngmaslik (zatuxaniya) darajasi psi = 1 - A2/A1 (ketma-ket maksimumlar)
peaks = []
for i in range(1, len(ys) - 1):
    if ys[i] > ys[i - 1] and ys[i] >= ys[i + 1] and ys[i] > y_ss:
        peaks.append((ts[i], ys[i]))
psi = None
if len(peaks) >= 2:
    A1 = peaks[0][1] - y_ss
    A2 = peaks[1][1] - y_ss
    if A1 > 1e-9:
        psi = 1.0 - A2 / A1

# Ob'ektning razgon egri chizig'i (regulyatorsiz, ochiq kontur step)
def simulate_object(Tend=2000.0, dt=0.25, step=1.0):
    n = int(Tend / dt)
    ndelay = int(round(tau / dt))
    ubuf = [0.0] * (ndelay + 1)
    x1 = x2 = x3 = 0.0
    ts, ys = [], []
    for k in range(n + 1):
        t = k * dt
        ubuf.append(step)
        u_del = ubuf[-(ndelay + 1)]
        dx1 = (K_ob * u_del - x1) / T_ob
        dx2 = (K_im * x1 - x2) / T_im
        dx3 = (K_d * x2 - x3) / T_d
        x1 += dx1 * dt; x2 += dx2 * dt; x3 += dx3 * dt
        ts.append(t); ys.append(x3)
        if len(ubuf) > 4 * (ndelay + 1):
            ubuf = ubuf[-(ndelay + 1):]
    return ts, ys


tso, yso = simulate_object()
y_ob_ss = yso[-1]


# ===========================================================================
# NATIJALARNI CHOP ETISH VA SAQLASH
# ===========================================================================
R = {
    "K_ob": K_ob, "T_ob": T_ob, "tau": tau,
    "K_im": K_im, "T_im": T_im, "K_d": K_d, "T_d": T_d, "K0": K0,
    "wu": wu, "Ku": Ku, "Pu": Pu,
    "Kp_zn": Kp_zn, "Ti_zn": Ti_zn,
    "Kp": Kp, "Ti": Ti,
    "wc": wc, "PM": PM,
    "w_pi": w_pi, "GM": GM, "GM_dB": GM_dB,
    "y_ss": y_ss, "y_max": y_max, "t_max": t_max,
    "overshoot": overshoot, "t_set": t_set, "t_rise": t_rise,
    "psi": psi, "y_ob_ss": y_ob_ss, "n_peaks": len(peaks),
}
with open("results.json", "w") as f:
    json.dump(R, f, indent=2)

print("=== OB'EKT ===")
print(f"K_ob={K_ob}  T_ob={T_ob}s  tau={tau}s")
print(f"T_im={T_im}s  T_d={T_d}s  K0={K0}")
print("=== ZIEGLER-NICHOLS ===")
print(f"wu={wu:.5f} rad/s  Ku={Ku:.3f}  Pu={Pu:.1f} s")
print(f"Kp_zn={Kp_zn:.3f}  Ti_zn={Ti_zn:.1f} s")
print("=== AKHIRGI PI ===")
print(f"Kp={Kp:.3f}  Ti={Ti:.1f} s")
print("=== ZAPASLAR ===")
print(f"wc={wc:.5f} rad/s  PM={PM:.1f} grad")
print(f"w_pi={w_pi:.5f} rad/s  GM={GM:.2f} ({GM_dB:.1f} dB)")
print("=== SIFAT ===")
print(f"y_ss={y_ss:.4f}  y_max={y_max:.4f}  t_max={t_max:.0f}s")
print(f"overshoot={overshoot:.1f}%  t_set(5%)={t_set:.0f}s  t_rise={t_rise:.0f}s")
print(f"psi={psi}  n_peaks={len(peaks)}")
print(f"object y_ss={y_ob_ss:.4f}")

# ===========================================================================
# Grafiklar foydalanuvchi talabiga ko'ra YARATILMAYDI (faqat sonli natijalar).
# ===========================================================================

# ---------------------------------------------------------------------------
# JADVALLAR UCHUN MA'LUMOTLAR
# ---------------------------------------------------------------------------
# 2.2.1-jadval: ob'ekt razgon egri chizig'i (tanlangan nuqtalar)
obj_table = []
sample_t = [0, 45, 100, 200, 300, 400, 600, 900, 1200, 1600, 2000]
for tq in sample_t:
    idx = min(range(len(tso)), key=lambda i: abs(tso[i] - tq))
    obj_table.append((tso[idx], yso[idx]))

# 2.2.2-jadval: ochiq kontur chastotaviy xarakteristikasi
freq_table = []
freq_points = [0.001, 0.002, 0.005, wc, 0.01, w_pi, 0.03, 0.05, 0.1]
freq_points = sorted(set(round(f, 6) for f in freq_points))
for w in freq_points:
    _, _, mag, ph = open_loop(w, Kp, Ti)
    L_db = 20 * math.log10(mag)
    phi_deg = math.degrees(ph)
    freq_table.append((w, mag, L_db, phi_deg))

# 2.3.1-jadval: yopiq kontur o'tish jarayoni (tanlangan nuqtalar)
closed_table = []
sample_tc = [0, 100, 188, 283, 400, 452, 600, 800, 1000, 1500, 2000]
for tq in sample_tc:
    idx = min(range(len(ts)), key=lambda i: abs(ts[i] - tq))
    closed_table.append((ts[idx], ys[idx]))

# ---------------------------------------------------------------------------
# ROUTH–HURWITZ: kechikishni Pade(1,1) bilan approksimatsiya qilib tahlil
#   e^{-tau s} ~ (1 - tau/2 s) / (1 + tau/2 s)
# Yopiq kontur xarakteristik tenglamasi tuziladi.
# ---------------------------------------------------------------------------
def poly_mul(a, b):
    r = [0.0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            r[i + j] += ai * bj
    return r


def poly_add(a, b):
    n = max(len(a), len(b))
    a = [0.0] * (n - len(a)) + a
    b = [0.0] * (n - len(b)) + b
    return [x + y for x, y in zip(a, b)]


# Polinomlar [eng yuqori daraja ... ozod had] ko'rinishida.
# Plant maxraji: (T_ob s+1)(T_im s+1)(T_d s+1)
den = [1.0]
for T in T_list:
    den = poly_mul(den, [T, 1.0])
# Pade maxraji (1 + tau/2 s) ni qo'shamiz
pade_den = [tau / 2.0, 1.0]
pade_num = [-tau / 2.0, 1.0]
# To'liq ochiq kontur: L(s) = Kp (Ti s + 1)/(Ti s) * K0 * pade_num / [den * pade_den]
# Xarakteristik tenglama: Ti s * den * pade_den + Kp (Ti s + 1) K0 pade_num = 0
left = poly_mul([Ti, 0.0], poly_mul(den, pade_den))          # Ti s * den * pade_den
right = poly_mul([Kp * K0], poly_mul([Ti, 1.0], pade_num))   # Kp K0 (Ti s+1) pade_num
char_poly = poly_add(left, right)

# Routh massivi
def routh_array(coeffs):
    n = len(coeffs)
    rows = n
    cols = (n + 1) // 2
    M = [[0.0] * cols for _ in range(rows)]
    for i in range(cols):
        if 2 * i < n:
            M[0][i] = coeffs[2 * i]
        if 2 * i + 1 < n:
            M[1][i] = coeffs[2 * i + 1]
    for r in range(2, rows):
        for c in range(cols - 1):
            a = M[r - 2][0]
            b = M[r - 1][0]
            if b == 0:
                b = 1e-12
            M[r][c] = (b * M[r - 2][c + 1] - a * M[r - 1][c + 1]) / b
    return M


routh = routh_array(char_poly)
first_col = [row[0] for row in routh]
sign_changes = sum(1 for i in range(len(first_col) - 1)
                   if first_col[i] * first_col[i + 1] < 0)
stable = (sign_changes == 0)

R["obj_table"] = obj_table
R["freq_table"] = freq_table
R["closed_table"] = closed_table
R["char_poly"] = char_poly
R["routh_first_col"] = first_col
R["sign_changes"] = sign_changes
R["stable"] = stable
with open("results.json", "w") as f:
    json.dump(R, f, indent=2)

print("\n=== ROUTH-HURWITZ (Pade(1,1)) ===")
print("Char. polinom koeff.:", [round(c, 4) for c in char_poly])
print("Routh 1-ustun:", [round(c, 5) for c in first_col])
print("Ishora o'zgarishlari:", sign_changes, " => turg'un:", stable)
print("\nNatijalar results.json fayliga saqlandi (grafiksiz).")
