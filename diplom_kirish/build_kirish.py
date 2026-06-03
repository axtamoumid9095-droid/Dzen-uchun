# -*- coding: utf-8 -*-
"""KIRISH qismi — desorbsiyalash jarayonini avtomatlashtirish diplom ishi.
Faqat matn (rasm yo'q). Standart .docx (Times New Roman, 14pt, A4)."""
from docx_builder import Docx


def B(t):
    return (t, {"bold": True})


def I(t):
    return (t, {"italic": True})


d = Docx(font="Times New Roman", size_pt=14)

# ===========================================================================
# KIRISH
# ===========================================================================
d.heading("KIRISH", level=1)

d.para([
    "Hozirgi kunda neft-gazni qayta ishlash, kimyo va oziq-ovqat sanoati "
    "korxonalarida texnologik jarayonlarni avtomatlashtirish ishlab chiqarish "
    "samaradorligini oshirishning asosiy yo'nalishlaridan biri hisoblanadi. "
    "Mamlakatimizda sanoatni modernizatsiya qilish, raqobatbardosh mahsulot "
    "ishlab chiqarish va resurs tejovchi texnologiyalarni joriy etish bo'yicha "
    "keng ko'lamli ishlar amalga oshirilmoqda. Bu jarayonda zamonaviy "
    "o'lchov-nazorat asboblari, mikroprotsessorli boshqaruv tizimlari va "
    "avtomatlashtirilgan boshqaruv vositalarini qo'llash muhim ahamiyat kasb etadi."
])

d.para([
    "Kimyoviy texnologiyaning eng keng tarqalgan jarayonlaridan biri "
    "massa almashinuvi jarayonlari bo'lib, ularga absorbsiya, desorbsiya, "
    "rektifikatsiya va ekstraksiya kiradi. ", B("Desorbsiyalash"),
    " (ya'ni suyuqlikka yutilgan gaz yoki bug' komponentlarini undan ajratib "
    "olish) jarayoni absorbsiyaning teskari jarayoni bo'lib, eritmadan qimmatli "
    "komponentlarni qaytarib olish hamda yutuvchi suyuqlikni (absorbentni) "
    "qayta tiklash uchun keng qo'llaniladi. Ushbu jarayon neft va gazni qayta "
    "ishlash zavodlarida, ammiak, oltingugurt birikmalari va boshqa mahsulotlarni "
    "ishlab chiqarishda muhim bosqich hisoblanadi."
])

# --- Dolzarbligi -----------------------------------------------------------
d.para([B("Mavzuning dolzarbligi. "),
    "Desorbsiyalash jarayoni murakkab, inersiyali va ko'p parametrli texnologik "
    "jarayon bo'lib, unda harorat, bosim, sath va suyuqlik sarfi kabi kattaliklarni "
    "bir vaqtning o'zida aniq nazorat qilish va barqaror ushlab turish talab "
    "etiladi. Bu parametrlarni qo'lda boshqarish mahsulot sifatining pasayishiga, "
    "energiya sarfining ortishiga va xavfsizlik darajasining kamayishiga olib "
    "keladi. Shu sababli desorbsiyalash jarayonini zamonaviy o'lchov vositalari "
    "(masalan, Levelflex FMP51 sath o'lchagichi) va avtomatlashtirilgan boshqaruv "
    "tizimlari yordamida avtomatlashtirish dolzarb vazifa hisoblanadi. "
    "Avtomatlashtirish mahsulot sifatini barqarorlashtirish, energiya va xom ashyo "
    "sarfini kamaytirish, jarayon xavfsizligini oshirish hamda inson omilining "
    "ta'sirini kamaytirish imkonini beradi."
])

# --- Maqsad ----------------------------------------------------------------
d.para([B("Bitiruv malakaviy ishining maqsadi. "),
    "Desorbsiyalash jarayonini boshqarish ob'ekti sifatida tahlil qilish, uning "
    "avtomatlashtirish funksional sxemasini ishlab chiqish, zamonaviy o'lchov "
    "vositalari va ijro mexanizmlarini tanlash hamda jarayon parametrlarini "
    "hisoblash orqali samarali avtomatlashtirilgan boshqaruv tizimini loyihalashdan "
    "iborat."
])

# --- Vazifalari ------------------------------------------------------------
d.para([B("Ishning vazifalari. "),
    "Qo'yilgan maqsadga erishish uchun quyidagi vazifalar belgilandi:"
])

d.bullet([
    "desorbsiyalash jarayonini texnologik jarayon sifatida o'rganish va unda "
    "qo'llaniladigan apparatlarni tasniflash;"
])
d.bullet([
    "Levelflex FMP51 sath o'lchagichini montaj qilish va sozlash ishlarini "
    "ko'rib chiqish;"
])
d.bullet([
    "desorbsiyalash jarayonini boshqarish ob'ekti sifatida tahlil qilish va "
    "avtomatlashtirishning funksional sxemasini tuzish;"
])
d.bullet([
    "o'lchov vositalari hamda ijro mexanizmlarining ulanish prinsipial sxemasini "
    "ishlab chiqish va avtomatlashtirilgan texnik vositalarni tanlash;"
])
d.bullet([
    "jarayonning mnemosxemasini ishlab chiqish va mantiqiy amallarni belgilash;"
])
d.bullet([
    "jarayonda ishlatiladigan ijro mexanizmlari (aralashtirgichlar) parametrlarini "
    "hisoblash;"
])
d.bullet([
    "hayot faoliyati xavfsizligi va atrof-muhit muhofazasi bo'yicha chora-tadbirlarni "
    "ishlab chiqish."
], spacing_after="120")

# --- Ob'ekt va predmet -----------------------------------------------------
d.para([B("Tadqiqot ob'ekti. "),
    "Desorbsiyalash texnologik jarayoni va uni amalga oshiruvchi texnologik "
    "qurilma (desorber)."
])

d.para([B("Tadqiqot predmeti. "),
    "Desorbsiyalash jarayonini avtomatlashtirish usullari, o'lchov-nazorat "
    "vositalari, ijro mexanizmlari va boshqaruv tizimining funksional hamda "
    "prinsipial sxemalari."
])

# --- Usullar ---------------------------------------------------------------
d.para([B("Tadqiqot usullari. "),
    "Ishda texnologik jarayonlarni tahlil qilish, avtomatik boshqaruv nazariyasi, "
    "o'lchov texnikasi asoslari, parametrlarni muhandislik hisobi hamda "
    "avtomatlashtirilgan boshqaruv tizimlarini loyihalash usullaridan foydalanildi."
])

# --- Amaliy ahamiyati ------------------------------------------------------
d.para([B("Ishning amaliy ahamiyati. "),
    "Ishlab chiqilgan avtomatlashtirish sxemalari va hisob natijalari desorbsiyalash "
    "jarayonini boshqarish sifatini oshirish, energiya va xom ashyo sarfini "
    "kamaytirish hamda jarayon xavfsizligini ta'minlashga xizmat qiladi. Olingan "
    "natijalardan o'xshash massa almashinuvi jarayonlarini avtomatlashtirishda "
    "hamda o'quv jarayonida foydalanish mumkin."
])

# --- Ishning tuzilishi (foydalanuvchi so'ragan "oxiriga ma'lumot") ---------
d.para([B("Bitiruv malakaviy ishining tuzilishi. "),
    "Ish kirish, to'rt bob, xulosa va foydalanilgan adabiyotlar ro'yxatidan iborat. "
    "Boblar mazmuni quyidagicha:"
])

d.bullet([B("I bob (Texnologik qism) "),
    "da desorbsiyalash jarayoni texnologik jarayon sifatida tasniflanadi, jarayonda "
    "qo'llaniladigan apparatlar ko'rib chiqiladi hamda Levelflex FMP51 sath "
    "o'lchagichini montaj qilish va sozlash ishlari bayon etiladi;"
])
d.bullet([B("II bob (Avtomatlashtirish qismi) "),
    "da desorbsiyalash jarayoni boshqarish ob'ekti sifatida tahlil qilinadi, "
    "avtomatlashtirishning funksional sxemasi, o'lchov vositalari va ijro "
    "mexanizmlarining prinsipial ulanish sxemasi tavsiflanadi, avtomatlashtirilgan "
    "texnik vositalar tanlanadi hamda jarayonning mnemosxemasi va mantiqiy amallari "
    "ishlab chiqiladi;"
])
d.bullet([B("III bob (Hisobiy qism) "),
    "da jarayonda ishlatiladigan ijro mexanizmlari (aralashtirgichlar) parametrlari "
    "hisoblab chiqiladi;"
])
d.bullet([B("IV bob (Hayot faoliyati xavfsizligi bo'limi) "),
    "da umumiy xavfsizlik talablari, desorbsion jarayonlardagi xavfsizlik qoidalari, "
    "yong'in xavfsizligi, fuqaro muhofazasi hamda atrof-muhit muhofazasi bo'yicha "
    "chora-tadbirlar yoritiladi."
], spacing_after="120")

d.para([
    "Xulosa qismida ish yuzasidan olingan asosiy natijalar umumlashtiriladi va "
    "amaliy tavsiyalar beriladi."
])

d.save("KIRISH_desorbsiya.docx")
print("KIRISH_desorbsiya.docx yaratildi.")
