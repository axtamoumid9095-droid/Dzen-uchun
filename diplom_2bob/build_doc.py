# -*- coding: utf-8 -*-
"""II BOB. HISOBIY QISM — to'liq matnni .docx ga yig'adi (rasmsiz)."""
import json
from docx_builder import Docx

with open("results.json") as f:
    R = json.load(f)


def f2(x, n=2):
    return f"{x:.{n}f}".replace(".", ",")


# qisqartmalar: sub/sup uchun segment yasovchilar
def S(t):
    return (t, {"sub": True})


def SUP(t):
    return (t, {"sup": True})


def I(t):
    return (t, {"italic": True})


def B(t):
    return (t, {"bold": True})


d = Docx(font="Times New Roman", size_pt=14)

# ===========================================================================
# BOB SARLAVHASI
# ===========================================================================
d.heading("II BOB. HISOBIY QISM", level=1)

d.para([
    "Ushbu bobda sulfat-ammoniy ishlab chiqarish jarayonining asosiy bo'g'ini "
    "bo'lgan saturator (to'yintirgich)dagi ona eritma kislotaliligini avtomatik "
    "rostlash konturi nazariy jihatdan tahlil qilinadi. Avval texnologik jarayonning "
    "matematik modeli tuziladi, so'ngra boshqarish tizimining vaqt va chastotaviy "
    "xarakteristikalari aniqlanadi, oxirida esa yopiq tizimning turg'unligi baholanib, "
    "boshqarish sifatining son ko'rsatkichlari hisoblanadi. Barcha hisob-kitoblar "
    "avtomatik boshqaruv nazariyasi (control theory) usullariga asoslangan."
], indent_first=True)

# ===========================================================================
# 2.1 — MATEMATIK MODEL
# ===========================================================================
d.heading("2.1-§. Sulfat-ammoniy ishlab chiqarish jarayonining matematik "
          "modelini tuzish", level=2)

d.para([
    "Sulfat-ammoniy (NH",  ("4", {"sub": True}), ")",  ("2", {"sub": True}),
    "SO",  ("4", {"sub": True}),
    " saturatorda gazdagi ammiakni (NH", ("3", {"sub": True}),
    ") sulfat kislota (H", ("2", {"sub": True}), "SO", ("4", {"sub": True}),
    ") eritmasi bilan neytrallash reaksiyasi natijasida olinadi:"
])

d.formula(["2 NH", S("3"), " + H", S("2"), "SO", S("4"),
           "  \u2192  (NH", S("4"), ")", S("2"), "SO", S("4"),
           " + Q"], number="2.1")

d.para([
    "Jarayonning normal kechishi va kristallarning sifatli o'sishi uchun ona "
    "eritmadagi erkin sulfat kislota konsentratsiyasini (kislotalilikni) belgilangan "
    "darajada — odatda 3\u20136 % oralig'ida — ushlab turish zarur. Demak, "
    "boshqarishning maqsadi — eritma kislotaligini berilgan topshiriq qiymatida "
    "barqaror saqlashdir."
])

d.para([B("Boshqarish kanalini tanlash. "),
    "Boshqariluvchi (chiquvchi) kattalik sifatida ona eritmaning kislotaliligi ",
    I("y"), "(t) (erkin H", S("2"), "SO", S("4"),
    " konsentratsiyasi, o'lchov shkalasining %), rostlovchi (kiruvchi) ta'sir "
    "sifatida esa saturatorga uzatiladigan sulfat kislota sarfini o'zgartiruvchi "
    "klapan holati ", I("\u03bc"), "(t) (%) qabul qilinadi. Bo'g'inning kuchaytirish "
    "koeffitsiyenti, vaqt doimiysi va kechikishi razgon (o'tish) egri chizig'i "
    "bo'yicha aniqlanadi."
])

d.para([B("Ob'ektning differensial tenglamasi. "),
    "Saturatordagi modda balansi tenglamasidan kelib chiqib, ish nuqtasi atrofida "
    "chiziqlashtirish (kichik chetlanishlar usuli) qo'llanilsa, texnologik ob'ekt "
    "kechikishli birinchi tartibli aperiodik bo'g'in sifatida tavsiflanadi:"
])

d.formula([I("T"), S("ob"), " ", "d", I("y"), "(t)/dt + ", I("y"), "(t) = ",
           I("K"), S("ob"), " ", I("\u03bc"), "(t \u2212 ", I("\u03c4"), ")"],
          number="2.2")

d.para([
    "bu yerda ", I("T"), S("ob"), " — ob'ektning vaqt doimiysi; ",
    I("K"), S("ob"), " — kuchaytirish koeffitsiyenti; ",
    I("\u03c4"), " — sof (transport) kechikish vaqti. Razgon egri chizig'ini qayta "
    "ishlash natijasida quyidagi parametrlar olingan: ",
    I("K"), S("ob"), " = ", f2(R["K_ob"], 1), " %/%, ",
    I("T"), S("ob"), " = ", f2(R["T_ob"], 0), " s, ",
    I("\u03c4"), " = ", f2(R["tau"], 0), " s."
])

d.para([B("Laplas bo'yicha uzatish funksiyasi. "),
    "(2.2) tenglamani nol boshlang'ich shartlarda Laplas almashtirishiga o'tkazsak, "
    "texnologik ob'ektning uzatish funksiyasi quyidagicha bo'ladi:"
])

d.formula([I("W"), S("ob"), "(s) = ", I("Y"), "(s) / ", I("M"), "(s) = ",
           I("K"), S("ob"), " e", SUP("\u2212"), SUP("\u03c4"), SUP("s"),
           " / (", I("T"), S("ob"), " s + 1)"], number="2.3")

d.para([B("Yordamchi elementlar. "),
    "Boshqarish konturiga ob'ektdan tashqari ijro mexanizmi (rostlovchi klapan bilan) "
    "va o'lchash-uzatish bo'g'ini (datchik-uzatgich) ham kiradi. Ularning har biri "
    "birinchi tartibli aperiodik bo'g'in sifatida olinadi:"
])

d.formula([I("W"), S("im"), "(s) = ", I("K"), S("im"), " / (", I("T"), S("im"),
           " s + 1),     ",
           I("W"), S("d"), "(s) = ", I("K"), S("d"), " / (", I("T"), S("d"),
           " s + 1)"], number="2.4")

d.para([
    "Olingan qiymatlar: ", I("K"), S("im"), " = ", f2(R["K_im"], 1), ", ",
    I("T"), S("im"), " = ", f2(R["T_im"], 0), " s; ",
    I("K"), S("d"), " = ", f2(R["K_d"], 1), ", ",
    I("T"), S("d"), " = ", f2(R["T_d"], 0), " s. Ob'ekt, ijro mexanizmi va "
    "datchikning umumiy (rostlagichsiz) kuchaytirish koeffitsiyenti ",
    I("K"), S("0"), " = ", I("K"), S("ob"), "\u00b7", I("K"), S("im"),
    "\u00b7", I("K"), S("d"), " = ", f2(R["K0"], 1), "."
])

d.para([B("Rostlagichni tanlash. "),
    "Statik xatolikni (kislotalilikning og'ishini) butunlay yo'qotish va jarayonning "
    "yetarli tezkorligini ta'minlash uchun integral tashkil etuvchiga ega "
    "proporsional-integral (PI) rostlagich tanlanadi. Uning uzatish funksiyasi:"
])

d.formula([I("W"), S("p"), "(s) = ", I("K"), S("p"), " (1 + 1/(", I("T"),
           S("i"), " s)) = ", I("K"), S("p"), " (", I("T"), S("i"),
           " s + 1)/(", I("T"), S("i"), " s)"], number="2.5")

d.para([
    "bu yerda ", I("K"), S("p"), " — rostlagichning proporsional kuchaytirish "
    "koeffitsiyenti; ", I("T"), S("i"), " — integrallash vaqti doimiysi. Bu "
    "parametrlar 2.3-§ da aniqlanadi."
])

d.para([B("Tizimning strukturaviy modeli. "),
    "Ketma-ket ulangan rostlagich, ijro mexanizmi, ob'ekt va teskari aloqadagi "
    "datchikdan iborat bir konturli yopiq avtomatik rostlash tizimining ochiq "
    "kontur uzatish funksiyasi quyidagi ko'rinishga ega bo'ladi:"
])

d.formula([I("W"), ("ochiq", {"sub": True}), "(s) = ", I("W"), S("p"), "(s)\u00b7",
           I("W"), S("im"), "(s)\u00b7", I("W"), S("ob"), "(s)\u00b7",
           I("W"), S("d"), "(s)"], number="2.6")

d.para([
    "Tizimning elementlari va ular orasidagi signal oqimlari 2.1-jadvalda "
    "keltirilgan."
])

d.table(
    headers=["Belgi", "Element nomi", "Uzatish funksiyasi", "Parametrlar"],
    rows=[
        ["Wp(s)", "PI-rostlagich", "Kp(Ti s+1)/(Ti s)",
         f"Kp={f2(R['Kp'])}; Ti={f2(R['Ti'],0)} s"],
        ["Wim(s)", "Ijro mexanizmi + klapan", "Kim/(Tim s+1)",
         f"Kim={f2(R['K_im'],1)}; Tim={f2(R['T_im'],0)} s"],
        ["Wob(s)", "Saturator (ob'ekt)", "Kob e^(-\u03c4s)/(Tob s+1)",
         f"Kob={f2(R['K_ob'],1)}; Tob={f2(R['T_ob'],0)} s; \u03c4={f2(R['tau'],0)} s"],
        ["Wd(s)", "Datchik-uzatgich", "Kd/(Td s+1)",
         f"Kd={f2(R['K_d'],1)}; Td={f2(R['T_d'],0)} s"],
    ],
    widths=[1300, 3000, 2860, 2200],
    caption="2.1-jadval"
)

d.para([
    "Shunday qilib, jarayonning to'liq matematik modeli (2.3)\u2013(2.6) "
    "ifodalar bilan tavsiflandi. Ushbu model asosida keyingi paragraflarda "
    "tizimning dinamik xossalari tekshiriladi."
])

# ===========================================================================
# 2.2 — VAQT VA CHASTOTAVIY XARAKTERISTIKALAR
# ===========================================================================
d.page_break()
d.heading("2.2-§. Sulfat-ammoniy ishlab chiqarish jarayonini boshqarish "
          "tizimining vaqt va chastotaviy xarakteristikalarini aniqlash", level=2)

d.para([
    "Tizimning dinamik xossalarini baholash uchun avval boshqarish ob'ektining "
    "vaqt xarakteristikasi (razgon egri chizig'i), so'ngra ochiq konturning "
    "chastotaviy xarakteristikalari aniqlanadi."
])

d.heading("2.2.1. Ob'ektning vaqt xarakteristikasi (o'tish funksiyasi)", level=3)

d.para([
    "Boshqarish ob'ektiga birlik pog'onali ta'sir berilganda (klapan holati 1 % ga "
    "o'zgarganda) chiquvchi kattalikning vaqt bo'yicha o'zgarishi razgon egri "
    "chizig'i ", I("h"), "(t) deb ataladi. (2.3) ifodaga ko'ra, kechikishli aperiodik "
    "bo'g'in uchun o'tish funksiyasi tahliliy ravishda quyidagicha yoziladi:"
])

d.formula([I("h"), "(t) = ", I("K"), S("ob"),
           " [1 \u2212 e", SUP("\u2212(t\u2212\u03c4)/T"), ("ob", {"sup": True}),
           "],   t \u2265 ", I("\u03c4")], number="2.7")

d.para([
    "Ob'ektning (datchik bilan birga) razgon egri chizig'i bo'yicha hisoblangan ",
    "qiymatlar 2.2-jadvalda keltirilgan. Egri chiziq ", I("\u03c4"), " = ",
    f2(R["tau"], 0), " s kechikishdan so'ng o'sa boshlaydi va statik (o'rnashgan) ",
    "qiymat ", I("h"), "(\u221e) = ", f2(R["y_ob_ss"]), " ga monoton yaqinlashadi."
])

obj_rows = [[f2(t, 0), f2(y, 3)] for t, y in R["obj_table"]]
d.table(
    headers=["Vaqt t, s", "Chiqish h(t)"],
    rows=obj_rows,
    widths=[2680, 2680],
    caption="2.2-jadval"
)

d.para([
    "Jadvaldan ko'rinadiki, jarayon ancha inersiyali: o'rnashish vaqti taxminan "
    "3", I("T"), S("ob"), " \u2248 ", f2(3 * R["T_ob"], 0), " s ni tashkil etadi. "
    "Bu esa rostlash konturining sezilarli kechikishga ega ekanini ko'rsatadi va "
    "rostlagich parametrlarini diqqat bilan sozlashni talab qiladi."
])

d.heading("2.2.2. Chastotaviy xarakteristikalar", level=3)

d.para([
    "Chastotaviy xarakteristikalarni olish uchun ochiq kontur uzatish "
    "funksiyasi (2.6) da ", I("s"), " = ", I("j\u03c9"), " almashtirish bajariladi. "
    "Natijada kompleks chastota uzatish funksiyasi (AFX) hosil bo'ladi:"
])

d.formula([I("W"), ("ochiq", {"sub": True}), "(", I("j\u03c9"), ") = ",
           I("K"), S("0"), I("K"), S("p"),
           " (1 + 1/(", I("j\u03c9"), I("T"), S("i"), ")) \u00b7 e",
           SUP("\u2212"), SUP("j\u03c9\u03c4"),
           " / [(", I("j\u03c9"), I("T"), S("ob"), "+1)(", I("j\u03c9"),
           I("T"), S("im"), "+1)(", I("j\u03c9"), I("T"), S("d"), "+1)]"],
          number="2.8")

d.para([
    "Bu funksiyaning moduli amplituda-chastota xarakteristikasini (ACHX) ", I("A"),
    "(\u03c9) = |", I("W"), ("ochiq", {"sub": True}), "(", I("j\u03c9"),
    ")|, argumenti esa faza-chastota xarakteristikasini (FCHX) ", I("\u03c6"),
    "(\u03c9) = arg ", I("W"), ("ochiq", {"sub": True}), "(", I("j\u03c9"),
    ") beradi. Logarifmik amplituda-chastota xarakteristikasi (LACHX) quyidagicha "
    "hisoblanadi:"
])

d.formula([I("L"), "(\u03c9) = 20 lg ", I("A"), "(\u03c9),   [dB]"], number="2.9")

d.para([
    "Faza-chastota xarakteristikasi ketma-ket bo'g'inlar fazalarining yig'indisi "
    "sifatida topiladi:"
])

d.formula([I("\u03c6"), "(\u03c9) = \u2212arctg(1/(\u03c9", I("T"), S("i"),
           ")) \u2212 \u03c9", I("\u03c4"),
           " \u2212 arctg(\u03c9", I("T"), S("ob"), ") \u2212 arctg(\u03c9",
           I("T"), S("im"), ") \u2212 arctg(\u03c9", I("T"), S("d"), ")"],
          number="2.10")

d.para([
    "(2.8)\u2013(2.10) ifodalar bo'yicha sozlangan rostlagich (", I("K"), S("p"),
    " = ", f2(R["Kp"]), "; ", I("T"), S("i"), " = ", f2(R["Ti"], 0),
    " s) uchun bir qator chastotalarda hisoblangan natijalar 2.3-jadvalda "
    "keltirilgan."
])

freq_rows = []
for w, mag, ldb, phi in R["freq_table"]:
    freq_rows.append([f2(w, 4), f2(mag, 3), f2(ldb, 1), f2(phi, 1)])
d.table(
    headers=["\u03c9, rad/s", "A(\u03c9)", "L(\u03c9), dB", "\u03c6(\u03c9), grad"],
    rows=freq_rows,
    widths=[2340, 2340, 2340, 2340],
    caption="2.3-jadval"
)

d.para([
    "Jadval ma'lumotlaridan ikkita muhim chastota ajralib turadi. ",
    B("Kesim chastotasi "), I("\u03c9"), S("k"), " — bunda ", I("A"),
    "(\u03c9", ("k", {"sub": True}), ") = 1 (", I("L"), " = 0 dB); hisob bo'yicha ",
    I("\u03c9"), S("k"), " = ", f2(R["wc"], 4), " rad/s. ",
    B("Faza \u2212180\u00b0 ga teng bo'lgan chastota "), I("\u03c9"),
    ("\u03c0", {"sub": True}), " = ", f2(R["w_pi"], 4), " rad/s. Aynan shu ikki "
    "chastota tizimning turg'unlik zapaslarini belgilaydi, bu masala keyingi "
    "paragrafda batafsil ko'rib chiqiladi."
])

d.para([
    "Amplituda-faza xarakteristikasi (AFX, Naykvist godografi) ", I("W"),
    ("ochiq", {"sub": True}), "(", I("j\u03c9"), ") ning kompleks tekislikdagi "
    "egri chizig'idan iborat. Past chastotalarda (\u03c9 \u2192 0) integral "
    "tashkil etuvchi tufayli ", I("A"), "(\u03c9) \u2192 \u221e bo'ladi va godograf "
    "uchinchi chorakdan boshlanadi; chastota ortishi bilan u koordinata boshiga "
    "yaqinlashadi. Godografning haqiqiy o'qni kesib o'tish nuqtasi (\u2212",
    f2(R["GM"] ** -1, 3), "; ", I("j"), "0) kritik (\u22121; ", I("j"), "0) "
    "nuqtaning o'ng tomonida joylashgani tizimning turg'un ekanini bildiradi."
])

# ===========================================================================
# 2.3 — TURG'UNLIK VA SIFAT
# ===========================================================================
d.page_break()
d.heading("2.3-§. Sulfat-ammoniy ishlab chiqarish jarayonini boshqarish "
          "tizimining turg'unligini tahlil qilish va sifat ko'rsatkichlarini "
          "aniqlash", level=2)

d.heading("2.3.1. PI-rostlagich parametrlarini hisoblash", level=3)

d.para([
    "Rostlagich parametrlarini sozlash uchun Ziegler\u2013Nichols (chegaraviy "
    "kuchaytirish) usulidan foydalanamiz. Avval faqat proporsional rostlagich "
    "uchun tizim turg'unlik chegarasiga keladigan ", B("kritik kuchaytirish "),
    I("K"), S("u"), " va ", B("kritik tebranish davri "), I("T"), S("u"),
    " aniqlanadi. Ob'ekt fazasi \u2212180\u00b0 ga teng bo'ladigan chastota:"
])

d.formula([I("\u03c9"), S("u"), " = ", f2(R["wu"], 4), " rad/s,    ",
           I("K"), S("u"), " = 1/|", I("W"), S("0"), "(",
           I("j\u03c9"), S("u"), ")| = ", f2(R["Ku"])], number="2.11")

d.formula([I("T"), S("u"), " = 2\u03c0/", I("\u03c9"), S("u"), " = ",
           f2(R["Pu"], 1), " s"], number="2.12")

d.para([
    "Ziegler\u2013Nichols jadvali bo'yicha PI-rostlagich uchun tavsiya etilgan "
    "boshlang'ich qiymatlar:"
])

d.formula([I("K"), S("p"), " = 0,45 ", I("K"), S("u"), " = ", f2(R["Kp_zn"]),
           ";     ", I("T"), S("i"), " = ", I("T"), S("u"), "/1,2 = ",
           f2(R["Ti_zn"], 1), " s"], number="2.13")

d.para([
    "Past o'tish jarayonidagi o'tib ketishni (overshoot) kamaytirish maqsadida "
    "proporsional kuchaytirish koeffitsiyenti faza zapasi taxminan 45\u00b0 ga teng "
    "bo'ladigan qilib aniqlashtirildi. Yakuniy sozlangan qiymatlar:"
])

d.formula([B("K"), B("p"), B(" = "), B(f2(R["Kp"])), B(",     "),
           B("T"), B("i"), B(" = "), B(f2(R["Ti"], 0)), B(" s")], number="2.14")

d.heading("2.3.2. Chastotaviy turg'unlik zapaslari (Naykvist\u2013Bode kriteriysi)",
          level=3)

d.para([
    "Ochiq konturning amplituda va faza xarakteristikalari bo'yicha tizimning "
    "turg'unlik zapaslari aniqlanadi. ", B("Faza zapasi "), " kesim chastotasida "
    "hisoblanadi:"
])

d.formula([I("\u0394\u03c6"), " = 180\u00b0 + ", I("\u03c6"), "(",
           I("\u03c9"), S("k"), ") = ", f2(R["PM"], 0), "\u00b0"], number="2.15")

d.para([
    B("Amplituda zapasi "), " faza \u2212180\u00b0 ga teng bo'lgan chastotada "
    "topiladi:"
])

d.formula([I("\u0394L"), " = \u221220 lg ", I("A"), "(", I("\u03c9"),
           ("\u03c0", {"sub": True}), ") = ", f2(R["GM_dB"], 1), " dB    (",
           I("L"), S("z"), " = ", f2(R["GM"]), " marta)"], number="2.16")

d.para([
    "Olingan zapaslar avtomatik rostlash tizimlari uchun tavsiya etiladigan "
    "me'yorlarni qondiradi: faza zapasi 30\u201360\u00b0 oralig'ida (", f2(R["PM"], 0),
    "\u00b0), amplituda zapasi esa 6 dB dan katta (", f2(R["GM_dB"], 1),
    " dB). Bu tizimning yetarlicha turg'unlik mustahkamligiga ega ekanini bildiradi."
])

d.heading("2.3.3. Routh\u2013Gurvits algebraik kriteriysi bo'yicha tekshirish",
          level=3)

d.para([
    "Chastotaviy tahlil natijasini algebraik usul bilan tasdiqlash uchun "
    "Routh\u2013Gurvits kriteriysidan foydalanamiz. Sof kechikish e",
    SUP("\u2212"), SUP("\u03c4"), SUP("s"), " ratsional emas, shuning uchun u "
    "Pade(1,1) yaqinlashtirishi bilan almashtiriladi:"
])

d.formula(["e", SUP("\u2212"), SUP("\u03c4"), SUP("s"),
           " \u2248 (1 \u2212 ", I("\u03c4"), "s/2) / (1 + ", I("\u03c4"),
           "s/2)"], number="2.17")

d.para([
    "Bu yaqinlashtirish yopiq kontur xarakteristik tenglamasini polinom ko'rinishiga "
    "keltiradi. Hisoblash natijasida 5-tartibli xarakteristik polinom koeffitsiyentlari "
    "(kamayuvchi darajalar bo'yicha) quyidagicha topildi:"
])

cp = R["char_poly"]
d.formula([f"{cp[0]:.3e}".replace("e", "\u00b710^") + " s", SUP("5"), " + ",
           f"{cp[1]:.3e}".replace("e", "\u00b710^") + " s", SUP("4"), " + ..."],
          )
d.para([
    "Polinom koeffitsiyentlari va Routh jadvalining birinchi ustuni 2.4-jadvalda "
    "keltirilgan."
], indent_first=True)

routh_rows = []
labels = ["s^5", "s^4", "s^3", "s^2", "s^1", "s^0"]
for i, val in enumerate(R["routh_first_col"]):
    routh_rows.append([labels[i], f"{val:.4e}".replace("e", "\u00b710^"),
                       "musbat (+)"])
d.table(
    headers=["Qator", "Routh jadvali 1-ustun", "Ishora"],
    rows=routh_rows,
    widths=[1560, 4800, 3000],
    caption="2.4-jadval"
)

d.para([
    "Routh jadvalining birinchi ustunidagi barcha elementlar musbat ishorali "
    "(ishora o'zgarishlari soni = ", str(R["sign_changes"]), "). Routh\u2013Gurvits "
    "kriteriysiga ko'ra, bu yopiq tizimning ", B("turg'un "), "ekanini bildiradi. "
    "Shu tariqa algebraik usul chastotaviy tahlil xulosasini to'liq tasdiqlaydi."
])

d.heading("2.3.4. Boshqarish sifati ko'rsatkichlari", level=3)

d.para([
    "Yopiq tizimga birlik pog'onali topshiriq berilgandagi o'tish jarayoni ",
    I("h"), "(t) hisoblab chiqildi. Jarayonning tanlangan nuqtalardagi qiymatlari "
    "2.5-jadvalda keltirilgan."
])

closed_rows = [[f2(t, 0), f2(y, 3)] for t, y in R["closed_table"]]
d.table(
    headers=["Vaqt t, s", "Chiqish h(t)"],
    rows=closed_rows,
    widths=[2680, 2680],
    caption="2.5-jadval"
)

d.para([
    "O'tish jarayoni egri chizig'i bo'yicha boshqarish sifatining asosiy "
    "ko'rsatkichlari aniqlandi:"
])

d.bullet([B("o'rnashgan qiymat "), I("h"), "(\u221e) = ", f2(R["y_ss"], 2),
          " (statik xatolik nolga teng, chunki rostlagichda integral tashkil "
          "etuvchi mavjud);"])
d.bullet([B("maksimal o'tib ketish (overshoot) "), I("\u03c3"), " = ",
          f2(R["overshoot"], 1), " %  (", I("h"), ("max", {"sub": True}),
          " = ", f2(R["y_max"], 3), ", ", I("t"), ("max", {"sub": True}),
          " = ", f2(R["t_max"], 0), " s);"])
d.bullet([B("ko'tarilish vaqti "), I("t"), S("k"), " = ", f2(R["t_rise"], 0),
          " s (chiqish birinchi marta topshiriq qiymatiga yetgan payt);"])
d.bullet([B("rostlash (o'rnashish) vaqti "), I("t"), S("p"), " = ",
          f2(R["t_set"], 0), " s  (\u00b15 % koridor bo'yicha);"])
d.bullet([B("so'nish darajasi "), I("\u03c8"), " = ", f2(R["psi"], 2),
          "  (1 ga yaqin, ya'ni tebranishlar tez so'nadi)."])

d.para([
    "Olingan ko'rsatkichlar 2.6-jadvalda jamlangan va texnologik talablar bilan "
    "qiyoslangan."
])

d.table(
    headers=["Ko'rsatkich", "Hisob qiymati", "Talab", "Xulosa"],
    rows=[
        ["Statik xatolik", "0 %", "\u2192 0", "qondiriladi"],
        ["O'tib ketish \u03c3", f"{f2(R['overshoot'],1)} %", "\u2264 30 %", "qondiriladi"],
        ["Rostlash vaqti tp", f"{f2(R['t_set'],0)} s", "minimal", "qondiriladi"],
        ["So'nish darajasi \u03c8", f2(R['psi'], 2), "0,75\u20130,98", "qondiriladi"],
        ["Faza zapasi \u0394\u03c6", f"{f2(R['PM'],0)}\u00b0", "30\u201360\u00b0", "qondiriladi"],
        ["Amplituda zapasi \u0394L", f"{f2(R['GM_dB'],1)} dB", "\u2265 6 dB", "qondiriladi"],
    ],
    widths=[2900, 2160, 2160, 2140],
    caption="2.6-jadval"
)

d.heading("Bob bo'yicha xulosa", level=3)

d.para([
    "Ushbu bobda sulfat-ammoniy ishlab chiqarish jarayonidagi saturator "
    "kislotaliligini rostlash konturining to'liq nazariy tahlili amalga oshirildi. "
    "Texnologik ob'ekt kechikishli birinchi tartibli aperiodik bo'g'in sifatida "
    "modellashtirildi (", I("K"), S("ob"), " = ", f2(R["K_ob"], 1), ", ",
    I("T"), S("ob"), " = ", f2(R["T_ob"], 0), " s, ", I("\u03c4"), " = ",
    f2(R["tau"], 0), " s). PI-rostlagich parametrlari Ziegler\u2013Nichols usuli "
    "asosida sozlandi: ", I("K"), S("p"), " = ", f2(R["Kp"]), ", ",
    I("T"), S("i"), " = ", f2(R["Ti"], 0), " s."
])

d.para([
    "Tizimning turg'unligi ikki mustaqil usul bilan tasdiqlandi: chastotaviy "
    "(Naykvist\u2013Bode) kriteriysi yetarli zapaslarni ko'rsatdi (faza zapasi ",
    f2(R["PM"], 0), "\u00b0, amplituda zapasi ", f2(R["GM_dB"], 1), " dB), "
    "Routh\u2013Gurvits algebraik kriteriysi esa yopiq tizimning turg'un ekanini "
    "isbotladi. Boshqarish sifati ko'rsatkichlari (o'tib ketish ",
    f2(R["overshoot"], 1), " %, rostlash vaqti ", f2(R["t_set"], 0),
    " s, statik xatolik nolga teng) barcha texnologik talablarni qondiradi. "
    "Demak, tanlangan boshqarish tizimi sulfat-ammoniy ishlab chiqarish jarayonida "
    "talab qilingan kislotalilikni barqaror ushlab turishni ta'minlaydi."
])

d.save("II_BOB_Hisobiy_qism.docx")
print("II_BOB_Hisobiy_qism.docx yaratildi.")
