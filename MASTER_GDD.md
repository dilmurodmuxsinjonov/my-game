# MASTER GAME DESIGN DOCUMENT

# VOXEL LORD: FEUDAL REALM 👑

**Hujjat maqomi:** Production Game Design Document  
**Versiya:** Specification 1.5 — Consolidated Production Edition  
**Janr:** First-Person / Voxel Sandbox / Colony Simulation / Strategy / Survival RPG  
**Dvigatel:** Godot Engine 4.3+  
**Asosiy dasturlash:** GDScript + zarur yuqori unumli modullar uchun C#  
**Platforma:** PC — Windows / Linux  
**Distribusiya:** Steam  
**Rejim:** Single Player + 2–4 kishilik Co-op / Multiplayer (Steam P2P)  
**Biznes model:** Premium Indie Game  
**Rejalashtirilgan narx:** $14.99–$19.99  
**Reliz modeli:** Early Access → 1.0  

---

# 0. LOYIHANING ASOSIY MAQSADI

Voxel Lord: Feudal Realm — o‘yinchini tayyor hukmdor sifatida emas, balki deyarli hech narsaga ega bo‘lmagan oddiy inson sifatida dunyoga tashlaydigan birinchi shaxs voxel koloniya simulyatori.

O‘yinchi:

**tirik qoladi → resurs yig‘adi → boshpana quradi → odamlarni qutqaradi → aholi tashkil qiladi → ishlab chiqarishni avtomatlashtiradi → qishloq quradi → qo‘shin tuzadi → yerlarini kengaytiradi → feodal hukmdorga aylanadi → sulola yaratadi → qirollik barpo qiladi.**

O‘yinchining asosiy farqi:
u osmonda uchib yuradigan RTS boshqaruvchisi emas.
Hukmdor o‘z shahrining ichida birinchi shaxs nigohida yashaydi.

U:
- daraxt kesishi;
- kon qazishi;
- ov qilishi;
- dehqonchilik qilishi;
- devor qurishi;
- askarlar bilan jang qilishi;
- sud o‘tkazishi;
- soliq belgilashi;
- odamlar bilan gaplashishi;
- turnirda qatnashishi;
- qo‘shin boshqarishi
mumkin.

Ammo qirollik rivojlangan sari bu ishlarni fuqarolar o‘z zimmasiga oladi.

---

# 1. O‘YINNING 5 ASOSIY USTUNI

## 1.1. Hukmdor nigohi (First-Person Monarch)
O‘yin to‘liq birinchi shaxs nuqtayi nazaridan boshqariladi. O‘yinchi dunyoning fizik qismi hisoblanadi. U jang maydonida ham, qurilishda ham, shahar boshqaruvida ham mavjud.

## 1.2. Living Citizens
Har bir fuqaro mustaqil simulyatsiya qilinadigan shaxs:
- ismi, yoshi, oilasi;
- sog‘ligi, kasbi, mahorati;
- xarakteri, ehtiyojlari;
- boyligi, uy-joyi, munosabatlari, tajribasi.
Fuqarolar havodan spawn bo‘lmaydi. Har bir yangi insonning mantiqiy kelib chiqishi mavjud.

## 1.3. Voxel Freedom
Dunyo to‘liq voxel asosida:
- yer qazish, tog‘ teshib o‘tish;
- tunnel yaratish, devor qurish;
- binoni buzish, relyefni o‘zgartirish.

## 1.4. Hands-on → Automation
O‘yinning eng muhim progression mexanikasi:
* Dastlab: *“Men buni qilishim kerak.”*
* Keyinchalik: *“Kimdir buni men uchun qilishi kerak.”*
* Oxirida: *“Qanday qilib butun davlatni samaraliroq ishlataman?”*

## 1.5. Feudal Rise
O‘yinchi bosqichma-bosqich:
**Sargardon → Oqsoqol → Baron → Graf/Gersog → Qirol** darajalaridan o‘tadi.

---

# 2. CORE GAMEPLAY LOOP

## 2.1. 30 soniyalik loop
O‘yinchi: resurs topadi → yig‘adi → foydalanadi → ehtiyojini qondiradi. (Masalan: daraxt → yog‘och → gulxan → issiqlik).

## 2.2. 5–10 daqiqalik loop
Resurs yig‘ish → asbob yasash → bino qurish → yangi imkoniyat ochish.

## 2.3. Bir o‘yin kuni
O‘yinchi:
- ishlarni taqsimlaydi;
- ishlab chiqarishni tekshiradi;
- oziq-ovqat holatini nazorat qiladi;
- xavfsizlikni tekshiradi;
- qurilish buyurtmalarini beradi;
- ekspeditsiyaga chiqadi.

---

# 3. VAQT TIZIMI

## 3.1. Kalendar
* **1 o‘yin yili = 28 o‘yin kuni.**
* Har fasl = 7 kun:
  * Bahor — 1–7 kunlar
  * Yoz — 8–14 kunlar
  * Kuz — 15–21 kunlar
  * Qish — 22–28 kunlar

## 3.2. Real vaqt
* Standart balans: **1 o‘yin kuni ≈ 24 real daqiqa** (1 game soat ≈ 1 real daqiqa).
* Tezlik boshqaruvi: Pause, x1, x2, x4 (Jang yoki birinchi shaxs harakatida x1).

---

# 4. BIOLOGIK VAQT VA YOSH BOSQICHLARI

Biologik yosh kalendar yiliga to‘g‘ridan-to‘g‘ri bog‘lanmaydi, balki o‘yin davomida avlodlar almashinuvini ta'minlash uchun maxsus simulyatsiya soati orqali hisoblanadi.

* **0–3 yosh:** Chaqaloq (Ona qaramog'ida).
* **4–10 yosh:** Bola. Yengil vazifalar: tuxum yig‘ish, meva terish, chorvaga yem berish.
* **11–15 yosh:** Shogird (Apprentice). Usta bilan ishlab kasb o'rganadi.
* **16–45 yosh:** Voyaga yetgan fuqaro. Maksimal jismoniy unumdorlik va harbiy xizmat.
* **46–60 yosh:** Tajribali fuqaro. Mahorat va donolik yuqori.
* **61–75 yosh:** Oqsoqol. Jismoniy kuch pasayadi, ammo Wisdom va Mastery eng yuqori darajada.

---

# 5. HUKMDORNING DAVOMIYLIGI VA YAGONA SHAXS MODELI (PERSISTENT MONARCH)

O‘yinchining hukmdori keksayib tabiiy o'lim topmaydi (Vorislik va sulola avlodlari o'yinchi uchun qo'llanilmaydi).
Hukmdor butun o‘yin davomida o'z saltanatini shaxsan barpo qiluvchi yagona doimiy qahramondir.
O'yinda "Hardcore" va "Casual Survival" deb sun'iy ravishda ikkiga bo'linmaydi — o'yin yagona, adolatli va jiddiy omon qolish qonuniyatiga tayanadi.
(Shahar fuqarolari esa tabiiy ravishda qariydi, ta'lim oladi, yangi avlod tug'iladi va vafot etadi).

---

# 6. HUKMDORNING JANGDA YIQILISHI VA DAVOLANISHI (KNOCKOUT & RECOVERY)

Hukmdor jangda yiqilsa, permadeath (butunlay yo'q bo'lish) bo'lmaydi:
1. **Og‘ir Yaralanish (Knocked Out):** Hukmdor jangda jarohatlanganda askarlari yoki fuqarolari uni darhol jang maydonidan xavfsiz boshpanaga olib chiqadi.
2. **Gospitalda Davolanish:** Bir necha o'yin kuni davomida saroy yoki tabibxona to'shagida yotadi (bu vaqtda shahar ishlari avtomatlashtirilgan tartibda davom etadi).
3. **Qayta Tiklanish:** Sog'aygach, hukmdor qaytadan o'z taxtiga o'tiradi va saltanatni boshqarishda davom etadi.

---

# 7. ORIGIN (KELIB CHIQISH) TIZIMI

## 7.1. Surgun Ritsar (Exiled Knight)
* Boshlaydi: qilich, eski zanjir sovut, qalqon.
* Bonus: Combat Skill (+20%).
* Kamchilik: Crafting va farming zaif.

## 7.2. Xonavayron Savdogar (Bankrupt Merchant)
* Boshlaydi: 25 kumush tanga, aravacha, xarita.
* Bonus: savdo narxlari ancha qulay, karvonlar bilan aloqa oson.
* Kamchilik: jang qobiliyati past.

## 7.3. Qochoq Ovchi (Runaway Hunter)
* Boshlaydi: kamon, 20 o‘q, bolta, tuzoq.
* Bonus: ov, iztoparlik va yovvoyi tabiatda omon qolish.
* Kamchilik: boshlang‘ich puli 0.

---

# 8. PLAYER STATS

Hukmdor quyidagi fizik ko'rsatkichlarga ega:
- **Health (Salomatlik)**
- **Stamina (Chidamlilik)**
- **Hunger (Ochlik)**
- **Thirst (Chanqoqlik)**
- **Temperature (Tana harorati)**
- **Fatigue (Charchoq)**
- **Armor (Himoya)**
- **Carry Weight (Ko'tarish vazni)**

---

# 9. INVENTORY TIZIMI

- **Hotbar:** 8 ta tezkor slot.
- **Backpack:** 24 ta bazaviy inventar sloti (sumkalar orqali kengaytiriladi).
- **Equipment Slotlari:** Head, Chest, Legs, Boots, Gloves, Main Hand, Off Hand, Back, Accessory ×2.

---

# 10. ITEM TIZIMI (ITEM SYSTEM ARCHITECTURE & DATA MODEL)

Voxel Lord: Feudal Realm o'yinida har bir jismoniy ashyo (item), moddiy resurs, asbob va qurol-yarog' Godot 4.3 dvijogining `Resource` arxitekturasi asosida qurilgan `ItemData` ma'lumotlar modeli orqali ifodalanadi. Ushbu arxitektura yengil xotira iziga (flyweight pattern) ega bo'lib, o'n minglab passiv resurslarni inventar va omborlarda xotirani ortiqcha yuklamasdan saqlash imkonini beradi.

### 10.1. 10 Asosiy Atributlar Sxemasi (10-Attribute Item Schema)

Har bir ashyo quyidagi 10 ta qat'iy tipga ega atributlar majmuasidan tashkil topadi:

1. **ItemID (`StringName`):** Dunyo bo'yicha noyob, qat'iy identifikator (masalan, `&"res_iron_ingot"`, `&"weap_steel_longsword"`). Lug'at (Dictionary) qidiruvlari uchun $O(1)$ tezlik ta'minlaydi.
2. **DisplayName (`String`):** Foydalanuvchi interfeysida (UI) aks etuvchi ko'p tilli mahalliylashtirilgan nom (O'zbekcha / Inglizcha formatda, masalan, `"Po'lat Qilich (Steel Longsword)"`).
3. **Category (`ItemCategory` Enum):** Ashyoning iqtisodiy va moddiy sinfi. Ombor filtrlari, inventar saralash va ishlab chiqarish zanjirlarini guruhlash uchun xizmat qiladi.
4. **WeightKg (`float`):** Ashyoning 1 donasi uchun sof fizik og'irligi (kilogrammda). Fuqaro va o'yinchining yuk ko'tarish limitini (`CarryWeight`), transport aravalarining dinamikasini belgilaydi.
5. **StackSize (`int`):** Bitta inventar yoki ombor katagida (slot) to'planishi mumkin bo'lgan maksimal birlik soni (1 dan 500 gacha).
6. **Durability (`Vector2i`):** `x = current_durability`, `y = max_durability`. Har bir zarba, qazish yoki ishlatishda eskiradi. Agar ashyo eskimaydigan bo'lsa (xomashyo, oziq-ovqat), qiymat `(-1, -1)` qilib belgilanadi.
7. **QualityTier (`QualityTier` Enum):** Buyumning yasalish sifati (Poor darajadan Legendary darajagacha). Parametrlarni masshtablovchi koeffitsiyentlarni taqdim etadi.
8. **BaseValue (`int`):** Bozor talab va taklifidan xoli bo'lgan, sof kumush tangadagi (Silver Pence) fundamental qiymati.
9. **Rarity (`ItemRarity` Enum):** Buyumning topilish va paydo bo'lish darajasi (Common, Uncommon, Rare, Epic, Mythic).
10. **Tags (`PackedStringArray`):** Moddiy va xulq-atvor teglari majmuasi (`"smeltable"`, `"flammable"`, `"perishable"`, `"edible_raw"`, `"edible_cooked"`, `"construction_grade"`, `"weapon_blunt"`, `"metal_flux"`).

### 10.2. Ashyolar Toifalari va Standart Parametrlari (Category Breakdown Table)

| Toifa ID | Kategoriya Nomi | Standart Stack | O'rtacha Og'irlik (kg) | Durability Mavjudligi | Asosiy Xususiyati va Ishlatilish Sohasi |
|---|---|---|---|---|---|
| `CAT_RAW` | Xomashyo (Raw Resources) | 100 | 1.5 – 5.0 kg | Yo'q (-1) | Qazib olingan rudalar, xoda, tosh, qum, gil. Bevosita qurilish va eritish uchun. |
| `CAT_PROCESSED` | Qayta Ishlangan (Materials) | 50 | 0.8 – 3.0 kg | Yo'q (-1) | Quymalar (ingots), taxtalar, g'ishtlar, charm, kanop iplari. |
| `CAT_FOOD` | Oziq-ovqat (Food & Rations) | 20 | 0.2 – 1.0 kg | Aynish vaqti (Freshness) | Don, sabzavot, pishirilgan go'sht, non, pishloq. Ochlik va ruhiyatni tiklaydi. |
| `CAT_TOOL` | Mehnat Qurollari (Tools) | 1 | 1.5 – 4.5 kg | Ha (60 – 10,000) | Cho'kich, bolta, ketmon, o'roq, temirchilik bosqoni. Mehnat unumdorligini beradi. |
| `CAT_WEAPON` | Qurol-Yarog' (Weapons) | 1 | 1.0 – 6.0 kg | Ha (200 – 3,500) | Qilich, nayza, o'q-yoy, arbalet, jangovar bolta. Jangovar zararni hisoblaydi. |
| `CAT_ARMOR` | Himoya Zirhlari (Armor) | 1 | 2.0 – 26.0 kg | Ha (60 – 1,200) | Shlem, gambezon, zanjir sovut, plita sovut, qalqonlar. Zararni sindiradi. |
| `CAT_AMMO` | Jangovar O'qlar (Ammunition) | 100 | 0.04 – 0.08 kg | Yo'q (1 martalik) | O'qlar (Arrows), arbalet boltchalari (Bolts), qamal toshlari. |
| `CAT_CONSUMABLE` | Iste'mol Mollari (Consumables)| 20 | 0.1 – 0.5 kg | Yo'q (-1) | Bog'ichlar (Bandages), malhamlar, dorivor giyohlar, mash'alalar. |
| `CAT_LUXURY` | Hashamat va Zargarlik (Luxury)| 10 | 0.05 – 1.0 kg | Yo'q (-1) | Oltin idishlar, zargarlik buyumlari, ipak mato, ziravorlar. Soliq va obro' beradi. |
| `CAT_ARCHITECT` | Arxitektura Modullari (Blocks) | 64 | 10.0 – 25.0 kg | Voxel HP bilan | Qal'a bloklari, eshiklar, panjaralar, suv novlari, tom yopqichlari. |

### 10.3. Godot 4 GDScript Arxitektura Ma'lumot Modeli (`ItemData.gd`)

```gdscript
# res://scripts/economy/item_data.gd
class_name ItemData
extends Resource

enum ItemCategory {
	RAW_RESOURCE,
	PROCESSED_MATERIAL,
	FOOD,
	TOOL,
	WEAPON,
	ARMOR,
	AMMUNITION,
	CONSUMABLE,
	LUXURY,
	ARCHITECTURAL
}

enum QualityTier {
	POOR = 0,
	COMMON = 1,
	FINE = 2,
	MASTERWORK = 3,
	ROYAL = 4,
	LEGENDARY = 5
}

enum ItemRarity {
	JUNK,
	COMMON,
	UNCOMMON,
	RARE,
	EPIC,
	MYTHIC
}

@export_group("Identification")
@export var item_id: StringName = &"unnamed_item"
@export var display_name: String = "Unnamed Item"
@export_multiline var description: String = ""
@export var icon: Texture2D

@export_group("Physical Properties")
@export var category: ItemCategory = ItemCategory.RAW_RESOURCE
@export_range(0.01, 1000.0, 0.01) var weight_kg: float = 1.0
@export_range(1, 500, 1) var stack_size: int = 50
@export var tags: PackedStringArray = []

@export_group("Durability & Quality")
@export var max_durability: int = -1 # -1 = eskimaydi
@export var quality_tier: QualityTier = QualityTier.COMMON

@export_group("Economics")
@export_range(0, 1000000, 1) var base_value: int = 1 # Kumush tanga
@export var rarity: ItemRarity = ItemRarity.COMMON

func is_damageable() -> bool:
	return max_durability > 0

func get_quality_value_multiplier() -> float:
	match quality_tier:
		QualityTier.POOR: return 0.50
		QualityTier.COMMON: return 1.00
		QualityTier.FINE: return 1.75
		QualityTier.MASTERWORK: return 3.50
		QualityTier.ROYAL: return 8.00
		QualityTier.LEGENDARY: return 20.00
	return 1.00
```

---

# 11. ITEM QUALITY (BUYUM SIFATI VA STATLARNI KO'PAYTIRISH)

O'yindagi har bir ishlab chiqarilgan buyum (asbob, qurol, sovut, taom, mebel) uni yasagan fuqaroning mahoratiga, ishlatilgan xomashyo sofligiga va ishlatilgan dastgohning texnologik darajasiga qarab 6 ta sifat toifasiga bo'linadi.

### 11.1. Sifat Darajalari va Matematik Ko'paytiruvchilar (Quality Multiplier Matrix)

| Sifat Darajasi (Quality Tier) | O'zbekcha / Inglizcha Nomi | Parametr Multiplikatori ($M_{stat}$) | Mustahkamlik Multiplikatori ($M_{dur}$) | Narx Ko'paytiruvchisi ($M_{val}$) | Vizual / Shader Effektlari |
|---|---|---|---|---|---|
| **Tier 0** | Xarob / Sifatsiz (Poor) | $0.80\times$ | $0.60\times$ | $0.50\times$ | Xira, zang bosgan, yoriq tekstura, kulrang hoshiya. |
| **Tier 1** | Oddiy / Standart (Common) | $1.00\times$ | $1.00\times$ | $1.00\times$ | Standart metall va yog'och ko'rinishi, oq hoshiya. |
| **Tier 2** | Sifatli / Sayqallangan (Fine) | $1.25\times$ | $1.40\times$ | $1.75\times$ | Toza silliqlangan metall jilosi, yashil hoshiya. |
| **Tier 3** | Usta Qo'li (Masterwork) | $1.60\times$ | $2.00\times$ | $3.50\times$ | Naqshinkor o'ymakorlik, ko'k hoshiya, mayin jilo. |
| **Tier 4** | Qirollik / Saroy (Royal) | $2.00\times$ | $3.00\times$ | $8.00\times$ | Oltin hoshiyali bezak, binafsharang fon, yaltiroq yorug'lik. |
| **Tier 5** | Afsonaviy / Nodir (Legendary) | $2.50\times$ | $5.00\times$ | $20.00\times$ | Qadimiy runik porlash, to'q sariq/olovrang nur zarralari. |

### 11.2. Sifatni Aniqlash va Ehtimollik Formulasi (Quality Roll & Failure Equation)

Hunarmand buyum yasayotganda sifat darajasi quyidagi ehtimollik taqsimoti orqali tasodifiy aniqlanadi:

$$QualityScore = \left(Skill_{crafter} \times 0.55\right) + \left(Tier_{station} \times 15.0\right) + \left(Purity_{mat} \times 0.30\right) + \text{rand\_range}(-10.0, +10.0)$$

Bunda:
- $Skill_{crafter} \in [0, 100]$: Ustanong ixtisoslashgan mehnat mahorati (Blacksmithing, Carpentry, Masonry).
- $Tier_{station} \in [1, 4]$: Dastgoh darajasi (1 = Dala gulxani, 2 = Oddiy bosqon, 3 = Suv tegirmonli bosqon, 4 = Qirollik eritish saroyi).
- $Purity_{mat} \in [0, 100]$: Xomashyoning metallurgik tozaligi va rudaning toifasi.

**Natijaviy Sifat Toifasini Tanlash Bosqichlari:**
- $QualityScore < 25$: **Poor** (Agar $Skill_{crafter} < Skill_{required}$ bo'lsa, quyidagi sinish xavfi hisoblanadi).
- $25 \le QualityScore < 60$: **Common**
- $60 \le QualityScore < 90$: **Fine**
- $90 \le QualityScore < 125$: **Masterwork**
- $125 \le QualityScore < 155$: **Royal**
- $QualityScore \ge 155$: **Legendary** (Faqat $Skill \ge 95$ va Tier 4 dastgoh bo'lgandagina ochiladi).

**Ishlab Chiqarishdagi Falokat va Sinish Ehtimoli (Critical Failure Rate):**
Agar ustaning mahorati retsept talabidan past bo'lsa ($Skill_{crafter} < Skill_{required}$), buyum butkul buzilib, yaroqsiz chiqindiga aylanish xavfi vujudga keladi:
$$P_{fail} = \min\left(0.65, \; (Skill_{required} - Skill_{crafter}) \times 0.025\right)$$
Falokat sodir bo'lganda buyum yo'qoladi, xomashyoning $35\%$ qismi chiqindi kul yoki tosh siniqlari (`res_slag`, `res_scrap_wood`) sifatida qaytadi.

---

# 12. ASBOBLAR PROGRESSIYASI (TOOL PROGRESSION & DURABILITY SPECIFICATIONS)

O'yinda mehnat unumdorligi ishchilarning qo'lidagi asbob turiga qat'iy bog'liq. Har bir asbob turi material darajasiga qarab qazish tezligini, qazib olinishi mumkin bo'lgan maksimal voxel qattiqligini va chidamliligini belgilaydi.

### 12.1. Asboblar Sinflari (Tool Classes)
1. **Cho'kich / Kulang (Pickaxe):** Konchilik, tosh, ko'mir va metall rudalarini qazish.
2. **Yog'ochkesar Boltasi (Woodcutting Axe):** Daraxtlarni yiqitish, xodalarni tilish, o'tin tayyorlash.
3. **Ketmon / Bel (Shovel & Hoe):** Tuproq, loy, shag'al qazish va ekin maydonlarini haydash, shudgorlash.
4. **O'roq / Qaychi (Sickle & Scythe):** G'alla, zig'ir, o'tlarni o'rish va qo'ylarning junini qirqish.
5. **Temirchilik Bosqoni (Smithing Hammer):** Anvil ustida metall quymalarini shakllantirish va qurol yasash.

### 12.2. Metall va Materiallar Progressiyasi Jadvali (Comprehensive Tool Balance Table)

| Asbob Tieri | Material Nomi | Qazish / Ish Tezligi Multiplikatori | Maksimal Qaziladigan Voxel Qattiqligi ($H_{max}$) | Maksimal Mustahkamlik ($Dur_{max}$) | 1 Voxel Qazishdagi Eskirish | Sinishdagi Xomashyo Qaytimi (Scrap Return) |
|---|---|---|---|---|---|---|
| **Tier 0** | Yog'och (Wood) | $0.60\times$ | 1 (Faqat yumshoq tuproq, loy) | 60 zarba | 1.0 durability | 1 dona shox-shabba |
| **Tier 1** | Tosh / Flint (Stone) | $1.00\times$ (Baza) | 2 (Ohaktosh, qumtosh, ko'mir) | 150 zarba | 1.0 durability | 1 dona tosh bo'lagi |
| **Tier 2** | Mis (Copper) | $1.35\times$ | 3 (Mis rudasi, qalay, gil) | 280 zarba | 0.9 durability | 1 dona mis siniq (Copper scrap) |
| **Tier 3** | Bronza (Bronze) | $1.75\times$ | 4 (Temir rudasi, qattiq tosh) | 450 zarba | 0.8 durability | 1 dona bronza parchasi |
| **Tier 4** | Temir (Iron) | $2.25\times$ | 6 (Granit, nikel, kumush, oltin) | 800 zarba | 0.7 durability | 1 dona temir parchasi |
| **Tier 5** | Po'lat (High-Carbon Steel)| $3.00\times$ | 8 (Bazalt, obsidian, qimmatbaho toshlar)| 1,600 zarba | 0.5 durability | 2 dona po'lat parcha |
| **Tier 6** | Damashq Po'lati (Damascus)| $4.00\times$ | 9 (Titan, meteorit, qora bazalt) | 3,500 zarba | 0.3 durability | 1 dona damashq plastinasi |
| **Tier 7** | Runik / Meteorit (Runic) | $5.50\times$ | 10 (Magmatik poydevor, tub jinslar) | 10,000 (O'zini tiklaydi)| 0.1 durability | Yo'qolmaydi, zaryadi so'nadi |

### 12.3. Asbob Yetishmasligi Jazosi (Tool Depletion Penalty)
Agar fuqaro o'z kasbiga oid asbobsiz ishlasa (masalan, konchi qo'li bilan tosh qazishga urinsa):
- Mehnat tezligi bazaviy tezlikning $0.20\times$ qismiga tushadi ($-80\%$ jazo).
- Qattiqligi $H \ge 2$ bo'lgan barcha voxellar qazib olinmaydi ("Asbob kerak" xatosi chiqadi).
- Ishchining charchoqlik (Fatigue) to'planishi $2.5\times$ ga tezlashadi va jarohat olish (qon ketish, qo'l lat yeyishi) ehtimoli $+15\%$ ga oshadi.

---

# 13. CRAFTING (YASASH) TIZIMI VA DASTGOHLAR ARXITEKTURASI

Voxel Lord: Feudal Realm o'yinida ishlab chiqarish mexanikasi real vaqt rejimida fizik simulyatsiya qilinadigan 3 pog'onali ierarxiya asosida amalga oshiriladi:

### 13.1. Ishlab Chiqarishning 3 Rejimi (Crafting Modes)

1. **Qo'lda Yasash (Hand Crafting):**
   - O'yinchi yoki fuqaroning shaxsiy inventarida amalga oshiriladi.
   - Hech qanday statsionar dastgohni talab qilmaydi.
   - Cheklov: Faqat ibtidoiy ashyolar — yog'och tayoqlar, tosh pichoq, bog'ichlar (bandage), dala mash'alasi va o't yoqish toshlari (flint & tinder).
2. **Statsionar Dastgohlarda Yasash (Workstation Crafting):**
   - Shaharda maxsus qurilgan ishlab chiqarish bloklari va binolarni talab qiladi.
   - Har bir dastgoh ma'lum xomashyo kiritish rezervuariga, yoqilg'i haroratiga va malakali operator-fuqaroga muhtoj.
   - Dastgoh texnologiyasi buyum sifatini oshiradi va ishlab chiqarish vaqtini qisqartiradi.
3. **Avtomatlashtirilgan Fuqarolar Ishlab Chiqarishi (Citizen Production Quotas):**
   - Hukmdor Royal Ledger yoki ustaxona menyusida 3 xil ishlab chiqarish qoidasini o'rnatadi:
     - `Produce X Times (X marta yasash)`: Buyurtma qilingan miqdor tayyor bo'lgach ishlab chiqarish to'xtaydi.
     - `Maintain Stock Level Y (Omborda Y miqdorni saqlash)`: Omborxonadagi zaxira tekshirib turiladi, zaxira Y dan kamaysa avtomatik buyurtma ochiladi.
     - `Continuous / Infinite (Uzluksiz ishlab chiqarish)`: Xomashyo yetarli bo'lgunga qadar tinimsiz ishlab chiqariladi.

### 13.2. Dastgohlar Master Katalogi (Master Workstations Catalog)

| Dastgoh Nomi | Bino Turi | Talab Qilinadigan Yoqilg'i / Energiya | Ishlash Samaradorligi | Ruxsat Etilgan Retseptlar Guruxi |
|---|---|---|---|---|
| **Yog'ochkesar Bolg'asi (Sawpit / Carpenter Bench)** | Duradgorxona | Yo'q (Qo'l mehnati) | $1.00\times$ | Taxta tilish, xoda yo'nish, qutilar, aravachalar, qalqonlar. |
| **Gidravlik Sawmill (Water-Powered Sawmill)** | Suv Tegirmoni | Daryo oqimi (Gidro-turbina) | $2.20\times$ | Katta hajmdagi taxtalar, qoplama bruslar (xomashyo yo'qotilmaydi). |
| **Qo'l Tegirmoni (Hand Quern)** | Oddiy Xona | Yo'q (Qo'l mehnati) | $0.65\times$ | Don yanchish (25% un yo'qotilishi bilan). |
| **Shamol / Suv Tegirmoni (Gristmill)** | Tegirmon Minorasi | Shamol kuchi yoki Suv oqimi | $2.50\times$ | Oliy navli un, kepak, pivo solodi. |
| **Nonvoyxona Pechi (Bakehouse Stone Oven)** | Nonvoyxona | O'tin yoki Yog'och ko'miri | $1.35\times$ (Issiq holda)| Non, pirog, qotirilgan quruq nonlar (hard tack). |
| **Past Haroratli Eritish Xumdoni (Bloomery)**| Eritish Maydoni | Yog'och ko'miri ($1100^\circ\text{C}$)| $0.85\times$ | Xom temir shlakini eritish, temir quymasi (chuyan). |
| **Domna Pechi (Blast Furnace)** | Qal'a Metallurgiyasi | Toshko'mir + Havo bosqoni ($1400^\circ\text{C}$) | $1.75\times$ | Yuqori uglerodli po'lat quyish, quyma qurollar. |
| **Damashq Tigel Xumdoni (Crucible Forge)** | Buyuk Saroy Temirxonasi | Maxsus koks ko'miri ($1550^\circ\text{C}$) | $1.20\times$ (Nozik)| Damashq po'lati, naqshli metall ingotlari. |
| **Pivo Qaynatish Qozoni (Brewery Vat)** | Qovoqxona / Pivo pishirish| O'tin + Doimiy toza suv | $1.10\times$ | El, qora pivo, asal sharbati (Mead). |
| **To'quv Dastgohi (Loom & Spinning Wheel)**| To'quvchilik Sehi | Yo'q (Qo'l mehnati) | $1.00\times$ | Zig'ir mato, jun mato, ipak, kiyim-kechak, qoplar. |

### 13.3. Ishlab Chiqarish Vaqti va Eskirish Formulalari (Crafting Formulas)

Har bir ishlab chiqarish siklining real davomiyligi quyidagi tenglama orqali hisoblanadi:

$$T_{craft} = \frac{BaseCraftTime}{SpeedMult_{tool} \times \left(1.0 + 0.015 \cdot Skill_{crafter}\right) \times Efficiency_{station}} \times M_{fatigue}$$

Bunda:
- $BaseCraftTime$: Retseptning sekundlardagi standart bazaviy vaqti.
- $SpeedMult_{tool}$: Ishlatilayotgan asbobning tezlik koeffitsiyenti (12-bo'limga qarang).
- $Skill_{crafter} \in [0, 100]$: Ustanong mahorati (har bir ball vaqtni $1.5\%$ ga qisqartiradi).
- $Efficiency_{station}$: Dastgohning texnologik koeffitsiyenti.
- $M_{fatigue}$: Agar ustaning charchog'i $Fatigue > 75$ bo'lsa, $M_{fatigue} = 1.40\times$; aks holda $1.00\times$.

**Dastgoh va Asbob Eskirishi:**
Har bir ishlab chiqarish sikli yakunida usta qo'lidagi asbob quyidagi miqdorda eskiradi:
$$\Delta Durability = BaseWear_{recipe} \times \left(1.0 - 0.005 \cdot Skill_{crafter}\right)$$
Professional ustalar ($Skill = 100$) asbobni $50\%$ ga kamroq eskirtiradi.

**Chiqindilarni Qayta Ishlash (Scrap Recovery Formula):**
Buzilgan yoki eskirgan buyumlar qayta eritilganda yoki duradgor stolida qismlarga ajratilganda qaytadigan xomashyo miqdori:
$$ScrapYield = \left\lfloor InputMaterialCount \times 0.35 \times \left(\frac{CurrentDurability}{MaxDurability}\right) \times (1.0 + 0.003 \cdot Skill_{crafter}) \right\rfloor$$
To'liq singan ($Durability = 0$) buyumdan boshlang'ich materialning qat'iy $15\%$ qismi qayta ishlanuvchi siniqlar sifatida tiklanadi.

---

# 14. AHOLINING PAYDO BO‘LISHI (POPULATION GENERATION & LIFECYCLE)

Voxel Lord: Feudal Realm o'yinida aholi sun'iy ravishda havodan yoki resurs sarflamasdan o'z-o'zidan paydo bo'lmaydi. Har bir fuqaro dunyo simulyatsiyasida aniq biologik, ijtimoiy va logistik sabab-oqibat zanjiri orqali dunyoga keladi yoki shaharga qo'shiladi.

### 14.1. Aholining Kelib Chiqish Kanallari (Immigration Vectors & Spawning)

1. **Xaloskor Gulxan (Signal Fire Beacon):**
   - O'yinning dastlabki (Tier I) bosqichida quriladigan signal o'ti.
   - Gulxan tutuni va yorug'ligi 250 metr radiusdagi sargardon qochqinlar (Refugees) va ovchilarni jalb qiladi.
   - Har 3 o'yin kunida 1 marta yangi sargardon kelish ehtimoli tekshiriladi ($P_{refugee} = 0.40$).
   - Kelgan qochqinlar past darajadagi asboblar va xarob kiyimlar bilan keladi, dastlabki mehnat kuchi bo'lib xizmat qiladi.

2. **Tutqunlarni Qutqarish (Captive Rescue Operations):**
   - Dushman qaroqchilar (Bandits) qarorgohlari, o'rmon lagerlari va vayron bo'lgan karvonlardan asirlarni ozod qilish orqali.
   - Ozod qilingan asirlar hukmdorga nisbatan $+50$ sodiqlik va minnatdorchilik hissi (`Grateful` xarakter xususiyati) bilan qo'shiladi.
   - Odatda ular orasida malakali hunarmandlar (duradgor, temirchi, tabib) uchraydi.

3. **Shahar Qo'ng'irog'i va Qasr Darvozasi (Village Bell & Gate Immigration):**
   - Tier II va Tier III bosqichida shahar markaziy maydoniga o'rnatilgan cherkov yoki minora qo'ng'irog'i orqali.
   - Yuqori obro' (Prestige $\ge 40$) va xalq roziligi (Morale $\ge 75$) bo'lganda, mintaqa bo'ylab tarqalgan erkin dehqonlar va hunarmand oilalar ko'chib keladi.

4. **Daryo Porti va Karvonsaroy (River Docks & Caravansary):**
   - Savdo yo'llari va suv transporti orqali professional yollanma ishchilar, olimlar, me'morlar va tajribali usta-qurollar keladi.
   - Yollash uchun shahar xazinasidan boshlang'ich kumush tanga (Contract Fee: 25–100 Silver) to'lanadi.

5. **Tabiiy Ko'payish (Demographic Generational Birth):**
   - Shaharda xususiy uyga ega bo'lgan, qonuniy nikohdan o'tgan oilalarda bolalar tug'ilishi orqali shahar aholisining tabiiy o'sishi.

---

### 14.2. Demografik Hayot Sikli va Yosh Egri Chiziqlari (Demographic Lifecycle)

Har bir fuqaroning hayoti 6 ta qat'iy biologik va ijtimoiy bosqichdan iborat:

| Yosh Bosqichi | Davri (Yillar) | Jismoniy Mehnat Salohiyati | Harbiy Xizmat | Oziq-ovqat Iste'moli | Maxsus Imkoniyatlar va Cheklovlar |
|---|---|---|---|---|---|
| **Chaqaloq (Infant)** | 0 – 3 yosh | 0% (Mehnat qilmaydi) | Yo'q | $0.35\times$ (Ona suti/bo'tqa) | Onaning harakatini $-15\%$ ga sekinlashtiradi. Uyda yoki beshikda bo'ladi. |
| **Bola (Child)** | 4 – 10 yosh | 25% (Yengil yordamchi) | Yo'q | $0.65\times$ | Tuxum yig'ish, qushlarni haydash, o'rmondan qulupnay terish, engil suv tashish. |
| **Shogird (Apprentice)**| 11 – 15 yosh | 65% (Hunarmand shogirdi) | Yordamchi | $0.90\times$ | Biror usta (Master)ga biriktiriladi. Mahoratini 0 dan 40 gacha rivojlantiradi. |
| **Voyaga Yetgan (Adult)**| 16 – 45 yosh | 100% (Maksimal unumdorlik)| To'liq chaqiruv | $1.00\times$ (Baza) | Nikoh qurish, og'ir konchilik, qurilish, dehqonchilik va armiyada xizmat qilish. |
| **Faxriy (Veteran)** | 46 – 60 yosh | 85% (Jismoniy sekinlashuv)| Zaxira soqchi | $0.95\times$ | Ishlab chiqarish sifati $+25\%$, yangi avlodni o'qitish tezligi $+50\%$. |
| **Oqsoqol (Elder)** | 61 – 75 yosh | 50% (Yengil aqliy mehnat) | Yo'q | $0.80\times$ | Sud maslahatchisi, diniy marosimlar boshqaruvchisi, shahar axloqiy nufuzi $+15\%$. |

---

### 14.3. Homiladorlik va Tug'ilish Ehtimoli Formulalari (Conception & Gestation)

Nikohdagi er-xotin (ayol yoshi 16–48 oralig'ida) shaxsiy xonadonga ega bo'lsa, har bir fasl (7 o'yin kuni) oxirida homilador bo'lish ehtimoli quyidagi formula asosida hisoblanadi:

$$P_{conception} = BaseFecundity(Age) \times \left(\frac{Morale}{100.0}\right)^2 \times ComfortMult \times NutritionMult \times (1.0 - 0.20 \times ExistingChildren)$$

Bunda parametrlar:
- **Yosh Koeffitsiyenti ($BaseFecundity$):**
  - 16 – 22 yosh: $0.18$
  - 23 – 32 yosh: $0.24$ (Maksimal reproduktiv cho'qqi)
  - 33 – 40 yosh: $0.10$
  - 41 – 48 yosh: $0.03$
  - 49+ yosh: $0.00$
- **Uy Qulayligi Multiplikatori ($ComfortMult$):**
  $$ComfortMult = 0.50 + 0.50 \times \left(\frac{Score_{house}}{100.0}\right)$$
  Qulay va issiq xonadon homiladorlik ehtimolini 2 barobarga oshiradi.
- **Oziqlanish Sifati ($NutritionMult$):**
  - Faqat non va suv: $0.60\times$
  - Go'sht va sabzavotlar qo'shilgan turfa ratsion: $1.25\times$
- **Mavjud Bolalar Cheklovi:** Har bir voyaga yetmagan bola oiladagi yangi homiladorlik ehtimolini $20\%$ ga qisqartiradi (maksimal 4 ta bolagacha).

**Homiladorlik Davri va Onalik Debafflari (Gestation Logistics):**
- **Davomiyligi:** 3 Fasl = 21 o'yin kuni (504 real daqiqa).
- **Fiziologik O'zgarishlar:**
  - Onaning harakatlanish tezligi: $-15\%$ sekinlashadi.
  - Kaloriya va ochlik sarflanishi: $+25\%$ ga oshadi.
  - Xavfli ishlardan ozod etish: Homilador ayol avtomatik ravishda harbiy xizmat, shaxtada kon qazish va og'ir tosh ko'tarish ishlaridan chetlatilib, yengil vazifalarga (to'quvchilik, non yopish, oshxona) o'tkaziladi.
- **Tug'ruq Jarayoni va Xavflar:**
  - Uyda issiqlik pechkasi va toza suv bo'lsa, ona va bolaning omon qolish ehtimoli $98\%$.
  - Sovuq, iflos yoki qorong'u kulbada tug'ruq paytida $15\%$ chaqaloq nobud bo'lishi yoki onaning infektsiya (`Sepsis`) olish xavfi mavjud. Tabib (Doctor) mavjudligi bu xavfni butkul bartaraf etadi.

---

# 15. MIGRATSIYA VA KETISH (MIGRATION & EMIGRATION DYNAMICS)

Shaharning aholi soni erkin bozor va hayot sharoitlariga mutanosib ravishda o'zgarib turadi. Farovon shahar yangi aholini o'ziga magnit kabi tortsa, qashshoqlashgan va xavfli shahar aholining ommaviy qochishiga sabab bo'ladi.

### 15.1. Migratsiya Oqimi Tenglamasi (Immigration Influx Formula)

Har bir o'yin kuni tongida (soat 06:00) yangi muhojirlar (Immigrants) karvoni kelishi quyidagi formula orqali hisoblanadi:

$$\Delta Immigrants = \begin{cases} 
  \min\left(FreeBeds, \; \left\lfloor (Morale - 70.0) \times 0.08 \times \left(1.0 + \frac{Prestige}{100.0}\right) \right\rfloor\right), & \text{agar } Morale > 75 \text{ va } FoodDays \ge 7 \\
  0, & \text{aks holda}
\end{cases}$$

Bunda:
- $FreeBeds$: Shahardagi bo'sh, tom bilan yopilgan va tayyor to'shaklar soni. Fuqarolar yotishga joyi bo'lmagan shaharga ko'chib kelmaydi.
- $Morale \in [-100, +100]$: Shahar aholisining o'rtacha umumiy ruhiyati.
- $Prestige \in [0, 100]$: Hukmdorning obro'yi, qurilgan saroylar, soborlar va toza ko'chalar beradigan nufuz.
- $FoodDays$: Shahar omboridagi mavjud oziq-ovqat zahirasining butun aholiga necha kunga yetishi ($FoodDays = \frac{FoodReserve}{Population \times DailyConsumption}$).

---

### 15.2. Shaharni Tashlab Ketish Tenglamasi (Emigration & Defection Formula)

Agar hayot sharoiti chidab bo'lmas darajaga tushsa, fuqarolar o'z mol-mulklarini yig'ishtirib, shahardan qochishga tushadi:

$$\Delta Emigrants = \begin{cases} 
  \left\lceil (35.0 - Morale) \times 0.04 \times Population \right\rceil, & \text{agar } Morale < 35 \text{ yoki } StarvationDays \ge 2 \\
  0, & \text{aks holda}
\end{cases}$$

**Aholining Ketishiga Sabab Bo'luvchi Kritik Triggerlar:**
1. **Ocharchilik (Famine):** Omborlarda 48 soatdan ortiq hech qanday taom qolmasligi va aholi ochlikdan salomatligini yo'qotishi ($-50$ Morale).
2. **Boshpanasizlik (Homelessness):** Qishda yoki yomg'irda ko'chada yotish (Har tun uchun $-35$ Morale va gipotermiya xavfi).
3. **Qaroqchilar va Reydlar Vahimasi:** Shahar devorlarining buzilishi, qo'riqchilar yo'qligi va fuqarolarning dushmanlar tomonidan o'ldirilishi ($-40$ Morale).
4. **Zulmkor Soliqlar (Extortionate Tax):** Daromad yoki hosilning $25\%$ dan ortiq qismini soliq sifatida tortib olish ($-40$ Morale).
5. **Karantinsiz Vabo va Ko'milmagan Jasadlar:** Ko'chalarda chiriyotgan murdalarning sassig'i va yuqumli o'lat ($-30$ Morale).

---

### 15.3. Ketish Logistikasi va Qaroqchilikka Qo'shilish Xavfi (Defection & Banditry)

- **Ketish Jarayoni:** Shaharni tark etishga qaror qilgan fuqaro o'z kasbiy vazifasini zudlik bilan tashlaydi, shaxsiy sumkasiga ozgina taom va kumushini soladi, eng yaqin shahar darvozasi yoki xarita chetiga qarab harakatlanadi (`FLEE / EMIGRATE` holati).
- **Qaroqchilikka O'tish Xavfi (Turn to Banditry):**
  Agar shahardan ketayotgan fuqaroning ruhiyati o'ta past bo'lsa ($Morale < 15$) hamda uning xarakterida g'azab yoki ochko'zlik (`Aggressive`, `Greedy`) mavjud bo'lsa, u shunchaki ketib qolmaydi:
  - U $45\%$ ehtimol bilan yaqin atrofdagi qaroqchilar to'dasiga qo'shiladi.
  - Sobiq fuqaro qaroqchilar yetakchisiga shahar himoyasining zaif nuqtalarini, oziq-ovqat omborlari joylashuvini va soqchilar sonini aytib beradi.
  - Bu keyingi qonli oydagi reydning aynan o'sha zaif darvozalarga yo'naltirilishiga sabab bo'ladi.

---

# 16. OILA VA QARINDOSHLIK TIZIMI (FAMILY & KINSHIP NETWORKS)

Har bir fuqaro shunchaki yolg'iz iqtisodiy birlik emas, balki murakkab ijtimoiy munosabatlar tarmog'iga ega bo'lgan oila a'zosidir. Ushbu munosabatlar fuqarolarning yashash joyini tanlashiga, ishlab chiqarishiga, meros qoldirishiga va ruhiyatiga tubdan ta'sir qiladi.

### 16.1. Oila Aloqalari Grafigi (Kinship Graph Data Structure)

Har bir fuqaroning ma'lumotlar modelida quyidagi qon-qarindoshlik rishtalari kuzatiladi:
- **Umr Yo'ldoshi (`Partner`):** Qonuniy nikohdagi eri yoki xotini.
- **Ota-Onasi (`Parents`):** Ota va ona (2 tagacha ID).
- **Farzandlari (`Children`):** Barcha tug'ilgan biologik bolalar ro'yxati.
- **Aka-Uka / Opa-Singillar (`Siblings`):** Bir ota-onadan tug'ilgan jigarlar.
- **Xonadon (`HouseholdID`):** Bitta tom ostida birgalikda yashovchi oila a'zolari to'plami.

**Munosabatlar Matritsasi ($Affinity \in [-100, +100]$):**
- Er-xotin o'rtasidagi doimiy mehr rishtasi har kuni birga ovqatlansa va bir to'shakda uxlasa $+0.5$ ga o'sadi (maksimal $+100$).
- Yaqin qarindoshlar bir xonadonda yashasa, shahar xavfsizligidan qoniqish $+15\%$ ga oshadi.
- Oiladagi janjallar (oziq-ovqat yetishmovchiligi, sovuq xona tufayli) munosabatlarni pasaytiradi.

---

### 16.2. Nikoh va Yangi Oila Qurish Qoidalari (Marriage Eligibility & Cohabitation)

Nikoh tuzilishi quyidagi qat'iy shartlar bajarilganda sodir bo'ladi:
1. **Yosh Cheklovi:** Ikkala nomzod ham 16 yoshdan oshgan va 48 yoshdan kichik bo'lishi lozim.
2. **Qarindoshlik Ta'qiqi:** To'g'ridan-to'g'ri ota-ona, farzand yoki o'zaro o'g'il/qiz jigarlar o'rtasida nikoh tuzilishi man etiladi.
3. **Munosabat Darajasi:** Ikkala fuqaroning bir-biriga bo'lgan ijobiy simpatiyasi $Affinity \ge 60$ bo'lishi kerak (bu ko'rsatkich Tavernada birga o'tirish, bozor maydonida muloqot va festivallarda oshadi).
4. **Boshpana Mavjudligi:** Shaharda kamida bitta bo'sh xususiy uy (yoki yangi juftlik uchun kengaytirilgan xona) mavjud bo'lishi shart.
5. **Nikoh To'yi (Wedding Feast):** Nikoh tuzilgach, mahalliy Cherkov/Soborda marosim o'tkaziladi va Tavernada kichik bayram qilinadi. Barcha mehmonlarga 24 soat davomida $+25$ Morale bonusi beriladi.
6. **Birga Yashash Qoidasi (Cohabitation):** Juftlik bir xonadon ID siga o'tadi va bitta ikki kishilik to'shakka joylashadi. Bir to'shakda uxlash tana haroratini $+2^\circ\text{C}$ ga ko'taradi va charchoqni $-15\%$ tezroq yozadi.

---

### 16.3. Yaqinlar Yo'qotilishi va Merosxo'rlik Mexanikasi (Kin Grief & Inheritance)

- **Motam va Qayg'u Debaffi (Grief):**
  - Oiladagi er/xotin yoki farzand vafot etganda, tirik qolgan yaqinlar darhol $-50$ Morale jarimasiga duchor bo'ladi.
  - Ushbu qayg'u 1 fasl (7 o'yin kuni) davomida chiziqli ravishda so'nib boradi ($Modifier_{grief}(t) = -50.0 \times (1.0 - \frac{t}{7})$).
  - Motam davrida fuqaroning ish unumdorligi $-25\%$ ga tushadi, u tez-tez shahar qabristoniga borib qabr ustida duo qiladi (`VISIT_GRAVE` xulq-atvori).
- **Merosxo'rlik (Inheritance Transfer):**
  - Fuqaro vafot etganda, uning cho'ntagidagi barcha shaxsiy kumush tangalar, asboblar va qimmatbaho buyumlar birinchi navbatda uning bevasiga o'tadi.
  - Agar bevasi bo'lmasa, to'ng'ich farzandiga (16 yoshdan katta bo'lsa), aks holda shahar yetimxonasiga yoki shahar xazinasiga topshiriladi.
- **Xun Da'vosi (Blood Feud / Vendetta):**
  - Agar fuqaro boshqa bir shahar fuqarosi tomonidan o'ldirilsa yoki zolimona qatl etilsa, marhumning aka-ukalari va farzandlari qotilga nisbatan $-100$ dushmanlik hissini shakllantiradi va imkon tug'ilganda shaxsiy qasos olishga intiladi.

---

# 17. UY-JOY TALABLARI (HOUSING QUALITY & ARCHITECTURAL SCORING)

Uy — fuqaroning jismoniy va ruhiy tiklanishining bosh qo'rg'onidir. Sovuq kulbalarda yashagan fuqarolar tez kasal bo'ladi va isyon ko'taradi, hashamatli tosh uylarda yashovchilar esa yuqori unumdorlik va sadoqat ko'rsatadi.

### 17.1. Algoritmik Uy Sifati Baholash Formulasi (Housing Quality Score Equation)

Har bir turar-joy binosi ichki voxellar tuzilishi, mebellari va haroratiga qarab $0.0$ dan $100.0$ ballgacha baholanadi:

$$Score_{house} = (S_{space} \times 0.20) + (S_{bed} \times 0.25) + (S_{warmth} \times 0.25) + (S_{materials} \times 0.15) + (S_{decor} \times 0.15)$$

Har bir komponentning hisoblanish qoidalari:
1. **Kenglik va Havo Hajmi ($S_{space} \in [0, 100]$):**
   $$S_{space} = \min\left(100.0, \; \frac{EnclosedAirVoxels}{Occupants \times 12} \times 100.0\right)$$
   Bunda har bir yashovchi uchun kamida 12 ta bo'sh havo voxeli ($12\text{ m}^3$) to'g'ri kelsa, maksimal 100 ball beriladi. Qisilib yashash bu ballni keskin tushiradi.
2. **To'shak Sifati ($S_{bed} \in [0, 100]$):**
   - Hamma yashovchiga taxta romli, pat yostiqli to'shak (`Comfortable Bed`): **100 ball**.
   - Quruq somon to'shak (`Straw Pallet`): **40 ball**.
   - Quruq yerda, tuproq ustida yotish (`Bare Ground`): **0 ball**.
3. **Issiqlik va Tutun Chiqarish ($S_{warmth} \in [0, 100]$):**
   - Tosh pechka (Hearth / Masonry Stove) va tom orqali tashqariga chiquvchi mo'ri (Chimney): **100 ball** (Harorat $+20^\circ\text{C}$, tutun yo'q).
   - Ochiq gulxan (Open Firepit / Brazier): **50 ball** (Harorat oshadi, ammo xona ichida tutun to'planadi, ko'z achishi va yo'tal debaffi beradi).
   - Isitish vositasi yo'q (muzdek xona): **0 ball**.
4. **Devor va Tom Qurilish Materiali ($S_{materials} \in [0, 100]$):**
   - Loy va qamishdan yasalgan chayla (Mud & Thatch): **20 ball**.
   - Yog'och xoda va taxtalar (Logs & Planks): **50 ball**.
   - Qoplama tosh devorlar (Cobblestone Masonry): **75 ball**.
   - Tarashlangan tosh bloklar va pishiq g'isht (Ashlar Stone & Fired Brick): **100 ball**.
5. **Ichki Bezak va Go'zallik ($S_{decor} \in [0, 100]$):**
   - Polga to'shalgan jun gilamlar, devoriy gobelenlar, javonlar, yog'och stol-stul, shamdonlar va sirlangan shisha derazalar (Glazed Glass Windows). Har bir bezak voxeli xonaga $+5$ dan $+15$ gacha dekor balli qo'shadi (maksimal 100).

---

### 17.2. Uy-joy Toifalari va O'yin Balansi (4-Tier Housing Classification Table)

| Toifa (Tier) | Ball Oralig'i | Uy Nomi va Konstruktsiyasi | Kunlik Morale Ta'siri | Homiladorlik / Tug'ilish Bonusi | Tungi Salomatlik Tiklanishi |
|---|---|---|---|---|---|
| **Tier 0** | $0 – 25$ | Qamish Kulba (Mud & Straw Hovel) | $-15$ (Doimiy norozilik) | $-50\%$ (Qattiq pasayish) | $+0 \text{ HP}$ (Tiklanmaydi) |
| **Tier 1** | $26 – 50$ | Yog'och Uycha (Timber Log Cabin) | $+5$ (Qoniqarli boshpana) | Bazaviy ($1.00\times$) | $+10 \text{ HP}$ har kecha |
| **Tier 2** | $51 – 75$ | Tosh Yarim-Karkas Uy (Stone Cottage)| $+15$ (Farovon xonadon) | $+20\%$ oshish | $+25 \text{ HP}$ har kecha |
| **Tier 3** | $76 – 100$ | Feodal Manor / Saroy (Manor Estate) | $+30$ (Aristokratik dabdaba) | $+50\%$ oshish | $+50 \text{ HP}$ (To'liq tiklanish)|

---

### 17.3. Tom Mustahkamligi va Ob-havodan Himoya (Roof Weatherproofing)

- **Yomg'ir va Qor O'tishi:** Agar tom voxellari qamish yoki eski taxtadan bo'lib, 3 fasldan ortiq ta'mirlanmasa, ularning suv o'tkazmasligi buziladi. Yomg'ir paytida xonada shilta ko'lmaklar paydo bo'ladi, issiqlik $-50\%$ ga soviydi va yashovchilarda shamollash (`Common Cold`) xastaligi boshlanadi.
- **Mo'ri Shamollatishi (Smoke Ventilation Physics):** Olov yoqilgan xonada tomga ochilgan havo yo'li yoki tosh mo'ri bo'lishi shart. Agar xona to'liq yopiq bo'lsa, xonadagi har bir fuqaro soatiga $5\text{ HP}$ yo'qotadi va `Smoke Asphyxiation` (Tutundan bo'g'ilish) holatiga tushadi.

---

# 18. FUQAROLAR EHTIYOJLARI (CITIZEN PHYSIOLOGICAL NEEDS SIMULATION)

Voxel Lord simulyatsiyasida fuqaroning hayotiyligi va mehnat unumdorligi doimiy ravishda hisoblab boriladigan fiziologik ehtiyojlar tizimiga asoslanadi. Har bir ehtiyoj o'ziga xos dinamik o'zgarish formulasiga ega.

### 18.1. Ochlik Mexanikasi va Sarflanish Tenglamasi (Hunger Drain)

Fuqaroning ochlik darajasi $Hunger \in [0.0, 100.0]$ oralig'ida bo'lib, 0 — to'q, 100 — qattiq ochlikni bildiradi.

$$\frac{d(Hunger)}{dt} = BaseHungerRate \times ActivityMult(State) \times TempMult$$

Bunda:
- $BaseHungerRate = \frac{100.0}{24 \times 60} \approx 0.0694 \text{ ball/daqiqa}$ (Fuqaro hech narsa qilmasa, 24 soatda to'liq ochiqadi).
- **Faoliyat Multiplikatori ($ActivityMult$):**
  - Uxlayotganda (`SLEEP`): $0.50\times$
  - Dam olayotganda / Gurunglashganda (`REST / SOCIALIZE`): $0.80\times$
  - Oddiy yurishda (`WALK`): $1.15\times$
  - Og'ir jismoniy mehnatda (Konchilik, Temirchilik, Yuk tashish): $1.60\times$
  - Jang maydonida yugurish va zarba berishda (`FIGHT / FLEE`): $2.20\times$
- **Harorat Ko'paytiruvchisi ($TempMult$):**
  Agar fuqaroning tana harorati $T_{body} < 35.0^\circ\text{C}$ ga tushsa, organizm o'zini isitish uchun kaloriyalarni ko'p yoqadi: $TempMult = 1.30\times$.

**Ochlik Bosqichlari va Salbiy Ta'sirlari:**
- $0 – 30$ (**To'q / Sated**): Hech qanday jarima yo'q, ruhiyat barqaror.
- $31 – 70$ (**Ishtaha Ochilgan / Peckish**): $-5$ Morale, fuqaro tushlik vaqtini kutadi.
- $71 – 90$ (**Och / Hungry**): $-20$ Morale, ish tezligi $-15\%$. Fuqaro eng yaqin oziq-ovqat omboriga borishni rejalashtiradi.
- $91 – 100$ (**Ocharchilik / Starving**): $-50$ Morale, ish tezligi $-40\%$. Fuqaro har soatda $2.5\text{ HP}$ salomatligini yo'qotadi va oxir-oqibat hushidan ketib halok bo'ladi.

---

### 18.2. Chanqoqlik Mexanikasi va Suv Ta'minoti (Thirst Drain)

Chanqoqlik darajasi $Thirst \in [0.0, 100.0]$:

$$\frac{d(Thirst)}{dt} = BaseThirstRate \times \left(1.0 + \max\left(0.0, \; \frac{T_{ambient} - 22.0}{10.0}\right)\right) \times ActivityMult$$

- $BaseThirstRate = \frac{100.0}{16 \times 60} \approx 0.1042 \text{ ball/daqiqa}$ (Suvsiz 16 soatda to'liq chanqaydi).
- **Issiq Havoda Bug'lanish:** Atrof-muhit harorati $22^\circ\text{C}$ dan oshganda har $10^\circ\text{C}$ uchun suv sarfi chiziqli oshib boradi (yozda $35^\circ\text{C}$ issiqda chanqoqlik $2.3\times$ tezlashadi).
- **Ichimlik Manbalari va Sifat Turlari:**
  - **Toza Quduq Suvi (Fresh Well Water):** Chanqoqni to'liq qondiradi, kasallik xavfi $0\%$.
  - **Taverna Eli / Qora Pivosi (Ale / Beer):** Chanqoqni bosadi, $+15$ Morale beradi va og'riqni kamaytiradi.
  - **Daryo Suvi (River Water):** Qoniqarli, ammo oqim yuqorisida shahar axlati bo'lsa $10\%$ ichburug' xavfi.
  - **Turg'un Botqoq Suvi (Stagnant Pond):** Chanqoqni qondiradi, ammo $60\%$ ehtimol bilan vabo (`Cholera / Dysentery`) yuqtiradi.
- **Suvsizlik Oqibati:** $Thirst = 100$ bo'lganda suvsizlanish (Dehydration) boshlanib, fuqaro har soatda $5.0\text{ HP}$ yo'qotadi va gandiraklab yuradi.

---

### 18.3. Issiqlik va Termoregulyatsiya Tenglamasi (Warmth & Thermoregulation)

Fuqaroning ichki tana harorati dinamik Nyuton sovish qonuniyati asosida simulyatsiya qilinadi:

$$\frac{dT_{body}}{dt} = \frac{(T_{ambient} + HeatSources + Insulation_{clothes}) - T_{body}}{\tau_{thermal}}$$

Bunda:
- Standart sog'lom tana harorati: $37.0^\circ\text{C}$.
- Issiqlik inertsiyasi doimiysi: $\tau_{thermal} = 45 \text{ daqiqa}$.
- **Kiyim Issiqlik Izolyatsiyasi ($Insulation_{clothes}$):**
  - Oddiy zig'ir ko'ylak (Linen Shirt): $+4^\circ\text{C}$
  - Qalin jun chakmon (Woolen Cloak): $+12^\circ\text{C}$
  - Mo'ynali po'stin (Heavy Fur Parka): $+22^\circ\text{C}$
- **Issiqlik Manbalari ($HeatSources$):**
  - Gulxan yonida (3 metr masofada): $+25^\circ\text{C}$
  - Uy ichidagi tosh kamin yonida: $+20^\circ\text{C}$
  - Qo'ldagi mash'ala (Torch): $+3^\circ\text{C}$

**Gipotermiya (Sovuq Qotish) Bosqichlari:**
- $35.0^\circ\text{C} \le T_{body} < 36.5^\circ\text{C}$ (**Sovuq Qotgan / Chilled**): $-10$ Morale, tishlar taqillaydi, mehnat tezligi $-10\%$.
- $32.0^\circ\text{C} \le T_{body} < 35.0^\circ\text{C}$ (**O'rtacha Gipotermiya**): $-30$ Morale, harakat tezligi $-35\%$, titroq tutadi, asboblar qo'ldan tushib ketishi mumkin.
- $T_{body} < 32.0^\circ\text{C}$ (**Og'ir Gipotermiya / Qon Muzlashi**): $-60$ Morale, fuqaro yerga yiqiladi, soatiga $10.0\text{ HP}$ yo'qotadi va 3 soat ichida qutqarilmasa vafot etadi.

---

### 18.4. Charchoq va Energiya Balansi (Fatigue & Energy Drain)

- **Uyg'oqlik Sarfi:** Fuqaro har daqiqada $+0.1042$ ball charchoq to'playdi (16 soatlik uzluksiz mehnatdan so'ng $Fatigue = 100$ ga yetadi).
- **Uyqudagi Tiklanish:**
  - Qulay uy to'shagida (`Bed`): daqiqasiga $-0.60$ ball (to'liq tiklanish 2.8 soatda / real vaqtda 2.8 daqiqada amalga oshadi).
  - Somon ustida yoki polda: daqiqasiga $-0.25$ ball.
- **Charchoq Oqibati:** $Fatigue > 90$ bo'lganda fuqaro har qanday ishni to'xtatadi va eng yaqin xavfsiz yerda to'g'ridan-to'g'ri yerga yiqilib uxlab qoladi (`COLLAPSE_SLEEP`).

---

# 19. CITIZEN AI ARXITEKTURASI (AI ARCHITECTURE & 10-STATE CANONICAL FSM)

Voxel Lord fuqarolarining xulq-atvori ikki qavatli gibrid arxitekturaga tayanadi: yuqori bosqichli kun tartibi rejalashtiruvchisi (Utility-Based High-Level Planner) va pastki bosqichli deterministik Ierarxik Chekli Avtomat (Hierarchical Finite State Machine — HFSM). Tizim 10 ta kanonik holatni (Canonical States: `Walk`, `Work`, `Eat`, `Sleep`, `Fight`, `Flee`, `Socialize`, `Heal`, `Transport`, `Rest`) to'liq qamrab oladi.

### 19.1. Ierarxik Qaror Qabul Qilish va Interrupt Darajalari

Fuqaro har bir simulyatsiya qadamida o'z holatini quyidagi ustuvorlik zinapoyasi bo'yicha baholaydi:
- **Priority Tier 0 (Favqulodda Falokat — Emergency):** O'lim xavfi, yong'in sodir bo'lishi, yirtqich hayvon yoki dushman qilich zarbasi ostida qolish. Har qanday joriy holatni bir zumda uzadi (Interrupt).
- **Priority Tier 1 (Kritik Fiziologik Ehtiyojlar — Critical Survival):** Ochlik $>85$, Chanqoqlik $>85$, Tana harorati $<33^\circ\text{C}$, Qon ketish travmasi.
- **Priority Tier 2 (Rejalashtirilgan Mehnat va Uyqu — Scheduled Shift):** Tonggi 06:00–18:00 ish smenasi, tungi 21:00–05:00 uyqu soati.
- **Priority Tier 3 (Ijtimoiy va Bo'sh Vaqt — Secondary / Leisure):** Taverna, suhbat, ibodat, shahar maydonida sayr qilish.

---

### 19.2. 10 Asosiy Holatli FSM O'tish Jadvali (Complete 10-State FSM Transition Matrix)

| Holat (State) | Kirish Shartlari (Entry Conditions) | Holat Ichidagi Fizik va Animatsion Xatti-harakat | Uzilish Triggerlari (Interrupt Conditions) | Chiqish Shartlari (Exit Conditions) | Keyingi Holat (Next State) |
|---|---|---|---|---|---|
| **1. WALK (Yurish)** | Belgilangan nuqtaga (Ishxona, To'shak, Ombor, Quduq) yo'l talab qilinganda. | `NavigationAgent3D` orqali marshrut hisoblaydi. Relyef koeffitsiyenti qo'llanadi (Loyda 0.8x, Tosh yo'lda 1.35x, Katta yo'lda 1.6x). | Dushman ko'rinsa $\rightarrow$ FLEE/FIGHT; Yong'in chiqsa $\rightarrow$ WORK (O'chirish); Ochlik $>85 \rightarrow$ EAT. | Mo'ljal masofasiga yetib kelindi ($\text{masofa} \le 1.2\text{m}$). | Mo'ljaldagi maqsadli holat (WORK, EAT, SLEEP, TRANSPORT). |
| **2. WORK (Mehnat)** | Ish smenasida (06:00–18:00) o'z ish stoliga yetib kelgan; zarur asbobi mavjud. | Ish animatsiyasini ijro etadi. Har bir tsiklda progressni oshiradi: $\Delta P = \Delta t \cdot Skill \cdot ToolQuality$. Ochlik va charchoq $1.5\times$ tezlashadi. | Xavf $\rightarrow$ FLEE/FIGHT; Yong'in $\rightarrow$ O'chirish; Ochlik/Chanqoqlik $>85 \rightarrow$ EAT; Charchoq $>90 \rightarrow$ REST. | Ishlab chiqarish sikli tugadi, mahsulot chiqdi yoki soat 18:00 bo'ldi. | TRANSPORT (mahsulotni omborga eltish) yoki REST/SOCIALIZE. |
| **3. EAT (Ovqatlanish)** | Ochlik $>60$ yoki rejadagi ovqat vaqti (12:00 tushlik, 19:00 kechki ovqat). | Eng yaqin oziq-ovqat ombori yoki xonadon qutisiga boradi. 1 porsiya taom olib, 8 sekund yeyish animatsiyasini o'ynaydi. Ochlikni tiklaydi. | To'g'ridan-to'g'ri jangovar hujum bo'lsa $\rightarrow$ FIGHT/FLEE; Yong'in trevogasi. | Ochlik 0 ga tushdi yoki oziq-ovqat to'liq yeb bo'lindi. | WORK (kunduzi bo'lsa) yoki SOCIALIZE / SLEEP (kechqurun bo'lsa). |
| **4. SLEEP (Uxlagani Yotish)**| Tun kirdi (21:00–05:00) yoki o'ta yuqori charchoq ($Fatigue > 90$). | O'z to'shagiga yotadi (yo'q bo'lsa polda). Yotish animatsiyasi. Charchoq soatiga $-36$ ball kamayadi, salomatlik tiklanadi. | Uyga o't ketsa; Qaroqchilar eshikni buzganda; Shahar trevoga qo'ng'irog'i chalinsa $\rightarrow$ FLEE/FIGHT. | Uyg'onish soati yetdi (05:30) va Charchoq $<5.0$. | EAT (nonushta) $\rightarrow$ WALK $\rightarrow$ WORK. |
| **5. FIGHT (Jang Qilish)** | Dushman ko'rish zonasida; Fuqaro askar/soqchi yoki qochishga yo'li yo'q fuqaro bo'lsa. | Qurol va qalqonni chiqaradi. Jangovar AI tsiklini boshlaydi: zarba berish, qalqon bilan to'sish, aylanib o'tish (strafe). | Salomatlik $<20\%$ va harbiy ruhiyat sinsa $\rightarrow$ FLEE; Komandir chekinish buyursa $\rightarrow$ FLEE. | Dushman o'ldirildi, hushidan ketdi yoki qochib ketdi. | HEAL (yarador bo'lsa) yoki GUARD / WALK. |
| **6. FLEE (Qochish)** | Qurolsiz fuqaro 18m masofada dushman ko'rsa, yoki askar ruhiyati $Morale < 20$ bo'lib vahimaga tushsa. | Dushmandan teskari yo'nalishda eng yaqin qal'a devori, qasr qo'rg'oni yoki mustahkam darvozaga qarab $1.4\times$ tezlikda yuguradi. | Yo'l to'silib burchakka qisilsa $\rightarrow$ FIGHT (jonsarak himoya); Salomatlik 0 bo'lsa $\rightarrow$ KNOCKED OUT. | Xavfdan $35\text{m}$ uzoqlashdi va xavfsiz devor ichiga kirdi. | REST / HEAL / HIDE. |
| **7. SOCIALIZE (Muloqot)** | Kechki bo'sh vaqt (18:00–21:00); Ochlik $<40$, Charchoq $<70$. | Taverna, qishloq qudug'i yoki shahar maydoniga boradi. Boshqa fuqarolar bilan gaplashadi, pivo ichadi. Morale $+15$ oshadi. | Shahar trevogasi $\rightarrow$ FLEE; Uyqu vaqti (21:00) $\rightarrow$ SLEEP; Ochlik $>75 \rightarrow$ EAT. | Muloqot vaqti (15–30 o'yin daqiqasi) tugadi yoki taverna yopildi. | WALK $\rightarrow$ SLEEP. |
| **8. HEAL (Davolanish)** | Qon ketish, suyak sinishi, jiddiy jarohat yoki Salomatlik $<60.0$ bo'lganda. | Eng yaqin gospitalga yoki o'z to'shagiga boradi. Tabib unga bog'ich va malham qo'yishini kutadi. Tinch holatda soatiga $+5\text{ HP}$ tiklanadi. | Gospitalga o't ketsa yoki dushman bostirib kirsa $\rightarrow$ FLEE. | Salomatlik $\ge 95\%$ ga yetdi va barcha salbiy travma statuslari ketdi. | WORK yoki WALK. |
| **9. TRANSPORT (Yuk Tashish)**| Ish joyida xomashyo tugasa yoki tayyor mahsulot to'lib ketganda, qurilish joyiga material kerak bo'lganda. | `ItemReservationManager` orqali ashyoni band qiladi, borib ko'taradi (yoki aravaga ortadi), omborga eltadi va bo'shatadi. | Yo'lda dushman uchrasa $\rightarrow$ yukni tashlab FLEE; Yong'in chiqsa $\rightarrow$ yukni tashlab WORK. | Yuk belgilangan ombor yoki dastgoh katagiga muvaffaqiyatli topshirildi. | WORK (avvalgi ishiga qaytish) yoki keyingi yuk tashish buyrug'i. |
| **10. REST (Nafas Rostlash)**| Charchoq $70–89$ oralig'ida bo'lsa, yoki og'ir mehnatda Stamina to'liq tugaganda. | O'rindiqqa, yog'och xodaga yoki yerga o'tiradi. 5–10 daqiqa harakatsiz turadi. Stamina soniyasiga $+2.0$ tiklanadi, charchoq to'planishi to'xtaydi. | Dushman hujumi $\rightarrow$ FLEE/FIGHT; Favqulodda yong'in signali. | Stamina $100\%$ to'ldi va Charchoq $<50$ ga tushdi. | Oldingi to'xtatilgan WORK yoki WALK holatiga qaytish. |

---

### 19.3. Godot 4 GDScript Arxitektura Modeli (`CitizenFSM.gd`)

```gdscript
# res://scripts/ai/citizen_fsm.gd
class_name CitizenFSM
extends Node

enum State {
	WALK,
	WORK,
	EAT,
	SLEEP,
	FIGHT,
	FLEE,
	SOCIALIZE,
	HEAL,
	TRANSPORT,
	REST
}

signal state_changed(old_state: State, new_state: State)

@export var current_state: State = State.REST
var previous_state: State = State.REST
var state_time: float = 0.0

@onready var citizen: Citizen = get_parent() as Citizen

func _physics_process(delta: float) -> void:
	state_time += delta
	check_emergency_interrupts()
	
	match current_state:
		State.WALK:
			_process_walk(delta)
		State.WORK:
			_process_work(delta)
		State.EAT:
			_process_eat(delta)
		State.SLEEP:
			_process_sleep(delta)
		State.FIGHT:
			_process_fight(delta)
		State.FLEE:
			_process_flee(delta)
		State.SOCIALIZE:
			_process_socialize(delta)
		State.HEAL:
			_process_heal(delta)
		State.TRANSPORT:
			_process_transport(delta)
		State.REST:
			_process_rest(delta)

func transition_to(new_state: State) -> void:
	if current_state == new_state:
		return
	
	_exit_state(current_state)
	previous_state = current_state
	current_state = new_state
	state_time = 0.0
	_enter_state(new_state)
	state_changed.emit(previous_state, current_state)

func check_emergency_interrupts() -> void:
	# Tier 0 Interrupt: Dushman tahdidi
	if citizen.perceived_threat != null and current_state != State.FIGHT and current_state != State.FLEE:
		if citizen.is_combatant():
			transition_to(State.FIGHT)
		else:
			transition_to(State.FLEE)
		return
	
	# Tier 1 Interrupt: O'lim darajasidagi ochlik
	if citizen.hunger >= 90.0 and current_state != State.EAT and current_state != State.FLEE:
		transition_to(State.EAT)
		return
```

---

# 20. VAZIFALAR USTUVORLIGI (TASK PRIORITY & UTILITY DISPATCHING)

Shaharda yuzlab topshiriqlar (daraxt kesish, kon qazish, hosil o'rish, tosh tashish, yaradorlarni davolash) vujudga kelganda, markaziy dispetcher har bir fuqaroga eng maqbul vazifani Matematik Foydalilik Funksiyasi (Utility Function) orqali taqsimlaydi.

### 20.1. Vazifalarni Baholash Foydalilik Funksiyasi (Job Utility Function)

Dispetcher har bir `(Citizen, Task)` juftligi uchun quyidagi ko'p faktorli ballni hisoblaydi:

$$Score(Citizen, Task) = Priority_{base}(Task) \times W_{priority} + Skill(Citizen, Task.type) \times W_{skill} - Distance(Citizen, Task.pos) \times W_{dist} - Fatigue(Citizen) \times W_{fatigue}$$

Bunda tizim vazn koeffitsiyentlari:
- $W_{priority} = 40.0$: Vazifaning shahar uchun hayotiy muhimlik vazni.
- $W_{skill} = 25.0$: Fuqaroning ushbu kasb bo'yicha mahorat ko'rsatkichi ($Skill \in [0, 100]$). Tajribali usta uzoqroqda bo'lsa ham unga topshiriladi.
- $W_{dist} = 0.50$: Har bir voxel-metr masofa uchun ball ayiriladi (ortiqcha yurish vaqtini tejash).
- $W_{fatigue} = 0.30$: Charchagan fuqaro og'ir jismoniy vazifalarga tanlanmaydi.

---

### 20.2. 7 Pog'onali Vazifalar Matritsasi (7-Tier Task Priority Base Matrix Table)

| Ustuvorlik Toifasi | Bazaviy Ball ($Priority_{base}$) | Vazifa Misollari | To'xtatish Mumkinligi (Interruptible?) | Javob Berish Vaqti Cheklovi |
|---|---|---|---|---|
| **1. Favqulodda Falokat (Emergency)** | 1,000 | Yong'inni chelak bilan o'chirish, yirtqich hujumini qaytarish, qon ketayotgan yaradorga jarrohlik. | Yo'q (Qat'iy blokirovka) | Zudlik bilan (1–2 sekund) |
| **2. Zudlik Harbiy (Urgent Military)** | 800 | Qal'a devoridagi merlonlarni egallash, tushirilgan panjarani yopish, devorni buzayotgan taranga hujum. | Faqat Emergency tomonidan | 5 sekund ichida |
| **3. Sanitariya va Tibbiyot (Sanitation)**| 600 | Chiriyotgan murdalarni ko'chadan yig'ish, o'lat bemorlarini karantinga olish, dori damlash. | Ha, Harbiy vazifalar bilan | 60 soniya ichida |
| **4. Kritik Omon Qolish (Critical Survival)**| 450 | Qorasovuq tushishidan oldin g'allani o'rib olish, granari bo'shab qolganda non yopish, qishki o'tin. | Ha | 2 o'yin soati ichida |
| **5. Standart Ishlab Chiqarish (Production)**| 250 | Rudadan temir eritish, bolta va qilich yasash, o'rmondan yog'och tilish, tosh yo'nish. | Ha | Standart ish kuni tartibida |
| **6. Logistika va Tashish (Hauling)** | 180 | Quymalarni qurolxonaga tashish, unni nonvoyxonaga eltish, bozor do'konlarini to'ldirish. | Ha | Navbat bilan bajariladi |
| **7. Bezatish va Fuqarolik (Civic)** | 80 | Tosh ko'chalarga mayda tosh yotqizish, haykallar o'ymakorligi, manzarali gulzorlar ekish. | Ha | Bo'sh vaqtda |

---

### 20.3. Zaxiralash Boshqaruvi va Poyga Oldini Olish (`ItemReservationManager`)

Bir nechta fuqarolarning bitta buyumga yoki cheklangan resursga birdaniga yugurishini (Race Condition) oldini olish uchun yagona markazlashtirilgan zaxira menejeri ishlaydi:
- Fuqaro biror xomashyoni olishga qaror qilganda, u `ItemReservationManager.reserve_item(item_id, citizen_id)` chaqiruvini yuboradi.
- Agar boshqa fuqaro avvalroq uni band qilgan bo'lsa, dispetcher zudlik bilan ikkinchi eng yaqin mos xomashyoni qidiradi.
- Agar fuqaro yo'lda dushmanga duch kelib qochsa yoki vafot etsa, uning band qilgan buyumlari 15 sekundlik `timeout` o'tgach yana umumiy havzaga qaytariladi.

---

# 21. KASBLAR TIZIMI (FEUDAL PROFESSION CATALOG & WORK SCHEDULES)

Voxel Lord feodal iqtisodiyoti chuqur ixtisoslashgan mehnat taqsimotiga tayanadi. Shaharda 23 ta kanonik feodal kasb mavjud bo'lib, ularning har biri o'z ish o'rni, asbobi, malaka talablari va kun tartibiga ega.

### 21.1. Mehnat Tashkiloti va Smena Qoidalari

- **Ish Vaqti:**
  - Kunduzgi smena: 06:00 dan 18:00 gacha (12 o'yin soati = 12 real daqiqa).
  - Tungi soqchilik smenasi: 18:00 dan 06:00 gacha (Qorovullar, tungi patrul).
- **Asbob Majburiyati:** Fuqaro o'z kasbiga oid asbobsiz ishlay olmaydi (12-bo'limga qarang).
- **Kasb Tanlash:** Fuqarolar o'zlarining eng yuqori mahoratiga qarab avtomatik tayinlanadi yoki Hukmdor tomonidan Royal Ledger orqali majburiy tayinlanishi mumkin.

---

### 21.2. Feodal Kasblar Master Katalogi (Comprehensive Feudal Job Catalog Matrix)

| Kasb Nomi (O'zbekcha / Inglizcha) | Asosiy Ish Joyi (Workstation) | Talab Qilinadigan Asbob | Asosiy Mahorat (Primary Skill) | Ish Smenasi | Bazaviy Mehnat Unumi / Mahsulot |
|---|---|---|---|---|---|
| **Dehqon (Farmer)** | Ekin Dalasi / Omoch | O'roq va Ketmon (Hoe & Scythe) | Agriculture | 06:00 – 18:00 | Kuniga 8 bog' g'alla / sabzavot ekish va yig'ish. |
| **Tegirmonchi (Miller)** | Shamol / Suv Tegirmoni | Qo'l mehnati / Richag | Milling | 07:00 – 18:00 | Kuniga 16 qop oliy navli un va kepak yanchish. |
| **Nonvoy (Baker)** | Nonvoyxona Pechi | Nonvoy kuragi (Baking Peel) | Baking | 05:00 – 16:00 | Kuniga 24 ta issiq xushbo'y non pishirish. |
| **Pivochi (Brewer)** | Pivo Qaynatish Xumi | Yog'och kurak, Qozon | Brewing | 08:00 – 18:00 | Kuniga 12 bochka to'yimli ale va pivo tayyorlash. |
| **O'rmonchi (Woodcutter)**| O'rmon / Yog'och Tilish Maydoni| Yog'ochkesar Boltasi (Axe) | Forestry | 06:00 – 17:00 | Kuniga 12 ta eman yoki qarag'ay xodasi tayyorlash. |
| **Duradgor (Carpenter)** | Duradgorxona Dastgohi | Arra, Randa va Bolg'a | Carpentry | 07:00 – 18:00 | Taxtalar, mebel, aravachalar va qurilish bloklari. |
| **Konchi (Miner)** | Shaxta / Qazilma Galereyasi | Cho'kich / Kulang (Pickaxe) | Mining | 06:00 – 18:00 | Kuniga 10 ta ruda, ko'mir yoki granit qazib olish. |
| **Erituvchi (Smelter)** | Domna Pechi / Bloomery | Olov qisqichi, Temir kurak | Metallurgy | 06:00 – 19:00 | Kuniga 8 ta tozalangan temir yoki po'lat quyma quyish. |
| **Temirchi (Blacksmith)** | Temirchilik Sandoni (Anvil) | Temirchilik Bosqoni (Hammer) | Blacksmithing | 07:00 – 18:00 | Kuniga 4 ta sifatli mehnat quroli yoki mixlar yasash. |
| **Quroloz (Armorer/Weaponsmith)**| Qal'a Qurolxonasi | Anvil, Charxtosh va Qisqich | Armorsmithing | 07:00 – 18:00 | Qilichlar, nayzalar, zanjir va plita sovutlar. |
| **Tosh Yo'nuvchi (Mason)**| Tosh Kesish Maydoni | Tosh qalamchasi va Bolg'a | Masonry | 06:00 – 18:00 | Qal'a devorlari va poydevor uchun tarashlangan tosh. |
| **To'quvchi (Weaver)** | To'quvchilik Dastgohi | Mokki (Shuttle), Ip urchug'i | Tailoring | 08:00 – 18:00 | Kuniga 6 to'p zig'ir yoki jun mato to'qish. |
| **Ko'nchi (Tanner)** | Teri Oshlash Xumlari | Teri qirg'ich pichoq | Leatherworking | 07:00 – 17:00 | Xom teridan qalin sovut va etikka yaraydigan charm. |
| **Tabib (Doctor/Herbalist)**| Gospital / Dorixona | Jarrohlik pichog'i, Qorishma hovoncha | Medicine | 24 soat navbatchilik | Yaradorlarni bog'lash, qon to'xtatish, dori berish. |
| **G'assol (Gravedigger)**| Murdaxona / Qabriston | Bel (Shovel), Murda aravasi | Undertaking | Har doim (Chaqiruvda)| Ko'chalardagi murdalarni yig'ish, qabr qazish, ko'mish. |
| **Shahar Soqchisi (Guard)**| Darvozaxona / Patrul Yo'li | Nayza va Qalqon (Spear & Shield)| Combat | 18:00 – 06:00 (Tungi)| Shahar ichki xavfsizligi, o'g'rilarni ushlash. |
| **Piyoda Askar (Soldier)**| Kazarma / Mudofaa Devori | Qilich va Zirh (Sword & Armor)| Combat | Doimiy saf tayyorgarligi| Qamal va reydlarni qaytarish, jangovar yurishlar. |
| **Kamonchi (Archer)** | Merlon Minorasi / Otish Maydoni| Jangovar Kamon va Sadaq | Marksmanship | 06:00 – 18:00 | Masofadan dushmanni yo'q qilish, devor himoyasi. |
| **Ritsar (Knight)** | Ritsarlar Zali / Otxona | Jangovar Ot, Po'lat Qilich, Nayza| Chivalry & Combat | Elita qo'shin | Otdagi yengilmas zarba, jangda fuqarolar ruhiyatini oshirish. |
| **Ruhoniy (Priest)** | Qishloq Cherkovi / Sobor | Muqaddas Kitob, Tutatqich | Theology | 06:00 – 20:00 | Diniy ibodatlar, nikoh marosimlari, qabrlarni muqaddaslash. |
| **Baxshi (Bard)** | Taverna / Shahar Maydoni | Lute (Tanbur), Skripka | Performance | 17:00 – 23:00 | Musiqa chalish, qo'shiq aytish, shaharda Morale $+15$. |
| **Bailiff (Shahar Boshqaruvchisi)**| Shahar Kengashi Zali | Pat-qalam, Hisob daftari | Stewardship | 08:00 – 17:00 | Soliq yig'ish, jinoyatchilarni sud qilish, hisobotlar. |
| **Savdogar (Merchant)** | Bozor Rastasi / Karvonsaroy | Tarozu va Tangalar | Commerce | 08:00 – 17:00 | Chet el karvonlari bilan savdo qilish, resurs ayirboshlash. |

---

# 22. DIPLOMATIYA, RAQIB FRAKTSIYALAR VA MULTIPLAYER (CO-OP)

Voxel Lord feodal dunyosida koloniya yakkalanib yashamaydi. Mintaqaviy xarita (Overworld Map) procedural yaratilganda o'yinchi atrofida mustaqil, iqtisodiy va harbiy jihatdan o'zini o'zi ta'minlovchi 4 ta yirik feodal fraktsiya qaror topadi. Diplomatiya tizimi shunchaki menyudagi tugmalar emas, balki real vaqt rejimida karvonlar qatnovi, chegara postlari, josuslik operatsiyalari, o'lpon to'lovlari va vayron bo'luvchi venzel qamallaridan iborat ko'p qatlamli simulyatsiyadir.

## 22.1. Feodal Fraktsiya Arxeotiplari va Dunyodagi Geopolitik Kuchlar

Har bir fraktsiya o'zining ijtimoiy-siyosiy tuzilmasi, afzal ko'rgan biomi, iqtisodiy resurslar monopoliyasi va o'ziga xos harbiy doktrinasiga ega:

1. **Sohil Savdogarlari Ligasi (The League of Coastal Merchants):**
   - **Tuzilmasi va Boshqaruvi:** Boy savdogar oligarxlar kengashi (Merchant Guilds) tomonidan boshqariladigan plutokratiya. Asosiy qarorgohi qirg'oq bo'yi estuariyalari va unumdor tekisliklarda joylashgan.
   - **Iqtisodiy Monopoliya:** Dengiz savdosi, xorijiy ziravorlar, ipak matolar, sayqallangan shisha idishlar, dengiz tuzi va dori-darmonlar. Bozor narxlarini manipulyatsiya qilish va kredit foizlarini belgilash qobiliyatiga ega.
   - **Harbiy Doktrina:** Yollanma arbaletchilar (Mercenary Crossbowmen), qirg'oq floti, to'siq pikelari va qimmatbaho plitali gvardiya. Urushda uzoq qamal qilishdan ko'ra iqtisodiy embargo, karvon yo'llarini to'sish va qaroqchilarni yollashni afzal biladi.
   - **Diplomatik Reaktsiyasi:** Past bojxona to'lovlari va ochiq chegaralarni yoqtiradi. Agar o'yinchi ularning karvonlariga hujum qilsa yoki savdo shartnomasini buzsa, darhol qattiq iqtisodiy sanktsiyalar joriy etadi.

2. **Shimoliy Temir Harbiy Feodallari (The Northern Iron Warlords):**
   - **Tuzilmasi va Boshqaruvi:** Shon-sharaf, kuch va jangovar tajribaga tayanuvchi harbiy gertsogliklar. Qarorgohlari baland tog' cho'qqilarida, basalt va granit qoyalar ustiga qurilgan qasrlarda joylashgan.
   - **Iqtisodiy Monopoliya:** Yuqori sifatli temir rudasi, koks ko'miri, qattiq po'lat xomashyosi, quyma sovutlar, og'ir qurollar va tosh kesish texnologiyalari.
   - **Harbiy Doktrina:** Og'ir ritsarlar (Knights), zarbdor ikki qo'lli qilichbozlar (Shock Infantry), mustahkam toshbuzar taranlar (Battering Rams) va og'ir katapultalar.
   - **Diplomatik Reaktsiyasi:** Har mavsum qat'iy o'lpon talab qiladi. O'yinchi armiyasining qudratini baholaydi — agar o'yinchi kuchsiz bo'lsa, o'lponni oshiradi va qamal urushini boshlaydi; agar o'yinchi harbiy kuchi teng yoki ustun bo'lsa, hurmat ko'rsatib sulh tuzadi.

3. **Muqaddas Quyosh Diniy Ordeni (The Holy Sun Order):**
   - **Tuzilmasi va Boshqaruvi:** Oliy Inkvizitor va Patriarx boshchiligidagi teokratik orden. Shaharlari oppoq marmar ibodatxonalar, soborlar va baland qo'ng'iroqxonalardan iborat.
   - **Iqtisodiy Monopoliya:** Marmar toshlari, muqaddas shamlar, asalarichilik mumi, monastir uzumzorlari va sharoblari, diniy yozuvlar va muqaddas artefaktlar.
   - **Harbiy Doktrina:** Templar ritsarlari, intizomli nayzabardorlar va yonuvchi neft snaryadlarini otuvchi muqaddas trebuchetlar.
   - **Diplomatik Reaktsiyasi:** O'yinchidan ibodatxonalar qurishni va diniy soliqlarni to'lashni talab qiladi. Qora jodu, qabrlarni qazish, bidsat yoki cherkov mulkiga daxl qilish holatlarini mutlaq kechirmaydi va darhol muqaddas urush (Crusade) e'lon qiladi.

4. **Dasht Otliqlari Qabilasi (The Steppe Horse Clans):**
   - **Tuzilmasi va Boshqaruvi:** Dasht xonlari va beklari ittifoqi. Harakatchan o'tovlar, ot boqiladigan yaylovlar va quruq dasht biomlarida yashaydi.
   - **Iqtisodiy Monopoliya:** Elita zotdor jangovar otlar, murakkab kompozit egik kamonlar, charmdan ishlangan engil sovutlar, qimiz va jun mahsulotlari.
   - **Harbiy Doktrina:** Tezkor otliq kamonchilar (Horse Archers), dasht nayzabardorlari. Taktikasi — to'g'ridan-to'g'ri devorga urilmasdan, tezkor pistirmalar, tashqi qishloqlarni talash va ta'minot zanjirlarini uzish.
   - **Diplomatik Reaktsiyasi:** Yaylov huquqlarini hurmat qilishni talab qiladi. Agar o'yinchi chegarasini dasht yaylovlariga qarab noqonuniy kengaytirsa, tezkor otliq bosqinlari bilan javob qaytaradi.

| Fraktsiya Nomi | Afzal Biomi | Asosiy Monopoliya Mahsulotlari | Harbiy Elita Birligi | Diplomatik Asosiy Talab |
|---|---|---|---|---|
| **League of Coastal Merchants** | Qirg'oq va Tekislik | Ziravorlar, Shisha, Ipak, Dori-darmon | Yollanma Arbaletchilar | Past savdo boji, erkin port |
| **Northern Iron Warlords** | Qoyali Tog'lar va Tayga | Temir, Po'lat, Koks, Toshbuzar Taran | Og'ir Plitali Ritsarlar | Mavsumiy oltin/kumush o'lpon |
| **Holy Sun Order** | Quyoshli Tekislik va Vodiy | Marmar, Mum, Monastir Sharobi, Kitoblar | Templar Paladinlari | Sobor qurish, diniy bay'at |
| **Steppe Horse Clans** | Quruq Dasht va Yaylov | Jangovar Otlar, Kompozit Kamon, Jun | Otliq Kamonchilar | Yaylov chegaralari daxlsizligi |

## 22.2. Xalqaro Aloqalar Spektri, O'lpon (Tribute) va Savdo Arbitraji

### 22.2.1. Munosabatlar Shkalasi (-100 dan +100 gacha)

O'yinchi va har bir fraktsiya o'rtasidagi aloqalar $-100$ dan $+100$ gacha bo'lgan sonli qiymat bilan o'lchanadi va 7 ta aniq pog'onaga ajratiladi:

| Pog'ona | Holat Nomi | Diapazon | Iqtisodiy Qoidalar | Chegara va Harakat Huquqi | Harbiy Harakatlar |
|---|---|---|---|---|---|
| **Tier 1** | Urush (War) | $[-100, -60]$ | Savdo butunlay to'xtatilgan, barcha aktivlar musodara qilinadi. | Chegaralar yopiq, ko'rilgan zahoti o'ldirish buyrug'i. | Doimiy harbiy qamallar, karvonlarni talash, qasrlarni buzish. |
| **Tier 2** | Dushmanlik (Hostile) | $[-59, -20]$ | To'liq iqtisodiy embargo, tovarlar almashinuvi taqiqlanadi. | Fuqarolar va elchilar chegaradan qaytariladi. | Chegara to'qnashuvlari, doimiy josuslik va diversiyalar. |
| **Tier 3** | Sovuq / Noqulay (Unfriendly) | $[-19, -1]$ | Eksport va import tovarlariga $+50\%$ og'ir bojxona solig'i. | Qurolli otryadlar o'tishi qat'iyan taqiqlanadi. | Diplomatik tahdidlar, o'lpon talablarini oshirish. |
| **Tier 4** | Neytral (Neutral) | $[0, +19]$ | Standart bozor narxlari va bazaviy tariflar ($0\%$ ustama). | Tinch fuqarolar va tijorat karvonlari erkin o'tadi. | Qo'shinlar neytral zonalarda to'qnashmaydi. |
| **Tier 5** | Do'stona (Friendly) | $[+20, +59]$ | Savdo bojlariga $-25\%$ chegirma, chegara bozorlariga ruxsat. | Hujum qilmaslik pakti (NAP), hududiy o'tish huquqi. | Razvedka ma'lumotlarini almashish, qaroqchilarga qarshi kurash. |
| **Tier 6** | Harbiy Ittifoq (Allied) | $[+60, +89]$ | Maxsus imtiyozli savdo, nodir texnologiyalar chizmalarini berish. | To'liq harbiy koridor, istehkomlardan birgalikda foydalanish. | Birgalikda mudofaa va umumiy dushmanga qarshi qo'shma qamal. |
| **Tier 7** | Qaramlik / Konfederatsiya | $[+90, +100]$ | O'yinchiga har mavsum $15\%$ sof daromad solig'i to'laydi. | To'liq birlashgan hududiy suverenitet. | Fraktsiya qo'shini o'yinchi amriga bo'ysunadi. |

Munosabatlar dinamikasi o'zgaruvchan bo'lib, faol aloqalar bo'lmaganda tabiiy ravishda neytral nuqtaga ($0$) qarab so'nib boradi:
$$\frac{dR}{dt} = -\lambda_{decay} \cdot (R - R_{neutral}) + \sum \Delta R_{actions}$$
Bunda $\lambda_{decay} = 0.02$ ball/kun. Ijobiy amallar (karvon savdosi hajmi $+1$ dan $+5$ gacha, o'lponni vaqtida to'lash $+12$, hadyalar berish $+10$) munosabatni oshirsa, tajovuzkorlik (chegara buzish $-15$, josuslik fosh bo'lishi $-50$, o'lpon to'lamaslik $-30$) uni keskin pasaytiradi.

### 22.2.2. Mavsumiy O'lpon (Tribute Demand) Tenglamasi

Agressiv Harbiy Feodallar va Diniy Ordenlar o'yinchidan mavsumiy o'lpon talab qiladi. Talab qilinadigan kumush tangalar miqdori quyidagi formula asosida hisoblanadi:

$$\text{Tribute}_{\text{demand}} = K_{base} \cdot \left(\frac{\text{Power}_{warlord}}{\text{Power}_{player} + 1.0}\right)^{1.35} \cdot \left(\text{Treasury}_{player}^{0.55} + 0.1 \cdot \text{Population}_{player}\right) \cdot \left(1.0 - \frac{\text{Distance}}{D_{max}}\right)$$

Formuladagi parametrlar:
- $K_{base} = 50.0$ (o'lponning bazaviy koeffitsiyenti).
- $\text{Power}_{warlord}$ va $\text{Power}_{player}$: Tomonlarning umumiy harbiy kuchi (askarlar soni, qurol sifati va qal'a darajasi yig'indisi).
- $\text{Treasury}_{player}$: O'yinchining xazinasidagi joriy kumush tanga zaxirasi.
- $\text{Population}_{player}$: Shahardagi jami fuqarolar soni.
- $\text{Distance}$: O'yinchi poytaxti bilan lord qal'asi orasidagi venzel masofasi (metrlarda).
- $D_{max} = 5000.0$ metr (diplomatik ta'sir doirasining maksimal chegarasi).

**Natijalar:**
- **To'lov o'z vaqtida amalga oshirilsa:** Munosabat $\Delta R = +12$ ga ko'tariladi, fraktsiya tajovuzkorlik hisobi (Aggression Score) nolga tushiriladi va 90 o'yin kuniga tinchlik kafolatlanadi.
- **To'lov rad etilsa yoki kechiktirilsa:** Fraktsiya tajovuzkorligi $\Delta \text{Aggression} = +45$ ga oshadi, munosabat $\Delta R = -35$ ga qulaydi va 48 o'yin soatiga mo'ljallangan qamal hisoblagichi (War Countdown Timer) ishga tushadi.

### 22.2.3. Karvon Yo'llari Logistikasi va Savdo Arbitraji

Karvonlar orqali amalga oshiriladigan ikki tomonlama savdo sayohat vaqti quyidagi formula bilan hisoblanadi:
$$T_{roundtrip} = 2 \times \sum_{k=1}^{N} \frac{D_k}{v_{caravan} \cdot M_{road, k}} + T_{post}$$

Bunda:
- $D_k$: Marshrutning $k$-segmenti uzunligi (metrlarda).
- $v_{caravan}$: Karvonning bazaviy tezligi (Yuk xachiri: $4.0\text{ km/soat}$, O'giz aravasi: $2.5\text{ km/soat}$, To'rt g'ildirakli og'ir furgon: $3.2\text{ km/soat}$).
- $T_{post} = 6.0$ soat (manzildagi tushirish-ortish va bojxona rasmiylashtiruvi vaqti).
- $M_{road, k}$: Yo'l qoplamasining harakat tezligi multiplikatori:
  - Yo'lsiz yovvoyi tabiat (Wilderness / Mud): $0.70\times$
  - Shag'al / Tuproq yo'l (Dirt Path): $1.15\times$
  - Toshlangan yo'l (Cobblestone Road): $1.35\times$
  - Qirollik shoh ko'chasi (Royal Highway): $1.60\times$

Karvon sayohatidan olinadigan sof foyda (Net Profit):
$$\text{NetProfit} = \sum_{i=1}^{M} Q_i \cdot \left(\text{Price}_{dest, i} - \text{Price}_{origin, i}\right) - \left(C_{escort} + C_{rations} + \text{Tariff}_{border}\right)$$

Bunda yuk sig'imi: Yuk xachiri ($150\text{ kg}$), O'g'iz aravasi ($600\text{ kg}$), Og'ir furgon ($1800\text{ kg}$). Agar savdo yo'lida qaroqchilar xavfi yuqori bo'lsa, qurolli soqchilar narxi ($C_{escort}$) keskin ortadi.

### 22.2.4. Josuslik Mexanikasi va Diversiya Turlari

Tier 3 Elchixona yoki Qorong'u Taverna orqali yollanadigan josuslar raqib qal'asiga yuboriladi. 5 ta diversiya topshirig'i mavjud:
1. **Texnologiya va Chizmalarni O'g'irlash (Steal Blueprint/Tech):** O'rganilmagan ishlab chiqarish retseptlari va arxitektura chizmalarini qo'lga kiritadi.
2. **Don Omborini Zaharlash (Poison Granary):** Ombordagi don zaxirasining $30\% - 60\%$ qismini yaroqsiz qiladi, shahar aholisi kayfiyatini $-25$ ballga tushiradi.
3. **Qasroga O't Qo'yish (Arson):** Yog'och taxta omborlari yoki qurilayotgan qamal qurollarini yoqib yuboradi.
4. **Dehqonlar Qo'zg'olonini Qo'zg'atish (Incite Peasant Revolt):** Fuqarolar sadoqatini pasaytirib, mahalliy qurolli isyonchilarni vujudga keltiradi.
5. **Qal'a Darvozasini Buzish (Sabotage Portcullis):** Qamal boshlanishi arafasida dushman darvozasining temir mexanizmini ishdan chiqarib, uni ochiq qoldiradi.

Josuslik muvaffaqiyati ehtimolligi ($P_{success}$):
$$P_{success} = \frac{\text{Skill}_{spy} \cdot (1.0 - \text{Security}_{target}) \cdot \left(1.0 + \frac{\text{Bribe}}{500}\right)}{\text{BaseDifficulty}_{mission} + \text{GuardAlertness}_{target}}$$

Agar operatsiya barbod bo'lsa, josus asir olinadi va qiynoqqa solinadi. Natijada dushman darhol $+60$ Casus Belli oladi, munosabat $\Delta R = -50$ ga pasayadi va butun mintaqa bo'ylab o'yinchi sha'niga la'nat e'lon qilinadi.

### 22.2.5. Urush E'lon Qilish Sabablari (Casus Belli Tizimi)

AI Lordlar o'zlarining Tajovuzkorlik Hisobi ($A_{score} \in [0, 150]$) $100$ balldan oshganda rasmiy urush e'lon qiladi:
1. To'lanmagan o'lpon muddati tugashi: $+50$ ball.
2. Bahsli chegara zonasida o'yinchi tomonidan Istehkom yoki Qorovul minorasi qurilishi: $+35$ ball.
3. Tijorat karvonining talanishi yoki savdogarlarning o'ldirilishi: $+40$ ball.
4. Diversiya paytida fosh etilgan josusning qo'lga olinishi: $+60$ ball.
5. Chegara ibodatxonalarining majburiy diniy o'zgartirilishi: $+40$ ball.
6. Qonuniy sulolaviy nikoh taklifining haqoratomuz rad etilishi: $+25$ ball.

## 22.3. Feodal Urushlar, Qamal Jangi va Hududlarni Bo'ysundirish

Urush holatida simulyatsiya keng ko'lamli taktik bosqichga o'tadi:
- **Voxel Qamallari va Istehkomlarning Buzilishi:** Dushman trebuchetlar, katapultalar va og'ir taranlar bilan hujum qiladi. Har bir tosh devor venzeli o'zining jismoniy mustahkamligiga ega — snaryadlar zarbidan devorlar real vaqtda parchalanadi, xarsanglar qulab tushadi va himoyachilarni ezib yuboradi.
- **Asosiy Qasr Zalini (Great Hall) Egallash:** Shahar mudofaasini yorib o'tib, markaziy taxt zali (`KeepCore`) egallansa va AI Lord taslim qilinsa, uning barcha qishloqlari, konlari va infratuzilmasi o'yinchining tobeligiga o'tadi.
- **Asirlar va Tovon Pulini Undirish:** Asirga olingan lordlar qasr zindoniga tashlanadi. O'yinchi ularga 3 xil chora ko'rishi mumkin:
  1. *Katta Tovon Puli (Ransom):* 5,000 dan 25,000 gacha kumush tanga evaziga ozod qilish.
  2. *Qat'iy Vassallik Qasamyodi:* Lordni o'z yerlarida qoldirib, har mavsumiy soliq to'lovchi vassalga aylantirish.
  3. *Ommaviy Qatl Qilish:* Boshqa dushman lordlarga qo'rquv solish, lekin ularning ittifoqchilari bilan munosabatni abadiy $-100$ darajasida muzlatish.

## 22.4. Ko'p O'yinchili Rejim (Steam P2P 2–4 O'yinchi) va Tarmoq Arxitekturasi

Voxel Lord Godot 4.3 platformasida 2 nafardan 4 nafargacha o'yinchilar uchun mo'ljallangan Steamworks P2P (Peer-to-Peer) ko'p o'yinchili kooperativ va raqobat rejimlarini taqdim etadi.

### 22.4.1. Tarmoq Topologiyasi va Boshqaruv Qoidalari

Tarmoq arxitekturasi **Host-Authoritative Client-Server** modeliga tayanadi. Bitta o'yinchi xost (Server) vazifasini bajaradi, qolgan 1–3 nafar o'yinchi esa mijoz (Client) sifatida ulanadi. Bog'lanish `SteamMultiplayerPeer` (GodotSteam GDExtension) orqali amalga oshiriladi, bu esa NAT-traversal, xavfsiz Steam ID autentifikatsiyasi va Steam Relay tarmoqlari orqali to'g'ridan-to'g'ri port ochmasdan o'ynash imkonini beradi. Mahalliy tarmoq (LAN) uchun esa Godotning standart `ENetMultiplayerPeer` drayveriga to'liq o'tish ta'minlangan.

- **Server Simulyatsiya Chastotasi (Tick Rate):** Qat'iy $20\text{ Hz}$ ($50\text{ ms}$ interval). Voxel fizikasi, qulashlar, shaxta gazi tarqalishi, AI FSM qarorlari va iqtisodiy oqimlar faqat xostda hisoblanadi.
- **Mijoz Render Interpolyatsiyasi:** $60 - 144\text{ Hz}$. Mijoz tomonida barcha personajlar va jonzotlar harakati Hermite kubik splayn (Hermite cubic spline) interpolyatsiyasi orqali silliqlanadi.
- **Tarmoq O'tkazuvchanlik Byudjeti (Bandwidth Budget):** Har bir ulangan mijoz uchun sekundiga ko'pi bilan $35\text{ KB/s}$ ma'lumotlar oqimi belgilangan.

### 22.4.2. Binar Tarmoq Paketlari Tuzilmasi (Packet Bit-Packing Layout)

Tarmoq uzatishlarida ortiqcha JSON yoki String formatlaridan voz kechilib, barcha ma'lumotlar ixcham xom baytlar (`PackedByteArray`) sifatida uzatiladi:

| Paket ID | Paket Nomi | Tarmoq Kanali | Hajmi (Bayt) | Aniq Binar Maydonlar Tuzilishi (Byte Layout) |
|---|---|---|---|---|
| `0x01` | **ClientInputPacket** | Unreliable Ordered (Kanal 0) | **14 B** | `[tick: uint32 (4B)]` `[move_x: int8 (1B)]` `[move_z: int8 (1B)]` `[pitch: int16 (2B)]` `[yaw: int16 (2B)]` `[input_flags: uint16 (2B)]` `[equipped_slot: uint16 (2B)]` |
| `0x02` | **VoxelDeltaModify** | Reliable Ordered (Kanal 1) | **11 B** | `[chunk_x: int16 (2B)]` `[chunk_y: int16 (2B)]` `[chunk_z: int16 (2B)]` `[local_voxel_idx: uint16 (2B)]` `[block_type: uint8 (1B)]` `[meta_flags: uint8 (1B)]` `[actor_id: uint8 (1B)]` |
| `0x03` | **EntitySnapshot** | Unreliable (Kanal 2) | **10 B / ob'ekt** | `[entity_id: uint16 (2B)]` `[pos_x: float16 (2B)]` `[pos_y: float16 (2B)]` `[pos_z: float16 (2B)]` `[packed_yaw_state: uint8 (1B)]` `[health_pct: uint8 (1B)]` |
| `0x04` | **CaveInEventPacket** | Reliable Ordered (Kanal 1) | **13 B** | `[center_x: int16 (2B)]` `[center_y: int16 (2B)]` `[center_z: int16 (2B)]` `[radius: uint8 (1B)]` `[collapse_seed: uint32 (4B)]` `[debris_count: uint16 (2B)]` |
| `0x05` | **GasPocketUpdate** | Unreliable (Kanal 2) | **8 B** | `[chunk_id: uint32 (4B)]` `[gas_type: uint8 (1B)]` `[concentration_pct: uint8 (1B)]` `[pressure: uint16 (2B)]` |
| `0x06` | **WorldChunkStream** | Reliable Fragmented (Kanal 3) | **O'zgaruvchan** | `[chunk_x: int16 (2B)]` `[chunk_y: int16 (2B)]` `[chunk_z: int16 (2B)]` `[compressed_len: uint16 (2B)]` `[zlib_compressed_voxels: 32x32x32 nibbles]` |

### 22.4.3. Voxel O'zgarishi RPC Ketma-ketligi va Reconciliation

Dunyo venzellarini o'zgartirish (qazish yoki qo'yish) jarayoni kechikishni (ping) yashirish uchun quyidagi aniq tartibda kechadi:
1. **Mijozning Vizual Taxmini (Client Prediction):** O'yinchi sichqoncha bilan venzelni burg'ulaganda, mijoz darhol bolg'alash ovozi, chaqnoq zarralari va yoriqlar teksturasini ko'rsatadi.
2. **Serverga So'rov Yuborish:** Mijoz `@rpc("call_local", "reliable") func request_voxel_modify(pos: Vector3i, new_type: int)` funktsiyasini chaqiradi.
3. **Xostning Avtoritar Tekshiruvi (Host Validation):**
   - O'yinchi va venzel orasidagi masofa $\le 4.5\text{ metr}$ ekanligi tekshiriladi.
   - O'yinchining qo'lida ushbu venzel qattiqligiga mos asbob (Pickaxe Tier) mavjudligi tekshiriladi.
   - Asbob sovish vaqti (cooldown) va o'yinchi harakat qoidalari tekshiriladi.
4. **Xostning Tasdiqlashi va Tarqatishi (Host Commit & Broadcast):** Xost dunyo matritsasini yangilaydi, saqlash buferiga delta o'zgarishini kiritadi, shaxta tayanch barqarorligini (`MinePhysicsServer`) tekshiradi va barcha ulangan mijozlarga `0x02` (`VoxelDeltaModify`) binar paketini jo'natadi.
5. **Xatolikni Qaytarish (Reconciliation):** Agar xost so'rovni rad etsa (masalan, boshqa o'yinchi shu venzelni bir necha millisekund oldin olib qo'ygan bo'lsa), xost tuzatuvchi paket yuboradi va mijozning vizual holati darhol asl holatiga qaytariladi (rollback).

### 22.4.4. O'yin Rejimlari: Yagona Qirollik va Feodal Tarqoqlik

1. **Yagona Taxt (Shared Kingdom / Co-op):**
   - Barcha o'yinchilar bitta umumiy g'azna, umumiy omborlar va yagona fuqarolar tarmog'iga ega bo'ladi.
   - Rollar ixtisoslashuvi: 1-O'yinchi — Iqtisodiyot va diplomatiya lordi; 2-O'yinchi — Qal'a me'mori va shaxtalar muhandisi; 3-O'yinchi — Mudofaa marshali va qo'shin qo'mondoni; 4-O'yinchi — Karvonlar va qishloq xo'jaligi boshqaruvchisi.
2. **Feodal Tarqoqlik (Rival Dynasties / PvPvE):**
   - Har bir o'yinchi $1000\times 1000$ masshtabdagi umumiy dunyoning turli nuqtalarida o'z mustaqil qasrlarini quradi.
   - O'yinchilar o'zaro savdo shartnomalari, ittifoqlar tuzishi, bir-birlariga josus yuborishi yoki nodir konlar uchun qamal urushlarini olib borishi mumkin.

---

# 23. MAHORAT TIZIMI (SKILL SYSTEM & CRAFT PROGRESSION)

Voxel Lord feodal dunyosida har bir fuqaro tug'ma va orttirilgan mehnat va jangovar ko'nikmalar majmuasiga ega. Mahorat tizimi har bir kasb bo'yicha $0$ dan $100$ gacha bo'lgan uzluksiz shkalada o'lchanadi. Mahorat darajasi bevosita ish tezligiga, buyum sifatiga, resurs tejashga va yangi texnologik retseptlarni ochishga ta'sir ko'rsatadi.

### 23.1. Mahorat Rivojlanishi Matematikasi va XP Tenglamalari (Progression Math)

Fuqaroning ma'lum bir mahorat bo'yicha keyingi darajaga (Level) ko'tarilishi uchun talab qilinadigan tajriba ochkolari (XP) eksponentsial qonuniyat asosida o'sib boradi:

$$XP_{required}(Level) = BaseXP \times (1 + Level)^{1.45}$$

Bunda:
- $BaseXP = 120 \text{ XP}$ (1-darajadan 2-darajaga o'tish uchun 120 XP kerak, 50-daraja uchun $\approx 35,400 \text{ XP}$, 100-daraja uchun $\approx 96,200 \text{ XP}$).

**Har Bir Mehnat Amali Uchun Beriladigan XP Formulasi ($\Delta XP$):**
Har safar fuqaro bitta qazish, eritish, bolg'alash, ekin o'rish yoki jangovar zarba amalini bajarganda:

$$\Delta XP = BaseActionXP \times \left(1.0 + 0.5 \times Tier_{station}\right) \times \left(\frac{ToolQuality}{1.0}\right) \times \left(1.0 - 0.005 \times Level\right)$$

- $BaseActionXP$: Amaliyot turiga qarab (Daraxt kesish: $8 \text{ XP}$, Temir qurol bolg'alash: $35 \text{ XP}$, Jarrohlik amaliyoti: $60 \text{ XP}$).
- $Tier_{station} \in [1, 4]$: Ilg'or dastgohda ishlash yangi uslublarni tezroq o'rgatadi.
- $ToolQuality$: Yuqori sifatli asbob bilan ishlash usta nozikligini oshiradi.
- $(1.0 - 0.005 \times Level)$: Daraja oshgan sari oddiy takroriy ishlardan olinadigan tajriba tabiiy ravishda kamayadi (99-darajada bazaviy o'sish $50\%$ ga tushadi, faqat murakkab qirollik buyurtmalari orqali Grandmaster darajasiga erishish mumkin).

---

### 23.2. 5 Pog'onali Malaka Unvonlari Jadvali (Mastery Tiers Balance Table)

| Malaka Pog'onasi | Mahorat Diapazoni (Level) | Mehnat / Qazish Tezligi Multiplikatori | Xato / Falokat Ehtimoli ($P_{fail}$) | Maksimal Buyum Sifati | Maxsus Imtiyozlar va Ta'lim Qobiliyati |
|---|---|---|---|---|---|
| **Yangi O'rganuvchi (Novice)** | $0 – 19$ | $1.00\times$ (Baza) | $15.0\%$ | Common (Oddiy) | Yangi shogird, ko'p charchaydi, asbobni tez eskirtiradi. Boshqalarga o'rgata olmaydi. |
| **Shogird (Apprentice)** | $20 – 39$ | $1.15\times$ | $8.0\%$ | Fine (Sifatli) | Standart retseptlarni mustaqil bajara oladi, asbob eskirishi $-10\%$. |
| **Usta Yordamchisi (Journeyman)**| $40 – 69$ | $1.35\times$ | $2.0\%$ | Masterwork (Usta) | Ishlab chiqarish unumi $+35\%$. Novice yoshlarni o'z yoniga shogirdlikka olish huquqi. |
| **Buyuk Usta (Master)** | $70 – 89$ | $1.65\times$ | $0.0\%$ (Xato qilmaydi) | Royal (Qirollik) | Murakkab qotishmalar va arxitektura bloklarini ochadi. Apprentice darajasidagi shogirdlarni tayyorlaydi. |
| **Afsonaviy Usta (Grandmaster)** | $90 – 100$ | $2.00\times$ | $0.0\%$ | Legendary (Afsonaviy)| Shahar nufuzi $+5$ Prestige aura beradi. Shahar bo'ylab tegishli sohada xomashyo isrofi $-15\%$. |

---

### 23.3. Ustoz-Shogird Tizimi va Bilim Uzatish Mexanikasi (Mentorship Dynamics)

- **Shogird Biriktirish:** Hukmdor yoki shahar mehnati dispetcheri 11–15 yoshli o'smirni Master ($Skill \ge 70$) hunarmandga biriktirishi mumkin.
- **Aura Ta'siri (Mentorship Proximity Bonus):**
  - Shogird o'z ustozi bilan bir xona ichida yoki 8 metr masofada birgalikda ishlaganda:
    $$\Delta XP_{apprentice} = \Delta XP \times 1.35$$
    Shogird $35\%$ tezroq tajriba to'playdi.
  - Usta shogirdning harakatlarini nazorat qiladi: agar shogird xatoga yo'l qo'ymoqchi bo'lsa, usta uni to'xtatadi ($P_{fail}$ xavfi $0\%$ ga tushadi).
- **Merosiy Tajriba Kitoblari (Master Treatises):**
  - Grandmaster darajasiga yetgan usta o'z hayotining so'nggi yillarida (Elder bosqichida) monastir kutubxonasida yoki o'z ustaxonasida "Hunarmand Risolasi" (`Craft Treatise`) kitobini yozishi mumkin.
  - Ushbu kitob shahar kutubxonasida saqlanadi va kelgusi avlodlarning o'rganish tezligini butun shahar miqyosida doimiy $+10\%$ ga oshiradi.

---

# 24. FEODAL MAQOMLAR (FEUDAL RANKS)

- **Sargardon:** Aholi 1–2 kishi.
- **Oqsoqol:** Aholi 3–10 kishi.
- **Baron:** Aholi 10–35 kishi.
- **Graf / Gersog:** Aholi 35–100 kishi.
- **Qirol:** Aholi 100+ kishi.

---

# 25. TEXNOLOGIYA BOSQICHLARI (TECH TIERS)

- **Tier I — Refugee Camp:** Boshlang'ich omon qolish va yog'och kulbalar.
- **Tier II — Craft Village:** Hunarmandchilik dastgohlari, asosiy iqtisodiyot.
- **Tier III — Feudal Town:** Tosh me'morchiligi, soqchilar, soliq tizimi, elchixona.
- **Tier IV — Kingdom:** Monumental inshootlar, ilg'or metallurgiya, milliy tizimlar.

---

# 26. QIROLLIKKA 3 YO‘L

1. **Qilich Yo'li:** Mintaqadagi barcha yovuz kuchlar va qaroqchilar boshliqlarini tor-mor etish.
2. **Oltin Yo'li:** Xazinada 10,000 Oltin to'plash, strategik savdo yo'llarini monopoliyaga olish.
3. **Xalq Mehri:** Obro' (Prestige) va xalq roziligi 95%+, Buyuk Sobor va Ajdodlar Toji.

---

# 27. DUNYO GENERATSIYASI VA 6 ASOSIY BIOM (WORLD GENERATION & 6 CORE BIOMES)

Voxel Lord: Feudal Realm dunyo generatsiyasi to'liq protsedural, deterministik urug' (world seed) asosida ishlaydigan ko'p qatlamli 3D OpenSimplex / FastNoiseLite tizimiga tayanadi. Dunyo balandlik xaritasi, harorat, namlik va eroziya shovqinlari integratsiyasi orqali shakllanadi va 6 ta asosiy ekologik biomga ajratiladi.

### 27.1. Protsedural Dunyo Xaritasi va Noise Qatlamlari (Procedural Generation & Noise Stacks)

Yer yuzasi va g'orlar tizimini generatsiya qilishda 5 ta mustaqil shovqin qatlami (noise octaves) qo'llaniladi:
1. **Continentalness ($N_{cont}$):** Katta masshtabli quruqlik va okeanlar chegarasini belgilaydi (Chastota $f = 0.0015$).
2. **Erosion ($N_{eros}$):** Tog'li tizmalar yemirilishi va yassi tekisliklarni shakllantiradi ($f = 0.004$).
3. **Peaks & Valleys ($N_{pv}$):** Mahalliy qoyatoshlar, daralar va kanyonlarni o'yadi ($f = 0.012$).
4. **Temperature ($N_{temp}$):** Global kenglik va balandlikka bog'liq harorat maydoni ($f = 0.002$).
5. **Humidity / Moisture ($N_{moist}$):** Yog'ingarchilik va yerosti suvlari to'yinishi ($f = 0.003$).

Har bir 3D koordinatadagi voxel zichligi quyidagi universal formula bo'yicha hisoblanadi:

$$D(x, y, z) = -y + N_{cont}(x, z) \cdot W_{cont} + N_{detail}(x, y, z) \cdot W_{detail} - S_{cave}(x, y, z)$$

Bu yerda:
- $y$ — dengiz sathidan balandlik (metrlarda, dengiz sathi $y = 0$).
- $W_{cont} = 120.0$, $W_{detail} = 35.0$ — relef og'irlik koeffitsiyentlari.
- $S_{cave}(x, y, z)$ — 3D Shveysariya pishlog'i (Swiss cheese) va qurt yo'llari (Worm caves) g'orlar shovqini. Agar $D(x, y, z) > 0$ bo'lsa, qattiq jins hosil bo'ladi, $D(x, y, z) \le 0$ bo'lsa, havo yoki suv bilan to'ldiriladi.
- Biom tanlovi Uittaker (Whittaker) iqlim diagrammasiga binoan mahalliy harorat $T(x, z) \in [-30^\circ\text{C}, +45^\circ\text{C}]$ va namlik $W(x, z) \in [0\%, 100\%]$ ko'rsatkichlari kesishmasida aniqlanadi.

### 27.2. Oltita Asosiy Biomning Katta Ekologik Matritsasi (6 Core Biomes Master Ecological Matrix)

Quyidagi jadvalda Voxel Lord: Feudal Realm olamidagi 6 ta asosiy biomning to'liq termodinamik, qishloq xo'jaligi, biologik va qurilish parametrlari keltirilgan:

| Biom Nomi (Biome) | O'rtacha Harorat ($T_{mean}$) | Fasllar Diapazoni ($\Delta T$) | Yillik Yog'ingarchilik (mm) | Tuproq Unumdorlik Indeksi | Flora O'sish Multiplikatori | Fauna Ekotizimi | Kasallik Xavfi (Virulence) | Grunt Ko'tarish Qobiliyati (Bearing Capacity kPa) | O'ziga Xos Ekologik Perk |
|---|---|---|---|---|---|---|---|---|---|
| **1. Unumdor Tekislik (Fertile Plains)** | $+14^\circ\text{C}$ | Bahor: $12^\circ\text{C}$, Yoz: $24^\circ\text{C}$, Kuz: $10^\circ\text{C}$, Qish: $-2^\circ\text{C}$ | $850\text{ mm}$ | $100\%$ ($1.00\times$) | $1.25\times$ | Qoramol, Qo'y, Yovvoyi Quyon, Ot | Asosiy me'yor ($1.00\times$) | $250\text{ kPa}$ (Standart zamin) | Don va sabzavotlar hosildorligi $+50\%$ |
| **2. Qalin O'rmon (Dense Forest)** | $+11^\circ\text{C}$ | Bahor: $9^\circ\text{C}$, Yoz: $20^\circ\text{C}$, Kuz: $8^\circ\text{C}$, Qish: $-6^\circ\text{C}$ | $1200\text{ mm}$ | $70\%$ ($0.70\times$) | $1.50\times$ (Daraxtlar) | Bug'u, Yovvoyi To'ng'iz, Bo'ri, Qo'ng'ir Ayiq | Past-O'rta ($1.10\times$) | $200\text{ kPa}$ (O'rmon chirindisi) | Cheksiz yog'och va qatron manbai |
| **3. Tik Qoyali Tog'lar (Craggy Mountains)** | $+4^\circ\text{C}$ | Bahor: $3^\circ\text{C}$, Yoz: $12^\circ\text{C}$, Kuz: $1^\circ\text{C}$, Qish: $-18^\circ\text{C}$ | $950\text{ mm}$ (Qor ko'p) | $20\%$ ($0.20\times$) | $0.40\times$ | Tog' Echkisi, Burgut, Qor Qoploni | Juda past ($0.50\times$) | $800\text{ kPa}$ (Mustahkam qoya) | Oliy toifadagi metall rudalari va granit |
| **4. Qorong'u Botqoqlik (Murky Swamp)** | $+16^\circ\text{C}$ | Bahor: $15^\circ\text{C}$, Yoz: $26^\circ\text{C}$, Kuz: $14^\circ\text{C}$, Qish: $+2^\circ\text{C}$ | $1800\text{ mm}$ | $45\%$ ($0.45\times$) | $1.10\times$ (Qamish/Mox) | Zuluk, Baqa, Botqoq Timsohi, Ilon | O'ta xavfli ($2.20\times$, Bezgak/Vabo) | $60\text{ kPa}$ (Qoziqli poydevor zarur) | Torf yoqilg'isi, botqoq temiri va dorivor giyohlar |
| **5. Muzlagan Tundra (Frozen Tundra)** | $-12^\circ\text{C}$ | Bahor: $-8^\circ\text{C}$, Yoz: $+3^\circ\text{C}$, Kuz: $-10^\circ\text{C}$, Qish: $-35^\circ\text{C}$ | $220\text{ mm}$ (Bo'ronlar) | $5\%$ (Abadiy muzlik) | $0.05\times$ (Ochiq tuproqda) | Qutb Bukasi, Oq Tulki, Oq Ayiq, Muz Yashiri | Sterillangan ($0.30\times$) | $500\text{ kPa}$ (Muzlagan grunt) | Oziq-ovqat va go'sht chirimasligi ($0\times$ aynish) |
| **6. Qurg'oqchil Dasht (Arid Steppe)** | $+22^\circ\text{C}$ | Bahor: $18^\circ\text{C}$, Yoz: $38^\circ\text{C}$, Kuz: $15^\circ\text{C}$, Qish: $-4^\circ\text{C}$ | $180\text{ mm}$ (Qurg'oqchilik) | $30\%$ ($0.30\times$) | $0.50\times$ (Quruq butalar) | Yovvoyi Ot, Jayron, Shoqol, Chayon | Past ($0.80\times$, Suv orqali) | $300\text{ kPa}$ (Zichlashgan gilli qatlam) | Zotdor jangovar otlar yetishtirish markazi |

### 27.3. Biomlar Oralig'idagi O'tish Zonasi va Blend Mexanikasi (Biome Blending & Voronoi Jitter)

Biom chegaralari keskin to'siq bo'lib qolmasligi uchun Voronoi diagrammasi asosida 48 voxel ($1.5$ chunk) kengligidagi o'tish zonasi (Transition Buffer) hisoblanadi. Ikki yoki undan ortiq biom tutashgan nuqtada iqlim ko'rsatkichlari og'irlikli teskari masofa formulasi (Inverse Distance Weighting) orqali tekislanadi:

$$T_{local}(x, z) = \sum_{k=1}^K w_k(x, z) \cdot T_{biome, k}, \quad w_k(x, z) = \frac{\frac{1}{d_k^2 + 0.01}}{\sum_{j=1}^K \frac{1}{d_j^2 + 0.01}}$$

Bu yerda:
- $d_k$ — ko'rib chiqilayotgan $(x, z)$ ustunidan $k$-biom markazigacha bo'lgan masofa.
- $w_k$ — normallashgan og'irlik koeffitsiyenti ($\sum w_k = 1.0$).
- Grunt bloklari chegarada aralashadi: masalan, O'rmon va Dasht chegarasida chimli tuproq (Grass Block) asta-sekin quruq qumloq tuproqqa (Coarse Dirt) aylanadi.

### 27.4. Flora va Yovvoyi Tabiatning Biomlar Bo'yicha Taqsimoti (Flora & Fauna Ecosystem)

1. **Daraxt Turlari:**
   - *Eman (Oak):* Unumdor Tekislik va Qalin O'rmon biomida o'sadi, yuqori zichlikdagi qurilish yog'ochi beradi.
   - *Qarag'ay (Pine):* Tik Qoyali Tog'lar va Tundra yonbag'rida uchraydi, qatron va yengil taxta manbai.
   - *Qayin (Birch):* O'rmon chetlari va tekisliklarda tarqalgan, o'ymakorlik va mebelchilik uchun xomashyo.
   - *Majnuntol (Willow):* Qorong'u Botqoqlik qirg'oqlarida o'sadi, egiluvchan savatlar va tirgaklar uchun qo'llaniladi.
   - *Qora Archa (Yew):* Tog' etaklarida kamyob o'sadi, eng kuchli jangovar uzun kamonlar (Longbow) uchun zarur.
   - *Akatsiya (Acacia):* Qurg'oqchil Dasht kanyonlarida o'sadi, qattiq va issiqqa chidamli yog'och.
2. **Yovvoyi Hayvonlar Populyatsiyasi va Ko'payishi:**
   - Har bir chunk ustunida maksimal o'txo'rlar va yirtqichlar sig'imi (Carrying Capacity) cheklangan: $K_{fauna} = A_{chunk} \cdot B_{density}$.
   - O'rmonlarda bug'ular va yovvoyi to'ng'izlar ozuqa izlab podada yuradi; qishda oziq-ovqat kamayganda bo'rilar aholi punktlariga yaqinlashib xavf tug'diradi.

---

# 28. VOXEL WORLD TEXNIK PARAMETRLARI (VOXEL WORLD TECHNICAL PARAMETERS)

Voxel Lord: Feudal Realm o'yin dunyosi Godot Engine 4.3 platformasida ishlab chiqilgan yuqori unumdorlikka ega, to'liq o'zgaruvchan (fully destructible) voxel texnologiyasiga tayanadi.

### 28.1. Standartlashtirilgan Chunk Strukturasi ($32 \times 32 \times 32$)

1. **Fizik O'lcham:**
   - 1 Voxel bloki = $1.0\text{ m} \times 1.0\text{ m} \times 1.0\text{ m}$ kub shaklidagi fazoviy hajm.
   - 1 Chunk = $32 \times 32 \times 32$ voxel = $32,768$ ta blokdan iborat to'liq kubik segment.
   - Dunyoning fazoviy masshtabi inson modeli ($1.8\text{ m}$ balandlik) bilan $1:1$ aniqlikda muvofiqlashtirilgan.
2. **Fazoviy Indekslash (Spatial Indexing):**
   - Chunk ichidagi har bir lokal voxel $(x, y, z)$ yagona 1D chiziqli massivga tekislanadi:

$$\text{Index}(x, y, z) = x + (z \times 32) + (y \times 32 \times 32) = x + 32z + 1024y$$

Bu yerda $x, y, z \in [0, 31]$. Ushbu tartib kesh lokalizatsiyasini (cache locality) ta'minlaydi va xotiradan ma'lumot o'qish tezligini oshiradi.

### 28.2. Chunk Xotira Bayt Formati (Chunk Byte Layout & Bit-Packing)

Har bir voxel bloki xotirada qat'iy 32-bit (4 bayt) butun son shaklida saqlanadi:

```
[Bit 0-11: Block ID] [Bit 12-15: Meta/Damage] [Bit 16-19: Sunlight] [Bit 20-23: BlockLight] [Bit 24-31: MicroBiome]
|--- 12 bit --------|--- 4 bit -------------|--- 4 bit ---------|--- 4 bit ------------|--- 8 bit ---------|
```

- **Bits 0–11 (12 bit):** Blok Turi identifikatori (`BlockID` $0 - 4095$ gacha turli minerallar, yog'ochlar, tuproqlar).
- **Bits 12–15 (4 bit):** Blok Holati va Buzilish Darajasi (`Metadata / Damage Stage`, $0 - 15$ darajali darz ketish animatsiyasi).
- **Bits 16–19 (4 bit):** Quyosh nuri intensivligi (`Sunlight`, $0 - 15$ daraja, osmondan tushuvchi dinamik nurlar).
- **Bits 20–23 (4 bit):** Sun'iy yorug'lik intensivligi (`BlockLight`, $0 - 15$ daraja, mash'ala, kamin, lava nurlari).
- **Bits 24–31 (8 bit):** Namlik va mahalliy mikro-harorat indeksi ($0 - 255$).

Quyidagi jadvalda chunklarning xotiradagi byudjeti keltirilgan:

| Chunk Turi | Voxel Soni | Xotira Hajmi (Uncompressed) | Siqish Usuli (Compression) | Siqilgan Hajm (Compressed) | Keshdagi Xotira Sig'imi (1024 chunk) |
|---|---|---|---|---|---|
| **Bo'sh Havo Chunki (Air Chunk)** | 32,768 | $128\text{ KB}$ | Yagona konstant ID (Flagged) | $16\text{ Bayt}$ | $16\text{ KB}$ |
| **Yaxlit Qoya Chunki (Solid Stone)** | 32,768 | $128\text{ KB}$ | RLE (Run-Length Encoding) | $64\text{ Bayt}$ | $64\text{ KB}$ |
| **Aralash Yerusti Chunki (Surface)** | 32,768 | $128\text{ KB}$ | Palette Compression (16 rang) | $18.4\text{ KB}$ | $18.8\text{ MB}$ |
| **Murakkab Shaxta Chunki (Mine/Caves)**| 32,768 | $128\text{ KB}$ | Deflate / Zlib oqimi | $32.6\text{ KB}$ | $33.4\text{ MB}$ |

### 28.3. Dunyo Chegaralari va Koordinata Konversiya Formulalari (World Boundaries & Coordinate Transforms)

1. **Dunyo Chegarasi:**
   - Gorizontal maydon: $X \in [-2048\text{ m}, +2048\text{ m}]$, $Z \in [-2048\text{ m}, +2048\text{ m}]$ (Umumiy maydon $16.78\text{ km}^2$, $128 \times 128$ chunk ustunlari).
   - Vertikal koordinatalar: $Y \in [-512\text{ m}, +256\text{ m}]$ (Jami balandlik $768\text{ m}$, 24 ta chunk qatlami).
2. **Koordinata Transformatsiyasi Formulalari:**
   Global dunyo koordinatasi $(X, Y, Z)$ dan Chunk koordinatasi $(CX, CY, CZ)$ va lokal voxel indeksi $(vx, vy, vz)$ ni hisoblash:

$$CX = \lfloor X / 32 \rfloor, \quad CY = \lfloor Y / 32 \rfloor, \quad CZ = \lfloor Z / 32 \rfloor$$

$$vx = X - (CX \times 32) = X \ \& \ 31$$

$$vy = Y - (CY \times 32) = Y \ \& \ 31$$

$$vz = Z - (CZ \times 32) = Z \ \& \ 31$$

Teskari konversiya (Lokal voxeldan global dunyo koordinatasiga):

$$X = CX \times 32 + vx, \quad Y = CY \times 32 + vy, \quad Z = CZ \times 32 + vz$$

---

# 29. VOXEL LOD (LEVEL OF DETAIL SYSTEM)

Katta hajmdagi voxel olamida yuqori kadrlar chastotasini (60–144 FPS) ta'minlash maqsadida 4 pog'onali iyerarxik Level of Detail (LOD) tizimi qo'llaniladi.

### 29.1. 4 Pog'onali LOD Iyerarxiyasi (4-Tier LOD Architecture)

1. **LOD 0 — Yaqin Masofa ($0 - 64\text{ m}$, 2 chunk radiusi):**
   - *Render:* To'liq Greedy Meshing algoritmi. Bir xil turdagi va bir tekislikda joylashgan qo'shni yuzalar bitta to'rtburchak polagonga birlashtiriladi. Natijada poligonlar soni 60% dan 85% gacha qisqaradi.
   - *Fizika:* To'liq `ConcavePolygonShape3D` statik to'qnashuv to'ri (collision mesh). Har bir voxel individual sindirilishi va kovlanishi mumkin.
   - *Yoritish:* Bloklararo dinamik Ambient Occlusion va yumshoq yorug'lik silliqlash.
2. **LOD 1 — O'rta Masofa ($64 - 160\text{ m}$, 2–5 chunk radiusi):**
   - *Render:* Okto-daraxt (Octree) asosidagi soddalashtirilgan Dual Contouring / Surface Decimation. $2 \times 2 \times 2$ voxel guruhlari bitta makro-katakka birlashtiriladi. Poligonlar soni LOD 0 ga nisbatan 75% kamayadi.
   - *Fizika:* Faqat personaj harakati uchun soddalashtirilgan qo'pol balandlik kolliziyasi; mayda g'or ichi kolliziyalari o'chiriladi.
3. **LOD 2 — Uzoq Masofa ($160 - 384\text{ m}$, 5–12 chunk radiusi):**
   - *Render:* Balandlik maydoni relied to'ri (Heightfield Terrain Mesh). Yer osti g'orlari va shaxtalar meshdan to'liq chiqarib tashlanadi (Occlusion culling). Faqat eng yuqori quyosh ko'radigan sirt $4 \times 4$ qadamda triyangulyatsiya qilinadi.
   - *Fizika:* Kolliziya to'liq o'chiriladi; uzoq masofadagi o'qlar va AI marshrutlari analitik balandlik tekshiruvi orqali yo'naltiriladi.
4. **LOD 3 — Ufq Chizig'i ($384 - 1024\text{ m}+$, ufq chegarasi):**
   - *Render:* Distant Horizon Impostors / Normal-mapped Billboard Mesh. Uzoqdagi tog' tizmalari va relef past poligonli siluet sifatida chiziladi va volumetrik tuman (Volumetric Fog) orqali silliq yashiriladi.

### 29.2. O'tish Histerezisi (LOD Transition Hysteresis)

Kamera LOD chegaralarida tebranganda poligon to'rlarining to'xtovsiz qayta generatsiya bo'lishi (LOD thrashing va stuttering) ning oldini olish uchun $\Delta_{hysteresis} = 8.0\text{ metr}$ o'lchamdagi histerezis buferi kiritiladi:

$$D_{upgrade} = D_{boundary} - \Delta_{hysteresis}, \quad D_{downgrade} = D_{boundary} + \Delta_{hysteresis}$$

Masalan, LOD 0 dan LOD 1 ga o'tish masofasi $64\text{ m}$ bo'lsa, kamera uzoqlashayotganda chunk $72\text{ m}$ ga yetgandagina LOD 1 ga o'tadi, yaqinlashayotganda esa $56\text{ m}$ ga yetgandagina LOD 0 ga qaytadi.

### 29.3. Ko'p Oqimli Mesh Generatsiyasi (Mesh Generation Threading Pipeline)

Mesh generatsiyasi asosiy o'yin oqimini (Main Thread) muzlatib qo'ymasligi uchun Godot 4 ning `WorkerThreadPool` tizimi asosida asinxron bajariladi:
1. **Prioritet Navbati (Priority Queue):** O'yinchining ko'rish konusidagi (Frustum) va eng yaqin masofadagi o'zgargan (dirty) chunklar eng yuqori ustuvorlikka ega bo'ladi:

$$\text{Priority} = \max(0, 1000 - \lfloor d_{camera} \rfloor) + (\text{InFrustum} \times 500)$$

2. **Xomashyo Buferi (Staging Buffer):** Fon oqimida vertex, normal, UV va indeks massivlari hisoblab chiqiladi.
3. **Asosiy Oqimga Yuklash:** Faqatgina tayyor `ArrayMesh` va `Shape3D` resurslari asosiy oqimga uzatiladi va GPU xotirasiga $1.5\text{ ms}$ vaqt chegarasida (Frame Budget) yuklanadi.

---

# 30. YER QATLAMLARI VA STRATALAR (SUBTERRANEAN STRATA LAYERS)

Voxel Lord: Feudal Realm ostidagi geologiya oddiy tasodifiy tosh emas, balki Yer qobig'ining qonuniy geologik evolyutsiyasini aks ettiruvchi vertikal qatlamlardan iborat.

### 30.1. Vertikal Geologik Qatlamlar Tuzilishi (0 to -350m+)

Subterranean muhit 6 ta alohida litosfera qatlamiga (strata) bo'linadi:

1. **1-Qatlam: Gumus va Cho'kindi Qatlam ($0 \to -15\text{ m}$):**
   - Organik qora tuproq, qum, daryo shag'ali va loy (Clay) qatlami.
   - Dehqonchilik, g'isht pishirish va kulolchilik uchun birlamchi qatlam. O'simlik ildizlari va grunt suvlari to'yinadi.
2. **2-Qatlam: Yumshoq Cho'kindi Tog' Jinslari ($-15 \to -60\text{ m}$):**
   - Qumtosh (Sandstone), Ohaktosh (Limestone) va dastlabki qalin Toshko'mir qatlamlari.
   - Qadimgi dengiz qoldiqlari bo'lgan Tosh tuzi (Halite) va mis oksidlarining yuqori shoxchalari uchraydi.
3. **3-Qatlam: O'tish Qatlami va Asosiy Metallar ($-60 \to -160\text{ m}$):**
   - Qattiq ohaktosh, kvarsit va slaneslar.
   - Temir rudasi (Gematit), Qalay (Kassiterit), Qo'rg'oshin (Galenit), Rux (Sfalerit) va Oltingugurt qatlamlari. Bronza va po'lat asrining poydevori.
4. **4-Qatlam: Magmatik Jinslar va Asil Metallar ($-160 \to -280\text{ m}$):**
   - Oq Marmar va ulkan Granit qoyalari.
   - Kumush rudasi (Akantit), Nikel (Pentlandit), Oltin tomirlari va yashil Zumrad kristallari. Shaxta o'pirilish xavfi va tog' bosimi keskin ortadi.
5. **5-Qatlam: Abissal Qatlam va Qimmatbaho Javohirlar ($-280 \to -350\text{ m}$):**
   - O'ta qattiq vulkanik Bazalt va qora diabazlar.
   - Oliy sof Oltin uyumlari, Platina, qizil Yoqut (Ruby) va Olmos (Diamond) kristallari. Yuqori harorat, metan va vodorod sulfid gazlari to'planadi.
6. **6-Qatlam: Magmatik Tub Qoya ($-350\text{ m}+$):**
   - Qazib bo'lmas Tub Qoya (Bedrock), erigan lava daryolari va obsidian plitalari. O'yin dunyosining mutlaq pastki chegarasi.

### 30.2. Gauss Taqsimoti Ehtimollik Zichligi (Gaussian Depth Probability Function)

Har bir mineral va rudaning qatlamlar bo'ylab uchrash ehtimoli Gaussning normal taqsimot qonuniyatiga bo'ysunadi. Bu orqali har bir ruda o'zining cho'qqi chuqurligi ($y_{peak}$) da eng ko'p, undan uzoqlashgan sari kamayib boruvchi tabiiy taqsimot hosil qiladi:

$$P_{ore}(y) = P_{peak} \cdot \exp\left(-\frac{(y - y_{peak})^2}{2\sigma_y^2}\right)$$

Bu yerda:
- $y \le 0$ — chuqurlik (metrlarda).
- $y_{peak}$ — rudaning eng ko'p to'plangan optimal chuqurligi.
- $\sigma_y$ — qatlam qalinligining standart og'ishi (tarqalish radiusi).
- $P_{peak}$ — cho'qqi chuqurlikdagi maksimal hosil bo'lish ehtimoli ($0.0 - 1.0$).

Dunyo generatsiyasi paytida voxel koordinatasi bo'yicha 3D tomir shovqini $N_{vein}(x, y, z) \in [0.0, 1.0]$ olinadi:

$$\text{Agar } N_{vein}(x, y, z) < P_{ore}(y) \implies \text{Voxel Bloki } = \text{OreBlockID}$$

### 30.3. 3D OpenSimplex / FastNoiseLite Shovqin Parametrlari

Qatlamlarning egilishi, tekis bo'lmagan to'lqinsimon chegaralari va ruda tomirlarining fazoviy klasterlanishi quyidagi FastNoiseLite parametrlari orqali boshqariladi:

| Shovqin Tizimi | Noise Turi | Chastota ($f$) | Oktavalar Soni | Lacunarity | Gain | Izoh va Geologik Vazifasi |
|---|---|---|---|---|---|---|
| **Strata Wave Noise** | Simplex Smooth | $0.008$ | 3 | $2.0$ | $0.5$ | Geologik qatlamlarning vertikal to'lqinlanishi va siljishini hosil qiladi |
| **Cellular Vein Noise** | Cellular (Worley)| $0.035$ | 2 | $2.0$ | $0.45$| Ruda tomirlarining ingichka, tarvaqaylagan linzalarini generatsiya qiladi |
| **Cave Density Noise** | Perlin 3D | $0.020$ | 4 | $2.2$ | $0.55$| Tabiiy karst g'orlari, karst bo'shliqlari va yerosti zallarini o'yadi |
| **Domain Warp Noise** | Simplex Domain Warp| $0.015$ | 2 | $2.0$ | $0.6$ | Qatlamlar va tomirlarni tektonik burmalanishdek qiyshaytiradi |

---

# 31. SHAXTALAR VA KONCHILIK MEXANIZMLARI (MINING MECHANICS & INFRASTRUCTURE)

Voxel Lord: Feudal Realm shaxta ishlari oddiy blok urish emas, balki real muhandislik, xavfsizlik va chuqur transport logistikasini talab qiluvchi sanoat tizimidir.

### 31.1. Kon Qazish Mexanikasi va Asbob Tiersi (Mining Mechanics & Pickaxe Progression)

Har bir qattiq blok o'zining mustahkamlik darajasiga (Hardness) ega. Agar o'yinchi yoki konchi fuqaroning qo'lidagi cho'kich (Pickaxe) tieri blok talabidan past bo'lsa, zarba berilganda asbob uchqun chiqarib orqaga qaytadi (Deflection), mineral buzilmaydi va asbob mustahkamligi $3\times$ tezroq yo'qoladi.

Blokni qazib olish uchun talab qilinadigan sof vaqt ($T_{mine}$) quyidagi formula bo'yicha hisoblanadi:

$$T_{mine} = \frac{\text{Hardness} \times 1.5}{\text{ToolSpeedMultiplier} \times \text{SkillMultiplier} \times \text{StaminaFactor}}$$

Bu yerda:
- $\text{Hardness}$ — mineralning jadvaldagi qattiqlik darajasi ($1 - 20$).
- $\text{ToolSpeedMultiplier}$ — cho'kich tezligi (Yog'och: $0.5\times$, Tosh: $1.0\times$, Bronza: $1.6\times$, Temir: $2.4\times$, Po'lat: $3.5\times$, Damashq po'lati: $5.0\times$).
- $\text{SkillMultiplier}$ — fuqaroning konchilik mahorati ($1.0 + 0.05 \times \text{Level}$).
- $\text{StaminaFactor}$ — konchining charchoq koeffitsiyenti ($1.0$ dan $0.4$ gacha pasayadi).

### 31.2. Shaxtani Yog'ochlash va Vertikal Ustunlar (Shaft Timbering & Shoring)

Chuqur yerosti shaxtalari ikki xil asosiy muhandislik yo'nalishida quriladi:
1. **Vertikal Shaxta Stvoli (Vertical Shaft):**
   - $3 \times 3$ yoki $4 \times 4$ voxel o'lchamida vertikal pastga qaziladi.
   - Yog'och qoplama (Shaft Lining) va to'rtburchak ramkalar (Square Sets) bilan qoplanishi shart.
   - Tepada yog'och chig'ir va ko'targich kran (Headframe & Winch Hoist) o'rnatiladi. U chuqurlikdan ruda qutilarini va konchilarni ko'tarib tushiradi.
2. **Gorizontal Shtolnya va Tunnellar (Horizontal Drift & Adit):**
   - Qiya yoki to'g'ri gorizontal kovlanadi.
   - Har 3–5 metrda yog'och tirgak ramkalari (Timber Sets: Cap, Post, Sill) o'rnatilishi shart.
   - Yumshoq qum va loy qatlamlarida to'kilishning oldini olish uchun yupqa taxtali qalqonlar (Spiling boards) qoqiladi.

### 31.3. Drenaj va Suv Qatlamlari (Mine Drainage, Aquifers & Sumps)

Chuqurligi $-60\text{ m}$ dan oshgan shaxtalarda grunt suvlari qatlami (Aquifer) ni teshib qo'yish xavfi mavjud.
- Agar konchi suvli qumtoshni teshib qo'ysa, shaxtaga minutiga $Q_{in} = 0.5 - 2.5\text{ m}^3$ tezlikda suv oqib kira boshlaydi.
- Drenaj choralari ko'rilmasa, shaxta to'lib, ish to'xtaydi va ichkaridagi konchilar cho'kib halok bo'ladi.
- **Suvni Bartaraf Etish Texnologiyalari:**
  1. *Drenaj Chuquri (Drainage Sump):* Shaxtaning eng chuqur burchagida qazilgan maxsus $3 \times 3 \times 3$ o'lchamli suv to'plagich.
  2. *Chelakli Charxpalak Ko'targich (Bucket Elevator):* Ot yoki suv charxpalagi kuchi bilan aylanuvchi uzluksiz charm chelaklar tizimi.
  3. *Arximed Vinti (Archimedes Screw):* Qiya o'rnatilgan yog'och vint suvni yuqori gorizontga haydaydi.
  4. *Yog'och Quvurli Drenaj Shtolnyasi (Gravity Adit):* Tog' etagiga chiqarilgan nishab ariq orqali suv o'z oqimi bilan tashqariga oqiziladi.

### 31.4. Ruda Transport Logistikasi (Subterranean Haulage & Mine Carts)

Chuqurlikdan rudani qo'lda ko'tarib chiqish konchilar unumdorligini 80% ga tushirib yuboradi. Shu sababli shaxta logistika tizimlari quriladi:
- **Yog'och va Temir Relslar:** Tunnellar poliga yotqiziladi. Harakat qarshiligini $4\times$ kamaytiradi.
- **Vagonetkalar (Mine Carts):** Sig'imi $600\text{ kg}$ dan $1500\text{ kg}$ gacha bo'lgan g'ildirakli temir/yog'och aravachalar. Konchilar yoki eshak/otlar orqali tortiladi.
- **Qiya Tortgichlar (Incline Gravity Tramway):** To'la yukli vagonetka pastga tushayotganda arqon orqali bo'sh vagonetkani yuqoriga tortib chiqaradi.

---

# 32. SHAXTA O‘PIRILISHI (CAVE-IN & STRUCTURAL STABILITY)

Har qanday yerosti kovlash ishlari tabiiy tosh massivida kuchlar muvozanatini buzadi. Katta bo'shliqlar hosil qilinganda tog' bosimi shiftga og'irlik qiladi va halokatli kaskadli o'pirilishlar (cave-in) yuzaga keladi.

### 32.1. Shift Mustahkamligi Indeksi ($S_c$) ning Matematik Modeli

Har bir ochiq bo'shliq ustidagi shift blokida $(x, y, z)$ Shift Mustahkamlik Indeksi ($S_c$) uzluksiz baholanadi:

$$S_c = \frac{K_{rock} \cdot \max\left(1.0, \sum_{i \in \text{Supports}} \frac{R_{sup, i}^2}{d_i^2 + 0.1}\right)}{1.0 + \alpha_{span} \cdot \left( \frac{L_{span}}{2} \right)^2 \cdot \left( 1.0 + \beta_{depth} \cdot \frac{|y|}{100} \right)}$$

Shu bilan birga, yagona tayanch va to'g'ridan-to'g'ri ochiq oraliq uchun chiziqli me'yoriy formula quyidagicha ifodalanadi:

$$S_c = K_{rock} \cdot \left(\frac{R_{sup}}{L_{span}}\right)$$

Bu formulalarda:
- $K_{rock}$ — tog' jinsining valent mustahkamlik koeffitsiyenti (Rock Tensile Strength Factor).
- $R_{sup, i}$ — $i$-raqamli tirgakning samarali qo'llab-quvvatlash radiusi (metrlarda).
- $d_i$ — shift blokidan $i$-tirgakkacha bo'lgan Evklid masofasi.
- $L_{span}$ — qarama-qarshi turgan yaxlit qoya devorlari orasidagi eng qisqa masofa (tayanchsiz oraliq, metrlarda).
- $\alpha_{span} = 0.08$ — oraliq kengayishi kuchlanishining ko'rsatkich koeffitsiyenti.
- $\beta_{depth} = 0.35$ — har 100 metr chuqurlikdagi ustki qatlam bosimi ortish koeffitsiyenti.
- $y \le 0$ — chuqurlik koordinatasi.

**Xavfsizlik Mezonlari:**
- $S_c \ge 1.0$: Shift mutlaq barqaror va xavfsiz.
- $0.75 \le S_c < 1.0$: Kritik holat. Yog'och tirgaklar qisirlaydi, shiftdan mayda tosh va chang to'kiladi, konchilar vahimaga tushadi.
- $S_c < 0.75$: Beqarorlik chegarasi. Har 2.0 sekundda qulash ehtimoli $P_{collapse} = 1.0 - S_c$ bo'yicha tekshiriladi va o'pirilish boshlanadi.

### 32.2. Jinslar Mustahkamlik Koeffitsiyenti ($K_{rock}$) va Tirgak Radiusi ($R_{sup}$)

Quyidagi jadvalda tog' jinslarining tabiiy mustahkamlik koeffitsiyentlari keltirilgan:

| Jins Turi (Rock Type) | Geologik Klassifikatsiya | Mustahkamlik Koeffitsiyenti ($K_{rock}$) | Maksimal Tayanchsiz Oraliq ($L_{max}$ m) | O'pirilish Xarakteri |
|---|---|---|---|---|
| **Tuproq / Qum / Loy (Soil/Clay)** | Bo'shashgan cho'kindi | $0.20$ | $1.5\text{ m}$ | Darhol to'kiluvchi qum va gilli ko'chki |
| **Qumtosh / Ohaktosh (Sandstone/Limestone)**| Cho'kindi qatlamli | $0.55$ | $4.5\text{ m}$ | Qatlam bo'ylab yorilib, yirik plitalar tushishi |
| **Marmar / Granit (Marble/Granite)** | Metamorfik / Magmatik | $0.90$ | $9.0\text{ m}$ | Sekin darz ketuvchi, ulkan monolit bloklar |
| **Granit Monolit (Monolithic Granite)** | Magmatik intruziya | $1.40$ | $12.0\text{ m}$ | O'ta qattiq mustahkam tabiiy gumbaz |
| **Bazalt / Tub Qoya (Basalt/Bedrock)**| Vulkanik tub jins | $1.00$ | $10.0\text{ m}$ | Yuqori bosimga chidamli, yoriqsiz qattiq massiv |

Shaxtada quriladigan sun'iy tirgaklarning samaradorlik ko'rsatkichlari:

| Tirgak Turi (Support Type) | Material Tarkibi | Himoya Radiusi ($R_{sup}$ m) | Samarali Himoya Maydoni ($m^2$) | Yuklama Bardoshligi (kPa) |
|---|---|---|---|---|
| **Yumshoq Yog'och Tirgak (Softwood Timber)** | Qarag'ay / Qayin xodalari | $3.0\text{ m}$ | $28.3\text{ m}^2$ | $150\text{ kPa}$ |
| **Qattiq Yog'och Ramka (Hardwood Frame)** | Qalin eman (Oak) to'sinlari | $5.0\text{ m}$ | $78.5\text{ m}^2$ | $450\text{ kPa}$ |
| **Eman Tayanch Ustun (Reinforced Oak Post)** | Zich eman monolit ustun | $6.0\text{ m}$ | $113.1\text{ m}^2$ | $600\text{ kPa}$ |
| **Tarashlangan Tosh Ustun (Cut Stone Pillar)** | Ohaktosh / Granit bloklar | $7.5\text{ m}$ | $176.7\text{ m}^2$ | $1200\text{ kPa}$ |
| **Temir Qoplamali Kamar (Iron-Reinforced Arch)**| Temir armatura va tosh ark | $11.0\text{ m}$ | $380.1\text{ m}^2$ | $3500\text{ kPa}$ |

### 32.3. Tog' Bosimi Formulasi (Overburden Pressure)

Chuqurlik ortishi bilan qazuv maydoni ustidagi millionlab tonna tog' jinsining gidrostatik litostatik bosimi ortib boradi:

$$P_{overburden} = \rho_{rock} \cdot g \cdot |y| \quad (\text{kPa})$$

Bu yerda:
- $\rho_{rock} \approx 2600\text{ kg/m}^3$ — tog' jinslarining o'rtacha zichligi.
- $g = 9.81\text{ m/s}^2$ — erkin tushish tezlanishi.
- $|y|$ — chuqurlik (metrlarda). Masalan, $-100\text{ m}$ chuqurlikda litostatik bosim $P = 2600 \times 9.81 \times 100 = 2,550,600\text{ Pa} \approx 2550\text{ kPa}$ ($25.5\text{ bar}$) ga yetadi.

### 32.4. Kaskadli O'pirilish BFS Algoritmi (Cascading Cave-in Algorithm)

Bitta blok qulaganda qo'shni shift bloklaridagi kuchlanish keskin ortadi va zanjirli kaskadli reaksiya yuz beradi. Tizim Breadth-First Search (BFS) algoritmi bo'yicha ishlaydi:

```gdscript
func process_cave_in_cascade(start_pos: Vector3i, chunk_manager: ChunkManager) -> void:
	var queue: Array[Vector3i] = [start_pos]
	var visited: Dictionary = {start_pos: true}
	var collapsed_blocks: Array[Vector3i] = []

	while not queue.is_empty():
		var current_pos: Vector3i = queue.pop_front()
		var rock_type: int = chunk_manager.get_block(current_pos)
		if rock_type == 0:
			continue

		var stability: float = evaluate_ceiling_stability(current_pos, rock_type)
		if stability < 0.75:
			collapsed_blocks.append(current_pos)
			# Qo'shni shift bloklarini tekshirish (6 tomonlama bog'lanish)
			for offset in [Vector3i(1,0,0), Vector3i(-1,0,0), Vector3i(0,0,1), Vector3i(0,0,-1), Vector3i(0,1,0)]:
				var neighbor: Vector3i = current_pos + offset
				if not visited.has(neighbor) and chunk_manager.get_block(neighbor) != 0:
					visited[neighbor] = true
					queue.push_back(neighbor)

	# Barcha beqaror bloklarni fizik qulovchi ob'ektlarga aylantirish
	for pos in collapsed_blocks:
		spawn_falling_debris_block(pos, chunk_manager.get_block(pos))
		chunk_manager.set_block(pos, 0) # Havoga aylantirish
```

### 32.5. Qulovchi Bloklar Fizikasi va Miner Jarohati

1. **Jarohat Hisoblash Formulasi:**
   Qulagan har bir $1.0\text{ m}^3$ tosh blokining massasi $m_{block} \approx 2600\text{ kg}$. Tushish balandligi $h_{fall}$ ga qarab kinetik energiya orqali konchiga yetkaziladigan ezuvchi zarba (Blunt Damage):

$$\text{Damage}_{miner} = m_{block} \cdot v_{impact} \cdot 0.25 = 2600 \cdot \sqrt{2 \cdot g \cdot h_{fall}} \cdot 0.25$$

$3\text{ metr}$ balandlikdan tushgan kichik parcha ham $50\text{ HP}$ dan ortiq maydalovchi zarba beradi. Maxsus temir dubulg'asiz konchilar joyida halok bo'ladi.
2. **Tunnel To'silib Qolishi:** Tushgan toshlar polga to'kilib, tunnelni $100\%$ germetik to'sib qo'yadi. Orqada qolgan konchilar havo va oziq-ovqatsiz qolib ketadi; qutqaruv otryadlari qazib ochguncha nafas qisilishidan o'lish xavfi yuzaga keladi.

---

# 33. METAN GAZI VA PORTLASH (SUBTERRANEAN GAS ACCUMULATION & VENTILATION)

Yer qa'ridagi organik chirish va termokimyoviy jarayonlar natijasida chuqur shaxtalarda o'ta xavfli, ko'zga ko'rinmas gaz cho'ntaklari paydo bo'ladi.

### 33.1. To'rtta Asosiy Kon Gazi Kimyosi va Xususiyatlari

Subterranean tizimda 4 ta tarixiy va fizik kon gazi simulyatsiya qilinadi:

| Gaz Nomi (Gas Name) | Kimyoviy Formula | Zichlik ($\rho_{air}=1.0$) | Shaxtadagi Xatti-harakati | Portlash Diapazoni (% hajmiy) | Toksik / Halokatli Chegara | Aniqlash Usuli (Detection) |
|---|---|---|---|---|---|---|
| **Firedamp (Metan)** | $CH_4$ | $0.55$ (Yengil) | Shift bo'shliqlari va cho'ntaklariga ko'tariladi | $5.0\% - 15.0\%$ (Cho'qqi portlash $9.5\%$) | Zaharli emas, lekin kislorodni siqib chiqaradi ($>50\%$) | Davy chirog'ida moviy alanga gardishi |
| **Blackdamp (Bo'g'uvchi gaz)**| $CO_2 + N_2$ | $1.52$ (Og'ir) | Shaxta tubi, quduqlar va drenaj sumplariga cho'kadi | Yonmaydi (Alangani o'chiradi) | $O_2 < 12\%$ (3 daqiqada behushlik, asfiksiya) | Sham va mash'ala alangasining so'nishi |
| **Stinkdamp (Vodorod Sulfid)**| $H_2S$ | $1.19$ (Og'irroq) | Suvli qatlamlar va sulfid rudalari bo'ylab polga yoyiladi| $4.3\% - 46.0\%$ | $>500\text{ ppm}$ ($0.05\%$, asab falaji va tezkor o'lim) | Chirigan tuxum hidi, qafasdagi kanareyka |
| **Afterdamp (Is gazi)** | $CO$ | $0.97$ (Teng) | Yong'in va portlashdan keyin butun shaxta bo'ylab diffuziyalanadi | $12.5\% - 74.0\%$ | $>1200\text{ ppm}$ ($0.12\%$, 10 daqiqada o'lim) | Qafasdagi kanareyka hushidan ketishi |

### 33.2. Gaz Sizib Chiqishi va Shamollatish Differensial Tenglamasi

Shaxta kamerasidagi gaz konsentratsiyasi $C_{gas}(t)$ (% hajmiy ulush) vaqt o'tishi bilan ochiq ruda yuzasidan gaz sizib chiqishi va ventilyatsiya tizimi chiqindisi balansiga tayanadi:

$$\frac{dC_{gas}}{dt} = \frac{G_{seep}(y) \cdot A_{wall}}{V_{cavity}} - \frac{Q_{vent}}{V_{cavity}} \cdot C_{gas}(t)$$

Bu yerda:
- $V_{cavity}$ — shaxta xonasining umumiy hajmi ($m^3$).
- $A_{wall}$ — ochiq turgan ko'mir yoki sulfid qatlamining devor sathi maydoni ($m^2$).
- $G_{seep}(y) = G_0 \cdot (1.0 + 0.005 \cdot |y|)$ — chuqurlikka bog'liq gaz sizish tezligi ($m^3 / (m^2 \cdot \text{soat})$). Ko'mir uchun $G_0 = 0.08$, oltingugurt uchun $G_0 = 0.15$.
- $Q_{vent}$ — ventilyatsiya orqali chiqarilayotgan havo hajmi ($m^3 / \text{soat}$).

Ushbu differensial tenglamaning analitik aniq yechimi:

$$C_{gas}(t) = \frac{G_{seep} \cdot A_{wall}}{Q_{vent}} + \left( C_0 - \frac{G_{seep} \cdot A_{wall}}{Q_{vent}} \right) e^{-\frac{Q_{vent}}{V_{cavity}} \cdot t}$$

**Ventilyatsiya Quvvati ($Q_{vent}$):**
- Tabiiy konveksiya quvuri: $Q_{vent} = 15.0 \cdot \sqrt{\Delta h_{shaft}}\text{ m}^3/\text{soat}$.
- Qo'lda aylanuvchi charm bosqon (Bellows): $Q_{vent} = 120.0\text{ m}^3/\text{soat}$.
- Suv charxpalagi yoki shamol tegirmoniga ulangan markazdan qochma ventilyator: $Q_{vent} = 850.0\text{ m}^3/\text{soat}$.

### 33.3. Gaz Qidirish va Aniqlash Metodlari (Davy Lamp & Canary)

1. **Devi Xavfsiz Shaxta Chirog'i (Davy Safety Lamp):**
   - Sir Devid Devi ixtirosi bo'lgan zich sim to'rli mis chiroq. Olov alangasini sim to'r sovutadi va tashqaridagi metanni chaqnatmaydi.
   - O'yinchi chiroqqa qaraganda metan darajasi aniqlanadi: agar havoda metan $2\%$ dan oshsa, olov tepasida moviy qalpog'cha (blue halo cap) paydo bo'ladi. Qalpog'cha balandligi metan foiziga to'g'ri proporsionaldir.
2. **Qafasdagi Konchi Kanareykasi (Canary Bird):**
   - Kanareykalarning metabolizmi va kislorod sarfi odamnikidan 15 barobar tez.
   - Havoda is gazi ($CO$) yoki vodorod sulfid ($H_2S$) paydo bo'lganda, kanareyka bezovtalanadi, sayrashdan to'xtaydi va 2 daqiqa ichida qafas poliga ag'dariladi. Bu konchilar uchun shoshilinch evakuatsiya signali hisoblanadi.

### 33.4. Portlash Mexanikasi va Portlash Radiusi Formulasi

Agar metan konsentratsiyasi portlash chegarasida ($5.0\% \le C_{CH4} \le 15.0\%$) bo'lsa va kameraga ochiq olov (mash'ala, oddiy sham yoki chaqmoqtosh uchquni) kiritilsa, bir lahzali deflagratsion portlash ro'y beradi.

Portlashda ajralib chiqadigan umumiy kinetik energiya:

$$E_{blast} = V_{pocket} \cdot \left(\frac{C_{CH4}}{100}\right) \cdot \Delta H_{combustion} \quad (\Delta H = 35.8\text{ MJ/m}^3)$$

Hosil bo'lgan zarba to'lqinining to'liq vayron qilish radiusi ($R_{destruct}$):

$$R_{destruct} = 0.28 \cdot \sqrt[3]{E_{blast}\text{ (in kJ)}}$$

**Portlash Oqibatlari:**
- $R_{destruct}$ ichidagi barcha yog'och tirgaklar parchalanib ketadi.
- Darhol ulkan ikkilamchi kaskadli o'pirilish (Secondary Cave-in) boshlanadi.
- Radiusdagi barcha jonli mavjudotlar $100 - 300\text{ HP}$ olovli va zarbali portlash zarari oladi.
- Kislorod bir zumda yonib tugab, o'rnida o'ldiruvchi Afterdamp ($CO$) gazi hosil bo'ladi.

---

# 34. 20+ GEOLOGIK MINERALLAR (24 GEOLOGICAL MINERALS & GEMS MASTER BALANCE TABLE)

Voxel Lord: Feudal Realm geologik katalogi feodal davr konchilik, metallurgiya, zargarlik, kimyo va qurilish ehtiyojlarini to'liq qamrab oluvchi 24 ta tabiiy mineral, tosh va qimmatbaho javohirlardan iborat.

### 34.1. 24 ta Mineral va Qimmatbaho Javohirlar Balans Jadvali

Quyidagi jadvalda dunyodagi barcha 24 ta mineralning qatlam chuqurligi taqsimoti, Gauss parametrlari, qattiqligi, asbob talablari va iqtisodiy qiymati to'liq belgilangan:

| # | Mineral / Javohir Nomi | Toifa (Category) | Qatlam Chuqurligi (Depth Strata m) | $y_{peak}$ (m) | $\sigma_y$ (m) | $P_{peak}$ (%) | Tomir O'lchami (Vein voxels) | Talab Qilinadigan Asbob Tieri | Qattiqlik (Hardness Hits) | Bazaviy Qiymat (Kumush) | Birlamchi Chiqish / Qayta Ishlash |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **O'simlik Tuprog'i (Topsoil / Loam)** | Tuproq | $0 \to -15\text{ m}$ | $-2\text{ m}$ | $5.0$ | $100.0\%$ | Yaxlit qatlam | Qo'l / Yog'och Belkurak | 1 | 0.05 | Haydalgan ekin maydoni / Kompost |
| 2 | **Kulolchilik Loyi (Clay)** | Cho'kindi | $0 \to -35\text{ m}$ | $-10\text{ m}$ | $8.0$ | $45.0\%$ | $12 - 36$ | Yog'och Belkurak | 2 | 0.20 | Kulolchilik xumdoni $\to$ Pishgan g'isht va idishlar |
| 3 | **Yoqilg'i Torfi (Peat)** | Yonuvchi organika | $0 \to -25\text{ m}$ | $-8\text{ m}$ | $6.0$ | $35.0\%$ | $16 - 48$ | Yog'och Belkurak | 2 | 0.30 | Quritilgan briket $\to$ O'choq yoqilg'isi ($1.2\times$ yog'och) |
| 4 | **Qumtosh (Sandstone)** | Cho'kindi jins | $-5 \to -60\text{ m}$ | $-25\text{ m}$ | $15.0$ | $60.0\%$ | Yaxlit qatlam | Tosh Cho'kich | 3 | 0.40 | Tosh yo'nuvchi $\to$ 1-Tier devor bloklari |
| 5 | **Ohaktosh (Limestone)** | Cho'kindi karbonat| $-15 \to -90\text{ m}$ | $-45\text{ m}$ | $20.0$ | $50.0\%$ | $24 - 64$ | Tosh Cho'kich | 4 | 0.60 | So'ndirilgan ohak (qurilish qorishmasi) / Metallurgiya flyusi |
| 6 | **Tosh Tuzi (Halite / Rock Salt)** | Cho'kindi mineral | $-20 \to -120\text{ m}$ | $-60\text{ m}$ | $25.0$ | $30.0\%$ | $18 - 40$ | Tosh Cho'kich | 3 | 2.50 | Tuzlash $\to$ Go'sht va baliqni uzoq saqlash |
| 7 | **Toshko'mir (Coal)** | Qazilma yoqilg'i | $-15 \to -180\text{ m}$ | $-75\text{ m}$ | $35.0$ | $55.0\%$ | $20 - 50$ | Tosh Cho'kich | 4 | 1.00 | Koks / Domna pechi yoqilg'isi ($3.0\times$ yog'och) |
| 8 | **Mis Rudasi (Copper / Chalcopyrite)**| Birlamchi metall | $-10 \to -110\text{ m}$ | $-50\text{ m}$ | $22.0$ | $40.0\%$ | $14 - 32$ | Tosh Cho'kich | 5 | 1.80 | Eritish pechi $\to$ Sof Mis quyma (Copper Ingot) |
| 9 | **Qalay Rudasi (Tin / Cassiterite)** | Rangli metall | $-25 \to -130\text{ m}$ | $-70\text{ m}$ | $24.0$ | $32.0\%$ | $10 - 24$ | Mis Cho'kich | 5 | 2.20 | Eritish: Mis bilan qo'shilib Bronza quymasi olinadi |
| 10 | **Oltingugurt (Sulfur)** | Vulkanik / Cho'kindi| $-40 \to -220\text{ m}$ | $-120\text{ m}$ | $30.0$ | $25.0\%$ | $8 - 20$ | Mis Cho'kich | 4 | 3.00 | Porox tayyorlash / Alkimyo / Teri oshlash |
| 11 | **Selitra (Saltpeter / Niter)** | Kimyoviy mineral | $-30 \to -160\text{ m}$ | $-90\text{ m}$ | $28.0$ | $22.0\%$ | $8 - 18$ | Mis Cho'kich | 3 | 3.50 | Qora porox komponenti / Mineral o'g'it ($+30\%$ hosil) |
| 12 | **Temir Rudasi (Iron / Hematite)** | Qora metall | $-45 \to -240\text{ m}$ | $-130\text{ m}$ | $40.0$ | $45.0\%$ | $16 - 42$ | Bronza Cho'kich | 7 | 4.00 | Domna pechi $\to$ Cho'yan va Temir quymasi (Iron Ingot) |
| 13 | **Qo'rg'oshin (Lead / Galena)** | Og'ir metall | $-60 \to -210\text{ m}$ | $-140\text{ m}$ | $35.0$ | $28.0\%$ | $12 - 26$ | Bronza Cho'kich | 6 | 3.20 | Qamal toshlari / Tom qoplamasi / Pevter qotishmasi |
| 14 | **Rux Rudasi (Zinc / Sphalerite)** | Rangli metall | $-70 \to -230\text{ m}$ | $-150\text{ m}$ | $35.0$ | $25.0\%$ | $10 - 22$ | Bronza Cho'kich | 6 | 3.80 | Mis bilan legirlash $\to$ Jez / Latun quymasi (Brass) |
| 15 | **Nikel (Nickel / Pentlandite)** | Oliy metall | $-90 \to -260\text{ m}$ | $-175\text{ m}$ | $38.0$ | $20.0\%$ | $8 - 18$ | Temir Cho'kich | 8 | 5.50 | Po'lat legirlash $\to$ Mustahkam Damashq po'lati |
| 16 | **Oq Marmar (Marble)** | Metamorfik tosh | $-50 \to -280\text{ m}$ | $-160\text{ m}$ | $50.0$ | $30.0\%$ | $32 - 96$ | Temir Cho'kich | 8 | 6.00 | Haykaltaroshlik / Sobor ustunlari / Saroy plitalari |
| 17 | **Kulrang Granit (Granite)** | Magmatik intruziya| $-80 \to -350\text{ m}$ | $-220\text{ m}$ | $65.0$ | $65.0\%$ | Yaxlit qatlam | Temir Cho'kich | 10 | 2.00 | Qal'a poydevori / Qamalga chidamli mustahkam devor |
| 18 | **Kumush Rudasi (Silver / Acanthite)**| Qimmatbaho metall | $-110 \to -280\text{ m}$| $-195\text{ m}$ | $35.0$ | $18.0\%$ | $8 - 18$ | Temir Cho'kich | 8 | 15.00 | Zarbxona $\to$ Feodal Kumush Tanga (Asosiy valyuta) |
| 19 | **Oltin Rudasi (Native Gold)** | Qimmatbaho metall | $-160 \to -340\text{ m}$| $-250\text{ m}$ | $40.0$ | $12.0\%$ | $6 - 14$ | Po'lat Cho'kich | 10 | 100.00 | Zarbxona $\to$ Oltin Dinar (1 Oltin = 100 Kumush) |
| 20 | **Platina Rudasi (Platinum)** | Oliy asil metall | $-220 \to -350\text{ m}+$| $-290\text{ m}$| $30.0$ | $6.0\%$ | $4 - 10$ | Po'lat Cho'kich | 12 | 220.00 | Hukmdor toji / Qirollik regaliyalari va muqaddas idishlar |
| 21 | **Vulkanik Bazalt (Basalt)** | Magmatik efuziv | $-250 \to -350\text{ m}+$| $-320\text{ m}$| $45.0$ | $50.0\%$ | Yaxlit qatlam | Po'lat Cho'kich | 12 | 3.00 | O'ta issiqqa chidamli domna pechi devorlari |
| 22 | **Zumrad (Emerald / Beryl)** | Qimmatbaho javohir| $-120 \to -260\text{ m}$| $-190\text{ m}$ | $25.0$ | $4.0\%$ | $2 - 6$ | Po'lat Cho'kich | 14 | 180.00 | Sayqallash ustaxonasi $\to$ Sayqallangan Zumrad (+Axloq) |
| 23 | **Yoqut (Ruby / Corundum)** | Qimmatbaho javohir| $-180 \to -320\text{ m}$| $-260\text{ m}$ | $30.0$ | $3.0\%$ | $2 - 5$ | Damashq Cho'kich | 16 | 280.00 | Qilich sopi bezagi / Qirollik xazinasi (+Obro') |
| 24 | **Olmos (Diamond)** | Oliy javohir | $-280 \to -350\text{ m}+$| $-330\text{ m}$| $22.0$ | $1.5\%$ | $1 - 4$ | Damashq/Runik Cho'kich| 20 | 500.00 | Runik kuchaytirish / Olmos parma / Imperator Asosi |

### 34.2. Mineral Guruhlarning Iqtisodiy va Texnologik Vazifalari

1. **Agro va Maishiy Cho'kindilar (1–3):** Koloniyaning dastlabki kunlaridanoq qishloq xo'jaligi, o'choq yoqish va boshpana qurish poydevorini yaratadi.
2. **Qurilish Toshlari (4, 5, 16, 17, 21):** Feodal qal'a va shaharlar arxitekturasini mustahkamlaydi. Granit va Bazalt dushman trebuchetlarining og'ir zarbalariga eng yuqori qarshilik ko'rsatadi.
3. **Metallurgiya Rudalari (8, 9, 12, 13, 14, 15):** Asbobsozlik, qurol-yarog' va zirh ishlab chiqarish sanoatining moddiy asosi.
4. **Kimyo va Poroxsozlik (10, 11):** Xitoy va Sharq alkimyosi orqali qora porox tayyorlash, tog' jinslarini portlatish va mushket o'qlari ishlab chiqarishga imkon beradi.
5. **Monetar va Qimmatbaho Javohirlar (6, 18, 19, 20, 22, 23, 24):** Savdo-sotiq, tashqi diplomatiya, qirollik soliqlarini to'lash va imperiya xazinasini boyitish vositalari.

---

# 35. METALLURGIYA ZANJIRI (METALLURGICAL CHAIN, SMELTING & FORGING)

Metallurgiya — Voxel Lord: Feudal Realm harbiy qudrati va sanoat taraqqiyotining yuragi hisoblanadi. Xom rudaning tayyor qilich yoki ritsar sovutiga aylanishi ko'p bosqichli fizik-kimyoviy jarayonlardan iborat.

### 35.1. To'liq Metallurgiya Qayta Ishlash Bosqichlari

Xom ruda quyidagi zanjir bo'yicha bosqichma-bosqich qayta ishlanadi:

```
[Ruda Qazish] 
      ↓
[Maydalash va Suvda Yuvish] (Gravitatsion boyitish, +25% unum)
      ↓
[Ochiq Qovurish / Roasting] (Oltingugurt va namlikni haydash)
      ↓
[Domna / Eritish Pechida Qaynatish] (+ Ohaktosh Flyusi va Ko'mir)
      ↓
[Shlakni Ajratish va Cho'yan / Shpon Temir Olish]
      ↓
[Tigel / Tigelda Legirlash va Qotishma Hosil Qilish] (Bronza, Po'lat)
      ↓
[Temirchilik Bosqoni va Sandonda Zarb Berish] (Plastik deformatsiya)
      ↓
[Termik Ishlov: Chiniqtirish va Bo'shatish] (Quenching & Tempering)
      ↓
[Tayyor Qurol / Sovut / Ishchi Asbob]
```

1. **Maydalash va Gravitatsion Yuvish:** Og'ir ruda toshlari yog'och to'qmoqlar bilan maydalanadi va oqar suv novlarida yuviladi. Bo'sh tog' jinsi oqib ketadi, og'ir metall zarrachalari cho'kadi (Boyitish darajasi $+25\%$).
2. **Qovurish (Roasting):** Sulfidli rudalar (xalkopirit, galenit) ochiq o'tda $500^\circ\text{C}$ da qovurilib, zararli gazlar uchirib yuboriladi.

### 35.2. Flyus Kimyosi va Ohaktoshning Vazifasi (Flux Chemistry)

Domna pechiga temir rudasi bilan birga Ohaktosh ($CaCO_3$) qo'shilishi shart. Harorat $900^\circ\text{C}$ dan oshganda ohaktosh parchalanadi:

$$CaCO_3 \xrightarrow{\Delta} CaO + CO_2\uparrow$$

Hosil bo'lgan so'nmagan ohak ($CaO$) rudaning tarkibidagi kvars va qum qoldiqlari ($SiO_2$) bilan reaksiyaga kirishadi:

$$CaO + SiO_2 \to CaSiO_3 \quad (\text{Suyuq Shlak / Slag})$$

**Texnologik Ahamiyati:**
- Agar ohaktosh flyusi solinmasa, qovushqoq kremniy shlaki domna pechini tiqib qo'yadi (Furnace Choking) va pech portlab ishdan chiqadi.
- Suyuq shlak erigan og'ir temir yuzasiga qalqib chiqadi va maxsus tirqishdan oqizib olinadi. Natijada olingan quyma tozaligi $+35\%$ ga oshadi.

### 35.3. Asosiy Qotishmalar Retsepti va Xususiyatlari

Metallurgiya pechlarida turli metallarni aralashtirish orqali yuqori xossali qotishmalar eritiladi:

| Qotishma Nomi (Alloy) | Komponentlar Nisbati | Erish Harorati (°C) | Qattiqlik Koeffitsiyenti | Asosiy Xossalari va Ishlatilish Sohasi |
|---|---|---|---|---|
| **Klassik Bronza (Bronze)** | $88\%$ Mis + $12\%$ Qalay | $950^\circ\text{C}$ | 6 | Korroziyaga chidamli, oson quyiladi; dastlabki pishiq asboblar, to'plar va qilichlar |
| **Jez / Latun (Brass)** | $68\%$ Mis + $32\%$ Rux | $920^\circ\text{C}$ | 5 | Oltinsimon yaltiroq, zanglamaydi; saroy bezaklari, soat mexanizmlari, quvur jo'mraklari |
| **Pevter (Pewter)** | $88\%$ Qalay + $10\%$ Qo'rg'oshin + $2\%$ Mis | $230^\circ\text{C}$ | 3 | Past erish harorati; zodagonlar idish-tovog'i, shamdonlar va bezak buyumlari |
| **Uglerodli Po'lat (Carbon Steel)**| $98.5\%$ Temir + $1.5\%$ Ko'mir/Uglerod | $1450^\circ\text{C}$ | 9 | Yuqori elastiklik va mustahkamlik; ritsar qilichlari, plastinka sovutlar, po'lat cho'kichlar |
| **Damashq Po'lati (Damascus Steel)**| $95\%$ Yuqori uglerodli po'lat + $5\%$ Nikel | $1400^\circ\text{C}$ | 14 | 256 qatlam buklab zarblangan to'lqinsimon po'lat; sinmaydi, o'tmaslashmaydi; afsonaviy qurollar |

### 35.4. Pech Turlari va Harorat Rejimlari

1. **Sirchiq Pech (Primitive Bloomery):**
   - Loy va toshdan yasalgan quvur pech. Harorat $950^\circ\text{C} - 1150^\circ\text{C}$.
   - Temir to'liq erimaydi, balki g'ovak shpon temir (Iron Sponge / Bloom) hosil bo'ladi. To'qmoq bilan urib shlakdan tozalanadi.
2. **Katta Domna Pechi (Blast Furnace):**
   - Balandligi 6–10 metrli tosh minora. Qo'sh bosqonlar suv charxpalagi orqali uzluksiz havo purkaydi.
   - Harorat $1350^\circ\text{C} - 1550^\circ\text{C}$. Temir to'liq suyuqlanib cho'yan (Pig Iron) holida ariqchalarga oqadi.
3. **Tigel Pechi (Crucible Furnace):**
   - Grafit va o'tga chidamli loy tigellar. Harorat $1400^\circ\text{C} - 1650^\circ\text{C}$.
   - Oliy sifatli Damashq po'lati va asil metallar (oltin, kumush) eritishda ishlatiladi.

### 35.5. Chiniqtirish Suyuqliklari va Termik Ishlov (Quenching & Tempering)

Temirchi qizdirilgan qurolni sandonda zarb qilgach, po'latning ichki kristall panjarasini qotirish uchun maxsus suyuqliklarda chiniqtiradi:
1. **Muzdek Suv (Water Quench):**
   - Eng tez sovitish usuli. Po'lat juda qattiq bo'ladi, lekin mo'rtlik ortib, urilganda sinib ketish xavfi tug'iladi.
2. **Zig'ir yoki Zaytun Moyi (Oil Quench):**
   - Sekinroq va bir maromda sovitish. Qattiqlik va elastiklik o'rtasida mukammal muvozanat hosil qiladi. Jangovar qilichlar uchun standart usul.
3. **Tuzli Sho'rva (Brine Quench):**
   - $10\%$ li tuzli suv bug' pardasini yorib o'tib agressiv sovitadi. Faqat og'ir zirh plitalari uchun qo'llaniladi.
4. **Bo'shatish (Tempering):**
   - Chiniqqan po'lat $250^\circ\text{C} - 350^\circ\text{C}$ gacha past olovda qayta qizdirilib, sekin sovitiladi. Bu ichki kuchlanishlarni yo'qotadi va pichoqning qayrilganda sinmasligini ta'minlaydi.

---

# 36. DEHQONCHILIK VA EKINLAR (AGRICULTURE & CROP GROWTH SIMULATION)

Voxel Lord: Feudal Realm qishloq xo'jaligi tizimi o'simlik biologiyasi, gidrologiya va tuproq kimyosi qonuniyatlariga asoslangan chuqur matematik simulyatsiya modeli orqali boshqariladi. Har bir ekin maydoni $2\times2$ voxel o'lchamidagi haydalgan tuproq (tilled farmland) bloklarida joylashadi.

### 36.1. Simulyatsiya Vaqt Bazasi va O'sish Taktlari (Simulation Time Base)

O'yinda barcha qishloq xo'jaligi va iqtisodiy jarayonlar qat'iy vaqt integratsiyasiga bo'ysunadi:
- **1 Real Sekund:** 1 O'yin Daqiqasiga teng (`TICK_DELTA = 1.0s`).
- **1 O'yin Soati:** 60 Simulyatsiya Takti (60 Real Sekund).
- **1 O'yin Kuni:** 24 O'yin Soati = 1,440 Takt = 24 Real Daqiqa.
- **1 Fasl (Season):** 7 O'yin Kuni = 10,080 Takt $\approx$ 2.8 Real Soat.
- **1 O'yin Yili:** 4 Fasl (Bahor, Yoz, Kuz, Qish) = 28 O'yin Kuni = 40,320 Takt $\approx$ 11.2 Real Soat.
- **Ekin O'sishini Baholash Oralig'i:** Har 60 Taktda (1 O'yin Soatida bir marta).

### 36.2. O'sish Progressi Formulalari (Crop Growth Equations)

Har bir soatlik baholash taktida o'simlikning pishib yetilish darajasi quyidagi differensial tenglama orqali oshiriladi:

$$\Delta Growth = \frac{1.0}{BaseGrowthHours} \times M_{fertility} \times M_{moisture} \times M_{temp} \times M_{tending}$$
$$GrowthProgress_{t+1} = \min\left(1.0, \; GrowthProgress_t + \Delta Growth\right)$$

O'simlik $GrowthProgress \ge 1.0$ qiymatiga yetganda, u vizual ravishda "Pishib Yetilgan (Mature Harvestable)" fazasiga o'tadi va hosil yig'ishga tayyor bo'ladi.

#### Modifikatorlar va Matematik Funksiyalar:
1. **Tuproq Unumdorligi Modifikatori ($M_{fertility}$):**
   $$M_{fertility} = 0.40 + 0.60 \times \left(\frac{SoilFertility}{100.0}\right)$$
   Unumdorligi $0\%$ bo'lgan qaqragan tuproqda ham ekin minimal $0.40\times$ tezlikda o'sadi, biroq sifati nihoyatda past bo'ladi.

2. **Tuproq Namligi Modifikatori ($M_{moisture}$):**
   $$M_{moisture} = \begin{cases} 
     \frac{Moisture}{30.0} \times 0.60, & \text{agar } Moisture < 30\% \text{ (Qurg'oqchilik / Chanqash)} \\
     1.00, & \text{agar } 30\% \le Moisture \le 80\% \text{ (Optimal Gidratsiya)} \\
     1.00 - \frac{Moisture - 80.0}{20.0} \times 0.50, & \text{agar } Moisture > 80\% \text{ (Botqoqlanish / Ildiz chirishi)}
   \end{cases}$$

3. **Atrof-muhit Harorati Modifikatori ($M_{temp}$):**
   - Agar $T_{ambient} < T_{min}$: O'sish to'liq muzlaydi ($M_{temp} = 0.0$). Agar harorat $-5^\circ\text{C}$ dan past bo'lib, 12 soatdan ortiq davom etsa, sovuqqa chidamsiz ekin nobud bo'ladi (`Withered Dead Crop`).
   - Agar $T_{min} \le T_{ambient} \le T_{max}$:
     $$M_{temp} = \max\left(0.10, \; 1.0 - \left(\frac{|T_{ambient} - T_{opt}|}{T_{opt} - T_{min}}\right)^2 \times 0.50\right)$$
   - Agar $T_{ambient} > T_{max}$: Ekin issiqdan quriydi va so'liydi ($M_{temp} = 0.20$).

4. **Dehqon Mehnatining Parvarish Modifikatori ($M_{tending}$):**
   - **Tashlandiq / Begona o't bosgan (Weedy/Neglected):** $0.70\times$.
   - **Boshlang'ich dehqon tomonidan o'toq qilingan (Novice Farmer):** $1.00\times$.
   - **Usta dehqon tomonidan mulchalangan va chopilgan (Master Farmer):** $1.35\times$.

### 36.3. 9 Asosiy Ekin Balans Jadvali (9-Crop Master Balance Table)

| Ekin ID | Ekin Nomi (O'zbek / Ingliz) | Pishish Vaqti (Kun / Soat) | Ekish Fasli | O'rish / Yig'im Fasli | $T_{min} / T_{opt} / T_{max}$ | Bazaviy Hosil ($2\times2$ plot) | Kunlik Suv Sarfi | Asosiy Tuproq Ozuqasi |
|---|---|---|---|---|---|---|---|---|
| `crop_wheat` | Bug'doy (Wheat) | 4 kun (96 soat) | Bahor / Yoz | Yoz / Kuz | $5^\circ\text{C} / 22^\circ\text{C} / 35^\circ\text{C}$ | 8 Bog'lam (Sheaves) | 15% | Azot (N) Kuchli iste'molchi |
| `crop_barley` | Arpa (Barley) | 3 kun (72 soat) | Bahor / Yoz | Yoz / Kuz | $3^\circ\text{C} / 19^\circ\text{C} / 32^\circ\text{C}$ | 7 Bog'lam (Sheaves) | 12% | O'rtacha N-P iste'molchi |
| `crop_rye` | Kuzgi Javdar (Winter Rye) | 4 kun (96 soat) | Kuz (Qishki) | Bahor / Yoz | $-2^\circ\text{C} / 15^\circ\text{C} / 28^\circ\text{C}$ | 6 Bog'lam (Sheaves) | 10% | Ayozbardosh Yengil iste'molchi |
| `crop_cabbage`| Karam (Cabbage) | 2.5 kun (60 soat) | Bahor / Kuz | Yoz / Qish | $0^\circ\text{C} / 16^\circ\text{C} / 26^\circ\text{C}$ | 12 Bosh (Heads) | 22% | Kaliy (K) Kuchli iste'molchi |
| `crop_turnip` | Sholg'om (Turnip) | 2 kun (48 soat) | Kuz / Qish | Qish / Bahor | $-4^\circ\text{C} / 12^\circ\text{C} / 24^\circ\text{C}$ | 14 Ildizmeva (Roots) | 10% | Qattiq sovuqqa bardoshli |
| `crop_carrot` | Sabzi (Carrot) | 2 kun (48 soat) | Bahor / Yoz | Yoz / Kuz | $4^\circ\text{C} / 18^\circ\text{C} / 30^\circ\text{C}$ | 10 Ildizmeva (Roots) | 14% | Fosfor (P) Yengil iste'molchi |
| `crop_flax` | Zig'ir (Flax / Linen) | 3.5 kun (84 soat) | Bahor | Yoz | $8^\circ\text{C} / 20^\circ\text{C} / 30^\circ\text{C}$ | 6 Poyacha + 3 Urug' | 16% | To'qimachilik / Ip xomashyosi |
| `crop_hops` | Xmel (Hops - Pivo guli) | 5 kun (120 soat) | Bahor | Kuz | $10^\circ\text{C} / 24^\circ\text{C} / 34^\circ\text{C}$ | 10 G'udda (Cones) | 25% | Pivo sanoati uchun |
| `crop_peas` | Mosh / Beda (Peas / Alfalfa) | 2.5 kun (60 soat) | Bahor / Yoz | Yoz / Kuz | $4^\circ\text{C} / 20^\circ\text{C} / 30^\circ\text{C}$ | 6 Dukkak (Pods) | 12% | **Azot Tiklovchi (Restorer)** |

### 36.4. Yakuniy Hosil Miqdori Formulalari (Harvest Yield Formula)

Dehqon pishgan ekinni o'rog'i bilan o'rib olganda, chiqadigan haqiqiy xomashyo soni quyidagicha aniqlanadi:

$$FinalYield = \left\lfloor BaseYield \times \left(0.50 + 0.50 \cdot \frac{SoilFertility}{100.0}\right) \times \left(1.0 + 0.40 \cdot IrrigationActive\right) \times \left(1.0 + 0.05 \cdot Skill_{farmer}\right) \times QualityMult_{tool} \right\rfloor$$

Bunda:
- $IrrigationActive = 1$, agar ekin maydoni faol sug'orish arig'i ta'sirida bo'lsa; aks holda $0$.
- $Skill_{farmer} \in [0, 10]$: Dehqonchilik darajasi (har bir daraja $+5\%$ qo'shimcha hosil beradi).
- $QualityMult_{tool}$: O'roq sifati koeffitsiyenti (Fine = 1.25x, Masterwork = 1.60x don to'kilishini kamaytiradi).

---

# 37. TUPROQ UNUMDORLIGI VA ALMASHINLAB EKISH (SOIL FERTILITY & CROP ROTATION)

Voxel Lord: Feudal Realm simulyatsiyasida yer shunchaki bo'sh sirt emas, balki mineral balansga ega tirik resursdir. Har bir shudgorlangan tuproq katagi o'zida N-P-K (Azot, Fosfor, Kaliy) elementlarini saqlaydi.

### 37.1. Ozuqa Moddalari Yemirilish Matritsasi (Nutrient Depletion Matrix)

Har bir hosil yig'ilganda ekin turi tuproqning umumiy unumdorligini va alohida ozuqa elementlarini quyidagi miqdorda kamaytiradi:

| Ekinlar Toifasi | Vakil Ekinlar | Azot (N) Yo'qotilishi | Fosfor (P) Yo'qotilishi | Kaliy (K) Yo'qotilishi | Umumiy Unumdorlik Pasayishi |
|---|---|---|---|---|---|
| **Kuchli Don Ekinlari** | Bug'doy, Arpa | $-14.0\%$ | $-8.0\%$ | $-8.0\%$ | **$-10.0\%$** |
| **Bargli Sabzavotlar** | Karam | $-8.0\%$ | $-6.0\%$ | $-16.0\%$ | **$-10.0\%$** |
| **Ildizmevalar** | Sholg'om, Sabzi | $-5.0\%$ | $-5.0\%$ | $-5.0\%$ | **$-5.0\%$** |
| **Sanoat Ekinlari** | Zig'ir, Xmel | $-10.0\%$ | $-10.0\%$ | $-10.0\%$ | **$-10.0\%$** |
| **Dukkaklilar / Beda** | Mosh, No'xat, Beda | **$+22.0\%$ (Boyitadi!)**| $-2.0\%$ | $-2.0\%$ | **$+6.0\%$ (Tiklaydi!)** |

### 37.2. Monomadaniyat Jazosi (Monoculture Penalty Equation)

Agar bir xil ekin bir maydonga ketma-ket bir necha mavsum davomida ekilsa, tuproqning charchashi va zararkunandalar ko'payishi keskin tezlashadi:

$$FertilityDecay_{monoculture} = FertilityDecay_{base} \times \left(1.0 + 0.50 \cdot ConsecutivePlantings\right)$$

- 1-marta takrorlanganda: Yemirilish $1.50\times$, begona o't/zamburug' ehtimoli $+20\%$.
- 2-marta takrorlanganda: Yemirilish $2.00\times$, kasallik ehtimoli $+40\%$.
- 3-marta takrorlanganda: Yemirilish $2.50\times$, maydonda qora chirish (Blight) epidemiyasi boshlanadi va hosilning $80\%$ qismi nobud bo'ladi.

### 37.3. Tuproqni Qayta Tiklash Usullari (Soil Restoration Mechanics)

1. **Vadasht Qoldirish (Fallow Field):**
   Ekin ekilmagan, dam berilgan maydon har o'yin kuni tabiiy ravishda $+1.5\%$ unumdorlikni tiklaydi (1 faslda $+10.5\%$).
2. **Qo'ton / Hayvon Boqish (Livestock Grazing on Fallow):**
   Vadasht yerda qo'y yoki qoramol boqilsa, tabiiy go'ng hisobiga tiklanish sur'ati kuniga $+4.0\%$ gacha oshadi.
3. **Kompost va Chirindi Solish (Manure / Compost Application):**
   Kompost chuqurida chirigan go'ng va somondan tayyorlangan 1 bochka kompost yer unumdorligini darhol $+25\%$ ga oshiradi (maksimal $100\%$ gacha).
4. **Yog'och Kuli va Ohak Solish (Wood Ash & Lime Treatment):**
   O'choq kuli solish tuproqdagi Kaliy (K) miqdorini $+15\%$ ga oshiradi va unumdorlik chegarasini $120\%$ gacha ochib beradi (Terra Preta effekti — hosil hajmi $+20\%$ ga oshadi).

### 37.4. Kanonik 4 Dalali Almashlab Ekish Jadvali (Canonical 4-Field Crop Rotation)

O'rta asrlarning eng samarali to'rt dalali dehqonchilik tizimi tuproqni hech qachon qashshoqlashtirmasdan yuqori hosil olishni ta'minlaydi:

| Dala Maydoni | 1-Yil (Year 1) | 2-Yil (Year 2) | 3-Yil (Year 3) | 4-Yil (Year 4) |
|---|---|---|---|---|
| **Dala A (Plot A)** | Bug'doy (Azot sarflovchi g'alla)| Mosh / Beda (Azot tiklovchi dukkak)| Sholg'om / Sabzi (Ildizmeva) | Vadasht + Qo'y boqish (Dam olish) |
| **Dala B (Plot B)** | Vadasht + Qo'y boqish (Dam olish) | Bug'doy (Azot sarflovchi g'alla)| Mosh / Beda (Azot tiklovchi dukkak)| Sholg'om / Sabzi (Ildizmeva) |
| **Dala C (Plot C)** | Sholg'om / Sabzi (Ildizmeva) | Vadasht + Qo'y boqish (Dam olish) | Bug'doy (Azot sarflovchi g'alla)| Mosh / Beda (Azot tiklovchi dukkak)|
| **Dala D (Plot D)** | Mosh / Beda (Azot tiklovchi dukkak)| Sholg'om / Sabzi (Ildizmeva) | Vadasht + Qo'y boqish (Dam olish) | Bug'doy (Azot sarflovchi g'alla)|

---

# 38. SUG‘ORISH TIZIMI (IRRIGATION & HYDROLOGY SIMULATION)

Feudal qirollikda qurg'oqchilik hosilni yo'q qiluvchi eng dahshatli ofatdir. Sug'orish tizimi tabiiy suv havzalaridan (daryolar, ko'llar, buloqlar) qishloq xo'jaligi maydonlariga suv oqimini yetkazuvchi gidrotexnik muhandislik tarmog'idir.

### 38.1. Namlik Diffuziyasi Tenglamasi (Hydrological Diffusion Formula)

Suv manbasidan yoki sug'orish arig'idan masofaga qarab tuproq blokining namligi quyidagi qonuniyat bo'yicha to'yinadi:

$$Moisture(d) = \max\left(BaseMoisture_{biome}, \; Moisture_{source} \times \left(1.0 - \frac{d}{R_{eff}}\right)^\alpha\right)$$

Bunda:
- $d$: Ekin blokidan eng yaqin suv oqimi voxeliga bo'lgan gorizontal masofa (metr/voxel).
- $R_{eff}$: Suv o'tkazgich inshootining samarali namlantirish radiusi.
- $\alpha = 1.35$: Tuproq g'ovakligiga bog'liq so'nish darajasi.
- $Moisture_{source} = 95\%$: Ochiq suv yuzasining to'yinganlik darajasi.

### 38.2. Suv O'tkazgich Inshootlarining Texnik Parametrlari

| Inshoot Turi | Qurilish Materiali | Namlantirish Radiusi ($R_{eff}$) | Suvning Sizib Yo'qolishi (Seepage Loss) | Oqim Tezligi |
|---|---|---|---|---|
| **Oddiy Tuproq Ariq (Dirt Ditch)** | Faqat tuproq qazish | 4 Voxel | $-8\%$ har 10 metrda | 1.2 m/s |
| **Loy Qoplangan Kanal (Clay-Lined Canal)**| Qazilgan ariq + Gil/Loy | 6 Voxel | $-2\%$ har 10 metrda | 1.8 m/s |
| **Tosh Akveduk / Nov (Stone Aqueduct)**| Yo'nilgan tosh + Ohak qorishmasi | 9 Voxel | **$0\%$ (Suv yo'qolmaydi)** | 3.5 m/s |
| **Shahar Quduqi (Village Well)** | Yog'och g'ildirak + Chuqur tosh shaxta| 12 Voxel (Doira bo'ylab) | Kunlik quvvat: 600 Litr toza suv | Statsionar |

### 38.3. Sug'orish Samarasi va Botqoqlanish Xavfi

- **Optimal Namlik Hududi ($40\% \le Moisture \le 75\%$):** Ekin hosildorligini $+40\%$ ga oshiradi, o'sish vaqtini $15\%$ ga tezlashtiradi.
- **Kam Suvli Hudud ($Moisture < 30\%$):** Qurg'oqchilik boshlanadi, ekin sarg'ayadi, pishish vaqti $2.0\times$ ga sekinlashadi.
- **Haddan Tashqari Namlanish ($Moisture > 85\%$):** Ildiz chirishi kasalligi (Root Rot) yuzaga keladi. O'simlik ostidagi tuproq botqoq loyga (Mud) aylanadi, hosildorlik $-50\%$ ga tushadi. Suv toshqini xavfini bartaraf etish uchun akveduklarda suv darvozalari (Sluice Gates) quriladi.

---

# 39. CHORVACHILIK (LIVESTOCK SYSTEMS & ANIMAL HUSBANDRY)

Chorvachilik — aholini yuqori kaloriyali oqsillar (go'sht, sut, pishloq), jun, charm va og'ir ishlar uchun tortuvchi hayvonlar (ot, ho'kiz) bilan ta'minlaydigan muhim tarmoqdir.

### 39.1. 5 Asosiy Xonaki Hayvon Turlarining Master Balans Jadvali

| Hayvon Turi (Species) | Voyaga Yetish Massasi | Kunlik Ozuqa Sarfi (Pichan/Don) | Kunlik Suv Sarfi | Homiladorlik Davri | Bolalash Soni | So'yishdagi Go'sht Hosili | Yog' / Chandiq | Teri / Jun Hosili | Qo'shimcha Kundalik Mahsulot |
|---|---|---|---|---|---|---|---|---|---|
| **Qoramol (Cattle / Cow)** | 550 kg | 12 kg pichan | 35 L | 9 kun (216h) | 1 buzoq | 180 kg mol go'shti | 35 kg yog' | 1 dona qalin mol terisi | 14 L Sut / kun |
| **Qo'y (Sheep / Ram)** | 70 kg | 3.0 kg o't/pichan | 6 L | 5 kun (120h) | 1–2 qo'zi | 28 kg qo'y go'shti | 8 kg dumba | 1 dona qo'y terisi | 2.5 kg Jun (har mavsum) |
| **Cho'chqa (Domestic Pig)**| 120 kg | 4.5 kg ozuqa chiqindisi | 10 L | 4 kun (96h) | 3–5 cho'chqacha | 65 kg cho'chqa go'shti | 25 kg yog' | 1 dona cho'chqa terisi | Bo'rdoqilash tez (+35%) |
| **Tovuq (Chicken / Hen)** | 2.5 kg | 0.2 kg don/urug' | 0.5 L | 2 kun (48h) | 4–6 jo'ja | 1.8 kg tovuq go'shti | 0.2 kg yog' | 15 dona pat (Feathers) | 1 Tuxum / kun |
| **Ishchi Ot (Draft Horse)** | 650 kg | 15 kg suli/pichan | 40 L | 11 kun (264h) | 1 qulun | 150 kg go'sht (oxirgi chora) | 20 kg yog' | 1 dona pishiq ot terisi | Arava tortish ($+300\%$ yuk)|

### 39.2. O'tloq Maydoni va Boqish Sig'imi (Grazing & Pasture Mechanics)

- Yaylovdagi maysa bloklari ochiq quyoshli havoda har kuni o'z biomassasini $+8\%$ ga tiklaydi.
- **Maksimal Boqish Sig'imi (Carrying Capacity):** Bitta $4\times4$ voxel o'lchamidagi maysazor maydoni maksimal 2 bosh qo'y yoki 0.5 bosh qoramolni boqishga yetadi.
- Agar hayvonlar soni me'yordan oshsa, o'tloq butunlay yeb bitirilib, qattiq qora tuproq yoki botqoq loyga aylanadi va qayta tiklanishi uchun kamida 1 butun fasl talab etiladi.
- Qish faslida qor ostida o'tloqlar muzlagani sababli chorva yopiq og'ilxonalarga (Barns) o'tkazilib, oldindan tayyorlab qo'yilgan pichan g'arami (Haystacks) va don bilan boqilishi shart. Yem-xashak yetishmasa, hayvonlar ozib ketadi va nobud bo'ladi.

---

# 40. OZIQ-OVQAT AYNISH MUDDATLARI (FOOD SPOILAGE & DYNAMIC SHELF-LIFE)

Voxel Lord: Feudal Realm o'yinida barcha organik oziq-ovqat mahsulotlari kimyoviy-biologik parchalanish qonuniga bo'ysunadi. Ushbu mexanika Arrenius kinetikasi va $Q_{10}$ harorat koeffitsiyenti asosida real vaqtda hisoblanadi.

### 40.1. Dinamik Aynish Differensial Tenglamasi (Dynamic Spoilage Equation)

Inventardagi yoki ombordagi har bir oziq-ovqat ashyosi `Freshness` (Yangilik darajasi, $1.0$ dan $0.0$ gacha) ko'rsatkichiga ega. Uning pasayish tezligi quyidagicha aniqlanadi:

$$\frac{d(Freshness)}{dt} = -\frac{1.0}{BaseShelfHours \times 60.0} \times M_{temp} \times M_{container} \times M_{preservation}$$

Ashyoning $Freshness$ qiymati $0.0$ ga tushganda, u butunlay ayniydi:
- Go'sht va baliq `Rotten Meat` (Zaharli aynigan go'sht) yoki `Rotten Waste`ga aylanadi.
- Sabzavot va non mog'or bosgan chiqindiga aylanadi va uni faqat kompost chuquriga tashlash mumkin bo'ladi. Aynigan taomni yegan fuqaro $90\%$ ehtimol bilan ichburug' (dysentery) va zaharlanish kasalligiga chalinadi.

#### Modifikatorlar:
1. **Harorat Modifikatori ($M_{temp}$ - Arrenius Kinetikasi, $Q_{10} = 2.0$):**
   $$M_{temp} = 2.0^{\left(\frac{T_{ambient} - 15.0}{10.0}\right)}$$
   - $T_{ambient} \le 0^\circ\text{C}$ (Qishki ayoz / Tundra / Muzxona): $M_{temp} = 0.05\times$ (Parchalanish deyarli to'xtaydi).
   - $T_{ambient} = 5^\circ\text{C}$ (Chuqur tosh podval / Cold Cellar): $M_{temp} = 0.50\times$ (Aynish $2\times$ sekinlashadi).
   - $T_{ambient} = 15^\circ\text{C}$ (Mo''tadil xona harorati - Baza): $M_{temp} = 1.00\times$.
   - $T_{ambient} = 25^\circ\text{C}$ (Yozgi iliq havo): $M_{temp} = 2.00\times$ (Aynish $2\times$ tezlashadi).
   - $T_{ambient} = 35^\circ\text{C}$ (Sahro / Kuchli jazirama issiq): $M_{temp} = 4.00\times$ (Taom $4\times$ tez ayniydi!).

2. **Idish va Saqlash Sig'imi Modifikatori ($M_{container}$):**
   | Saqlash Joyi / Idish Turi | $M_{container}$ Koeffitsiyenti | Kunlik Zararkunandalar (Sichqon/Hasharot) Xavfi |
   |---|---|---|
   | Ochiq Yerda / Ochiq Aravada | $1.50\times$ | $8.0\%$ |
   | Oddiy Yog'och Quti (Wooden Chest) | $1.00\times$ (Standart) | $3.0\%$ |
   | Qopqoqli Murtak Bochka / Sopol Xum (Clay Amphora)| $0.60\times$ | $0.5\%$ |
   | Shamollatiladigan Ko'tarma Don Ombori (Granary) | $0.25\times$ | $0.1\%$ |
   | Qishki Muz Bloklari Terilgan Tosh Podval (Cold Cellar)| $0.20\times$ | **$0.0\%$ (Mutlaqo xavfsiz)** |

### 40.2. 11 Asosiy Taom Aynish Balans Jadvali (Food Shelf-Life Master Table)

| Taom ID | Oziq-ovqat Mahsuloti | Bazaviy Saqlanish ($15^\circ\text{C}$, Qutida) | Ozuqaviylik (Ochlikni Qondirish) | Ruhiyatga Ta'siri (Morale) | Aynigandagi Natija |
|---|---|---|---|---|---|
| `food_milk_raw` | Yangi Sog'ilgan Sut | 24 soat (1 kun) | 20 ball | $+2$ | Qatiq / Achigan achitqi |
| `food_meat_raw` | Xom Go'sht (Mol, Qo'y, Cho'chqa)| 48 soat (2 kun) | 25 ball (40% kasallik xavfi) | $-10$ | Zaharli sassiq go'sht |
| `food_fish_raw` | Yangi Daryo Balig'i | 36 soat (1.5 kun) | 20 ball (35% kasallik xavfi) | $-8$ | Aynigan baliq |
| `food_stew` | Qaynoq Go'shtli Sho'rva / Bo'tqa| 72 soat (3 kun) | 60 ball | $+15$ | Achigan sho'rva |
| `food_bread` | Tandoor / O'choq Noni | 144 soat (6 kun) | 35 ball | $+5$ | Mog'orlagan qotgan non |
| `food_vegetable` | Yangi Sabzavotlar (Karam, Sabzi)| 168 soat (7 kun) | 20 ball | $0$ | Chirigan sabzavot |
| `food_cheese` | Qattiq Quritilgan Pishloq | 672 soat (28 kun / 1 yil) | 45 ball | $+10$ | Sifatini sekin yo'qotadi |
| `food_smoked_meat`| Dudlangan Go'sht va Qazi | 720 soat (30 kun) | 55 ball | $+12$ | Qotgan dudlangan go'sht |
| `food_salted_meat`| Bochkadagi Tuzlangan Go'sht | 2,016 soat (84 kun / 3 yil)| 40 ball | $+2$ | Haddan tashqari sho'r qatlam |
| `food_dried_fruit`| Qoqi Mevalar / Quritilgan Olma| 1,344 soat (56 kun / 2 yil)| 25 ball | $+6$ | Quruq meva |
| `food_grain` | Tozalangan Don (Bug'doy, Arpa) | 4,032 soat (168 kun / 6 yil)| Xom yeb bo'lmaydi | $0$ | Don qo'ng'izi / Chiqindi |

---

# 41. SAQLASH USULLARI (FOOD PRESERVATION RECIPES & CRAFTING)

Uzoq davom etadigan qahraton qish va ehtimoliy qurg'oqchilik yillarida aholini qirg'indan qutqarib qolishning yagona yo'li oziq-ovqat mahsulotlarini qayta ishlab, ularning saqlanish muddatini sun'iy ravishda uzaytirishdir.

### 41.1. 4 Asosiy Konservalash Texnologiyasi Retseptlari

1. **Go'sht va Baliqni Tuzlash (Salting Mechanics):**
   - **Ish Stoli:** Qassobxona Tuzlash Stolchasi (Butchery Salting Bench).
   - **Xomashyo Sarfi:** 10 birlik Xom Go'sht/Baliq + 2 birlik Osh Tuzi (`mineral_salt` - Galit).
   - **Mehnat Vaqti:** 20 sekund.
   - **Natija:** 10 birlik Tuzlangan Go'sht (`food_salted_meat`).
   - **Parametrlar:** $M_{preservation} = 0.07$ (Saqlanish muddati 84 kungacha / 3 yilgacha uzayadi). Chanqoqlikni $+15\%$ ga oshiradi.

2. **Dudlash (Smoking Mechanics):**
   - **Ish Stoli:** Shahar Dudxonasi (Smokehouse / Dudxona).
   - **Xomashyo Sarfi:** 10 birlik Xom Go'sht/Baliq + 2 birlik Qattiq Yog'och O'tini (Eman/Zarang).
   - **Mehnat Vaqti:** 45 sekund qizdirish va dudlash.
   - **Natija:** 10 birlik Dudlangan Go'sht/Baliq (`food_smoked_meat`).
   - **Parametrlar:** $M_{preservation} = 0.10$ (Saqlanish muddati 30 kunga uzayadi). Iste'mol qilinganda xushbo'y ta'mi evaziga fuqarolarga $+12$ Morale baxt beradi.

3. **Quyoshda Quritish (Solar Drying):**
   - **Ish Stoli:** Ochiq Dala Quritish So'risi (Outdoor Drying Rack).
   - **Xomashyo Sarfi:** 8 birlik Yangi Meva (Olma, O'rik) yoki Qo'ziqorin.
   - **Mehnat Vaqti:** 24 O'yin Soati ochiq quyoshli havoda quritiladi (Yomg'irda to'xtaydi).
   - **Natija:** 4 birlik Qoqilar / Quritilgan Rasion (`food_dried_fruit`).
   - **Parametrlar:** $M_{preservation} = 0.08$ (Saqlanish muddati 56 kunga uzayadi). Yengil vazn (0.1 kg), karvonlar va uzoq yurishlar uchun ideal ozuqa.

4. **Tuzlamalar va Podvalda Fermentatsiya Qilish (Pickling & Fermentation):**
   - **Ish Stoli:** Podval Solish Xumi (Cellar Fermentation Vat).
   - **Xomashyo Sarfi:** 10 birlik Karam/Sabzavot + 1 Ko'za Sirka/Tuzli Suv (Brine) + 1 Tuz.
   - **Mehnat Vaqti:** 60 sekund tayyorlash va achitish.
   - **Natija:** 10 birlik Tuzlangan Karam / Bodring Ko'zasi (`food_pickled_veg`).
   - **Parametrlar:** Saqlanish muddati 42 kunga yetadi. Qish paytida qabul qilinganda lavsha (Scurvy / Singa) kasalligining oldini oladi.

---

# 42. OMBORXONALAR VA MAXSUS FILTRLAR (STORAGE INFRASTRUCTURE & STOCKPILE FILTERING)

Logistikaning yuragi to'g'ri tashkil etilgan omborlar tarmog'idir. Har qanday mahsulot ochiq havoda qoldirilsa, yomg'ir, shamol va zararkunandalar ta'sirida tezda yemiriladi.

### 42.1. Ixtisoslashgan Ombor Bino Turlari

1. **Don Ombori (Granary - Don Ombori):**
   - Maxsus yog'och tirgaklar ustiga ko'tarilgan, pol ostidan shamol aylanadigan shamollatish panjaralariga ega.
   - Faqat quruq donlar, urug'lar, un va xmel qoplarini saqlash uchun mo'ljallangan.
   - Namlikdan saqlanish koeffitsiyenti $98\%$, kemiruvchilar (kalamush) kirishiga to'siq bo'ladi.
2. **Muzxona / Sovuq Podval (Cold Cellar & Icehouse):**
   - Yer ostiga 4–8 voxel chuqurlikda qazilgan, devorlari qalin yo'nilgan granit toshdan terilgan bino.
   - Qishda daryodan arralab olingan muz bloklari (`res_ice_block`) bilan to'ldiriladi. Ichki harorat butun yoz davomida $2^\circ\text{C} – 5^\circ\text{C}$ darajada ushlab turiladi.
   - Tez ayniydigan oziq-ovqatlar (sut, pishloq, go'sht, sho'rva) saqlanadi.
3. **Qurolxona / Aslaha Ombori (Armory):**
   - Quruq, pechka orqali quritiladigan maxsus xona.
   - Qilichlar, sovutlar, o'q-yoylar va qalqonlarni saqlash stendlari bilan jihozlangan. Metall buyumlarning zanglashini (rust decay) $100\%$ oldini oladi.
4. **Umumiy Xomashyo Ombori (Warehouse & Open Stockpile):**
   - Yog'och tagliklar (pallets) va mustahkam tomli ochiq angarlar. Xoda, tosh, quymalar, g'isht va ko'mir saqlash uchun.

### 42.2. Ombor Sig'imi va Zaxira Zichligi Metrikalari

- Har bir standart saqlash vokseli ($1\text{m} \times 1\text{m} \times 1\text{m}$ hajm) o'zining toifasiga ko'ra quyidagi massani qabul qila oladi:
  - Og'ir rudalar va tosh: 1,500 kg / $m^3$.
  - Metall quymalar: 2,500 kg / $m^3$.
  - Don va sabzavotlar: 600 kg / $m^3$.
  - O'tin va xodalar: 450 kg / $m^3$.

### 42.3. Ombor Filtrlari Mantiqi va Ustuvorlik Boshqaruvi (Stockpile Filter Logic)

Har bir omborxona konteyneri va joyi foydalanuvchi interfeysida (UI) bitmask filtr matritsasi orqali sozlanadi:
- **Kategoriya / Subkategoriya ruxsatnomasi:** Foydalanuvchi bitta katakka faqatgina "Po'lat quymalar" yoki faqat "Dudlangan go'sht" saqlashni belgilashi mumkin.
- **Sifat darajasi filtri (Quality Gate):** Masalan, qirol saroyiga yaqin omborga faqat `Masterwork` va `Royal` sifatli oziq-ovqat va sharoblar kiritiladi; oddiy kazarmaga esa `Common` darajadagi rasion jo'natiladi.
- **Ustuvorlik Pog'onasi (Priority Tier):**
  1. `Urgent Buffer (O'ta Muhim Zaxira)`: Bo'shagan zahoti boshqa omborlardan bu yerga yuk tashuvchilar yuk olib keladi.
  2. `Preferred (Afzal Ko'rilgan)`
  3. `Standard (Standart Qabul Qilish)`
  4. `Overflow Dump (Ortiqcha Mollarni Tashlash)`: Barcha asosiy omborlar to'lganda ishlatiladi.

---

# 43. YUK TASHISH LOGISTIKASI (HAULING LOGISTICS & ITEM RESERVATION)

Feudal shahar rivojlangani sari minglab ashyolarni qazib olingan joydan ustaxonalarga va omborlarga tashish eng ko'p ishchi kuchini talab qiluvchi tarmoqqa aylanadi.

### 43.1. Band Qilish Tizimi Arxitekturasi (`ItemReservationManager`)

Ikki yoki undan ortiq fuqaro bir vaqtning o'zida bitta buyumni olishga borishi natijasida yuzaga keladigan resurslar to'qnashuvi (race condition) oldini olish uchun yagona `ItemReservationManager` serveri ishlaydi:

1. **Band Qilish Tokeni (Reservation Token):**
   Ishchi yuk tashish vazifasini (`TRANSPORT` state) qabul qilganda, menejer buyumni `(ItemID, SourceVoxel, Quantity)` bo'yicha bloklaydi:
   `ItemReservationManager.reserve_item(item_instance, carrier_agent_id)`
2. **Token Holatlari:**
   - `RESERVED_FOR_HAUL`: Boshqa hech bir fuqaro bu ashyoni ko'rmaydi va unga yo'l ololmaydi.
   - `IN_TRANSIT`: Ashyo ishchining inventariga / aravasiga yuklandi.
   - `DELIVERED`: Mo'ljaldagi ombor katagiga tushirildi va blokirovka bekor qilindi.
3. **Favqulodda Vaqt Chegarasi (Lease Timeout):**
   Agar ishchi yo'lda qaroqchilar hujumiga uchrab halok bo'lsa yoki qochib ketsa, buyum ustidagi blokirovka 30 soniyadan so'ng avtomatik tarzda bekor qilinadi (`Released to Pool`) va boshqa erkin tashuvchilar ro'yxatiga qaytadi.

### 43.2. Yuk Ko'tarish Quvvati va Tashish Vositalari (Carry Capacity & Transport Gear)

| Tashish Vositasi | Maksimal Yuk Sig'imi | Harakatlanish Tezligi Modifikatori | Talab Qilinadigan Infratuzilma |
|---|---|---|---|
| **Piyoda Ishchi (Backpack)** | 25 kg (Kuchli ishchi: 35 kg) | $1.00\times$ (Yuk to'lganda $0.75\times$) | Yo'lsiz erkin yuradi |
| **Yog'och Qo'l Aravacha (Wheelbarrow)**| 120 kg | $1.15\times$ (Yo'lda), $0.65\times$ (Loyda) | Boshlang'ich tuproq yo'l |
| **Ikki G'ildirakli Katta Arava (Handcart)**| 250 kg | $1.25\times$ (Tosh yo'lda), $0.40\times$ (Loyda)| Pishiq tosh yo'l talab etiladi |
| **Ot / Ho'kiz Qo'shilgan Katta Furgon**| 800 kg | $1.50\times$ (Magistralda), Botqoqda tiqiladi| Keng shoh ko'cha (2x2 voxel)|

### 43.3. To'plamli Yuk Tashish Algoritmi (Batch Hauling Logic)
Tashuvchi har safar bitta don uchun bormaydi. Algoritm $5$ metr radiusdagi bir xil toifadagi ashyolarni qidiradi va yuk ko'tarish chegarasi to'lgunga qadar barcha resurslarni bitta yurishda yig'ib oladi (Greedy Nearest-Neighbor Collection).

---

# 44. YO‘LLAR VA TRANSPORT SAMARADORLIGI (ROADS & TRANSPORT SPEED MULTIPLIERS)

Yo'l infratuzilmasi harakat tezligini va tashish samaradorligini keskin oshiruvchi asosiy omildir. Qurilmagan yerlar vaqt o'tishi bilan fuqarolar yurishi natijasida tabiiy so'qmoqlarga aylanadi, tosh yotqizilgan ko'chalar esa shahar logistikasining tezkor qon tomiridir.

### 44.1. Qoplamalar va Harakat Tezligi Multiplikatorlari

| Yo'l Qoplamasi Turi | Tezlik Multiplikatori ($M_{speed}$) | Chidamlilik va Eskirish | Qurilish Xarajatlari (1 Voxel uchun) |
|---|---|---|---|
| **Botqoqlik / Chuqur Loy / Qalin Qor** | **$0.70\times$ (Jazo)** | — | Harakatlanish qiyin, charchoq $+50\%$ |
| **Yovvoyi O'tloq / Shudgorlanmagan Yer**| **$1.00\times$ (Baza)** | Tabiiy bosilish | Bepul (Tabiiy relyef) |
| **Bosilgan Tuproq Yo'l (Dirt Trail)** | **$1.15\times$** | Yomg'irda loyga aylanadi | Fuqarolar 50 marta yursa o'zi paydo bo'ladi |
| **Chag'iltosh Yo'l (Gravel Road)** | **$1.25\times$** | O'rtacha eskirish | 2 dona Shag'al + 1 dona Qum |
| **Tosh Yotqizilgan Ko'cha (Cobblestone Street)**| **$1.40\times$** | Yuqori mustahkamlik | 2 dona Yo'nilgan Tosh (Cobble) |
| **Qirollik Shoh Ko'chasi (Royal Paved Highway)**| **$1.60\times$** | Eskirmaydi (Mangu) | 2 Taroshlangan Granit + 1 Ohak qorishmasi |

### 44.2. Yo'llarning Yemirilishi va Ta'mirlash Mexanikasi
- Kuchli kuzgi yomg'irlar vaqtida og'ir yuk aravalari o'tgan tuproq yo'llar $10\%$ ehtimol bilan chuqur loyga aylanadi va transport harakatini to'xtatib qo'yadi.
- Shahar yo'l ustalari (Road Laborers) avtomatik tarzda chuqurlarni shag'al bilan to'ldirib, ko'chalarni tartibga solib turadi.

### 44.3. Karvonlar Yo'nalishini Hisoblash (A* Road Graph Integration)
Fuqarolar va savdo karvonlari manzilga borishda tekis chiziq bo'ylab emas, balki yo'llar tarmog'i bo'ylab eng kam vaqt sarflanadigan yo'nalishni tanlaydi. Graf qirralarining og'irligi quyidagi formula bo'yicha hisoblanadi:
$$EdgeCost = \frac{Distance_{voxels}}{M_{speed}}$$

---

# 45. IQTISODIYOT ASOSI (MACROECONOMIC VALUE CHAINS & EQUILIBRIUM)

Voxel Lord: Feudal Realm iqtisodiy modeli to'liq yopiq va muvozanatlashgan xomashyo aylanmasi (Circular Economy) tamoyiliga tayanadi. O'yinda sehrli ravishda paydo bo'ladigan resurslar mavjud emas — har bir non, har bir nayza va har bir tanga fuqarolarning jismoniy mehnati orqali yaratiladi.

### 45.1. Makroiqtisodiy Zanjirning 4 Pog'onasi

```
[1. Birlamchi Xomashyo Qazib Olish] 
       ↓ (Ruda, Xoda, Don, Jun)
[2. Ikkilamchi Qayta Ishlash va Boyitish]
       ↓ (Quymalar, Taxtalar, Un, Iplar)
[3. Uchlamchi Sanoat va Qurol-Yarog' Ishlab Chiqarish]
       ↓ (Qilichlar, Sovutlar, Non, Mebel, Kiyim-kechak)
[4. Yakuniy Iste'mol, Ichki Bozor va Xalqaro Eksport]
```

### 45.2. Iqtisodiy Barqarorlik Indeksi (Settlement Economic Health Index)

Shahar xo'jaligining sog'lomligi quyidagi birlashgan ko'rsatkich orqali monitoring qilinadi:

$$\text{EconomicHealthIndex} = 0.35 \cdot FoodSecurity + 0.25 \cdot ToolSufficiency + 0.20 \cdot TreasuryGrowth + 0.20 \cdot TradeBalance$$

- Agar $FoodSecurity < 1.0$ bo'lsa (ya'ni oziq-ovqat zaxirasi aholining 7 kunlik ehtiyojidan kam bo'lsa), iqtisodiyotda signal trevogasi chalinadi, hashamatli qurilishlar to'xtatilib, barcha erkin ishchilar dehqonchilik va ovchilikka yo'naltiriladi.

---

# 46. BUG‘DOY VA NON ZANJIRI (GRAIN, FLOUR, BREAD & BREWING VALUE CHAIN)

Oziq-ovqat sanoatining eng asosiy tayanchi g'allachilik va novvoychilik tarmog'idir. Ushbu zanjir quyidagi qat'iy ishlab chiqarish nisbatlari bilan ishlaydi:

### 46.1. Zanjirning Bosqichma-bosqich Oqimi va Retsept Nisbatlari

1. **G'alla O'rish (Field Harvesting):**
   - 1 ta pishgan $2\times2$ bug'doy maydoni $\rightarrow$ 8 Bog'lam Bug'doy (`food_wheat_sheaf`).
2. **Xirmonda Yanchish (Threshing Floor):**
   - **Kiritish:** 4 Bog'lam Bug'doy.
   - **Mehnat:** 10 sekund qo'l mehnati (Dastak bilan urish).
   - **Chiqarish:** 8 Birlik Toza Bug'doy Doni (`food_grain`) + 4 Birlik Somon (`res_straw`). Somon molxonalarda to'shama va g'isht quyishda armatura sifatida ishlatiladi.
3. **Tegirmonda Un Qilish (Milling Stage):**
   - **Variant A (Qo'l Tegirmoni - Hand Quern):** 4 Don $\rightarrow$ 3 Qop Un (`food_flour`) (25 sekund mehnat, 25% isrof).
   - **Variant B (Shamol / Suv Tegirmoni - Gristmill):** 4 Don $\rightarrow$ 4 Qop Oliy Navli Un (`food_flour`) + 1 Kepak (`res_bran` - chorva yemi) (8 sekund avtomatik maydalash, 0% isrof).
4. **Nonvoyxona Pechida Non Yopish (Baking Stage):**
   - **Kiritish:** 2 Qop Un + 1 Chelak Toza Suv (`res_water_bucket`) + 0.5 birlik O'tin (`res_firewood`).
   - **Pishirish Vaqti:** 15 sekund tosh pechda qizdirish.
   - **Chiqarish:** 4 dona Yangi Issiq Non (`food_bread`).
   - **Iste'mol:** Bitta fuqaro kuniga o'rtacha 1 dona non iste'mol qiladi. Non $35$ Ochlik ballini tiklaydi va $+5$ Morale beradi.
5. **Pivo Pishirish Zanjiri (Brewery / Ale Production):**
   - **Solod Tayyorlash:** 3 Don Arpa suvga bo'ktiriladi $\rightarrow$ 3 Solod (`res_malt`).
   - **Qaynatish Qozoni:** 3 Solod + 1 G'udda Xmel (`crop_hops`) + 2 Chelak Suv + 1 O'tin.
   - **Chiqarish:** 6 Bochka Xushbo'y El Pivasi (`food_ale_keg`).
   - **Samara:** Pivo ichgan jangchi va fuqarolarning chanqog'i $15$ ballga qonadi, ruhiyati $+20$ Morale ko'tariladi, yengil jarohat og'rig'i (Pain) 6 soatga bloklanadi.

---

# 47. TEMIR VA QUROL ZANJIRI (METALLURGY, FORGING & ARMORY SUPPLY CHAIN)

Qirollik qudrati va mudofaasi metallurgiya sanoatiga asoslanadi. Rudadan to eng mukammal jangovar qurollargacha bo'lgan ishlab chiqarish zanjiri to'liq moddiy hisob-kitobga ega.

### 47.1. Metallurgik Eritish va Qayta Ishlash Bosqichlari

1. **Yog'och Ko'miri Tayyorlash (Charcoal Mound - Xumkash):**
   - **Kiritish:** 6 Xoda Yog'och + 2 Tuproq voxeli qoplamasi.
   - **Jarayon:** 60 sekund havosiz tutash.
   - **Chiqarish:** 5 birlik Sanoat Ko'miri (`res_charcoal`).
2. **Rudani Maydalash (Ore Stamping Mill):**
   - **Kiritish:** 2 dona Xom Temir Rudasi (`res_iron_ore`).
   - **Chiqarish:** 2 dona Boyitilgan Mayda Ruda (`res_crushed_iron`) + 0.5 Shag'al chiqindi.
3. **Past Haroratli Eritish Pechi (Bloomery Smelter):**
   - **Kiritish:** 2 Boyitilgan Ruda + 2 Yog'och Ko'miri.
   - **Harorat:** $1100^\circ\text{C}$ (30 sekund).
   - **Chiqarish:** 1 dona G'ovak Temir Shlaki (Iron Bloom) + 1 Shlak tosh (`res_slag`).
4. **Temirchilik Sandoni (Refining Anvil):**
   - **Kiritish:** 1 Iron Bloom + Bolg'a bilan 15 marta zarba berish.
   - **Chiqarish:** 1 dona Sof Temir Quymasi (`res_iron_ingot`).
5. **Domna Pechi (Blast Furnace - Po'lat Eritish):**
   - **Kiritish:** 2 Temir Quymasi + 2 Toshko'mir + 1 Ohaktosh (`res_limestone` - flyus moddasi).
   - **Harorat:** $1400^\circ\text{C}$ (45 sekund).
   - **Chiqarish:** 1 dona Yuqori Uglerodli Po'lat Quymasi (`res_steel_ingot`).
6. **Damashq Po'lati Tigel Pechi (Crucible Damascus Forge):**
   - **Kiritish:** 2 Po'lat Quymasi + 1 Nikel Rudasi + Ko'mir kuli.
   - **Jarayon:** 120 sekund qizdirish, qatlama buklash va bolg'alash (Master Smith talab etiladi).
   - **Chiqarish:** 1 dona Damashq Po'lat Zagotovkasi (`res_damascus_billet`).
7. **Bronza Eritish:**
   - 3 Mis Rudasi + 1 Qalay Rudasi (`res_tin_ore`) + 1 Ko'mir $\rightarrow$ 4 Bronza Quymasi (`res_bronze_ingot`).

### 47.2. Qurolxona va Aslahasozlik Chiqarish Jadvali (Armory Production Master Table)

| Tayyor Mahsulot Nomi | Ish Stoli | Kerakli Materiallar | Bolg'alash Vaqti | Mustahkamlik ($Dur_{max}$) | Bozor Bazaviy Narxi |
|---|---|---|---|---|---|
| **Temir Kulang (Iron Pickaxe)** | Temirchi Sandoni | 1 Temir Quyma + 1 Yog'och Dasta | 15s | 800 zarba | 18 Kumush |
| **Temir Bolta (Iron Axe)** | Temirchi Sandoni | 1 Temir Quyma + 1 Yog'och Dasta | 15s | 800 zarba | 18 Kumush |
| **Temir Qilich (Iron Arming Sword)** | Qurolsoz Sandoni | 2 Temir Quyma + 1 Qayish Charm | 30s | 350 urish | 45 Kumush |
| **Po'lat Qilich (Steel Longsword)** | Qurolsoz Sandoni | 3 Po'lat Quyma + 1 Dasta + 2 Charm | 50s | 750 urish | 120 Kumush |
| **Damashq Qilichi (Damascus Sword)** | Tigel Sandoni | 2 Damashq Zagotovkasi + 1 Kumush Sim + 2 Asil Charm | 100s | 1,800 urish | 450 Kumush (4.5 Oltin) |
| **Zanjir Sovut (Chainmail Hauberk)** | Sovutsoz Sandoni | 5 Temir Quyma + 2 Teri Qoplama | 60s | 500 zarba | 110 Kumush (1.1 Oltin) |
| **To'liq Po'lat Zirh (Full Plate)** | Sovutsoz Sandoni | 8 Po'lat Quyma + 4 Tasma + 1 Gambezon | 120s | 1,200 zarba | 320 Kumush (3.2 Oltin) |
| **Og'ir Po'lat Arbalet (Crossbow)** | Kamonsoz Stoli | 2 Po'lat + 2 Yog'och Taxta + 1 Mexanizm | 60s | 600 otish | 140 Kumush |
| **Po'lat O'qlar (Bodkin Arrows x20)**| Kamonsoz Stoli | 1 Temir Quyma + 2 Tayoq + 5 Qush Pati | 20s | 20 o'q | 12 Kumush |

---

# 48. VALYUTA TIZIMI (CURRENCY, MINTING & DENOMINATIONS)

Voxel Lord: Feudal Realm iqtisodiyotida natural ayirboshlashdan (barter) tashqari, uch metalli (Trimetallic) qat'iy pul tizimi amal qiladi. Barcha hisob-kitoblar, maoshlar, bozor savdolari va davlat xazinasi ushbu valyutalar orqali yuritiladi.

### 48.1. Pul Birliklari va Ayirboshlash Standarti

- **Mis Chaqa / Fals (Copper Pence):** Mayda kundalik hisob-kitoblar, bitta non yoki sabzavot sotib olish uchun ishlatiladi.
- **Kumush Tanga / Dirham (Silver Dirham):** Asosiy o'yin iqtisodiy o'lchov birligi. Qurol-yarog', ishchilarning oylik maoshi, qurilish materiallari kumushda baholanadi.
- **Oltin Dinar / Sovereign (Gold Sovereign):** Katta davlat operatsiyalari, feodal soliqlar, qasrlar sotib olish va xalqaro savdo karvonlari uchun oliy valyuta.

**Qat'iy Matematik Nisbat:**
$$100 \text{ Mis Chaqa (Copper)} = 1 \text{ Kumush Tanga (Silver)}$$
$$100 \text{ Kumush Tanga (Silver)} = 1 \text{ Oltin Tanga (Gold)}$$
$$1 \text{ Oltin Tanga (Gold)} = 10,000 \text{ Mis Chaqa (Copper)}$$

### 48.2. Qirollik Zarbxonasi (The Royal Mint & Coinage)

O'yinchi o'z qal'asida Zarbxona binosini qurganidan so'ng, qazib olingan sof metall quymalarini qonuniy tangalarga zarb qilish huquqiga ega bo'ladi:
- 1 dona Mis Quyma $\rightarrow$ 100 dona Mis Chaqa.
- 1 dona Kumush Quyma $\rightarrow$ 100 dona Kumush Tanga.
- 1 dona Oltin Quyma $\rightarrow$ 100 dona Oltin Tanga.

**Senyoraj (Zarbxona Boji) va Tangalarni Qadrsizlantirish (Debasement):**
- **Qonuniy Zarb Xarajati (Seigniorage):** Zarbxona har 100 tangadan 5 tasini davlat xazinasiga boj sifatida olib qoladi (5% sof daromad).
- **Qalbaki / Qadrsizlantirilgan Tanga Chiqarish Qonuni (Coin Debasement Edict):**
  Hukmdor og'ir moliyaviy inqiroz paytida kumush tangalar tarkibiga $20\%$ qo'rg'oshin yoki mis qo'shish haqida farmon berishi mumkin.
  - *Natija:* Xazina darhol $+20\%$ qo'shimcha tanga ishlab chiqaradi.
  - *Oqibat:* Bozor savdogarlari buni darhol sezadi; inflyatsiya yuz berib barcha tovarlar narxi $+25\%$ qimmatlashadi, aholining hukmdorga bo'lgan ishonchi pasayadi (Fuqarolar ruhiyati $-15$ Morale).

---

# 49. BOZOR MEXANIKASI VA DINAMIK NARXLAR (DYNAMIC MARKET PRICING & ELASTICITY)

Bozordagi tovarlar narxi doimiy o'zgarmas emas. Narxlar talab va taklif qonuni, aholi soni, mavsumiy ehtiyojlar va o'yinchining savdogarlar gildiyasi oldidagi obro'siga ko'ra dinamik ravishda o'zgarib turadi.

### 49.1. Dinamik Narx Belgilash Formulalari (Algorithmic Pricing Equations)

Xaridor (o'yinchi yoki fuqaro) bozordan tovar sotib olayotgandagi narx ($P_{buy}$) quyidagi formula bo'yicha hisoblanadi:

$$P_{buy}(item) = \text{clamp}\left( BasePrice \times \left(1.0 + k_d \cdot \frac{Stock_{target} - Stock_{current}}{Stock_{target}}\right)^\gamma \times M_{season} \times M_{rep}, \; 0.20 \cdot BasePrice, \; 5.00 \cdot BasePrice \right)$$

O'yinchi o'z tovarini bozorga sotgandagi qabul qilinadigan narx ($P_{sell}$):

$$P_{sell}(item) = P_{buy}(item) \times \left(1.0 - Tariff_{guild}\right) \times \left(1.0 - 0.20 \times \left(1.0 - \frac{MerchantSkill}{100.0}\right)\right)$$

#### Formuladagi O'zgaruvchilar va Koeffitsiyentlar:
- $BasePrice$: Ashyoning kumush tangadagi fundamental boshlang'ich qiymati.
- $k_d = 0.85$: Talab sezgirligi koeffitsiyenti.
- $\gamma = 1.25$: Narx elastikligi darajasi (Eksponensial egri chiziq keskin taqchillikda narxni tez ko'taradi).
- $Stock_{target}$: Shahar aholisining 14 kunlik xavfsiz ehtiyoj zaxirasi:
  $$Stock_{target} = Population \times DailyConsumption \times 14$$
- $Stock_{current}$: Ayni paytda shahar omborlarida mavjud bo'lgan amaldagi zaxira.
- $Tariff_{guild} = 0.15$: Savdogarlar gildiyasining bazaviy komissiyasi ($15\%$).
- $\text{clamp}(x, 0.20 \cdot P_{base}, 5.00 \cdot P_{base})$: Hech bir tovar o'z qiymatidan 5 barobardan ortiq qimmatlashishi yoki 5 barobardan ortiq arzonlashib ketishi mumkin emas (Bozor barqarorligi himoyasi).

**Obro' Modifikatori ($M_{rep}$):**
$$M_{rep} = 1.0 - 0.25 \times \left(\frac{Reputation - 50.0}{50.0}\right)$$
- Obro' $100$ (Exalted / E'zozli): $M_{rep} = 0.75$ ($25\%$ chegirma).
- Obro' $50$ (Neutral / Neytral): $M_{rep} = 1.00$.
- Obro' $0$ (Distrusted / Yomon): $M_{rep} = 1.25$ ($25\%$ jarima ustamasi).

**Mavsumiy Talab Ko'paytiruvchilari ($M_{season}$):**
- Qish faslida O'tin va Qalin Kiyimlar: $M_{season} = 2.20\times$.
- Qish oxiri va erta bahorda Bug'doy va Non: $M_{season} = 1.80\times$.
- Kuzgi yig'im-terim paytida Yangi Meva va Sabzavotlar: $M_{season} = 0.60\times$ (Mavsumiy to'kinlik).
- Qamal va urush holatida Qurollar va O'q-dorilar: $M_{season} = 1.75\times$.

### 49.2. 18 Asosiy Ashyolar Guruhi Master Narxlar Jadvali (BasePrice Catalog in Silver Coins)

| Kategoriya ID | Ashyo Nomi | Kod Identifikatori | Bazaviy Narx ($P_{base}$) | Min Narx (0.2x To'kinlik) | Max Narx (5.0x Qahatchilik) | Kunlik Tebranish |
|---|---|---|---|---|---|---|
| **Oziq-ovqat** | Bug'doy Bog'lami | `food_wheat_sheaf` | 1 Kumush | 0.2 Kumush | 5.0 Kumush | $\pm 5\%$ |
| **Oziq-ovqat** | Yangi Non | `food_bread` | 2 Kumush | 0.5 Kumush | 10.0 Kumush | $\pm 3\%$ |
| **Oziq-ovqat** | Pishirilgan Sho'rva | `food_stew` | 4 Kumush | 1.0 Kumush | 20.0 Kumush | $\pm 4\%$ |
| **Oziq-ovqat** | Tuzlangan Go'sht | `food_salted_meat` | 6 Kumush | 1.5 Kumush | 30.0 Kumush | $\pm 2\%$ |
| **Oziq-ovqat** | Pivo Bochkasi | `food_ale_keg` | 8 Kumush | 2.0 Kumush | 40.0 Kumush | $\pm 5\%$ |
| **Xomashyo** | O'tin Bog'lami | `res_firewood` | 1 Kumush | 0.2 Kumush | 5.0 Kumush | $\pm 8\%$ |
| **Xomashyo** | Qurilish Xodasi | `res_timber_log` | 2 Kumush | 0.5 Kumush | 10.0 Kumush | $\pm 4\%$ |
| **Xomashyo** | Qazilgan Tosh | `res_stone_cobble` | 1 Kumush | 0.2 Kumush | 5.0 Kumush | $\pm 3\%$ |
| **Minerallar** | Temir Rudasi | `res_iron_ore` | 3 Kumush | 0.8 Kumush | 15.0 Kumush | $\pm 6\%$ |
| **Minerallar** | Toshko'mir | `res_coal` | 3 Kumush | 0.8 Kumush | 15.0 Kumush | $\pm 5\%$ |
| **Minerallar** | Osh Tuzi (Galit) | `mineral_salt` | 4 Kumush | 1.0 Kumush | 20.0 Kumush | $\pm 7\%$ |
| **Quymalar** | Temir Quyma | `res_iron_ingot` | 10 Kumush | 2.5 Kumush | 50.0 Kumush | $\pm 4\%$ |
| **Quymalar** | Po'lat Quyma | `res_steel_ingot` | 28 Kumush | 7.0 Kumush | 140.0 Kumush | $\pm 5\%$ |
| **Quymalar** | Oltin Quyma | `res_gold_ingot` | 100 Kumush (1 Oltin)| 80.0 Kumush | 200.0 Kumush | $\pm 1\%$ |
| **Asboblar** | Temir Mehnat Quroli| `item_iron_tool` | 18 Kumush | 5.0 Kumush | 90.0 Kumush | $\pm 4\%$ |
| **Harbiy** | Temir Qilich | `weap_iron_sword` | 45 Kumush | 12.0 Kumush | 225.0 Kumush | $\pm 6\%$ |
| **Harbiy** | Po'lat Qilich | `weap_steel_sword` | 120 Kumush | 30.0 Kumush | 600.0 Kumush | $\pm 7\%$ |
| **Harbiy** | Zanjir Sovut | `armor_chainmail` | 110 Kumush | 30.0 Kumush | 550.0 Kumush | $\pm 5\%$ |

---

# 50. SAVDO KARVONLARI (TRADE CARAVANS & REGIONAL COMMERCE)

Hech bir qirollik barcha resurslarni o'z hududida yetishtira olmaydi. Boshqa feodal shahar-davlatlar va chet el savdogarlari bilan yo'lga qo'yiladigan karvon savdosi iqtisodiy qudratning poydevoridir.

### 50.1. Karvonlarning Kelishi va Savdogarlar Turlari

Tashqi savdo karvonlari shahar darvozasiga har 7–14 kunda bir marta tashrif buyuradi. Shaharda Savdo Maydoni (Market Square) va Mehmonxona (Caravanserai) mavjudligi karvonlar chastotasini $+50\%$ ga oshiradi.

#### Savdogarlar Gildiyasi Toifalari:
1. **Oziq-ovqat va G'alla Savdogari (Provisions Merchant):** Janubiy unumdor o'lkalardan don, meva, ziravorlar va zaytun moyi olib keladi; mahalliy yog'och va qorako'l terilarni sotib oladi.
2. **Konchilik va Ruda Savdogari (Mining & Ore Trader):** Tog'li hududlardan qalay, mis, nikel va toshko'mir keltiradi; mahalliy oziq-ovqat va pivo xarid qiladi.
3. **Ipak va Hashamat Savdogari (Silk & Luxury Merchant):** Sharq mamlakatlaridan ipak matolar, zargarlik buyumlari, chinni idishlar va qimmatbaho kitoblar olib keladi.
4. **Qurol-Yarog' Savdogari (Arms & War Merchant):** Harbiy otlar, arbaletlar, po'lat qurollar va qamal vositalarini taklif etadi.

### 50.2. Karvon Qatnov Vaqti va Xavf Formulalari (Route Roundtrip Time)

Karvonning qo'shni shahar bilan aylanma qatnov vaqti quyidagicha hisoblanadi:

$$T_{roundtrip} = \frac{2 \times Distance_{km}}{V_{caravan}} \times \left(1.0 + Risk_{bandit} \times 0.50\right) + T_{trading}$$

Bunda:
- $Distance_{km}$: Ikki shahar orasidagi kilometrlardagi masofa.
- $V_{caravan}$: Harakat tezligi (Asosiy tosh yo'lda: $4.5\text{ km/soat}$; qirlar va so'qmoqlarda: $2.2\text{ km/soat}$).
- $Risk_{bandit} \in [0.0, 1.0]$: Yo'nalishdagi qaroqchilar xavfi (Qo'riqchi postlari yo'q bo'lsa, karvon sekinlashadi yoki yo'lda talon-taroj qilinadi).
- $T_{trading} = 24 \text{ soat}$: Shahar bozorida savdo qilish uchun to'xtash vaqti.

### 50.3. Karvon Foydasi Tenglamasi (Net Trade Profit Equation)

Karvon savdosidan olinadigan sof daromad:

$$\Pi_{caravan} = \sum_{i} \left(P_{sell}(i) - P_{buy}(i)\right) \times Q_i - \left(Cost_{guards} + Cost_{feed} + Toll_{bridge}\right)$$

Hududlararo arbitraj imkoniyati: Masalan, cho'l biomi shaharlarida yog'och narxi $3.0\times$ qimmat bo'lgani bois, o'rmon hukmdori yog'och eksportidan katta foyda ko'radi.

---

# 51. SOLIQ QONUNCHILIGI (TAX SYSTEM & TREASURY FISCAL POLICY)

Soliqlar — davlat xazinasini to'ldirish, armiyani ta'minlash va yangi shahar devorlarini qurishning asosiy moliyaviy dastagidir. Biroq adolatsiz soliq siyosati xalq isyoniga va aholining qochib ketishiga sabab bo'ladi.

### 51.1. Soliq Stavkalari va Ijtimoiy Reaksiyalar (Tax Brackets)

Hukmdor Royal Ledger orqali soliqlarni $0\%$ dan $40\%$ gacha belgilashi mumkin:

| Soliq Stavkasining Diapazoni | Feodal Siyosat Nomi | Fuqarolar Ruhiyati (Morale) | Immigratsiya / Migratsiya Oqimi | Xazina To'lish Sur'ati | Ehtimoliy Xavf-Xatarlar |
|---|---|---|---|---|---|
| **$0\% – 5\%$** | Saxiy Hukmdor (Generous Lord) | **$+15$ Morale** | Immigratsiya $+35\%$ ga oshadi | O'ta sust (Xazina deyarli bo'sh)| Mudofaa uchun pul yetishmaydi |
| **$6\% – 15\%$** | Adolatli Soliq (Fair Tax - Baza)| **$+5$ Morale** | Barqaror tabiiy o'sish | Barqaror va sog'lom balans | Xavf yo'q |
| **$16\% – 25\%$** | Og'ir Soliq (Heavy Feudal Tax) | **$-15$ Morale** | Immigratsiya to'xtaydi, $-10\%$ ketish| Tez to'ladi | Shaharda o'g'rilik paydo bo'ladi |
| **$26\% – 40\%$** | Zulmkorona Zulm (Extortionate) | **$-40$ Morale** | Ommaviy qochish (Emigration $+50\%$)| Qisqa muddatda juda yuqori | **Qurolli dehqonlar qo'zg'oloni (Revolt)**|

### 51.2. Kunlik Soliq Tushumi Tenglamasi (Treasury Revenue Equation)

Shahar xazinasiga har kuni tongda (soat 06:00 da) tushadigan sof kumush tangalar miqdori:

$$Revenue_{daily} = \sum_{c \in Citizens} \left(Income_{wage}(c) \times TaxRate\right) + \sum_{p \in Plots} LandTax(p) + CustomsTariff - CorruptionLeak$$

#### Korrupsiya va O'g'irlanish Formulasi:
Agar shaharda soliq nazorati (Bailiff / Mirshab) yetarli bo'lmasa, yig'ilgan mablag'ning bir qismi talon-taroj qilinadi:
$$CorruptionLeak = Revenue_{raw} \times 0.25 \times \left(1.0 - \frac{Skill_{bailiff}}{100.0}\right)$$
Agar shahar sud boshqaruvchisi ($Skill_{bailiff}$) $100$ ballga ega bo'lsa, korrupsiya $0\%$ ga tushadi va har bir chaqa xazinaga yetib boradi.

---

# 52. FUQAROLAR RUHIYATI (CITIZEN MORALE & COMPOSITE HAPPINESS SYSTEM)

Har bir fuqaroning ijtimoiy qoniqishi, mehnat unumdorligi va sodiqligi uning shaxsiy ruhiyat (Morale) ko'rsatkichiga bog'liq. Ushbu ko'rsatkich $-100.0$ dan $+100.0$ gacha bo'lgan oraliqda o'zgaradi.

### 52.1. Ruhiyatni Hisoblashning Birlashgan Formulasi (Composite Morale Formula)

Fuqaroning oniy ruhiy holati uning hayotiy ehtiyojlari va atrof-muhit ta'sirlari yig'indisi sifatida shakllanadi:

$$Morale = \text{clamp}\left(50.0 + \sum_{i=1}^{N} Modifier_i, \; -100.0, \; +100.0\right)$$

### 52.2. To'liq Ruhiyat Modifikatorlari Jadvali (Comprehensive [-100, +100] Lookup Table)

| Hayotiy Soha | Holat / Hodisa Sharti | Morale Modifikatori | Ta'sir Qilish Muddat / So'nish Qonuni |
|---|---|---|---|
| **Oziq-ovqat** | Och qolish (Hunger $>90$, ochlik) | **$-50$** | Ochlik davom etguncha doimiy |
| **Oziq-ovqat** | Xom go'sht yoki aynigan taom yeyish | **$-20$** | 12 o'yin soati davomida |
| **Oziq-ovqat** | Bir xil quruq non bilan cheklanish | **$+5$** | 8 o'yin soati davomida |
| **Oziq-ovqat** | To'yimli xilma-xil taom (Go'sht + Non + Sabzavot)| **$+25$** | 16 o'yin soati davomida |
| **Oziq-ovqat** | Qovoqxonada el pivasi ichish | **$+15$** | 12 o'yin soati davomida |
| **Boshpana** | Boshpanasiz (Ochiq yerda, sovuqda uxlash) | **$-35$** | 24 o'yin soati davomida |
| **Boshpana** | Sovuq, isitilmagan kulbada uxlash | **$-15$** | 12 o'yin soati davomida |
| **Boshpana** | Hashamatli tosh saroyda yashash (Tier 3) | **$+25$** | Shu uyda yashaguncha doimiy |
| **Xavfsizlik** | Shahar devori dushmanlar tomonidan buzib o'tildi | **$-40$** | 2 o'yin kuni davomida |
| **Xavfsizlik** | Oilasi yoki yaqin do'stining o'limini ko'rish | **$-50$** | 1 butun fasl (7 kun) davomida so'nadi |
| **Xavfsizlik** | Ko'chada ko'milmagan sassiq murda yotishi | **$-30$** | Murda ko'milgunga qadar doimiy |
| **Xavfsizlik** | Shahar to'liq himoyalangan (Soqchilar soni $\ge 12\%$)| **$+15$** | Doimiy tinchlik holatida |
| **Boshqaruv** | Soliq stavkasi $0\% – 5\%$ (Saxiy Hukmdor) | **$+15$** | Soliq amal qilguncha doimiy |
| **Boshqaruv** | Soliq stavkasi $6\% – 15\%$ (Adolatli me'yor) | **$+5$** | Doimiy |
| **Boshqaruv** | Soliq stavkasi $16\% – 25\%$ (Og'ir soliq) | **$-15$** | Doimiy |
| **Boshqaruv** | Soliq stavkasi $>25\%$ (Zulmkor talonchilik) | **$-40$** | Doimiy (Isyonga undaydi) |
| **Madaniyat** | Cherkov / Jome ibodatxonasidagi bayramda qatnashish| **$+20$** | 24 o'yin soati davomida |
| **Madaniyat** | Mayxonada baxshi va sozandalar qo'shig'ini tinglash| **$+15$** | 12 o'yin soati davomida |
| **Madaniyat** | Qirollik Fasliy Katta Saylida (Festival) ishtirok| **$+45$** | 48 o'yin soati davomida |
| **Salomatlik**| Og'ir jarohat (Qon ketish, suyak sinishi) | **$-30$** | Davolangunga qadar |
| **Salomatlik**| Shahar tabibxonasida to'liq shifo topish | **$+20$** | 24 soat davomida |

### 52.3. Ruhiyat Darajalari va Fuqarolarning Xulq-Atvori (Behavioral Thresholds)

- **Farovon / Baxtiyor ($+75$ dan $+100$ gacha):**
  Mehnat unumdorligi $+20\%$ ga oshadi. Hunarmandlar yasagan buyumlarning sifati bir pog'onaga yuqori chiqish ehtimoli $+30\%$ ga yetadi. Tug'ilish ko'rsatkichi $+50\%$ ga oshadi. Jinoyatchilik $0\%$.
- **Qoniqarli / Tinch ($+25$ dan $+74$ gacha):**
  Standart ish tartibi va barqaror shahar hayoti.
- **Norozi / Xavotirli ($-15$ dan $+24$ gacha):**
  Ish unumdorligi $-15\%$ ga pasayadi. Fuqarolar mayxonalarda norozilik bildiradi, ish tashlashlar (strikes) ehtimoli paydo bo'ladi.
- **Isyonkor / G'azablangan ($-50$ dan $-16$ gacha):**
  Ish unumdorligi $-40\%$ ga tushadi. Shaharda o'g'rilik va omborlarni talash boshlanadi. Fuqarolar shahardan qochib keta boshlaydi (Emigration).
- **Qurolli Qo'zg'olon ($-100$ dan $-51$ gacha):**
  Fuqarolar mehnatni butunlay to'xtatadi. Qurollangan dehqonlar qo'zg'oloni ko'tarilib, shahar don omborlariga o't qo'yadi va hukmdor saroyiga hujum qiladi. Tartibni faqat qurolli gvardiya kuchi bilan tiklash mumkin bo'ladi.

---

# 53. JANG TIZIMI (COMBAT MECHANICS & MELEE TACTICS)

Voxel Lord: Feudal Realm o'yinida yaqin jang tizimi (Melee Combat Engine) Godot 4 ning fizik hisoblash yadrosiga asoslangan bo'lib, Dark Souls, Mount & Blade hamda Kingdom Come: Deliverance o'yinlarining chuqur mexanikalarini o'zida mujassam etadi. Har bir hujum, mudofaa va manyovr voxel olamidagi fazoviy koordinatalar, real vaqt rejimidagi to'qnashuv hitboxlari (Collision Raycasting) hamda aniq charchoq (Stamina) sarfiga bog'langan.

### 53.1. Asosiy Jangovar Harakatlar Sikli (5-Action Combat Loop)

1. **Hujum (Attack):**
   - **Yengil Tezkor Hujum (Light Attack):** Kam charchoq sarflaydi, dushmanning mudofaa teshiklariga tezkor zarba berish uchun mo'ljallangan.
   - **Og'ir Kuchaytirilgan Zarba (Heavy Charged Attack):** Qurolni orqaga tortib quvvatlash orqali dushman mudofaasini yorib o'tish (Guard Break) va yuqori zarba (Stagger) yetkazish.
   - **Hujumni Soxtalashtirish (Feint Cancel):** Shamollatish (Windup) fazasida zarbani to'xtatib, dushmanni erta blok qo'yishga majbur qilish va qarshi zarba berish.
2. **Bloklash (Block & Guard):**
   - Qalqon yoki qurol dastagi bilan dushman zarbasini to'sish. Qalqon bilan bloklash 110 darajali frontal konusni qamrab oladi va kesuvchi hamda sanchuvchi zarbalarni 100% to'sadi. Qurol bilan bloklash 70 darajali burchakda ishlaydi va zararning bir qismini o'tkazib yuboradi.
3. **Mukammal Qaytarish (Perfect Parry):**
   - Dushman zarbasi tegishiga 9-18 freym (0.15-0.30 soniya) qolganda amalga oshiriladigan faol mudofaa harakati. Muvaffaqiyatli parry dushmanning muvozanatini (Poise) butunlay buzadi, uni 1.2 soniyaga karaxt qiladi va o'yinchiga kafolatlangan kritik qarshi zarba (Riposte) berish imkonini yaratadi.
4. **Chetlanish va Sakrash (Dodge & Evade):**
   - Qadam tashlab chetlanish (Sidestep) va yerda dumalash (Combat Roll). Dumalash harakati 60 FPS chastotada 12 ta daxlsizlik freymiga (Invulnerability Frames / i-frames) ega. Sovut og'irligi oshgan sari dumalash tezligi va masofasi qisqaradi.
5. **Muvozanatni Yo'qotish va Yiqitish (Stagger & Poise):**
   - Har bir jangchida 0 dan 100 gacha bo'lgan Poise (Muvozanat zaxirasi) mavjud. Og'ir gurzi va bolta zarbalari muvozanatni tezda 0 ga tushiradi. Poise tugaganda personaj 1.5 soniyaga himoyasiz qoladi (Guard Broken) yoki yerga yiqiladi (Knockdown).

### 53.2. Charchoq (Stamina) Sarfi Formulalari

Jangdagi har bir jismoniy harakat qat'iy matematik qonuniyatlar asosida charchoq sarflaydi:

$$\Delta Stamina_{attack} = BaseStaminaCost(Weapon) \times \left(1.0 + \frac{Weight_{weapon}}{10.0}\right) \times \left(1.0 - 0.25 \times \frac{Agility}{100.0}\right)$$

$$\Delta Stamina_{block} = RawDamage \times (1.0 - ShieldBlockEfficiency) \times \left(1.0 - 0.30 \times \frac{Strength}{100.0}\right)$$

$$\Delta Stamina_{dodge} = 22.0 \times \left(1.0 + 0.02 \times ArmorWeight_{kg}\right)$$

Agar jangchining Stamina miqdori 0 ga tushib qolsa (Stamina Exhaustion):
- Harakatlanish tezligi -50% ga sekinlashadi.
- Blok va parry harakatlarini amalga oshirish imkonsiz bo'ladi.
- Qabul qilingan har qanday kuchli zarba avtomatik ravishda to'liq yiqilishga (Knockdown) sabab bo'ladi.

### 53.3. Hujum Freym Ma'lumotlari (Attack Frame Data at 60 FPS)

| Qurol Turi | Shamollatish (Windup) | Faol Hitbox (Active) | Qaytarish (Recovery) | Feint Oynasi (Cancel) | Stamina Sarfi |
|---|---|---|---|---|---|
| Xanjir (Dagger) | 8 freym (0.13s) | 6 freym (0.10s) | 12 freym (0.20s) | 1-6 freym | 8 ball |
| Qisqa Qilich (Shortsword) | 14 freym (0.23s) | 8 freym (0.13s) | 16 freym (0.26s) | 1-10 freym | 12 ball |
| Ritsar Qilichi (Arming Sword) | 18 freym (0.30s) | 10 freym (0.16s) | 22 freym (0.36s) | 1-14 freym | 16 ball |
| Uzun Qilich (Longsword) | 24 freym (0.40s) | 12 freym (0.20s) | 28 freym (0.46s) | 1-18 freym | 22 ball |
| Ikki Qo'lli Qilich (Greatsword) | 36 freym (0.60s) | 16 freym (0.26s) | 42 freym (0.70s) | 1-26 freym | 36 ball |
| Jangovar Bolta (Battleaxe) | 22 freym (0.36s) | 10 freym (0.16s) | 26 freym (0.43s) | 1-16 freym | 20 ball |
| Ikki Qo'lli Bolta (Greataxe) | 38 freym (0.63s) | 14 freym (0.23s) | 46 freym (0.76s) | 1-28 freym | 40 ball |
| Jangovar Gurzi (Mace) | 20 freym (0.33s) | 8 freym (0.13s) | 24 freym (0.40s) | 1-15 freym | 18 ball |
| Jangovar Cho'kich (Warhammer) | 26 freym (0.43s) | 10 freym (0.16s) | 32 freym (0.53s) | 1-20 freym | 25 ball |
| Piyoda Nayzasi (Spear) | 16 freym (0.26s) | 12 freym (0.20s) | 24 freym (0.40s) | 1-12 freym | 15 ball |
| Gevis / Alabarda (Halberd) | 32 freym (0.53s) | 14 freym (0.23s) | 38 freym (0.63s) | 1-24 freym | 32 ball |
| Ritsar Oyboltasi (Poleaxe) | 30 freym (0.50s) | 12 freym (0.20s) | 36 freym (0.60s) | 1-22 freym | 30 ball |

### 53.4. Qurol Uzunligi va Fazoviy Voxel Qamrovi (Weapon Reach & Hitboxes)

Voxel Lord olamida har bir qurol fazoda real 3D qamrov radiusiga ega (1 Voxel = 1.0 Metr):

| Qurol Nomi | Reach (Voxel Metr) | Hitbox Radiusi ($R_{sweep}$) | Optimal Masofa (Sweetspot) | Hujum Traektoriyasi Burchagi |
|---|---|---|---|---|
| Xanjir (Dagger) | 0.85 m | 0.15 m | 0.50 m - 0.80 m | 45 daraja qiya sanchish |
| Qisqa Qilich (Shortsword) | 1.20 m | 0.25 m | 0.80 m - 1.15 m | 90 daraja gorizontal kesish |
| Ritsar Qilichi (Arming Sword) | 1.45 m | 0.30 m | 0.90 m - 1.40 m | 120 daraja yarim aylana kesish |
| Uzun Qilich (Longsword) | 1.75 m | 0.35 m | 1.10 m - 1.70 m | 140 daraja keng aylanma |
| Ikki Qo'lli Qilich (Greatsword) | 2.15 m | 0.45 m | 1.40 m - 2.10 m | 180 daraja yalpi tozalovchi zarba |
| Jangovar Bolta (Battleaxe) | 1.30 m | 0.30 m | 0.90 m - 1.25 m | 100 daraja vertikal chopish |
| Jangovar Gurzi (Mace) | 1.15 m | 0.25 m | 0.70 m - 1.10 m | 80 daraja diagonal ezish |
| Jangovar Cho'kich (Warhammer) | 1.25 m | 0.25 m | 0.80 m - 1.20 m | 90 daraja tepadan zarba |
| Piyoda Nayzasi (Spear) | 2.85 m | 0.18 m | 2.00 m - 2.80 m | 25 daraja to'g'ri chiziqli sanchish |
| Gevis / Alabarda (Halberd) | 2.60 m | 0.40 m | 1.80 m - 2.55 m | 130 daraja diagonal qirqish |
| Ritsar Oyboltasi (Poleaxe) | 2.25 m | 0.35 m | 1.50 m - 2.20 m | 110 daraja gibrid zarba |

### 53.5. Jangovar Kombinatsiyalar (Combo Chains)

- **Qilich va Qalqon Taktikasi (Sword & Board):** Shield Bash (Dushmanni 0.8 soniya stagger qiladi) -> Quick Thrust (Qalqon ortidan himoyalangan sanchish) -> Low Slash (Oyoqqa kesuvchi zarba).
- **Uzun Qilich Zanjiri (Longsword Mastery):** Left Diagonal Slash -> Right Diagonal Slash -> Overhead Heavy Chop (Zanjirning yakuniy zarbasi blokni yorib o'tish imkoniyatini +65% ga oshiradi).
- **Nayzadorlar Saflanishi (Spear Thrust & Step):** Thrust -> Backstep (Orqaga qadam) -> Lunge Thrust (Uzaytirilgan zarba, otliq dushmanlarga qarshi 3.0x zarar).
- **Gurzi va Cho'kich Zanjiri (Bone-Cracker Combo):** Pommel Strike (Miya chayqalishi travmasi) -> Downward Skull-Crusher (Sovutni hisobga olmagan holda ichki organlarni maydalash).

---

# 54. ZARAR HISOBLASH FORMULASI (DAMAGE)

O'yinda barcha yaqin va uzoq masofali hujumlar uchun quyidagi universal fizika-mexanik hisoblash tenglamasi qo'llaniladi:

$$RawDamage = BaseDamage(Weapon) \times \left(1.0 + \frac{SkillLevel}{100.0} \times 0.75\right) \times QualityMult \times AttackTypeMult \times HitZoneMult$$

### 54.1. Formula O'zgaruvchilari va Chegaralari

1. **$BaseDamage(Weapon)$:** Qurolning metall tarkibi va geometriyasi tomonidan belgilanadigan fundamental boshlang'ich zarar miqdori.
2. **$SkillLevel$ (0-100):** Jangchining ushbu qurol toifasidagi shaxsiy mahorati. 100-darajada qurol zarari +75% ga oshadi.
3. **$QualityMult$:** Qurolchilik ustaxonasida yasalgan buyumning temirchilik sifati:
   - Xomaki / Sinish arafasidagi (Poor): 0.80x
   - Oddiy standart (Common): 1.00x
   - Sifatli po'lat (Fine): 1.25x
   - Usta ishi (Masterwork): 1.60x
   - Shohona saroy quroli (Royal): 2.00x
   - Afsonaviy qadimiy po'lat (Legendary): 2.50x
4. **$AttackTypeMult$:**
   - Yengil zarba (Light Attack): 0.75x
   - Standart hujum (Normal Strike): 1.00x
   - Kuchaytirilgan og'ir hujum (Heavy Charged): 1.75x
   - Ot ustidagi tezkor hujum (Mounted Charge): $1.00 + 0.18 \times Velocity_{horse}$ (Maksimal 3.20x ga yetadi).
5. **$HitZoneMult$:** Tana a'zosiga yetkazilgan zarba koeffitsienti:
   - Bosh va Bo'yin (Head & Neck): 2.20x (Kritik jarohat, miya chayqalishi xavfi).
   - Yuqori Gavda va Ko'krak (Chest & Upper Torso): 1.00x (Standart tayanch hudud).
   - Yelka va Qo'llar (Shoulders & Arms): 0.70x (Qurolni qo'ldan tushirish ehtimoli 15%).
   - Qorin va Chov sohasi (Abdomen & Groin): 0.85x (Kuchli og'riq va qon ketish).
   - Boldir va Oyoq panjalari (Legs & Feet): 0.65x (Harakat tezligini -50% ga tushiradi).

### 54.2. 12 ta Qurol Toifasi Bo'yicha Bosh Balans Jadvali

| Qurol Turi | Qurol Nomi | Bazaviy Zarar | Asosiy Zarar Turi | Ikkilamchi Zarar Turi | Hujum Tezligi | Guard Break Koeffitsienti | Kritik Multiplikator | Talab Qilingan Kuch/Chaqqonlik |
|---|---|---|---|---|---|---|---|---|
| Xanjir | Po'lat Xanjir | 14 HP | Sanchuvchi (Pierce) | Kesuvchi (Slash) | 2.2 zarba/s | 0.25x | 2.50x | Kuch 5 / Chaqqonlik 14 |
| Qisqa Qilich | Qadimiy Gladius | 20 HP | Kesuvchi (Slash) | Sanchuvchi (Pierce) | 1.6 zarba/s | 0.50x | 1.80x | Kuch 8 / Chaqqonlik 10 |
| Ritsar Qilichi | Bir Qo'lli Arming Sword | 28 HP | Kesuvchi (Slash) | Sanchuvchi (Pierce) | 1.3 zarba/s | 0.75x | 1.75x | Kuch 10 / Chaqqonlik 8 |
| Uzun Qilich | Feodal Bastard Sword | 38 HP | Kesuvchi (Slash) | Sanchuvchi (Pierce) | 1.0 zarba/s | 1.10x | 1.85x | Kuch 14 / Chaqqonlik 10 |
| Buyuk Qilich | Ikki Qo'lli Zweihander | 55 HP | Kesuvchi (Slash) | Maydalovchi (Blunt) | 0.7 zarba/s | 1.80x | 1.60x | Kuch 18 / Chaqqonlik 8 |
| Jangovar Bolta | Skandinav Boltasi | 34 HP | Kesuvchi (Slash) | Maydalovchi (Blunt) | 1.1 zarba/s | 1.25x | 1.50x | Kuch 12 / Chaqqonlik 6 |
| Ikki Qo'lli Bolta | Og'ir Qamal Boltasi | 58 HP | Kesuvchi (Slash) | Maydalovchi (Blunt) | 0.65 zarba/s | 2.10x | 1.55x | Kuch 20 / Chaqqonlik 6 |
| Jangovar Gurzi | Qirrali Cho'qmor (Flanged Mace) | 30 HP | Maydalovchi (Blunt) | Sanchuvchi (Pierce) | 1.2 zarba/s | 1.40x | 1.35x | Kuch 12 / Chaqqonlik 6 |
| Jangovar Cho'kich | Ritsar Klevetsi (Warhammer) | 32 HP | Maydalovchi (Blunt) | Sanchuvchi (Pierce) | 1.0 zarba/s | 1.60x | 1.65x | Kuch 14 / Chaqqonlik 8 |
| Piyoda Nayzasi | Po'lat Uchli Nayza | 26 HP | Sanchuvchi (Pierce) | Maydalovchi (Blunt) | 1.4 zarba/s | 0.60x | 2.00x | Kuch 8 / Chaqqonlik 12 |
| Gevis / Alabarda | Feodal Halberd | 46 HP | Kesuvchi (Slash) | Sanchuvchi (Pierce) | 0.8 zarba/s | 1.65x | 1.75x | Kuch 16 / Chaqqonlik 8 |
| Ritsar Oyboltasi | Og'ir Poleaxe | 48 HP | Maydalovchi (Blunt) | Kesuvchi (Slash) | 0.75 zarba/s | 1.85x | 1.70x | Kuch 17 / Chaqqonlik 7 |

---

# 55. SOVUTLAR VA ZARAR TURLARI

Voxel Lord feodal olamida har bir sovut ikki bosqichli haqiqiy mudofaa tenglamasi (Two-Stage Defense Equation) asosida zararni qaytaradi:

$$Damage_{absorbed} = \max\left(0.0, \; (RawDamage - D_{flat}) \times (1.0 - A_{\%})\right)$$

### 55.1. Ikki Bosqichli Mudofaa Mexanikasi

1. **Birinchi Bosqich — Statik Qaytish ($D_{flat}$ / Flat Deflection):**
   - Sovutning tashqi po'lat yoki charm qobig'i zarba kinetik energiyasini qaytarish qobiliyati.
   - Agar $RawDamage \le D_{flat}$ bo'lsa, tig' sovutdan sirg'alib uchqun sochib ketadi (Glancing Blow) va jangchiga faqat 1.0 ballik yuzaki tirnalish shikasti yetadi.
2. **Ikkinchi Bosqich — Foizli Yutish ($A_{\%}$ / Percentage Absorption):**
   - Sovut tagidagi paxtali gambezon, kigiz va ichki to'qimalarning kinetik energiyani o'ziga yutib yoyib yuborish koeffitsienti.
   - Sovut orqali o'tgan qoldiq zarar $1.0 - A_{\%}$ nisbatida kamaytiriladi.

### 55.2. Sovut Toifalari Bo'yicha Asosiy Matritsa (Master Armor Mitigation Matrix)

Quyidagi jadval 6 ta sovut toifasining kesuvchi (Slash), sanchuvchi (Pierce) va maydalovchi (Blunt) hujumlarga nisbatan statik qaytarish (Flat Deflection) va foizli yutish (Percentage Absorption) parametrlarini belgilaydi:

| Sovut Toifasi | Og'irlik (kg) | Slash Deflection / Absorption | Pierce Deflection / Absorption | Blunt Deflection / Absorption | Chidamlilik (Durability) | Harakatlanish Jarimasi |
|---|---|---|---|---|---|---|
| Zig'ir Tolali Kiyim (Linen Clothes) | 1.5 kg | 0 Flat / 5% Absorption | 0 Flat / 0% Absorption | 0 Flat / 0% Absorption | 60 HP | 0% |
| Paxtali Gambezon (Padded Gambeson) | 4.0 kg | 3 Flat / 30% Absorption | 1 Flat / 15% Absorption | 4 Flat / 35% Absorption | 180 HP | -2% |
| Qattiq Charm Sovut (Hardened Leather) | 7.5 kg | 6 Flat / 45% Absorption | 4 Flat / 30% Absorption | 3 Flat / 25% Absorption | 250 HP | -5% |
| Zanjir Sovut (Chainmail Hauberk) | 14.0 kg | 14 Flat / 80% Absorption | 6 Flat / 45% Absorption | 3 Flat / 20% Absorption | 500 HP | -10% |
| Plastinkali Sovut (Scale / Brigandine) | 18.0 kg | 16 Flat / 75% Absorption | 10 Flat / 65% Absorption | 6 Flat / 40% Absorption | 650 HP | -14% |
| To'liq Po'lat Zirh (Full Steel Plate) | 26.0 kg | 26 Flat / 92% Absorption | 18 Flat / 78% Absorption | 8 Flat / 50% Absorption | 1,200 HP | -20% |

### 55.3. Zarar Turlari va Sovut O'rtasidagi O'zaro Ta'sir Taktikasi

1. **Kesuvchi Zarar (Slash - Qilichlar, Boltalar):**
   - Paxtali kiyim va yupqa charmga qarshi dahshatli halokatli kuchga ega (+35% qon ketish effekti).
   - Temir zanjir sovut va to'liq po'lat zirhga qarshi deyarli samarasiz: $D_{flat}$ ko'rsatkichi tufayli po'lat plastinkadan sirg'alib ketadi va o'tkir tig' to'g'ridan-to'g'ri to'xtatiladi.
2. **Sanchuvchi Zarar (Pierce - Nayzalar, Bodkin O'qlari, Rapiyerlar):**
   - Tor maydonga yuqori bosim beradi. Zanjir sovutning halqalarini uzib kirib ketadi (Chainmail penetration).
   - To'liq po'lat zirhning bo'g'imlariga (qo'ltiq osti, tomoq, son chovlari) tushganda himoyani chetlab o'tish imkoniyatiga ega.
3. **Maydalovchi Zarar (Blunt - Gurzilar, Jangovar Cho'kichlar):**
   - Po'lat plastinkani teshish talab etilmaydi. Kinetik zarba to'lqini zirh orqali to'g'ridan-to'g'ri ichki skeletga o'tadi.
   - Kam $D_{flat}$ tufayli og'ir zirh kiygan ritsarlarni karaxt qilish (Stagger), qovurg'a va qo'l suyaklarini sindirish hamda ichki qon ketish keltirib chiqarishda yagona eng samarali quroldir.

### 55.4. Sovutning Yeyilishi va Ta'mirlanishi

Har bir qabul qilingan zarbada sovut chidamliligi pasayadi:

$$\Delta Durability = 0.05 \times Damage_{absorbed}$$

Agar sovut chidamliligi 0 ga tushsa, uning himoya koeffitsientlari 75% ga zaiflashadi va po'lat parchalanib tushadi. Sovutni temirchilik ustaxonasida (Blacksmith Anvil) temir quyma va charm tasmalar evaziga qayta tiklash talab etiladi.

---

# 56. MASOFADAN JANG (RANGED COMBAT)

Voxel Lord feodal simulyatorida barcha o'q-yoy va arbalet snaryadlari real vaqt rejimida 3D fazoda differentsial tenglamalar asosida harakatlanadi. O'qlar to'g'ri chiziq bo'ylab emas, balki tortishish kuchi, havo qarshiligi va shamol siljishi ta'sirida trayektoriya chizadi.

### 56.1. 3D Ballistik Harakat Tenglamalari

Godot 4 fizika siklida ($\Delta t = 1/60 \text{ soniya}$) har bir snaryadning tezlanishi va koordinatalari quyidagi tenglamalar bo'yicha hisoblanadi:

$$\vec{a}_t = \vec{g} - \frac{1}{2m} \rho C_d A |\vec{v}_{rel}| \vec{v}_{rel}$$

$$\vec{v}_{rel} = \vec{v}_{projectile} - \vec{v}_{wind}$$

$$\vec{v}_{t+\Delta t} = \vec{v}_t + \vec{a}_t \Delta t$$

$$\vec{x}_{t+\Delta t} = \vec{x}_t + \vec{v}_t \Delta t$$

- $\vec{g} = (0, -9.81, 0) \text{ m/s}^2$ — erkin tushish tezlanishi.
- $\rho = 1.225 \text{ kg/m}^3$ — dengiz sathidagi havoning zichligi.
- $C_d = 0.045$ — patli o'qning aerodinamik qarshilik koeffitsienti.
- $A = 0.00012 \text{ m}^2$ — o'qning ko'ndalang kesim yuzasi.
- $m$ — o'qning massasi (kilogrammda).
- $\vec{v}_{wind}$ — dinamik ob-havo tizimi tomonidan taqdim etiladigan shamol tezligi vektori.

### 56.2. Yoy Ipini Tortish va Boshlang'ich Tezlik Formulasi

Kamonchining o'q uzish kuchi uning ipni qancha vaqt tortib turganiga (Hold Duration) bog'liq:

$$V_0 = V_{max} \times \min\left(1.0, \; \frac{HoldDuration}{FullDrawTime}\right)^{1.4}$$

Agar o'yinchi ipni oxirigacha tortmasdan qo'yib yuborsa ($HoldDuration < FullDrawTime$), o'q 1.4 darajali eksponent bo'yicha kinetik kuchini yo'qotadi, yaqin masofada yerga qulaydi va aniqlik tebranishi (Accuracy Spread) 4.0x ga kengayadi. Ipni 4.0 soniyadan ortiq ushlab turish esa kamonchining qo'llarini titratadi va charchoqni har soniyada -15 Stamina ga yo'qotadi.

### 56.3. Masofaviy Qurollar Bosh Balans Jadvali

| Qurol Nomi | Tortish/O'qlash Vaqti | Maksimal Tezlik $V_{max}$ | O'q Massasi | Samarali Masofa | Maksimal Masofa | Kinetik Energiya | Zirhni Teshish Koeffitsienti |
|---|---|---|---|---|---|---|---|
| Qisqa Ov Kamoni (Shortbow) | 0.8 s | 42 m/s | 0.025 kg | 40 m | 95 m | 22.0 J | 0.85x |
| Qayrilma Kompozit Kamon (Recurve) | 1.3 s | 60 m/s | 0.032 kg | 75 m | 180 m | 57.6 J | 1.15x |
| Katta Ingliz Kamoni (War Longbow) | 1.8 s | 72 m/s | 0.045 kg | 120 m | 260 m | 116.6 J | 1.50x |
| Yengil Ov Arbaleti (Light Crossbow) | 2.5 s | 75 m/s | 0.035 kg | 60 m | 140 m | 98.4 J | 1.30x |
| Og'ir Vorotli Arbalet (Arbalest) | 5.0 s | 98 m/s | 0.065 kg | 140 m | 320 m | 312.1 J | 2.35x |

### 56.4. O'q-Dori Turlari va Taktik Qo'llanilishi

1. **Bodkin O'qlari (Piercing Bodkin Arrows):**
   - Ignasimon qotirilgan po'lat uchi tufayli zanjir sovut halqalarini parchalaydi. Zirhni teshish bonusi +50%.
2. **Keng Tig'li Ov O'qlari (Broadhead Arrows):**
   - Zirhsiz nishonlar va hayvonlarga qarshi kesuvchi jarohat yetkazadi. Kuchli qon ketish (Severe Bleeding) chaqiradi, ammo temir sovutlarga qarshi $D_{flat}$ ga urilib sinadi.
3. **Olovli Qamal O'qlari (Fire Incendiary Arrows):**
   - Qatron shimdirilgan uchli o'qlar. Parvoz tezligi -15% ga sekinroq, ammo tushgan yog'och yoki somon voxel blokini 85% ehtimollik bilan yondiradi.

---

# 57. HARBIY FAZILATLAR (WARRIOR TRAITS)

Har bir fuqaro tug'ma yoki jang maydonida qozongan qonli tajribasi evaziga noyob jangovar xislatlarga (Warrior Combat Traits) ega bo'lishi mumkin. Ushbu xususiyatlar shaxsiy jang uslubini, safdagi o'rnini va favqulodda vaziyatlardagi xatti-harakatlarini belgilaydi.

### 57.1. Jangovar Fazilatlar Katalogi

1. **Berserker (Qonxo'r Qasoskor):**
   - **Tavsif:** Og'riqni his qilmaydigan, qon hididan mast bo'luvchi quturgan jangchi.
   - **Ijobiy Bonus:** Sog'liq 30% dan pastga tushganda yaqin jang zarari +40% ga, harakat tezligi +20% ga oshadi; zarba karaxtligi (Stagger Duration) -50% ga qisqaradi.
   - **Cheklov / Salbiy Ta'sir:** Qalqon ishlata olmaydi, bloklash harakatlari bloklanadi, mudofaa buyruqlariga bo'ysunmaydi.
2. **Qalqon Saflari Faxriysi (Shield Wall Veteran):**
   - **Tavsif:** Saf intizomini mukammal o'zlashtirgan, qalqonini tanasining bir bo'lagiga aylantirgan askar.
   - **Ijobiy Bonus:** Qalqon bilan bloklash samaradorligi +35%, blok paytida charchoq sarfi -50%, yonidagi safdoshlariga +15 Morale ruhiy quvvat beradi.
   - **Cheklov / Salbiy Ta'sir:** Yakka tartibda jang qilganda harakatlanish tezligi -15%.
3. **Merganko'z (Deadshot):**
   - **Tavsif:** Masofani, shamol yo'nalishini va nishon harakatini benuqson his etuvchi kamonchi.
   - **Ijobiy Bonus:** Kamon ipini to'liq tortganda kamerani kattalashtirish (Zoom Focus) +50%, qo'llar qaltirashi (Bow Sway) -70%, boshga tekkanda kritik ko'paytiruvchi +40%.
   - **Cheklov / Salbiy Ta'sir:** Yaqin masofali pichoqbozlikda hujum kuchi -25%.
4. **Temir Iroda (Iron Will):**
   - **Tavsif:** O'limdan qo'rqmaydigan, hatto butun qo'shin qochganda ham o'z postini tark etmaydigan matonat timsoli.
   - **Ijobiy Bonus:** Komandir vafot etgandagi shok to'lqiniga to'liq immunitet (0 Morale yo'qotish), og'riq chegarasi +20%, qochish (Flee) holatiga hech qachon kirmaydi.
   - **Cheklov / Salbiy Ta'sir:** Taktik chekinish buyrug'ini qabul qilganda orqaga qaytishga ikkilanadi.
5. **Bahaybat Qotili (Giant Slayer):**
   - **Tavsif:** Trollar, vishallar, qamal mashinalari va bahaybat maxluqlarga qarshi kurashish bo'yicha mutaxassis.
   - **Ijobiy Bonus:** Katta va gigant nishonlarga qarshi yetkaziladigan barcha zararlar +60%, ularning zarbalaridan chetlanish (Dodge) daxlsizlik freymlari +25%.
   - **Cheklov / Salbiy Ta'sir:** Odam toifasidagi mayda tezkor dushmanlarga qarshi aniqlik ko'rsatkichi -10%.
6. **Nayzadorlar Saflanish Ustasi (Phalanx Drillmaster):**
   - **Tavsif:** Pike va uzun nayzalarni to'g'ri burchak ostida ushlab, dushman otliqlarini kutib olish bo'yicha harbiy murabbiy.
   - **Ijobiy Bonus:** Nayzaning sanchish tezligi +30%, dushman otliqlarining hujumini kutib olganda dushman tezligiga mutanosib ravishda 3.0x qaytarma zarba beradi.
   - **Cheklov / Salbiy Ta'sir:** Tor xonalar va g'orlar ichida jang qilish qobiliyati -40%.
7. **Chaqqon Shamshirboz (Swiftblade):**
   - **Tavsif:** O'z tanasining yengilligi va chaqqonligiga tayanuvchi qilichboz.
   - **Ijobiy Bonus:** Yengil yoki o'rta sovutda harakat va hujum tezligi +20%, dumalash va chetlanish charchog'i -30%.
   - **Cheklov / Salbiy Ta'sir:** Og'ir plastinkali sovut kiyganda barcha bonuslar yo'qoladi va charchoq 2.0x tez tugaydi.
8. **Qal'a Devori Posboni (Stalwart Defender):**
   - **Tavsif:** Qal'a devorlari, minoralar va tor darvozalarni himoya qilishga ixtisoslashgan posbon.
   - **Ijobiy Bonus:** Balandlikda turib jang qilganda statik mudofaa (Deflection) +25%, tosh parapet orqasida turganda o'qlardan himoyalanish +40%.
   - **Cheklov / Salbiy Ta'sir:** Ochiq tekislikda yugurish tezligi -10%.

---

# 58. ASKARLARNI O‘QITISH VA RUTBALAR

Feodal jamiyatda tinch fuqarolarni professional qo'shinga aylantirish mustahkam harbiy infratuzilma, doimiy o'quv mashg'ulotlari hamda yuqori sifatli moddiy ta'minotni talab qiladi.

### 58.1. Harbiy Rutbalar va Bosqichlar (5 Military Tiers)

1. **Xalq Lashkari (Militia / Peasant Levies - Tier 1):**
   - Oddiy dehqonlar va hunarmandlardan yig'ilgan majburiy qo'shin. Yog'och nayza, o'roq, chopqi va oddiy kamon bilan qurollangan. Sovutlari — oddiy matoli kiyim yoki yupqa charm. Jangovar ruhi juda beqaror.
2. **Piyoda Askari (Man-at-Arms / Town Guard - Tier 2):**
   - Kazarmada professional harbiy xizmatni o'tayotgan shahar soqchilari. Temir qilich, qisqa nayza, doiraviy yog'och qalqon va paxtali gambezon yoki zanjir jilet bilan ta'minlangan.
3. **Tajribali Harbiy (Veteran Soldier - Tier 3):**
   - Ko'plab janglarda toblangan elita askarlar. Uzun ikki qo'lli qilichlar, og'ir alabardalar, krossbovlar va mustahkam temir halqali zanjir sovut (Chainmail Hauberk) kiyishadi. Saf intizomi va taktik buyruqlarga so'zsiz bo'ysunadi.
4. **Elita Ritsar (Feudal Knight / Heavy Cavalry - Tier 4):**
   - Shohona zodagonlar toifasidan chiqqan og'ir zirhli ritsarlar. To'liq po'lat zirh (Full Steel Plate), jangovar destrie tulporlari, uzun nayza (Lance) va Damashq po'latidan yasalgan qilichlar bilan qurollangan. Quruqlikdagi yorib o'tuvchi asosiy zarba kuchi.
5. **Shoh Chempioni (Paladin / Champion of the Realm - Tier 5):**
   - Butun qirollik bo'ylab sanoqli, afsonaviy qudratga ega yengilmas bahodirlar. Qadimiy ritsarlik qasamini ichgan, eng oliy sifatli saroy po'lati bilan qurollangan, jangga kirganda atrofdagi barcha askarlarning ruhiyatini eng yuqori darajaga ko'taradi.

### 58.2. Mashg'ulot Maydonlari va Tajriba To'plash (XP Rates)

Kazarma hududida o'rnatilgan harbiy inshootlar orqali askarlar harakat qiladi:
- **Somon Qopli Mashg'ulot Qo'g'irchog'i (Straw Training Dummy):** Boshlang'ich qurollanish mashg'ulotlari. Tajriba: +12 XP/soat.
- **Harbiy O'q Otish Tiri (Archery Targets):** Kamon va arbalet nishonlari. Tajriba: +18 XP/soat.
- **Jangovar Qilichbozlik Maydoni (Sparring Arena with Drillmaster):** Murabbiy bilan haqiqiy jang amaliyoti. Tajriba: +35 XP/soat.
- **Otliqlar Maydoni (Jousting Yard):** Ritsarlarning ot ustida manyovr qilish maydoni. Tajriba: +45 XP/soat.

### 58.3. Rutba Ko'tarilish Bosqichlari va Ta'minot Xarajatlari

| Harbiy Tieri | Rutba Nomi | Talab Qilingan XP | Kunlik Maosh (Kumush) | Ta'minot Rasioni | Haftalik Qurol Ta'miri | Bazaviy Jangovar Ruh |
|---|---|---|---|---|---|---|
| Tier 1 | Xalq Lashkari | 0 XP | 0.5 Kumush | Oddiy Non va Suv | 1.0 Kumush | 35 ball |
| Tier 2 | Piyoda Askari | 500 XP | 2.5 Kumush | Qovurilgan Go'sht va Non | 3.0 Kumush | 55 ball |
| Tier 3 | Tajribali Harbiy | 1,800 XP | 6.0 Kumush | Go'sht, Pishloq va El Pivosi | 8.0 Kumush | 70 ball |
| Tier 4 | Elita Ritsar | 5,000 XP | 18.0 Kumush | Dabdabali Go'shtli Taom va Sharob | 25.0 Kumush | 85 ball |
| Tier 5 | Shoh Chempioni | 12,000 XP | 45.0 Kumush | Shohona Ziyofat Ratsioni | 60.0 Kumush | 98 ball |

---

# 59. HARBIY SAFLAR VA BUYRUQLAR (FORMATIONS)

Jang maydonidagi g'alaba faqatgina alohida jangchilarning mahoratiga emas, balki guruh bo'lib saflanish va komandirning taktik signallariga bog'liq.

### 59.1. 5 ta Taktik Saf (Formations)

1. **Chiziqli Saf (Line Formation):**
   - **Tuzilishi:** Askarlar 2 yoki 3 qator bo'lib yonma-yon tiziladi.
   - **Xususiyati:** Eng keng hujum jabhasi yaratadi, kamonchilar va arbaletchilar uchun bir vaqtda yalpi o't ochish imkoniyatini beradi.
   - **Parametrlari:** Harakat tezligi 1.00x, frontal zarba quvvati +15%, qanotlardan oson aylanib o'tilishi mumkin.
2. **Ponasimon Saf (Wedge Formation / Boar's Snout):**
   - **Tuzilishi:** Uchburchak shaklidagi pona, markazda eng kuchli zirhli ritsarlar turadi.
   - **Xususiyati:** Dushmanning zich saflarini ikkiga yorib o'tish va markaziy komandirni o'rab olish uchun otliqlar tomonidan qo'llaniladi.
   - **Parametrlari:** Yugurish tezligi +20%, frontal yorib o'tish zarari +45%, ammo orqa qanotlar himoyasiz qoladi.
3. **Qalqon Devori (Shield Wall):**
   - **Tuzilishi:** Old qatordagi askarlar katta qalqonlarini bir-birining ustiga mindirib yaxlit devor hosil qiladi, orqa qatordagilar nayzalarini oldinga cho'zadi.
   - **Xususiyati:** Frontal o'q-yoylardan 80% himoya, yaqin jang zarbalarini qaytarish +50%.
   - **Parametrlari:** Harakat tezligi -60% ga tushadi, faqat oldinga qadam tashlash mumkin.
4. **Kare / Qal'a Saflari (Square Formation):**
   - **Tuzilishi:** To'rtburchak shaklidagi yopiq saf, nayzalar barcha 360 daraja yo'nalishlarga qaratiladi.
   - **Xususiyati:** Qanotdan yoki orqadan aylanib o'tish xavfini butunlay yo'qotadi. Dushman otliqlarining hujumlarini yo'qqa chiqarish uchun eng optimal mudofaa usuli.
   - **Parametrlari:** Harakatlanish mumkin emas (statik mudofaa), otliqlar zarbasiga to'liq daxlsizlik.
5. **Tarqoq Saf (Skirmish Spread):**
   - **Tuzilishi:** Askarlar orasida 3-4 metr bo'sh joy qoldiriladi.
   - **Xususiyati:** Dushman katapultalari, trebuchetlari va kamonchilarining ommaviy zarbalaridan minimal talofat ko'rish uchun qo'llaniladi.
   - **Parametrlari:** Hududiy snaryad zararlaridan -70% talofat kamayishi, ammo dushman otliqlari kelsa osongina yakson qilinadi.

### 59.2. Saf Parametrlari Balans Jadvali

| Saf Nomi | Harakat Tezligi | Oldingi Mudofaa Bonusi | Yon/Orqa Mudofaa | Optimal Qo'shin Turi |
|---|---|---|---|---|
| Chiziqli Saf (Line) | 1.00x | +15% Hujum kengligi | 0% (Standart) | Kamonchilar va Qilichbozlar |
| Ponasimon Saf (Wedge) | 1.20x | +45% Yorib o'tish zarari | -25% Qanot zaifligi | Og'ir Otliq Ritsarlar |
| Qalqon Devori (Shield Wall) | 0.40x | +80% O'qlardan, +50% Yaqin jang | -30% Orqa zaiflik | Qalqonli Nayzadorlar |
| Kare Saflari (Square) | 0.00x (Harakatsiz) | +40% Barcha yo'nalishlarda | +40% To'liq 360 burchak | Elita Pikechilar |
| Tarqoq Saf (Skirmish) | 1.15x | -15% Yaqin jang mudofaasi | -15% Alohida jang | Yengil Razvedkachilar |

### 59.3. Qo'mondonlik Gorn Signallari (Tactical Horn Commands)

O'yinchi yoki otryad komandiri jang maydonida gorn chalaroq 120 voxel radiusdagi barcha ittifoqchilarga zumda buyruq berishi mumkin:
1. **"Saf Tort!" (Form Up - Bir Uzoq Jarangdor Sado):** Sochilib ketgan yoki tartibsiz jang qilayotgan barcha askarlar komandir bayrog'i atrofida belgilangan safga zudlik bilan tiziladi.
2. **"Qalqon Ko'tar!" (Raise Shields - Ikki Qisqa Past Sado):** Askarlar zumda mudofaa holatiga o'tadi, qalqonlarini bosh va ko'krak ustiga ko'taradi.
3. **"Oldinga Hujum!" (Charge - Ko'tariluvchi Shiddatli Sado):** Butun saf dushman nishoniga qarab maksimal tezlikda sprint bilan bostirib boradi (+20% harakat tezligi, +30% dastlabki zarba quvvati).
4. **"Mergonlar Yalpi O't Ochsin!" (Volley Fire - Uchta Qisqa Baland Sado):** Kamonchilar va arbaletchilar belgilangan hududga koordinatali bir paytda yuzlab o'q uzadi.
5. **"Orqaga Saf bilan Chekin!" (Tactical Withdrawal - Cho'ziq Past Sado):** Askarlar yuzlarini dushmanga qaratgan holda, qalqonlarini tushirmasdan tartibli ravishda qal'a darvozasi tomon chekinadi (Ruhiyat sinmaydi).

---

# 60. JANGOVAR RUH (MILITARY MORALE)

Urush taqdirini nafaqat qurollar, balki askarlarning yuragidagi jangovar ruh va ishonch hal qiladi. Qo'rqinch va ruhiy tushkunlik eng kuchli qo'shinni ham parokanda qilib yuborishi mumkin.

### 60.1. Harbiy Ruhiyat Formulasi

Har bir harbiy bo'linma va alohida jangchining ruhiyati (0-100) quyidagi dinamik tenglama bo'yicha har soniyada hisoblanadi:

$$Morale_{unit} = BaseMorale + \Delta M_{casualties} + \Delta M_{officer} + \Delta M_{flank} + \Delta M_{formation} + \Delta M_{terror}$$

### 60.2. Ruhiyat Bosqichlari va Xatti-Harakatlar (Behavioral Thresholds)

- **75-100 Ball — Matonatli (Steadfast):**
  - Askarlar qat'iy ishonch bilan kurashadi. Hujum tezligi +10%, yengil vahima va qon ko'rishga to'liq immunitet. Saf tartibini qat'iy ushlab turadi.
- **40-74 Ball — Intizomli (Disciplined):**
  - Standart jangovar rejim. Berilgan buyruqlarni benuqson bajaradi, pozitsiyasini saqlaydi.
- **20-39 Ball — Ikkilanayotgan (Wavering):**
  - Qo'rquv va sarosima paydo bo'ladi. Saf jipsligi buziladi, askarlarning harakat tezligi -30% ga sekinlashadi, ba'zilar orqaga chekinishga harakat qiladi.
- **0-19 Ball — Vahima va Qochish (Routed / Panic):**
  - Askarlar qalqon va og'ir qurollarini yerga tashlab, shartsiz FLEE holatiga o'tadi. Eng yaqin qal'a darvozasiga yoki xaritadan tashqariga qarab qochadi.

### 60.3. Dinamik Ruhiyat Modifikatorlari

| Vaziyat / Voqea | Modifikator ($\Delta M$) | Davomiyligi / Shart |
|---|---|---|
| Otryad Talafoti (Casualties) | $-1.2 \times \text{Talafot Foizi}$ | Masalan, 40% o'lim bo'lsa -48 ball |
| Komandir Halok Bo'lishi (Officer Slain) | -35 ball | 35 metr radiusdagi barcha ittifoqchilarga zudlik bilan shok to'lqini |
| Orqadan Qanot Qilinishi (Flanked / Rear Attack) | -25 ball | Orqadan zarba berilayotgan vaqtda |
| Dushmanning Son Jihatdan Ustunligi | $-15 \times \log_2\left(\frac{EnemyCount}{FriendlyCount}\right)$ | Dushman 2x ko'p bo'lsa -15, 4x ko'p bo'lsa -30 |
| Qalqon Devori Saqlanib Turishi | +20 ball | Saf buzilmagan paytda |
| Ittifoqchi Trebuchet Toshining Dushmanga Tushishi | +15 ball | Muvaffaqiyatli qamal zarbasidan so'ng 30 soniya |
| Dushman Katapultasi O'ti Ostida Qolish | -20 ball | Snaryad portlashi atrofida bo'lganda |
| Qahramonona Qarshilik (O'yinchining Elita Qotilligi) | +25 ball | Dushman boshlig'i yiqitilganda |

### 60.4. Vahimadagi Qo'shinni Qayta Jamlash (Rallying Mechanics)

Qochayotgan askarlarni to'xtatish uchun quyidagi choralardan foydalaniladi:
1. **Qo'mondon Gorn Sadosi:** Qochayotgan askarlar komandir gornini eshitsa, 50% ehtimollik bilan to'xtab, +20 ruhiyat bilan qayta saflanadi.
2. **Ruhoniy Duosi va Muqaddas Relikviya:** Ruhoniy o'zining muqaddas ramzini ko'targanda 15 metr radiusdagi qo'rquvni bosadi va ruhiyatni +25 ga tiklaydi.
3. **Mustahkam Qal'a Devorlari Panohi:** Qochayotgan askarlar mudofaa qilingan darvozadan ichkariga kirsa, vahima to'xtaydi.

---

# 61. QAMAL TEXNIKASI (SIEGE ENGINES)

Voxel Lord: Feudal Realm o'yinining eng hayratlanarli xususiyatlaridan biri — butun qal'a devorlari, darvozalari, tomlari va ko'priklarining qamal qurollari zarbasi ostida dinamik parchalanuvchi fizik bloklarga aylanishidir.

### 61.1. Qamal Mashinalarining Bosh Mexanik Balans Jadvali

Quyidagi jadval barcha 4 ta asosiy qamal mashinasining texnik parametrlarini to'liq ochib beradi:

| Qamal Mashinasi | Ekipaj Soni | Yig'ish Materiallari | Qayta O'qlash Vaqti | Snaryad Massasi | Boshlang'ich Tezlik | Kinetik Energiya | Portlash Radiusi | Qamal Shikasti |
|---|---|---|---|---|---|---|---|---|
| Devor Yoruvchi Taran (Battering Ram) | 6 nafar askar | 45 Xoda, 12 Temir, 6 G'ildirak | 4.0 s (Har bir tebranish) | 900 kg po'lat bosh | 5.5 m/s | 13.6 kJ | To'g'ridan-to'g'ri (1 voxel) | 550 HP Qamal Zarari |
| Yengil Mangonel (Mangonel) | 2 nafar askar | 30 Taxta, 8 Arqon, 6 Temir | 12.0 s | 40 kg tosh yadro | 38.0 m/s | 28.8 kJ | 1.5 metr radius | 750 HP Qamal Zarari |
| Og'ir Trebuchet (Trebuchet) | 4 nafar askar | 90 Yog'och, 25 Arqon, 30 Temir, 150 Tosh yuk | 30.0 s | 130 kg yo'nilgan tosh | 52.0 m/s | 175.7 kJ | 3.5 metr sferik krater | 3,200 HP Qamal Zarari |
| Mudofaa Ballistasi (Ballista) | 2 nafar askar | 20 Taxta, 6 Po'lat, 6 Arqon | 8.0 s | 8 kg po'lat nayza | 75.0 m/s | 22.5 kJ | To'g'ri chiziqli teshish | 450 HP Sanchuvchi Zarar |

### 61.2. Voxel Materiallarining Qattiqligi va Chidamlilik Jadvali

Har bir voxel bloki zarbani qaytarish darajasi (Hardness Tier) va umumiy chidamlilikka (HP) ega:

| Voxel Materiali | Material Sinf | Voxel HP ($HP_{max}$) | Qattiqlik Tieri ($H$) | Yong'in Xavfi (Flammability) | Qamal Bardoshlilik Koeffitsienti |
|---|---|---|---|---|---|
| Yumshoq Tuproq va Loy (Dirt / Clay) | Tuproq | 80 HP | 1 | 0% | 0.50x |
| Yog'och Taxta va Xodalar (Timber Planks) | Yog'och | 200 HP | 2 | 85% | 0.80x |
| Qora Boshbosh Tosh (Cobblestone) | Tosh | 600 HP | 4 | 0% | 1.20x |
| Yo'nilgan Qal'a G'ishti (Chiseled Stone Brick)| Og'ir Tosh | 1,200 HP | 6 | 0% | 1.60x |
| Mustahkamlangan Tosh Devor (Reinforced Stone)| Fortifikatsiya | 2,500 HP | 8 | 0% | 2.20x |
| Quyma Temir Panjara va Darvoza (Iron Portcullis)| Metall | 3,500 HP | 9 | 0% | 3.00x |

### 61.3. Portlash Shikastini Tarqatish Formulasi (Voxel Blast Dispersion)

Trebuchet yoki mangonel snaryadi $\vec{P}_{impact}$ nuqtasiga urilganda, portlash to'lqini atrofidagi har bir $\vec{X}$ koordinatadagi voxel blokiga quyidagi formula asosida tarqaladi:

$$Damage_{voxel}(\vec{X}) = \frac{ImpactDamage}{1.0 + |\vec{X} - \vec{P}_{impact}|^2} \times \left(1.0 - \frac{HardnessTier}{10.0}\right)$$

Agar voxel blokining qabul qilgan jami zarari uning $HP_{max}$ ko'rsatkichidan oshib ketsa:
1. Blok VoxelChunk ma'lumotlar massividan o'chiriladi va uning o'rni bo'shliq deb e'lon qilinadi.
2. Godot 4 ning NavigationRegion3D navmesh tizimi real vaqtda yangilanadi va dushman piyodalari uchun devorda yangi yo'l ochiladi.
3. Yo'q qilingan har bir blok o'rnida massasi $m = 85 \text{ kg}$ bo'lgan 3 dan 6 tagacha RigidBody3D fizik tosh bo'laklari (Rubble) vujudga keladi.

### 61.4. Qulagan Toshlar Fizikasi va Bosib Qolish Shikasti

Qulab tushayotgan tosh bo'laklari yerga tushgunga qadar erkin tushish tezlanishida harakatlanadi. Har qanday pastda turgan askar yoki fuqaroga tosh tekkanida uning kinetik energiyasiga mutanosib maydalovchi zarba beriladi:

$$Damage_{crushing} = \frac{1}{2} m v^2 \times 0.05$$

10 metr balandlikdan qulagan tosh blok (tezligi taxminan 14 m/s) piyoda askarga 416 HP zarar yetkazib, uni bir zumda ezib tashlaydi. Qulagan vayronalar yo'llarni to'sib qo'yadi va ularni tozalash uchun ishchilar tosh qoldiqlarini (res_stone_rubble) yig'ib olishi talab etiladi.

---

# 62. QURILISHNING IKKI XIL REJIMI

1. **Manual Voxel Mode:** Har bir blokni shaxsan o'rnatish (birinchi shaxs nigohida).
2. **Blueprint Mode:** Bino chizmasini joylashtirish — g'isht teruvchi fuqarolar avtomatik material tashib quradi.

---

# 63. LOYIHALASH KAMERASI (PLANNING CAMERA)

Katta qal'alar va shahar tumanlarini rejalashtirishda erkin ko'rinish beruvchi taktik kamera.

---

# 64. BINO O‘LCHAMLARI

- Kichik: 3×3 – 5×5 (Kulbalar, soqchilar xonasi).
- O'rta: 7×7 – 10×10 (Ustaxonalar, omborlar).
- Katta: 15×15 – 20×20 (Kazarmaxona, bozor maydoni).
- Monumental: 30×30 – 100×100 (Shohona Qasr, Buyuk Sobor).

---

# 65. BINO MUSTAHKAMLIGI VA FIZIKA (STRUCTURAL STABILITY)

Voxel Lord: Feudal Realm arxitekturasi shunchaki vizual bloklar terish emas, balki real statik yuk taqsimoti, bosim qarshiligi va tortishish kuchiga asoslangan qurilish muhandisligi simulyatsiyasidir. Havoda muallaq turuvchi imkonsiz konstruksiyalar yoki tayanchsiz qoldirilgan og'ir tosh tomlar o'z og'irligi ostida halokatli tarzda qulab tushadi.

### 65.1. Strukturaviy Barqarorlik Indeksi ($S_{struct}$)

Har bir voxel bloki o'zining tayanch nuqtasiga (poydevor, ustun yoki yuk ko'taruvchi devor) nisbatan barqarorlik indeksini hisoblab boradi:

$$S_{struct} = K_{material} \times \frac{R_{support}}{Span_{unsupported}}$$

- **$K_{material}$:** Materialning ichki molekulyar bog'lanish va siqilishga chidamlilik koeffitsienti.
- **$R_{support}$:** Eng yaqin vertikal yuk ko'taruvchi ustun yoki poydevorning effektiv tayanch radiusi.
- **$Span_{unsupported}$:** Blokning eng yaqin mustahkam vertikal tayanchdan gorizontal uzoqlashish masofasi (Voxel metr hisobida).

**Barqarorlik Holatlari:**
- $S_{struct} \ge 1.0$: To'liq barqaror va xavfsiz konstruksiya. Bino har qanday tashqi tebranishlarga bardosh beradi.
- $0.75 \le S_{struct} < 1.0$: Zo'riqish holatidagi konstruksiya (Structural Strain). To'sinlar qirsillaydi, tosh oralaridan qum va ohak to'kiladi, qo'shimcha yuk tushsa qulaydi.
- $S_{struct} < 0.75$: Kritik buzilish chegarasi. Bog'lamlar uziladi va bloklar darhol kaskadli qulash (Cascading Cave-in) fizik rejimiga o'tadi.

### 65.2. Gorizontal Tayanchsiz Masofa Chegaralari Jadvali

Quyidagi jadval 4 ta asosiy qurilish materiali uchun ruxsat etilgan maksimal gorizontal tayanchsiz masofa (Overhang Span) va mexanik ko'rsatkichlarni belgilaydi:

| Material Nomi | Maksimal Tayanchsiz Masofa | Material Koeffitsienti ($K_{material}$) | Maksimal Vertikal Yuk | Tavsiya Qilingan Ustun Oralig'i |
|---|---|---|---|---|
| Yog'och Taxta va Xodalar (Wood) | 5 voxel metr | 1.00 | 450 kg/m | Har 4 voxelda bitta yog'och ustun |
| Qora Boshbosh Tosh (Cobble) | 3 voxel metr | 0.85 | 1,200 kg/m | Har 2-3 voxelda tosh tayanch |
| Yo'nilgan Arkasimon Tosh (Chiseled Arch) | 8 voxel metr | 1.45 | 3,800 kg/m | Har 7 voxelda arkali poydevor |
| Mustahkamlangan Po'lat To'sin (Iron-Beam) | 14 voxel metr | 2.20 | 9,500 kg/m | Har 12 voxelda karkasli quyma ustun |

### 65.3. Yuk Ko'taruvchi Ustunlar va Poydevor Talablari

1. **Vertikal Bosim Zanjiri (Vertical Load Transfer):**
   - Bino tomi va yuqori qavatlarining massasi to'g'ridan-to'g'ri vertikal ustunlar (Pillars) orqali pastga — ona zaminga uzatilishi shart.
   - Bo'shliq yoki oddiy yog'och pol ustiga qurilgan og'ir tosh devorlar pastki polni sindirib pastga tushadi.
2. **Poydevor Bloklari (Foundation Blocks):**
   - Poydevor qatlami faqat qattiq tabiiy tosh (Granit, Ohaktosh) yoki mustahkamlangan yo'nilgan tosh poydevordan iborat bo'lishi kerak.
   - Yumshoq tuproq, loy yoki qum ustiga qurilgan og'ir devorlar poydevor cho'kishi (Foundation Sinking) natijasida bino darz ketishiga va qulashiga sabab bo'ladi.

### 65.4. Kaskadli Qulash Algoritmi (Cascading Cave-In Engine)

Agar dushman qamal trebucheti zarbasi, shaxtadagi portlash yoki yong'in bitta yuk ko'taruvchi markaziy ustunni yo'q qilsa, Godot 4 dvigateli zudlik bilan kenglik bo'yicha qidiruv (Breadth-First Search / BFS) algoritmini ishga tushiradi:
1. Yo'q qilingan blok atrofidagi barcha qo'shni 6 ta voxel tekshiriladi.
2. Har bir voxel uchun ona zamin bilan to'g'ridan-to'g'ri bog'langan yuk ko'tarish yo'li mavjudligi aniqlanadi.
3. Agar bino tomi yoki shiftining biror qismi zamin bilan barqaror bog'lanishini yo'qotsa ($S_{struct} < 0.75$), ushbu voxel guruhi VoxelChunk statik to'ridan ajratib olinadi.
4. Ajratilgan barcha bloklar avtomatik ravishda fizik xususiyatga ega RigidBody3D obyektlariga aylanadi va tortishish kuchi ta'sirida pastki qavatlarga qulaydi.
5. Qulagan bloklar pastki konstruksiyalarga dinamik urilish zarbasi berib, butun ko'p qavatli binoni zanjirli kaskad shaklida to'liq vayron qiladi.

---

# 66. YONG‘IN XAVFI VA O‘CHIRISH (FIRE HAZARD)

O't va alangalar feodal shaharchaning eng dahshatli ofatlaridan biridir. Chaqmoq urishi, qamal paytidagi olovli o'qlar yoki beparvo fuqaroning pechkadan sochgan cho'g'i butun yog'och mavzelarni sanoqli daqiqalarda kulga aylantirishi mumkin.

### 66.1. Issiqlik Alangalanish Chegaralari (Thermal Ignition Thresholds)

Har bir material o'zining termodinamik xususiyatlariga ko'ra o'z-o'zidan yonish haroratiga ($T_{ignite}$) ega:
- **Somon Tom va Pichanpoya (Thatch & Straw):** 220 daraja C (Juda tez alangalanadi).
- **Yog'och To'sinlar va Plitalar (Timber Planks):** 300 daraja C (Sekin tutab yonadi, kuchli issiqlik chiqaradi).
- **Quruq Torf va Ko'mir Ombri (Peat & Coal):** 180 daraja C (Tutunsiz ichki yonish, o'chirish juda qiyin).
- **Qora Tosh va Ohaktosh G'ishti (Stone & Brick):** Yonmaydi ($T_{ignite} = \infty$).
- **Temir Panjara va Po'lat Zirhlar (Iron & Steel):** Yonmaydi ($T_{ignite} = \infty$).

### 66.2. Materiallarning Yonuvchanlik Matritsasi

| Material Nomi | Yonuvchanlik Darajasi | Yonish Davomiyligi | Chiqaradigan Issiqlik | Tutun Zaharliyligi |
|---|---|---|---|---|
| Somon Tom (Thatch) | 95% | 45 soniya | 350 kW/m2 | O'rtacha bo'g'uvchi |
| Qoraqarag'ay Yog'ochi (Pine Timber) | 85% | 120 soniya | 620 kW/m2 | Yuqori quyuq tutun |
| Eman Yog'ochi (Hardwood Oak) | 65% | 240 soniya | 850 kW/m2 | Qizigan ko'mir qoldig'i |
| Jun va Gazlama Mato (Wool / Cloth) | 75% | 60 soniya | 280 kW/m2 | Bo'g'uvchi zaharli gaz |
| Tosh va Pishiq G'isht (Stone Masonry) | 0% | 0 soniya | 0 kW/m2 | Tutun chiqarmaydi |

### 66.3. Shamol Tezligi Asosida Olovning Tarqalish Ehtimoli Formulasi

Yonayotgan voxel blokidan qo'shni voxel bloklariga olov sakrash ehtimoli shamol vektori va havo namligiga qat'iy bog'liq:

$$P_{spread} = BaseSpreadRate \times \left(1.0 + k_w \cdot (\vec{v}_{wind} \cdot \vec{d}_{voxel})\right) \times (1.0 - Humidity)$$

- **$BaseSpreadRate$:** Somon uchun $0.15 \text{ s}^{-1}$, yog'och uchun $0.05 \text{ s}^{-1}$.
- **$k_w = 0.25$:** Shamol yo'nalishining olov uchqunlarini (Embers) uchirish koeffitsienti.
- **$\vec{v}_{wind} \cdot \vec{d}_{voxel}$:** Shamol yo'nalishi va maqsadli qo'shni voxel vektori orasidagi skalyar ko'paytma. Shamol esayotgan tomondagi binolar 4.0x tezroq yonadi va uchqunlar 12 voxel masofagacha uchib borishi mumkin.
- **$Humidity$:** Havo namligi. Bahorgi jala va yomg'ir paytida ($Humidity \ge 0.85$) olov tarqalishi deyarli butunlay to'xtaydi.

### 66.4. O't O'chirish Tizimi va Chelaklar Zanjiri AI Protokoli (Bucket Brigade)

Shahar hududida olov chiqqanda fuqarolik AI tizimi darhol 0-darajali Favqulodda Holat (Emergency Priority 1,000) rejimiga o'tadi:
1. **O't O'chiruvchilar Safarbarligi:**
   - 45 metr radiusdagi barcha mehnatga layoqatli fuqarolar zudlik bilan kundalik ishini to'xtatadi.
   - Fuqarolar shahar qudug'i (Village Well), daryo yoki suv ombori tomon yugurib, yog'och chelaklar (item_bucket_wood) oladi.
2. **Chelaklar Zanjiri Taktikasi (Bucket Brigade):**
   - Agar quduqdan olovgacha masofa uzoq bo'lsa, fuqarolar yo'l bo'ylab bir qatorga tizilib, to'la chelaklarni qo'ldan-qo'lga uzatish zanjirini hosil qiladi. Bu harakat tezligini 3.5x ga oshiradi.
   - Bitta chelak suv yonayotgan voxel blokiga sepilganda blok harorati -250 daraja C ga sovutiladi va ochiq alanga 80% ehtimol bilan o'chiriladi.
3. **Nazorat Ostida Bino Buzish (Firebreak Demolition):**
   - Agar yong'in qamrovi 5 tadan ortiq binoni qamrab olsa va shamol kuchi haddan tashqari yuqori bo'lsa, soqchilar va o'rmonchilar olov yo'lidagi qo'shni yog'och binolarni boltalar bilan shoshilinch buzib tashlaydi (Firebreak). Ushbu to'siq olovning boshqa mavzelarga o'tishini oldini oladi.

---

# 67. DINAMIK OB-HAVO (DYNAMIC WEATHER SYSTEM)

Voxel Lord: Feudal Realm dinamik ob-havo tizimi atmosfera bosimi, fasllar almashinuvi va biomlarning harorat-namlik maydonlari bilan to'liq bog'langan deterministik chekli avtomat (Weather Finite State Machine) orqali boshqariladi.

### 67.1. Ob-havo Chekli Avtomat Holatlari (Weather Finite State Machine)

Ob-havo 7 ta asosiy holatdan iborat bo'lib, har 30 daqiqada (o'yin vaqti bilan) ehtimollik matritsasi bo'yicha yangilanadi:

1. **Musaffo / Quyoshli (Clear / Sunny):**
   - Quyosh nuri maksimal ($1.0\times$), bug'lanish kuchayadi, ekinlar fotosintezi faol, fuqarolar kayfiyati $+5$.
2. **Bulutli (Overcast):**
   - Diffuz yorug'lik ($0.65\times$), harorat $2^\circ\text{C} - 4^\circ\text{C}$ pasayadi, yog'ingarchilikka o'tish ehtimoli yuqori.
3. **Mayda Yomg'ir va Jala (Light Rain & Downpour):**
   - Tuproq namligi jadal to'yinadi, ochiq mash'alalar o'chadi, ko'rish masofasi $50\%$ qisqaradi, aravachalar tezligi $-20\%$.
4. **Momaqaldiroqli Bo'ron (Thunderstorm):**
   - Kuchli shamol ($18 - 32\text{ m/s}$), chaqmoq urishi xavfi mavjud (baland tosh/yog'och minoralarga chaqmoq urib yong'in chiqarishi mumkin), fuqarolar boshpanaga qochadi.
5. **Qor Bo'roni (Blizzard):**
   - Tundra va Qish faslida faollashadi. Harorat $-15^\circ\text{C} \dots -35^\circ\text{C}$ gacha tushadi, ko'rish masofasi $8\text{ metr}$, sovuq urishi (Frostbite) xavfi favqulodda yuqori.
6. **Jazirama / Qurg'oqchilik (Heatwave):**
   - Dasht va Yoz oylarida uchraydi. Harorat $+38^\circ\text{C} \dots +45^\circ\text{C}$. Suv havzalari bug'lanadi, tuproq quriydi, yong'in xavfi $+80\%$ ortadi, fuqarolarda chanqoqlik $2.5\times$ tezlashadi.
7. **Zaharli Smog va Kon Gazi Tumani (Toxic Smog / Gas Mist):**
   - Botqoqliklarda yoki chuqur shaxta ventilyatsiyasi yer yuzasiga yetarli filtrlanmagan chiqindilarni haydaganda hosil bo'ladi. Nafas qisishi, o'pka kasalliklari va ko'z achishiga sabab bo'ladi.

Quyidagi jadvalda fasllar bo'yicha ob-havo holatlarining o'tish ehtimolliklari keltirilgan:

| Ob-havo Holati | Bahor Ehtimoli | Yoz Ehtimoli | Kuz Ehtimoli | Qish Ehtimoli | Davomiyligi (O'yin soati) |
|---|---|---|---|---|---|
| **Musaffo (Clear)** | $35\%$ | $55\%$ | $30\%$ | $20\%$ | $4 - 12\text{ soat}$ |
| **Bulutli (Overcast)** | $30\%$ | $25\%$ | $35\%$ | $30\%$ | $3 - 8\text{ soat}$ |
| **Yomg'ir / Jala (Rain)** | $25\%$ | $10\%$ | $25\%$ | $5\%$ (Qorga aylanadi) | $2 - 6\text{ soat}$ |
| **Bo'ron (Storm)** | $8\%$ | $5\%$ | $7\%$ | $0\%$ | $1 - 3\text{ soat}$ |
| **Qor Bo'roni (Blizzard)** | $0\%$ | $0\%$ | $2\%$ | $40\%$ | $4 - 10\text{ soat}$ |
| **Jazirama (Heatwave)** | $2\%$ | $5\%$ | $0\%$ | $0\%$ | $6 - 16\text{ soat}$ |
| **Zaharli Smog (Smog)** | $0\%$ | $0\%$ | $1\%$ | $5\%$ | $2 - 4\text{ soat}$ |

### 67.2. Yog'ingarchilik va Tuproq Namligi Dinamikasi (Precipitation & Soil Moisture Dynamics)

Yog'ingarchilik tuproqning gidrologik balansiga bevosita ta'sir ko'rsatadi:

$$\frac{dW_{soil}}{dt} = P_{precip} - E_{evap}(T) - D_{drain}$$

Bu yerda:
- $P_{precip}$ — yog'ingarchilik intensivligi (Musaffo: $0.0$, Mayda yomg'ir: $+0.05\text{ mm/daqiqa}$, Jala: $+0.30\text{ mm/daqiqa}$).
- $E_{evap}(T)$ — haroratga bog'liq bug'lanish tezligi.
- $D_{drain}$ — tuproq drenaj o'tkazuvchanligi. Loyli tuproqda $D_{drain} = 0.02$, toshli/shag'alli tuproqda $D_{drain} = 0.15$.
- **Suv Toshqini va Chirish:** Agar $W_{soil} > 90\%$ bo'lib 12 o'yin soatidan ortiq saqlanib qolsa, ekinlarning ildiz tizimi chiriydi (Waterlogging). O'yinchi ariqlar va tosh kanallar qazishi shart.

### 67.3. Shamol Vektori va Fizik Tizimlarga Ta'siri (Wind Vector Mechanics)

Har bir hududda dinamik shamol vektori mavjud: $\vec{v}_{wind} = (v_x, 0, v_z)\text{ m/s}$.

1. **Ballistika Trayektoriyasi:**
   Kamon o'qlari, arbalet boltlari va trebuchet toshlarining uchish trayektoriyasi shamol aerodinamik kuchi bilan og'adi:

$$\vec{a}_{wind} = \frac{1}{2 m} C_d \rho A |\vec{v}_{wind} - \vec{v}_{proj}| (\vec{v}_{wind} - \vec{v}_{proj})$$

Kuchli bo'ronda uzoq masofali merganlik aniqligi $40\%$ ga pasayadi; jangchilar shamol yo'nalishini hisobga olib oldindan nishonga olishi talab etiladi.
2. **Yong'in Tarqalish Tezligi:**
   Shamol yo'nalishi bo'ylab olov uchqunlari $2.5\times$ tezroq uchadi va yong'inning qo'shni binolarga sakrash ehtimolini keskin oshiradi.
3. **Shamol Tegirmoni Quvvati:**
   Un tegirmonlari va ventilyatsiya fanlarining aylanish momenti shamol tezligining kubiga to'g'ri proporsional ($P_{mill} \propto |\vec{v}_{wind}|^3$); shamolsiz paytda un tortish to'xtaydi.

---

# 68. TANA HARORATI VA GIPOTERMIYA (THERMOREGULATION, HYPOTHERMIA & GEOTHERMAL GREENHOUSES)

Voxel Lord: Feudal Realm tirik qolish realizmining muhim qismi — personajlarning issiqlik almashinuvi va atrof-muhit harorati bilan termodinamik muvozanatidir.

### 68.1. Inson Tana Harorati Balansi Differensial Tenglamasi (Thermoregulation Equation)

Har bir inson (o'yinchi va fuqarolar) tanasining harorati $T_{body}$ ($^\circ\text{C}$) quyidagi differensial issiqlik balansi orqali boshqariladi:

$$C_{body} \frac{dT_{body}}{dt} = M_{metabolic} + \dot{Q}_{radiation} - \frac{A_{skin}}{R_{clothing} + R_{air}} (T_{body} - T_{ambient}) - \dot{Q}_{evap}$$

Bu yerda:
- $C_{body} \approx 3.5\text{ kJ}/(\text{kg}\cdot\text{K}) \times 75\text{ kg} = 262.5\text{ kJ/K}$ — inson tanasining issiqlik sig'imi.
- $M_{metabolic}$ — metabolik issiqlik ishlab chiqarish quvvati:
  - Tinch uxlayotganda: $80\text{ W}$
  - Oddiy yurishda: $140\text{ W}$
  - Og'ir konchilik va jangda: $280\text{ W}$
- $\dot{Q}_{radiation}$ — yaqin olov, kamin yoki quyosh nurlaridan yutilgan issiqlik oqimi ($0 - 450\text{ W}$).
- $A_{skin} \approx 1.8\text{ m}^2$ — inson tanasining teri sathi maydoni.
- $R_{clothing}$ — kiyimning termal qarshiligi ($m^2\cdot\text{K/W}$ yoki Clo birliklari).
- $R_{air}$ — teri ustidagi chegara havo qatlami qarshiligi (shamol kuchiga qarab kamayadi).
- $\dot{Q}_{evap}$ — terlash orqali yo'qotiladigan issiqlik (jaziramada sovutish mexanizmi).

### 68.2. Kiyim Izolyatsiyasi Bosqichlari (Clothing Insulation Tiers)

Fuqarolarning kiyimi ularni sovuqdan asrovchi asosiy himoya vositasidir:

| Kiyim Turi (Clothing Type) | Izolyatsiya (Clo) | Termal Qarshilik ($R_{clothing}$) | Shamolga Chidamlilik | Xavfsiz Harorat Diapazoni | Kerakli Xomashyo |
|---|---|---|---|---|---|
| **Yirtiq Mato (Ragged Linen)** | $0.3\text{ Clo}$ | $0.046\text{ m}^2\text{K/W}$ | Juda past ($10\%$) | $+15^\circ\text{C} \dots +30^\circ\text{C}$ | Birlamchi latta-puttalar |
| **Jun Ko'ylak va Shim (Woolen Garments)**| $1.0\text{ Clo}$ | $0.155\text{ m}^2\text{K/W}$ | O'rtacha ($45\%$) | $+5^\circ\text{C} \dots +20^\circ\text{C}$ | Qo'y juni, to'qimachilik dastgohi |
| **Mo'ynali Nimcha va Etik (Fur-lined Leather)**| $2.2\text{ Clo}$ | $0.341\text{ m}^2\text{K/W}$ | Yuqori ($75\%$) | $-10^\circ\text{C} \dots +10^\circ\text{C}$ | Bo'ri/Tulkining oshlangan terisi |
| **Og'ir Ayiq Po'stini (Heavy Bear Hide Coat)**| $3.8\text{ Clo}$ | $0.589\text{ m}^2\text{K/W}$ | Mukammal ($95\%$) | $-35^\circ\text{C} \dots 0^\circ\text{C}$ | Oq ayiq terisi, qalin charmlar |

### 68.3. Gipotermiya va Gipertermiya Bosqichlari

Inson tanasi harorati me'yori $36.6^\circ\text{C} - 37.0^\circ\text{C}$ hisoblanadi. Undan og'ish fuqaro holatiga quyidagicha ta'sir qiladi:

1. **Yengil Gipotermiya ($35.0^\circ\text{C} \le T_{body} < 36.5^\circ\text{C}$):**
   - Kuchli qaltirash (shivering), qo'llar uvishishi. Ish tezligi va yurish tezligi $-20\%$ ga pasayadi.
2. **O'rta Gipotermiya ($32.0^\circ\text{C} \le T_{body} < 35.0^\circ\text{C}$):**
   - Qaltirash to'xtaydi, harakat koordinatsiyasi buziladi, qurol va asboblar qo'ldan tushib ketadi, ong xiralashadi, baxt darajasi $-40$ ga qulaydi.
3. **Og'ir Gipotermiya ($T_{body} < 32.0^\circ\text{C}$):**
   - Fuqaro qorga yiqilib behush bo'ladi. Har 10 sekundda $15\text{ HP}$ sovuq shikastlanishi oladi. Agar zudlik bilan issiq kamin yoniga keltirilmasa, muqarrar o'lim yuz beradi.
4. **Gipertermiya ($T_{body} > 39.5^\circ\text{C}$):**
   - Jazirama va issiq quyosh ostida suvsiz qolganda ro'y beradi. Qon quyulishi, ko'ngil aynishi, hushdan ketish va quyosh urishi.

### 68.4. Tundra Geotermal Issiqxonasi Termodinamikasi (Geothermal Greenhouse Thermodynamics)

Muzlagan Tundra biomida ochiq havoda harorat $-12^\circ\text{C} \dots -35^\circ\text{C}$ bo'lib, ochiq tuproqda qishloq xo'jaligi mutlaqo imkonsizdir ($Yield = 0\%$). Aholini boqishning yagona yo'li — yerosti vulkanik issiq bug' teshiklari (Geothermal Steam Vents) ustida maxsus izolyatsiyalangan **Geotermal Issiqxona (Geothermal Greenhouse)** qurishdir.

#### 1. Issiqlik Balansi Differensial Tenglamasi

Yopiq issiqxona havo harorati $T_{in}(t)$ ning vaqt bo'yicha evolyutsiyasi quyidagi termodinamik muvozanatga tayanadi:

$$C_{air} \cdot \rho_{air} \cdot V \cdot \frac{dT_{in}}{dt} = \dot{Q}_{geothermal} + \dot{Q}_{solar} - \dot{Q}_{conduction} - \dot{Q}_{infiltration}$$

Bu yerda:
- $V$ — issiqxonaning umumiy ichki hajmi ($m^3$).
- $\rho_{air} \approx 1.2\text{ kg/m}^3$ — havo zichligi, $C_{air} \approx 1005\text{ J}/(\text{kg}\cdot\text{K})$ — solishtirma issiqlik sig'imi.
- $\dot{Q}_{geothermal}$ — vulkanik teshikdan kiruvchi issiqlik quvvati (Vattda):

$$\dot{Q}_{geothermal} = \dot{m}_{steam} \cdot c_{p,steam} \cdot (T_{vent} - T_{exhaust}) + \sum_{pipes} U_{pipe} \cdot A_{pipe} \cdot (T_{fluid} - T_{in})$$

Ochiq bug' manbai quvvati: $\dot{Q}_{geothermal} = 8.4\text{ kW} - 180\text{ kW}$ ($8400\text{ W} - 180,000\text{ W}$).
- $\dot{Q}_{solar}$ — kvars/shisha tom orqali tushuvchi quyosh nuri issiqligi:

$$\dot{Q}_{solar} = \tau_{glass} \cdot I_{solar} \cdot A_{skylight} \cdot \cos(\theta_{sun})$$

Bu yerda $\tau_{glass} = 0.75$ (shaffoflik koeffitsiyenti), $I_{solar} \approx 350 - 400\text{ W/m}^2$.
- $\dot{Q}_{conduction}$ — devor va tom orqali tashqi muhitga yo'qotiladigan konduktiv issiqlik:

$$\dot{Q}_{conduction} = \sum_{material} \frac{A_i}{R_i} \cdot (T_{in} - T_{out}) = \sum (U_i A_i) \cdot (T_{in} - T_{out})$$

Qurilish materiallarining termal qarshiligi $R_i$ ($m^2\cdot\text{K/W}$) va issiqlik o'tkazuvchanligi $U_i$ ($W/(m^2\cdot K)$):
- Yagona qavatli oddiy shisha (Single-pane Glass): $R = 0.18\text{ m}^2\text{K/W}$ ($U = 5.55\text{ W/m}^2\text{K}$, yuqori issiqlik yo'qotish).
- Ikki qavatli kvars oyna (Double-glazed Quartz): $R = 0.55\text{ m}^2\text{K/W}$ ($U = 1.82\text{ W/m}^2\text{K}$).
- Tosh devor (1 metrli tosh blok): $R = 0.80\text{ m}^2\text{K/W}$ ($U = 1.25\text{ W/m}^2\text{K}$).
- Izolyatsiyalangan qo'sh yog'och devor (Insulated Timber): $R = 1.60\text{ m}^2\text{K/W}$ ($U = 0.625\text{ W/m}^2\text{K}$).
- Qalin chim va tuproqli marza devor (Turf / Earth-berm Sod): $R = 2.40\text{ m}^2\text{K/W}$ ($U = 0.417\text{ W/m}^2\text{K}$, eng yuqori izolyatsiya).

#### 2. Barqaror Holatdagi Muvozanat Harorati (Steady-State Equilibrium)

Tizim barqarorlashganda ($\frac{dT_{in}}{dt} = 0$) ichki muvozanat harorati $T_{eq}$ quyidagi formula bilan hisoblanadi:

$$T_{eq} = T_{amb} + \frac{\dot{Q}_{geothermal} + \dot{Q}_{solar}}{\sum (U_i A_i) + \dot{m}_{inf} c_p}$$

**Aniq Matematik Simulyatsiya Misoli (Auditor Benchmark):**
- Tundra qishki tashqi harorati: $T_{amb} = -15.0^\circ\text{C}$.
- Issiqxona to'liq sirt maydoni: $Area = 120.0\text{ m}^2$.
- O'rtacha devor/tom izolyatsiyasi: $U = 2.0\text{ W}/(\text{m}^2\cdot\text{K})$.
- Geotermal bug' kiritish quvvati: $\dot{Q}_{geothermal} = 8400.0\text{ W}$ ($8.4\text{ kW}$).
- Harorat farqi hisobi:

$$\Delta T = \frac{\dot{Q}_{geothermal}}{U \cdot Area} = \frac{8400.0}{2.0 \times 120.0} = \frac{8400.0}{240.0} = 35.0^\circ\text{C}$$

$$T_{eq} = T_{amb} + \Delta T = -15.0^\circ\text{C} + 35.0^\circ\text{C} = +20.0^\circ\text{C}$$

Natijada ichki harorat $+20.0^\circ\text{C}$ ga yetadi va tashqarida $-15^\circ\text{C}$ bo'ron bo'lishiga qaramay, issiqxonada bug'doy, sabzavotlar va mevalar gurkirab o'sadi.

#### 3. Ichki Haroratning Hosil Unumdorligiga Ta'siri (Crop Yield Multipliers)

Issiqxonada ekilgan ekinlarning hosildorligi $T_{eq}$ ga to'g'ridan-to'g'ri bog'langan:
- $T_{eq} < 0^\circ\text{C}$: Muzlab nobud bo'lish ($Yield = 0\%$, barcha ko'chatlar o'ladi).
- $0^\circ\text{C} \le T_{eq} < 10^\circ\text{C}$: Qattiq sovuq urishi ($Yield = 25\%$, o'sish deyarli to'xtaydi).
- $10^\circ\text{C} \le T_{eq} < 18^\circ\text{C}$: Sub-optimal oraliq ($Yield = 65\%$, sekin o'sadi).
- $18^\circ\text{C} \le T_{eq} \le 28^\circ\text{C}$: **Optimal Issiqxona Hosildorligi** ($Yield = 100\%$, eng yuqori unum).
- $T_{eq} > 35^\circ\text{C}$: Haddan tashqari qizish / Qurib qolish ($Yield = 30\%$, shamollatish darchalari ochilishi shart).

#### 4. Godot 4 GDScript Arxitekturasi (`GreenhouseThermalSystem`)

```gdscript
class_name GreenhouseThermalSystem
extends Node

## Muzlagan Tundrada geotermal issiqxonalar termodinamik muvozanatini hisoblovchi tizim.

@export var ambient_temperature: float = -15.0 # Tundra qishi
@export var solar_irradiance: float = 350.0   # W/m2

func calculate_greenhouse_temp(volume_m3: float, glass_area: float, insulated_wall_area: float, geothermal_vent_kw: float) -> float:
	var u_glass: float = 1.0 / 0.18 # 5.55 W/m2*K
	var u_wall: float = 1.0 / 1.60  # 0.625 W/m2*K
	var total_conductance: float = (glass_area * u_glass) + (insulated_wall_area * u_wall)

	var q_solar_watts: float = glass_area * solar_irradiance * 0.75
	var q_geo_watts: float = geothermal_vent_kw * 1000.0
	var total_heat_in: float = q_solar_watts + q_geo_watts

	var delta_t: float = total_heat_in / max(1.0, total_conductance)
	return ambient_temperature + delta_t

func get_crop_yield_multiplier(internal_temp: float) -> float:
	if internal_temp < 0.0:
		return 0.0
	elif internal_temp < 10.0:
		return 0.25
	elif internal_temp < 18.0:
		return 0.65
	elif internal_temp <= 28.0:
		return 1.00
	else:
		return 0.30
```

---

# 69. TABIIY VA YIRTQICH DUSHMANLAR

Bo'rilar to'dasi, ayiqlar, qaroqchilar, g'or kalamushlari, gigant zaharli o'rgimchaklar.

---

# 70. QONLI OY REYDLARI (BLOOD MOON)

Voxel Lord: Feudal Realm olamida har 28 kunda (to'liq feodal yil / 4 fasl almashinuvi yakunida) osmonda dahshatli astronomik hodisa — Qonli Oy (Blood Moon) yuz beradi. Ushbu tun davomida qizil tuman yer bag'irlaydi, yovvoyi maxluqlar aqldan ozadi va atrofdagi barcha qaroqchilar hamda qamal otryadlari o'yinchining qal'asini yo'q qilish uchun ommaviy yurish boshlaydi.

### 70.1. Xavf Darajasi Hisoblash Formulasi (Threat Scaling Formula)

Qonli Oy bosqinining soni, elita qo'shinlar tarkibi va qamal mashinalari hajmi o'yinchi shahrining iqtisodiy va demografik qudratiga qarab quyidagi formula orqali hisoblanadi:

$$ThreatScore = (Population \times 1.2) + (TreasurySilver \times 0.05) + (ActiveWorkstations \times 4.0)$$

**Xavf Bosqichlari va Dushman Armiyasi Tarkibi:**
- **Tier I — Boshlang'ich Bosqin ($ThreatScore < 150$):**
  - 15-20 nafar qurollangan qaroqchilar (Bandit Marauders), o'roq va yog'och dubinalar, qatronli mash'alalar. Yog'och eshik va devorlarni yoqishga harakat qiladi.
- **Tier II — Uyushgan Qamal Qo'shini ($150 \le ThreatScore < 400$):**
  - 35-50 nafar tajribali askarlar, temir qilichlar va arbaletlar, 1 ta Devor Yoruvchi Taran (Battering Ram), katta yog'och paviza qalqonlari ortidagi o'qchilar.
- **Tier III — Professional Yollanma Armiya ($400 \le ThreatScore < 900$):**
  - 70-90 nafar og'ir zirhli yollanma askarlar, 2 ta Mangonel katapultasi, muhandis laqimchilar (Sappers) va zaharli olov otuvchi maxsus o'qchilar.
- **Tier IV — Qonli Sarkarda O'rdasi ($ThreatScore \ge 900$):**
  - 120 dan ortiq elita qotillar, to'liq temir zirhli ritsarlar, 2 ta Og'ir Trebuchet, laqimchilar tunneli, quturgan urush trollari va qora sehrgarlar.

### 70.2. Elita Qamal Qaroqchilari va Muhandis Laqimchilar (Sapper Tunnelers)

Oddiy o'g'rilardan farqli ravishda, Qonli Oy reydi yuqori taktik intizom bilan harakat qiladi:
1. **Muhandis Laqimchilar (Sapper Tunnelers):**
   - Agar shahar baland tosh devor va chuqur xandaq bilan o'ralgan bo'lsa, 4-6 nafardan iborat laqimchilar guruhi kirka va belkuraklar bilan devor poydevori ostidan yerosti yo'li (Tunnel) qazishga kirishadi.
   - Ular devor ostidagi poydevor bloklarini yo'q qilib, devorning kaskadli qulashiga sabab bo'ladi yoki to'g'ridan-to'g'ri shahar omborxonasi ichidan chiqib keladi.
2. **Katta Paviza Qalqonchilari (Pavise Shieldbearers):**
   - 2 metrli qalin yog'och qalqonlarni yerga qadab, orqadagi o'qchilar uchun ko'chma mudofaa istehkomi yaratadi. Qal'a kamonchilarining o'qlarini 90% qaytaradi.
3. **O't Qo'yuvchi Diversantlar (Arsonist Saboteurs):**
   - Devordan oshib o'tish uchun qamal narvonlarini qo'yadi, shahar ichkarisidagi don ombori, ferma va uylarga moy ko'zalari uloqtirib yong'in chiqaradi.

### 70.3. Qonli Tunning Atmosferaviy va Ruhiy Ta'sirlari

- **Qizil Tuman va Osmon Vizuali:** Godot 4 ning WorldEnvironment tizimi orqali osmon to'q qizil rangga kiradi, tuman ko'rish masofasini 25 voxel metrgacha cheklaydi.
- **Fuqarolik Ruhiyati Shoki:** Tinch aholi vahimaga tushadi (Morale -15 ball), hamma o'z uyiga berkinadi va ibodat qiladi.
- **Yovvoyi Hayvonlar G'alayoni:** Shahar atrofdagi bo'rilar va yirtqichlar g'azablanib (+50% tajovuzkorlik, ko'zlari qizil yonadi), har qanday tirik jonga tashlanadi.

---

# 71. DUNYONING 5 AFSONAVIY BOSSI (CANONICAL 5 BOSSES)

Voxel Lord: Feudal Realm olamida qirollik taqdirini hal qiluvchi 5 ta afsonaviy bosh maxluq (World Bosses) mavjud. Ushbu gigantlar o'zlarining shaxsiy arenalarida yashaydi, minglab salomatlikka (HP), ko'p bosqichli fazalarga, telegraf qilingan halokatli hujumlarga hamda atrofdagi butun voxel relyefni yakson qilish qobiliyatiga ega.

### 71.1. Tog'lar Hukmdori — Grok'Gar (Mountain Troll King)
- **Tieri va Salomatligi:** Tier II Boss | 4,500 HP | Qattiq Teri ($D_{flat} = 12$).
- **Aronasi:** Qadimgi Baland Qoyatosh G'ori (Granite Crag Hollow).
- **Jang Bosqichlari (Phases):**
  - **Faza 1 (100% - 50% HP):**
    - *Qarag'ay Daraxti Zarbasi (Tree Trunk Sweep):* 4 metr radiusdagi barcha o'yinchilarni uchirib yuboruvchi aylanma zarba (120 HP zarba).
    - *Qoyatosh Uloqtirish (Boulder Toss):* Uzoq masofaga 300 kg tosh otadi, tushgan joydagi 3x3 tosh devorlarni parchalaydi.
    - *Yer Tepish (Ground Stomp):* 6 metr radiusda seysmik to'lqin tarqatib, barchani yerga yiqitadi (Knockdown).
  - **Faza 2 (50% - 0% HP — Enraged Berserk):**
    - Quturish holati: Harakat va hujum tezligi +40% ga oshadi.
    - *Shiddatli Hujum (Rampage Charge):* To'g'ri chiziq bo'ylab yugurib, yo'lidagi barcha yog'och va tosh binolarni bir zumda ezib o'tadi.
- **Voxel Vayronkorligi:** Har bir og'ir zarbasi 4x4 voxel maydondagi tosh va yog'och bloklarni bir zumda parchalab fizik tosh uyumiga aylantiradi.
- **Tushadigan Noyob O'ljalar (Masterwork Drop Table):**
  - *Troll Qirolining Yuragi (Heart of Grok'Gar):* Qayta tiklanish eliksiri tayyorlash uchun afsonaviy modda (+5 HP/soniya doimiy regeneratsiya).
  - *Qora Granit Cho'qmor (Club of Granite Might):* 65 Blunt bazaviy zararga ega gigant qurol.
  - *Qoyatosh Toji (Crown of Crags):* Barcha shaxtyorlarning tosh qazish tezligini +25% ga oshiruvchi qirollik toji.

### 71.2. Mal'un Baron Mordred (Cursed Necromancer Baron)
- **Tieri va Salomatligi:** Tier III Boss | 6,500 HP | Qora Sehr Qalqoni ($D_{flat} = 16$).
- **Aronasi:** Qadimgi Shohona Mozoat Kriptasi (Crypt of the Fallen Sovereign).
- **Jang Bosqichlari (Phases):**
  - **Faza 1 (100% - 60% HP):**
    - *Zulmat Sharilari (Necrotic Shadow Orbs):* O'yinchini ta'qib qiluvchi 3 ta qora shar (Har biri 45 HP sehrli zarar).
    - *Suyak Nayzasi (Bone Spear Pierce):* Yerdan otilib chiquvchi o'tkir suyaklar.
    - *O'liklarni Tiriltirish (Raise Skeletons):* G'or polidagi qabrlardan 6 nafar zirhli skelet jangchilarni chaqiradi.
  - **Faza 2 (60% - 25% HP):**
    - *Jasadlar Portlashi (Corpse Explosion):* Yiqilgan barcha skelet jasadlarini detanatsiya qilib, 5 metr radiusda zaharli blast tarqatadi.
    - *Soya Teleportatsiyasi:* O'yinchining orqasiga yashirin o'tib, bo'yinga sanchuvchi xanjar zarbasi beradi.
  - **Faza 3 (25% - 0% HP — Lich Formasi):**
    - *O'lmaslik Qobig'i (Phylactery Ward):* Baron to'liq daxlsiz bo'lib qoladi. O'yinchi kriptaning 4 burchagidagi qurbongoh suyak filakteriyalarini buzib tashlashi shart.
- **Voxel Vayronkorligi:** Qora sehr unumdor tuproqni chirindi zaharga aylantiradi, yog'och ustunlarni chirigan qora kukun qilib qulatadi.
- **Tushadigan Noyob O'ljalar (Masterwork Drop Table):**
  - *Qon So'ruvchi Rapiyer (Baron's Cursed Rapier):* Har bir sanchuvchi zarbada yetkazilgan zararning 25% qismini o'yinchi salomatligiga qo'shadi.
  - *Qora Sehr Filakteriyasi (Grim Phylactery):* Shaharda halok bo'lgan 1 nafar elita fuqaroni qayta tiriltirish imkonini beruvchi artefakt.
  - *Zulmat Xalati (Robes of Shadow Veil):* Dushman kamonchilari aniqligini -40% ga tushiruvchi qadimiy kiyim.

### 71.3. Botqoqlik Vivernasi — Vessaria (Swamp Wyvern Matriarch)
- **Tieri va Salomatligi:** Tier III-IV Boss | 9,000 HP | Qalin Qora Tangachalar ($D_{flat} = 20$).
- **Aronasi:** Zaharli Botqoqlik Ko'rfazi (Venomous Mire Lagoon).
- **Jang Bosqichlari (Phases):**
  - **Faza 1 (100% - 70% HP — Havodagi Hujum):**
    - *Kislotali Qusish (Acid Spit Vomit):* Havodan turib botqoq kislotasi purkaydi. Tushgan joydagi sovutlarning chidamliligini 5.0x tezlikda eritadi.
    - *Shiddatli Sho'ng'ish (Swoop Attack):* O'yinchilarni panjalari bilan changallab balandlikdan pastga uloqtiradi.
  - **Faza 2 (70% - 30% HP — Quruqlikdagi Bo'ron):**
    - Viverna yerga qo'nadi. Qanotlari bilan kuchli shamol to'lqini hosil qilib (Wing Buffet), o'yinchilarni botqoq suviga uloqtiradi.
    - *Zaharli Dum Qamchisi (Tail Whip):* Orqadagi barcha jangchilarga 180 HP zarar va kuchli zahar statusi beradi.
  - **Faza 3 (30% - 0% HP — Ona Qasosi):**
    - G'azab faryodi: Botqoq inlaridan 12 ta yosh viverna bolalarini (Broodlings) yordamga chaqiradi.
- **Voxel Vayronkorligi:** Kislota oqimi yog'och ko'priklar, to'siqlar va qayiqlarni butunlay eritib yo'q qiladi; qanot zarbasi tomlardagi somon va koshinlarni uchirib yuboradi.
- **Tushadigan Noyob O'ljalar (Masterwork Drop Table):**
  - *Viverna Kislota Xaltasi (Wyvern Acid Sac):* Qamal katapultalari uchun 10 ta o'ta halokatli devor erituvchi snaryad tayyorlash manbai.
  - *Zaharli Qilich (Venomfang Greatsword):* Zarba berilganda dushmanga 15 soniya davomida sekundiga 12 HP zahar yetkazadi.
  - *Ajdaho Terisi Sovuti (Dragonhide Scale Cuirass):* Zahar va kislotaga 75% immunitet beruvchi yengil elita sovut.

### 71.4. Qor Devlari Sardori — Thrym (Frost Jotun Chieftain)
- **Tieri va Salomatligi:** Tier IV Boss | 12,000 HP | Muzlagan Po'lat Tan ($D_{flat} = 24$).
- **Aronasi:** Abadiy Muzlik Cho'qqisi (Glacial Pinnacle Spire).
- **Jang Bosqichlari (Phases):**
  - **Faza 1 (100% - 65% HP):**
    - *Muzli Cho'kich Zarbasi (Glacial Cleave):* 8 metr uzunlikdagi muz to'lqini yo'lidagi barcha tirik mavjudotlarni muzlatib qotirib qo'yadi.
    - *Qor Bo'roni Qichqirig'i (Blizzard Howl):* Hududdagi haroratni bir zumda -35 daraja C ga tushiradi (Gipotermiya xavfi 3.0x oshadi).
  - **Faza 2 (65% - 30% HP):**
    - *Muz Ustunlari Chaqiruvi (Frost Pillars):* Yerdan 5 voxel balandlikdagi 6 ta ulkan muz ustunlarini otilib chiqaradi.
    - *Muz Qoyalari Qulashi (Avalanche Slam):* Shiftga zarba berib, tepadan o'yinchilar boshiga tonnalik muz qoyalarini yog'diradi.
  - **Faza 3 (30% - 0% HP — Absolyut Muzlash):**
    - *Ustunlarni Portlatish (Pillar Shatter):* Barcha muz ustunlarini parchalab, butun arena bo'ylab millionlab muz parchalarini o'qdek sochadi.
- **Voxel Vayronkorligi:** Oqar daryolar va suv manbalarini qattiq muz bloklariga aylantiradi, tosh devorlarni sovuqdan qirsillatib yorib parchalaydi.
- **Tushadigan Noyob O'ljalar (Masterwork Drop Table):**
  - *Dev Qor Cho'kichi (Jotun's Glacial Greathammer):* 72 Blunt zararga ega; har bir zarbada dushmanni 2 soniyaga muzlatadi.
  - *Abadiy Muzlik Runasi (Rune of Permafrost):* Shahar yerto'lasiga o'rnatilganda barcha oziq-ovqatlarning aynishini umrbod 0 ga tushiradi.
  - *Qor Devi Po'stini (Frost Giant Pelt Cloak):* O'yinchiga +35 daraja C doimiy tana issiqligi beradi (Qishki sovuqqa mutlaq daxlsizlik).

### 71.5. Tubanlik Golemi — Tartaros (Corrupted Abyssal Golem)
- **Tieri va Salomatligi:** Tier IV+ Yakuniy Dunyo Bossi | 15,000 HP | Qora Magma Graniti ($D_{flat} = 28$).
- **Aronasi:** Yer Tubidagi Magma O'chog'i (Magma Crucible of the Deep Abyss).
- **Jang Bosqichlari (Phases):**
  - **Faza 1 (100% - 75% HP):**
    - *Magma Mushti Zarbasi (Magma Fist Slam):* Yerga urilganda to'lqin shaklida oqib keluvchi olovli lava xandaqlarini ochadi.
    - *Yadro Nuri (Molten Core Beam):* Ko'kragidan uzluksiz lazer shaklidagi issiqlik nuri otadi (Soniyasiga 140 HP yondiruvchi zarar).
  - **Faza 2 (75% - 40% HP — Obsidiyan Qalqon):**
    - Golem sovib qotgan obsidiyan qobig'iga o'ranadi (Barcha fizik zararlarga 100% immunitet). O'yinchi uning bo'g'imlariga suv va qor bloklarini tashlab, issiq bug' portlashi orqali qobiqni yorishi lozim.
  - **Faza 3 (40% - 15% HP):**
    - *Qizigan Reaktor (Overheating Core):* Arena harorati +60 daraja C ga ko'tariladi, o'yinchilar har soniyada issiqlik zarbasi oladi.
    - *Voxel Zilzilasi:* Butun g'or polidagi bloklar silkinib, pastki lava qa'riga qulashni boshlaydi.
  - **Faza 4 (15% - 0% HP — O'z-o'zini Yo'q Qilish Sanog'i):**
    - Golem yadrosi kritik rejimga o'tadi. O'yinchida 90 soniya vaqt bor. Agar shu vaqt ichida golem o'ldirilmasa, termoyadroviy portlash butun g'orni va yaqin atrofdagi shahar hududini yo'q qiladi.
- **Voxel Vayronkorligi:** Tosh g'ishtlarni erigan suyuq lavaga aylantiradi, metall konstruktsiyalarni bir necha soniyada bug'lantirib yuboradi.
- **Tushadigan Noyob O'ljalar (Masterwork Drop Table):**
  - *Tartaros Yadrosi (Heart of Tartaros):* Shahar metallurgiya pechlari uchun cheksiz issiqlik manbai (Ko'mir sarfisiz uzluksiz po'lat eritish).
  - *Tubanlik Katta Qalqoni (Abyssal Core Greatshield):* Frontal olov va zarbalarni 100% yutuvchi eng qudratli ritsar qalqoni.
  - *Afsonaviy Damashq Po'lati Chizmasi (Blueprint: Mythic Crucible):* Qirollikdagi eng oliy darajali afsonaviy qurol-aslahalarni yasash imkoniyati.

---

# 72. BOSS PROGRESSIYASI

Dunyoning 5 ta afsonaviy bossi shunchaki xaritada aylanib yurmaydi. Ularning har biri qadimiy qurbongohlar (Summoning Altars) orqali chaqiriladi va ularni mag'lub etish butun feodal shohlik miqyosida doimiy global farmonlar (Realm-Wide Edicts) hamda passiv iqtisodiy-harbiy bonuslarni ochib beradi.

### 72.1. Bosslarni Chaqirish Qurbongohlari va Talab Qilinadigan Yutuqlar

| Boss Nomi | Qurbongoh Joylashuvi | Talab Qilinadigan Shohlik Yutug'i | Qurbongoh Qurbonligi (Ritual Offering) |
|---|---|---|---|
| 1. Grok'Gar (Troll King) | Qadimiy Tosh Mozoat (Ancient Barrow) | Shahar Aholisi 35+ kishi, Tier II Qal'a | 10 ta Yovvoyi Qobon Oziqi + 5 Bochka Asal Sharobi |
| 2. Baron Mordred (Necromancer) | Mal'un Kripta Darvozasi (Mausoleum) | 5 nafar Elita Veteran Askari, Shahar Ibodatxonasi | Halok bo'lgan Bahodir Bosh Suyagi + 3 Kumush Kosa |
| 3. Vessaria (Swamp Wyvern) | Botqoqlik Uyasi (Festering Mire Altar) | To'liq Zanjir Sovutli Qo'shin, Katta Don Ombri | Oltin Ajdaho Tuxumi + 20 Halit Tuz Qopchasi |
| 4. Thrym (Frost Jotun) | Abadiy Muzlik Qurbongohi (Glacial Spire) | Qishki Issiqlik Tizimi, Tier IV Shahar Kengashi | 5 ta Moviy Yoqut (Sapphire) + Qor Bo'risi Yuragi |
| 5. Tartaros (Abyssal Golem) | Magma O'chog'i Qurbongohi (Crucible Altar) | Avvalgi 4 ta Bossni Mag'lub Etish Yutug'i | 4 ta Boss Trofeyining Birlashtirilgan Qotishmasi |

### 72.2. Mag'lubiyatdan So'ng Ochiladigan Doimiy Shohona Farmonlar (Realm Edicts)

Har bir afsonaviy dushman mag'lub etilganda qirol taxt zalida butun shohlik hududida umrbod amal qiluvchi maxsus farmon (Edict) e'lon qiladi:

| Mag'lub Etilgan Boss | Shohona Farmon (Realm Edict) | Butun Shohlikka Doimiy Ta'siri | Yangi Ochiladigan Texnologiya |
|---|---|---|---|
| Grok'Gar (Troll King) | Farmon: Qoya O'ymakorligi (Edict of Stonecrafters) | Konda tosh qazish tezligi +25%, barcha binolar mustahkamligi +20% | Gigant Tosh Blokli Qal'a Devorlari |
| Baron Mordred (Necromancer) | Farmon: Muqaddas Zamin (Edict of Sanctified Soil) | Tungi o'liklar hujumi to'xtaydi, dorivor giyohlar hosili +30% | Gospitalda Jarrohlik va Antiseptika |
| Vessaria (Swamp Wyvern) | Farmon: Buyuk Savdo Karvoni (Edict of Trade Guilds) | Savdogarlar boji -50% ga arzonlashadi, soliqqa toqatlilik +15% | Kislotaga Chidamli Zirh Qoplamalari |
| Thrym (Frost Jotun) | Farmon: Qishki Matonat (Edict of Frost Mastery) | Qishda o'tin sarfi -35% ga kamayadi, fuqarolar muzlab qolmaydi | Yerto'lada Doimiy Muzxona Sovutgichi |
| Tartaros (Abyssal Golem) | Farmon: Buyuk Feodal Shohlik Toji (Imperial Coronation) | O'yinning bosh g'alabasi, barcha qo'shni feodallar vassal bo'ladi | Afsonaviy Damashq Po'lati Domna Pechi |

---

# 73. JAROHAT VA SALOMATLIK STATUSLARI (TRAUMA CONDITIONS & WOUND MECHANICS)

Voxel Lord: Feudal Realm o'yinida inson tanasi shunchaki bitta umumiy Health paneli bilan cheklanmaydi. Har bir fuqaro va hukmdor jang, kon qazish, yiqilish yoki sovuq urishi oqibatida vujudga keluvchi lokal travmatik statuslar (Trauma Status Effects) tizimiga ega. Davolanmagan jarohatlar o'z vaqtida bartaraf etilmasa, qon ketishidan o'limga yoki qorason (gangrena) asoratlariga olib keladi.

### 73.1. Travmatik Holatlar va Fiziologik Buzilishlar Katalogi

1. **Qon Ketishi (Bleeding Trauma):**
   - **Yengil Qon Ketish (Minor Bleeding):** Pichoq yoki qamish kesganda. Qon yo'qotish: $-1.5 \text{ HP/min}$. 15 daqiqada o'z-o'zidan ivishi mumkin.
   - **O'rtacha Qon Ketish (Moderate Bleeding):** Qilich yoki o'q jarohati. Qon yo'qotish: $-5.0 \text{ HP/min}$. Bog'ich (`Linen Bandage`) qo'yilmasa, 20 daqiqada qon tugab hushidan ketadi.
   - **Arterial Kuchli Qon Ketish (Severe Arterial Bleeding):** Og'ir bolta yoki nayza sanchilganda. Qon yo'qotish: $-25.0 \text{ HP/min}$. Fuqaro 90 soniya ichida jgut yoki zudlik bilan jarrohlik ko'rsatilmasa vafot etadi.

2. **Suyak Sinishi (Fractures & Dislocations):**
   - **Qo'l Sinishi (Arm Fracture):** Og'ir gurzi (Blunt) zarbasi yoki tosh qulashi oqibatida. Fuqaro qo'lidagi asbob yoki qurolni darhol tushirib yuboradi, ishlab chiqarish va jang qilish qobiliyati $0\%$ ga tushadi.
   - **Oyoq Sinishi (Leg Fracture):** Baland qoyadan yoki qal'a devoridan yiqilganda. Harakatlanish tezligi $-75\%$ ga sekinlashadi, fuqaro oqsoqlanib sudraladi, charchoq sarfi $3.0\times$ tezlashadi.
   - **Qovurg'a Sinishi (Rib Fracture):** Kuchli zarba zarbasi. Stamina sig'imi $-50\%$, yugurish va og'ir yuk ko'tarish mutlaqo mumkin emas.

3. **Miya Chayqalishi va Travma (Concussion & Head Trauma):**
   - Dubulg'asiz boshga tushgan tosh yoki cho'kich zarbasi.
   - 12 o'yin soati davomida ko'rish maydoni xiralashadi (Tunnel vision vignetting), harakatlanish trayektoriyasi chayqaladi (Erratic pathfinding), fuqaro o'z uyini adashtirib qo'yishi mumkin.

4. **Kuyish Jarohatlari (Burns — 1st to 3rd Degree):**
   - Olov, qaynoq smola (Boiling Pitch) yoki qamal mash'alalari ta'sirida.
   - Terining himoya qatlami kuyishi oqibatida infektsiya tushish ehtimoli $+50\%$ ga oshadi, doimiy qattiq og'riq (Pain $-35$ Morale) beradi.

5. **Yaraning Yiringlashi va Qorason (Wound Infection & Sepsis):**
   - Agar ochiq qonagan yara 12 soat ichida toza bog'ich bilan bog'lanmasa va dezinfektsiya qilinmasa:
     $$P_{infection} = 0.40 \times (1.0 + 0.5 \times MiasmaLocal)$$
   - Isitma ko'tariladi ($T_{body} > 39.5^\circ\text{C}$), fuqaro alahsiraydi, har soatda $-2.0 \text{ HP}$ yo'qotadi. Tabib tomonidan kuydirish (Cautery) yoki amputatsiya qilinmasa, 48 soatda qon zaharlanib o'ladi.

---

### 73.2. Travma Balans Jadvali (Trauma Balance Table)

| Travma Nomi | Asosiy Sababi | HP Sarflanishi / Minut | Mehnat / Harakat Cheklovi | Davomiyligi (Davolanmasa) | Talab Qilinadigan Tibbiy Amaliyot |
|---|---|---|---|---|---|
| **Yengil Kesilish** | Tikon, pichoq, asbob | $-1.5 \text{ HP}$ | Ish tezligi $-10\%$ | 15 daqiqa (O'zi bitadi) | Toza mato / Bog'ich |
| **Arterial Qonash**| Qilich, nayza, halberd | $-25.0 \text{ HP}$ | Yugura olmaydi, hushdan ketadi| 90 soniya (O'lim muqarrar) | Turniket, Zudlik bilan Jarrohlik |
| **Oyoq Sinishi** | Qulash, bolg'a zarbasi | $-0.2 \text{ HP}$ | Tezlik $-75\%$, yuk ko'tarmaydi| 7 kun (Noto'g'ri bitadi) | Yog'och shina (`Splint`) + 48h to'shak |
| **Qo'l Sinishi** | Taran, devor qulashi | $-0.2 \text{ HP}$ | Qurol/asbob ishlata olmaydi | 7 kun (Nogironlik xavfi)| Fiksatsiya bog'ichi + Yengil ish |
| **Miya Chayqalishi**| Boshga tosh urilishi | $0.0 \text{ HP}$ | Tezlik $-30\%$, yo'ldan adashish| 12 o'yin soati | Tinch qorong'u xonada uyqu |
| **3-Darajali Kuyish**| Qaynoq smola, olov | $-1.0 \text{ HP}$ | Mehnat qobiliyati $-60\%$ | 5 kun (Doimiy chandiq) | Asal malhami (`Poultice`) + Toza doka |
| **Qorason (Gangrena)**| Nopok yara, iflos botqoq| $-2.0 \text{ HP/soat}$ | Butkul to'shakka mixlanadi | 48 soat (Halokatli) | Jarrohlik amputatsiyasi / Kuydirish |

---

# 74. TABOBAT VA GOSPITAL TIZIMI (MEDICINE, SURGERY & CLINIC INFRASTRUCTURE)

Shahar kengaygan sari jarohatlangan jangchilar va kasalmand fuqarolarni davolash uchun professional tibbiy infratuzilma — Qishloq Tabibxonasi (Apothecary) va Shahar Gospitali (Infirmary / Hospital) zarur bo'ladi.

### 74.1. Shahar Gospitali Infratuzilmasi va Xonalari

1. **Ko'rik Stoli (Examination Table):**
   - Tabib yangi kelgan yaradorlarni qabul qiladi, travma turini aniqlaydi va birinchi yordam ko'rsatadi.
2. **Jarrohlik To'shagi (Surgical Bed):**
   - Suyaklarni to'g'rilash, chuqur o'qlarni sug'urish va amputatsiya amaliyotlari uchun mustahkam charm tasmali to'shak.
3. **Dorixona Dastgohi (Apothecary Alchemy Still & Mortar):**
   - Dorivor giyohlarni maydalash, spirtli damlamalar tayyorlash va antiseptik moylar qaynatish stoli.
4. **Izolyatsiya Palatasi (Quarantine Ward):**
   - Yuqumli kasallikka chalingan fuqarolarni boshqalardan ajratib saqlash uchun mo'ljallangan qalin devorli xona.
5. **Kir Yuvish va Qaynatish Xomi (Sanitary Cauldron):**
   - Iflos qonli dokalarni qaynoq suvda qaynatib qayta tozalash joyi (Infektsiya tarqalishini $95\%$ kamaytiradi).

---

### 74.2. Dorivor Giyohlar va Tibbiy Retseptlar (Herbal Medicine Recipes)

| Dori / Malham Nomi | Kerakli Xomashyo | Tayyorlash Dastgohi | Tayyorlash Vaqti | Tibbiy Ta'siri va Qo'llanilishi |
|---|---|---|---|---|
| **Oddiy Bog'ich (Linen Bandage)** | 1 Zig'ir Mato + 1 Qaynoq Suv | Dorixona Stoli | 5 sekund | Qon ketishini (Bleeding) to'xtatadi. |
| **Asalli Antiseptik Malham (Poultice)** | 1 Yovvoyi Asal + 2 Dorivor Giyoh | Hovoncha (Mortar) | 12 sekund | Yiringlash (Infection) xavfini yo'qotadi, kuyishni bitiradi. |
| **Shina / Fiksator (Bone Splint)** | 2 Yog'och Taxta + 1 Doka Bog'ich | Duradgor Stoli | 10 sekund | Sinishni fiksatsiya qiladi, bitish vaqtini 7 kundan 2 kunga tushiradi. |
| **Tol Po'stlog'i Damlamasi (Willow Bark)**| 2 Tol Po'stlog'i + 1 Suv Idishi | Dorixona Qozoni | 20 sekund | Og'riqni bosadi (Pain $-80\%$), shamollash isitmasini tushiradi. |
| **Mo''jizaviy Panatseya (Miracle Elixir)**| 1 Tog' Za'faroni + 1 Spirt + 1 Oltingugurt | Distillyator | 45 sekund | Qora o'lat va qorasonning dastlabki bosqichini $60\%$ tuzatadi. |

---

### 74.3. Tabib Davolash Samaradorligi Formulasi (Doctor Healing Rate)

Gospitalda yotgan bemorning har soatda tiklanadigan sog'lig'i quyidagi formula orqali hisoblanadi:

$$Rate_{heal} = BaseHealRate \times \left(1.0 + 0.02 \cdot Skill_{doc}\right) \times Tier_{bed} \times CleanlinessMult$$

Bunda:
- $BaseHealRate = 4.0 \text{ HP/soat}$.
- $Skill_{doc} \in [0, 100]$: Tabibning tibbiy mahorat darajasi (100-darajali Tabib davolash tezligini 3 barobarga oshiradi).
- $Tier_{bed}$: Oddiy to'shak = $1.0\times$, Dezinfektsiyalangan pat to'shak = $1.4\times$.
- $CleanlinessMult$: Gospital ichidagi sanitariya darajasiga qarab ($0.5\times$ dan $1.25\times$ gacha).

**Jarrohlik Asboblari va Gigiyena:**
Tabib qo'lida po'lat skalpel, suyak arrasi va kuydirish temiri (`Cautery Iron`) bo'lishi kerak. Har bir amaliyotdan oldin asboblar olovda qizdirilmasa, bemorga $30\%$ ehtimol bilan qon infektsiyasi yuqadi.

---

# 75. YUQUMLI KASALLIKLAR MEXANIKASI (EPIDEMIOLOGY & TRANSMISSION VECTORS)

Zich joylashgan o'rta asr shaharlarida sanitariya qoidalariga rioya qilinmasa, epidemiyalar vujudga keladi. Kasalliklar tarqalishi klassik SIR (Susceptible-Infectious-Recovered) matematik epidemiologik modeli asosida real vaqtda hisoblanadi.

### 75.1. Matematik Epidemiologik Model (Differential SIR Equations)

Shahar aholisi 3 guruhga ajratiladi: $S$ — kasallikka moyil aholi, $I$ — yuqtirgan faol bemorlar, $R$ — tuzalib immunitet hosil qilganlar.

$$\frac{dS}{dt} = -\beta \frac{S \cdot I}{N}$$
$$\frac{dI}{dt} = \beta \frac{S \cdot I}{N} - \gamma I - \mu I$$
$$\frac{dR}{dt} = \gamma I$$

Bunda:
- $N = S + I + R$: Jami shahar aholisi.
- $\beta$: Kasallik yuqish koeffitsiyenti (Aholi zichligi, ko'chalardagi najas va kalamushlar soniga bog'liq).
- $\gamma$: Sog'ayish tezligi koeffitsiyenti ($\gamma = \frac{1}{\text{Kasallik Davomiyligi}} \times (1.0 + 0.5 \cdot HospitalCare)$).
- $\mu$: O'lim koeffitsiyenti.
- **Bazaviy Reproduktiv Son ($R_0$):**
  $$R_0 = \frac{\beta}{\gamma + \mu}$$
  Agar $R_0 > 1.0$ bo'lsa, shaharda epidemiya eksponentsial avj oladi; agar shahar sanitariyasi va karantin hisobiga $R_0 < 1.0$ ga tushirilsa, kasallik so'nadi.

---

### 75.2. O'rta Asr Yuqumli Kasalliklar Katalogi

| Kasallik Nomi | Asosiy Tarqalish Vektori | Inkubatsiya Davri | Simptomlar va Debafflar | Davolanmaganda O'lim Koeffitsiyenti ($\mu$) | Tuzalish / Immunitet |
|---|---|---|---|---|---|
| **Ichburug' / Vabo (Dysentery/Cholera)**| Iflos quduq suvi, buzilgan ovqat | 12 soat | Kuchli suvsizlanish, ich ketishi, harakat $-50\%$ | $35\%$ | 3 kun (Toza suv va tuzli sho'rva) |
| **Zotiljam / Gripp (Influenza)** | Nafas yo'llari, sovuq xonalar | 24 soat | Yo'tal, baland isitma, ish tezligi $-40\%$ | $15\%$ (Keksalarda $45\%$) | 5 kun (Issiq kamin, tol po'stlog'i)|
| **Kaltama (Typhus)** | Kiyimdagi tana bitlari, kir o'rinlar| 48 soat | Qizil toshmalar, alahsish, qattiq holsizlik | $40\%$ | 7 kun (Yuvinish, kiyimlarni qaynatish)|
| **Quturish (Rabies)** | Quturgan bo'ri/it tishlashi | 36 soat | Suvdan qo'rqish, agressiv jazava, fuqarolarga hujum | $100\%$ (Davosi yo'q) | 2 soat ichida yara kuydirilmasa o'lim |

---

### 75.3. Tarqalish Zanjiri va Infektsiya Vektorlari (Vectors & Containment)

1. **Kalamushlar va Bitlar Vektori (Vermin Vector):**
   - Don omborlarida bug'doy nam tortsa yoki ko'chada axlat to'plansa, kalamushlar populyatsiyasi ko'payadi. Kalamushlar o'z ustida vabo burgalarini (`Xenopsylla`) tashiydi.
2. **Ifloslangan Quduqlar (Waterborne Contamination):**
   - Agar chiqindi o'rasi (Cesspool) quduqdan 15 metrdan yaqinroq masofada joylashsa, yerosti sizot suvlari orqali quduq zaharlanadi. Quduqdan ichgan har bir fuqaro $70\%$ ehtimol bilan vabo yuqtiradi.
3. **Zich Tavernalar va Bozorlar (Airborne Droplet Vector):**
   - Shamollagan fuqaro taverna yoki cherkovga borsa, 4 metr radiusdagi barcha suhbatdoshlariga zotiljam yuqtirish ehtimoli $+25\%$ ga oshadi.

---

# 76. SHAHAR SANITARIYASI (MUNICIPAL SANITATION & WASTE MANAGEMENT)

Shahar kengaygani sari inson va chorva chiqindilari, oziq-ovqat qoldiqlari va iflos suvlar tabiiy ravishda to'planib boradi. Sanitariya nazorat qilinmasa, ko'chalarni Miasma (sassiq zaharli bug') qoplaydi.

### 76.1. Chiqindi va Miasma To'planishi Dinamikasi

Har bir turar-joy va ko'cha voxeli bo'yicha ifloslik darajasi $Filth \in [0.0, 100.0]$ har soatda quyidagi balans asosida yangilanadi:

$$\frac{d(Filth)}{dt} = \sum Pop \times WasteRate + \sum Livestock \times DungRate - \sum SweeperCapacity$$

- Har bir voyaga yetgan fuqaro kuniga $1.2 \text{ kg}$ maishiy va biologik chiqindi chiqaradi ($WasteRate \approx 0.05 \text{ filth/soat}$).
- Har bir mol/ot kuniga $8.0 \text{ kg}$ go'ng chiqaradi ($DungRate \approx 0.25 \text{ filth/soat}$).
- **Miasma Portlashi:** Agar ko'chadagi $Filth > 70.0$ bo'lsa, ushbu ko'chadan o'tgan fuqarolar $-20$ Morale yo'qotadi va pashshalar to'dasi paydo bo'ladi.

---

### 76.2. Sanitariya Infratuzilmasi va Toza Suv Tizimi

1. **Hojatxona va Chiqindi O'rasi (Cesspool / Latrine Pit):**
   - Qazilgan $2\times2\times3$ chuqurlikdagi tosh bilan qoplangan o'ra. Shahar najosatini o'ziga yutadi va ko'chaga chiqishini to'xtatadi.
   - Har faslda bir marta tozalanishi shart.
2. **Kompast O'ralari (Composting Pits):**
   - Chiqindilar somon bilan aralashtirilib chirindi o'g'itga aylantiriladi. 1 fasldan so'ng ekin unumdorligini $+25\%$ ga oshiruvchi tabiiy o'g'it (`Fertilizer Barrel`) olinadi.
3. **Oqova Ariqlar (Stone Drainage Ditches):**
   - Tosh yotqizilgan ko'cha chetlaridagi ariqlar yomg'ir suvlarini shahar tashqarisidagi daryoga olib chiqib ketadi, ko'chalarda ko'lmak hosil bo'lishini bartaraf etadi.
4. **Qopqoqli Suv Hovuzlari va Akveduklar (Aqueducts & Cisterns):**
   - Tog' buloqlaridan tosh novlar orqali toza suv olib kelish. Quduqlarga tushadigan yukni kamaytiradi va vabo xavfini butunlay yo'q qiladi.

---

### 76.3. Shahar Tozalovchilari va Kemiruvchilarga Qarshi Kurash

- **Tozalovchi (Street Sweeper / Dung Collector):**
  - Qo'lida supurgi, belkurak va 2 g'ildirakli chiqindi aravasi bo'lgan munitsipal xizmatchi.
  - Kundalik vazifasi: Ko'chalardagi axlat va tezaklarni to'plab shahar chetidagi kompost o'rasiga yoki kul xumdoniga eltish. 1 ta tozalovchi 35 ta fuqaroning chiqindisini zararsizlantirishga qodir.
- **Mushuklar va Qopqonchi Itlar (Biological Pest Control):**
  - Shaharda boqiladigan erkin mushuklar (Domestic Cats) omborlar va uylar atrofidagi sichqon va kalamushlar sonini $80\%$ ga qisqartiradi.
  - Maxsus o'rgatilgan kalamush ovlovchi itlar (Terriers) shahar sanitariya darajasini $+15\%$ ga oshiradi.

---

# 77. QORA O‘LAT VA KARANTIN (THE BLACK PLAGUE & QUARANTINE PROTOCOLS)

Qora O'lat (The Black Death / Bubonic Plague) — Voxel Lord dunyosidagi eng dahshatli tabiiy demografik ofatdir. U to'satdan shahar boyligi cho'qqiga chiqqanda yoki sanitariya kollapsga uchraganda boshlanadi va butun aholining uchdan ikki qismini qirib yuborish qudratiga ega.

### 77.1. Qora O'latning Boshlanish Triggerlari va Klinik Bosqichlari

O'lat epidemiyasi quyidagi omillar birlashganda yuzaga keladi:
- Shahar o'rtacha iflosligi $Filth > 80.0$.
- Ko'chada 48 soatdan ortiq ko'milmay yotgan jasadlar mavjudligi.
- Kalamushlar soni aholi sonidan 2 barobar oshib ketishi.
- Tashqi infitsirlangan savdo kemasi yoki karvoni shahar portiga kelishi.

**O'latning Fiziologik Bosqichlari:**
1. **Bubonik Bosqich (Bubonic Plague):**
   - Qora burgalar chaqishi orqali yuqadi. Bo'yin, qo'ltiq va chovda qora zaharli bezlar (Buboes) shishib chiqadi.
   - Harorat $41^\circ\text{C}$, darmonsizlik. Davolanmaganda o'lim darajasi: $65\%$.
2. **Pnevmonik Bosqich (Pneumonic Plague):**
   - Agar bubonik bemorlar olomon orasida yashasa, vabo nafas yo'llariga o'tadi va havo orqali tupuk zarralari bilan tarqala boshlaydi.
   - O'pka qonab eriydi, qon tupurish. O'lim darajasi: $95\%$. Bemor 24–36 soat ichida halok bo'ladi.

---

### 77.2. Favqulodda Karantin Protokollari va Shahar Izolyatsiyasi

Hukmdor shaharda o'lat aniqlanganda Royal Ledger orqali "Qora Karantin Farmoni" (`Black Quarantine Edict`) e'lon qilishi lozim:

1. **Xonadonlarni Qulflash (Boarding Up Infected Houses):**
   - Ichida o'lat chiqqan uyning eshigiga oq bo'yoq bilan Qizil Xoch (Red Cross) chiziladi va eshik tashqaridan taxtalar bilan qoqib mixlanadi.
   - Barcha oila a'zolari 14 kun davomida uy ichida qoladi. Ularga maxsus darcha orqali non va suv berib turiladi.
2. **Qochishga Qarshi Qurolli Kordon (Armed Sanitary Cordon):**
   - Shahar darvozalari to'liq yopiladi, barcha savdo karvonlari to'xtatiladi.
   - Shahardan ruxsatsiz qochmoqchi bo'lgan har qanday fuqaro kamonchilar tomonidan o'ldiriladi (Chunki bitta qochqin qo'shni qishloqlarga ham kasallik olib borishi mumkin).
3. **Kiyim-kechak va To'shaklarni Yoqish (Sanitary Pyres):**
   - Vafot etganlarning barcha kiyimlari, to'shaklari va yog'och asboblari shahar tashqarisidagi o'lat olovida kulga aylantiriladi.

---

### 77.3. O'lat Tabibi va Maxsus Himoya Vositalari (The Plague Doctor)

Shaharda karantin choralari boshlanganda maxsus roldagi shifokor — **O'lat Tabibi (Plague Doctor)** tayinlanadi.

- **Himoya Kostyumi Mexanikasi:**
  - **Qush Tumshuqli Niqob (Beak Mask):** Tumshuq ichiga kofur (camphor), lavanda, yalpiz va quritilgan gul barglari tiqiladi. Bu tabibni zaharli "miasma" va tomchilar orqali zaharlanishdan asraydi.
  - **Mum Shimdirilgan Teri Chopon (Waxed Heavy Leather Cloak):** Qalin charmga eritilgan mum surtiladi, bu o'lat burgalarining choponga yopishishi va chaqishiga to'sqinlik qiladi.
  - **Tekshiruv Tayog'i (Wooden Examination Cane):** Tabib bemorga qo'li bilan tegmasdan, tayoq orqali kiyimini ko'tarib bubonlarni tekshiradi va pulsni o'lchaydi.
- **O'yin Effekti:**
  - O'lat Tabibi ishlayotgan hududda kasallik yuqish koeffitsiyenti $\beta$ darhol $-60\%$ ga pasayadi.
  - Shahar aholisining vahima hissi pasayadi ($+15$ Morale himoya hissi).
  - Tabib maxsus "Kuydirish Malhami" orqali bemorlardagi bubonlarni kuydirib, tirik qolish ehtimolini $25\%$ dan $60\%$ gacha oshiradi.

---

# 78. JINOYATCHILIK SABABLARI

Ochlik, haddan tashqari yuqori soliqlar, ishsizlik, spirtli ichimliklar ta'siri, tushkunlik va shahardagi soqchilar yetishmasligi.

---

# 79. JINOYATNI TERGOV QILISH VA HIBSI

`Jinoyat sodir bo'lishi → Guvohlar va ashyoviy dalillar → Soqchilar tergovi → Gumondorni hibsga olish → Sud jarayoni`.

---

# 80. HUKMDOR SUDI VA JAZO CHORALARI (ROYAL COURT)

Hukmlar: Afv etish (Pardon), Jarima solish (Fine), Jazo ustuniga kishanlash (Stocks), Qasr zindoni (Dungeon), Majburiy og'ir mehnat (Shaxta), Surgun qilish (Exile), Qatl (Execution).

---

# 81. QONUNLAR TIZIMI (CODEX OF LAWS)

Soliq qonuni, Oziq-ovqat me'yori, Harbiy majburiyat, Tungi komendantlik soati, Savdo boji, O'rmondan foydalanish qoidalari.

---

# 82. FAVQULODDA FARMONLAR (ROYAL EDICTS)

Vaqtinchalik shoshilinch choralar (Masalan: Shoshilinch hosil yig'ish — mehnat unumi +30%, fuqarolar kayfiyati -10%).

---

# 83. TASHQI MUNOSABATLAR VA STATUSTLAR

Feodal dunyoda suverenitet faqat harbiy qudrat bilan emas, balki mintaqadagi qo'shni lordlar, diniy iyerarxiya va savdogarlar gildiyalari bilan o'rnatilgan o'zaro diplomatik aloqalar orqali kafolatlanadi. O'yinchi har bir mustaqil hukmdor bilan o'zaro ishonch ($Trust \in [0, 100]$), xalqaro obro' ($Honor \in [0, 100]$) va diplomatik munosabat ($Relation \in [-100, +100]$) ko'rsatkichlariga ega bo'ladi.

### 83.1. Diplomatik Statuslar Matritsasi

O'yinchi va AI davlatlar o'rtasida quyidagi 7 ta yuridik status amal qiladi:

| Status Nomi | Munosabat Diapazoni | Diplomatik Harakatlar Huquqi | Chegara va Bojxona Qoidalari | Harbiy Eskalatsiya Xavfi |
|---|---|---|---|---|
| **Urush (War)** | $[-100, -60]$ | Har qanday diplomatik muzokara faqat taslim bo'lish yoki tovon to'lash sharti bilan ochiladi. | Chegaralar mutlaq yopiq. Barcha elchilar hibsga olinadi yoki qatl etiladi. | Maksimal; qamal qo'shinlari, qishloqlarni yoqish va reydlar doimiy kechadi. |
| **Dushmanlik (Hostile)** | $[-59, -20]$ | Faqat norozilik notalari va chegara demarkatsiyasi talablari yuborilishi mumkin. | To'liq iqtisodiy embargo, tovarlar almashinuvi taqiqlangan, savdo yo'llari yopilgan. | Yuqori; chegarada qurolli to'qnashuvlar va josuslik diversiyalari faol olib boriladi. |
| **Sovuq (Unfriendly)** | $[-19, -1]$ | Savdo tariflarini pasaytirish bo'yicha cheklangan muzokaralar olib borish mumkin. | Tovarlarga $+50\%$ eksport-import boji qo'llaniladi. Qurolli otryadlar kirishi taqiqlanadi. | O'rtacha; kichik chegaraviy tushunmovchiliklar ham jiddiy mojaroga olib kelishi mumkin. |
| **Neytral (Neutral)** | $[0, +19]$ | Elchilar almashinuvi, asosiy tijorat shartnomalari, karvonsaroy ochish huquqi. | Standart bozor narxlari ($0\%$ boj). Tinch fuqarolar erkin harakatlanadi. | Past; tomonlar faqat o'z manfaatlarini himoya qiladi, tajovuz qilmaydi. |
| **Do'stona (Friendly)** | $[+20, +59]$ | Hujum qilmaslik pakti (NAP), texnologiya litsenziyalari, mudofaa maslahatlashuvlari. | Bojxona to'lovlariga $-25\%$ chegirma. Chegarada qurolsiz tranzit o'tishga ruxsat. | Minimal; har ikki tomon do'stona aloqalarni mustahkamlashga intiladi. |
| **Harbiy Ittifoq (Allied)** | $[+60, +89]$ | Umumiy harbiy rejalashtirish, birgalikda qamal boshlash, o'zaro qurol-yarog' yetkazib berish. | To'liq erkin savdo koridori. Qo'shinlar ittifoqchi qal'alarda bepul davolanadi va ta'minlanadi. | Nol; ittifoqchilar bir-biriga hujum qilmaydi va dushmanga qarshi birgalikda kurashadi. |
| **Vassallik / Qaramlik (Vassalage)** | $[+90, +100]$ | Vassal lord o'yinchi farmonlariga bo'ysunadi, harbiy chaqiriqlarga majburiy askar yuboradi. | Vassal o'zining sof mavsumiy daromadining $15\%$ qismini o'yinchi xazinasiga o'tkazadi. | Maxsus; agar vassalning sadoqati (Loyalty) $30$ balldan tushib ketsa, ozodlik isyoni ko'taradi. |

### 83.2. Ishonch (Trust) va Obro' (Honor) Dinamikasi

Munosabatlar balansi vaqt o'tishi bilan o'zgaradi:
- **Ishonchning Tabiiy So'nishi (Trust Decay):** Har qanday faol shartnomasiz qolgan munosabatlar har mavsumda $50$ bazaviy nuqtaga qarab siljiydi:
  $$\frac{d(Trust)}{dt} = -\mu \cdot (Trust - 50)$$
  Bunda $\mu = 0.015$ kunlik koeffitsiyent.
- **Xalqaro Obro' (Honor):** Shartnomalarni buzish (masalan, Hujum qilmaslik paktini buzib to'satdan qamal boshlash) o'yinchining obro'sini $-50$ ga tushiradi. Past obro' barcha neytral lordlarning o'yinchiga nisbatan shubhasini oshiradi va yangi ittifoqlar tuzish narxini $3.0\times$ barobar qimmatlashtiradi.

### 83.3. Diplomatik Elchilar (Emissaries) Mexanikasi

Diplomatik takliflar darhol menyu orqali yetib bormaydi. O'yinchi Elchixonadan (Embassy) maxsus chopar yoki elchini (Emissary) jo'natishi shart:
- Elchi dunyo xaritasi bo'ylab jismoniy personaj sifatida yo'lga chiqadi ($v_{emissary} = 5.5\text{ km/soat}$).
- Yo'lda elchiga qaroqchilar hujum qilishi yoki dushman josuslari tomonidan o'ldirilishi xavfi mavjud.
- Elchi dushman qal'asiga kirgach, 12 soat davomida muzokaralar o'tkazadi va javob maktubi bilan qaytib keladi.

---

# 84. DIPLOMATIK SHARTNOMALAR

Feodal diplomatiya tizimida shartnomalar tomonlarning iqtisodiy va harbiy imkoniyatlarini mustahkamlovchi yuridik bitimlardir. O'yinchi elchilar orqali quyidagi 6 ta asosiy shartnomani imzolashi mumkin:

### 84.1. Asosiy Shartnoma Turlari

1. **Savdo Bitimi (Bilateral Trade Agreement):**
   - Ikki shahar o'rtasida muntazam karvonlar qatnovini ochadi.
   - Har ikki tomonda import tovarlariga qo'yiladigan soliqlar $50\%$ kamaytiriladi.
   - O'yinchining bozorlarida chet el mahsulotlari (ipak, noyob rudalar, ziravorlar) paydo bo'ladi.
2. **Hujum Qilmaslik Pakti (Non-Aggression Pact - NAP):**
   - 120 o'yin kuniga mo'ljallangan mudofaa kafolati.
   - Tomonlar bir-birining chegara zonasida istehkomlar qurmaslik majburiyatini oladi.
   - Agar bir tomon paktni buzsa, xalqaro maydonda "Qasamyodbuzar" (Oathbreaker) tamg'asini oladi va barcha boshqa fraktsiyalar bilan munosabati $-40$ ga tushadi.
3. **Mudofaa Ittifoqi (Mutual Defense Treaty):**
   - Agar ittifoqchilardan biriga uchinchi tomon hujum qilsa, ikkinchi tomon 72 soat ichida kamida 25 nafar qurolli askar yoki har mavsum $2,000$ kumush tanga harbiy yordam yuborishga majbur.
4. **Sulolaviy Nikoh Diplimatiyasi (Dynastic Marriage):**
   - O'yinchi sulolasining shahzoda yoki malikasini qo'shni lord xonadoniga uzatish yoki kelin qilish.
   - Munosabatlar darhol $+40$ ga ko'tariladi va 360 kunga mustahkamlanadi.
   - Kelajakda qo'shni lord vafot etsa, uning taxtiga qonuniy merosxo'rlik da'vosini (Dynastic Claim) qo'yish imkonini beradi.
5. **Mavsumiy O'lpon va Himoya Bitimi (Tribute & Protectorate Treaty):**
   - Zaif shahar-davlat qudratli lordga har 30 kunda belgilangan miqdorda kumush yoki oziq-ovqat to'lab turish evaziga uning harbiy soyaboniga kiradi.
6. **Sulh va Tovon Shartnomasi (Armistice & Peace Treaty):**
   - Urushni to'xtatuvchi 180 kunlik qat'iy sulh.
   - Mag'lub tomon g'olibga urush tovonini (War Indemnity: $5,000 - 30,000$ kumush) to'laydi va chegaradagi bahsli konlarni topshiradi.

### 84.2. AI Lordlarning Takliflarni Qabul Qilish Ehtimoli (Acceptance Score)

AI lordlar o'yinchi taklif qilgan shartnomani qabul qilish yoki rad etishni quyidagi ko'p faktorli baholash formulasi orqali hisoblaydi:

$$AcceptanceScore = \left(Relation \times 0.40\right) + \left(\frac{Power_{player}}{Power_{AI}} \times 25.0\right) + \left(OfferValue \times 0.15\right) - \left(DemandValue \times 0.20\right) + \left(Honor_{player} \times 0.20\right)$$

Bunda:
- $Relation \in [-100, +100]$: Joriy diplomatik munosabat bali.
- $\frac{Power_{player}}{Power_{AI}}$: Harbiy kuchlar nisbati.
- $OfferValue$: O'yinchi taklif qilayotgan to'lov yoki hadyalar qiymati (har 100 kumush tangaga 1 ball).
- $DemandValue$: O'yinchi so'rayotgan talablar (yer, texnologiya, soliq) og'irligi.
- $Honor_{player} \in [0, 100]$: O'yinchining obro' darajasi.

**Qaror chegaralari:**
- $AcceptanceScore \ge 60.0$: Bitim to'liq qabul qilinadi va muhr bosiladi.
- $40.0 \le AcceptanceScore < 60.0$: AI lord qo'shimcha tovon yoki o'zgartirish talab qiladi (Counter-offer).
- $AcceptanceScore < 40.0$: Taklif qat'iy rad etiladi va elchi sharmandalik bilan qaytariladi.

---

# 85. HUDUD CHEGARALARI (TERRITORY CONTROL)

Feodal qirollikning yer chegaralari faqat xaritadagi chiziq emas, balki real venzel olamida fuqarolar xavfsiz harakatlanadigan, dehqonchilik qilinadigan, daraxtlar kesiladigan va konlar qaziladigan suveren hududdir.

### 85.1. Hududiy Ta'sir Sohalari va Radiusi

Chegara nazorati ma'muriy va harbiy binolardan tarqaluvchi ta'sir maydoniga (Influence Radius) asoslanadi:

| Bino / Inshoot Nomi | Bazaviy Ta'sir Radiusi ($R_{influence}$) | Qurilish Narxi | Chegara Vazifasi va Imkoniyatlari |
|---|---|---|---|
| **Asosiy Qasr Zali (Great Keep Core)** | $150.0\text{ metr}$ | 500 Tosh, 200 Yog'och, 50 Temir | Poytaxtning markaziy suverenitet o'zagi; barcha soliqlar shu yerdan hisoblanadi. |
| **Toshli Qorovul Minorasi (Watchtower)** | $45.0\text{ metr}$ | 120 Tosh, 40 Yog'och | Chegarani kengaytiradi, 4 nafar kamonchi uchun kuzatuv va o't ochish pozitsiyasi. |
| **Chegara Tosh Belgisi (Boundary Stone)** | $25.0\text{ metr}$ | 10 Kesilgan Tosh, 2 Ohak | Arzon demarkatsiya belgisi; yaylov va o'rmon chegaralarini rasmiylashtiradi. |
| **Harbiy Fort / Chegara Istehkomi (Border Fort)** | $80.0\text{ metr}$ | 300 Tosh, 150 Yog'och, 20 Temir | Strategik tog' yo'llari va daryo kechuvlarini nazorat qiluvchi mustahkam garnizon. |

### 85.2. Chegara Ta'sirining Matematik Dala Formulasi

Biror venzel koordinatasidagi $(x, z)$ nuqtada shaharning suverenitet ta'sir kuchi ($I_{border}$) markazdan uzoqlashgan sari pasayadi:

$$I_{border}(d) = \frac{Power_{settlement}}{1.0 + \left(\frac{d}{R_{influence}}\right)^2}$$

Bunda:
- $d$: Nuqtadan eng yaqin chegara inshootigacha bo'lgan gorizontal masofa (metrlarda).
- $Power_{settlement} = 100.0 \times \left(1.0 + 0.05 \cdot Population\right)$: Shaharning ma'muriy kuchi.
- Agar bir nuqtada ikki raqib davlatning ta'sir kuchi to'qnashsa, qaysi tomonning $I_{border}$ ko'rsatkichi yuqori bo'lsa, o'sha tomon hududiy nazoratni o'z qo'liga oladi.

### 85.3. Neytral Bufer Hududlar (Neutral Wilderness Buffer Zones)

Ikkala davlat ta'sir doirasi yetib bormagan oraliq zonalar "Neytral Bufer Hudud" hisoblanadi:
- Bu hududda o'yinchi ham, AI lordlar ham daraxt kesishi, loy va tosh qazishi mumkin.
- Ushbu zonalarda qonun va tartib yo'q — qaroqchilar to'dalari lager quradi, yovvoyi yirtqichlar ko'payadi va karvonlarga pistirmalar uyushtiriladi.
- Bufer zonada o'yinchi yangi Qorovul minorasi qursa, bu raqib davlat tomonidan tajovuz deb baholanadi va ularning tajovuzkorlik hisobiga (Aggression Score) darhol $+35$ ball qo'shiladi.

### 85.4. Chegara Buzilishi va Mojaroning Eskalatsiyasi

Chegara daxlsizligi qat'iy nazorat qilinadi:
1. **1-Darajali Qoidabuzarlik (Tranzit Ogohlantirish):** Agar qurolli dushman otryadi shartnomasiz chegaradan $10\text{ metrdan}$ ko'proq ichkariga kirsa, diplomatik ogohlantirish yuboriladi va har soatda chegara zo'riqishi $+5$ ga oshadi.
2. **2-Darajali Qoidabuzarlik (Iqtisodiy O'g'rilik):** Chet el fuqarolari o'yinchi chegarasida ruda qazisa yoki o'rmon kessa, soqchilar ularni hibsga oladi, asboblari va qazilgan resurslari musodara qilinadi.
3. **3-Darajali Qoidabuzarlik (Istehkom Qurilishi):** O'zga davlat chegarasi ichida noqonuniy bino qurilsa, bu to'g'ridan-to'g'ri urush sababi (Casus Belli $+60$) bo'lib xizmat qiladi va mahalliy garnizonga binoni buzish va himoyachilarni yo'q qilish amri beriladi.

---

# 86. MADANIYAT VA MA’NAVIYAT (CULTURE SYSTEM)

Madaniyat manbalari: Bardlar kuylari, Taverna suhbatlari, Buyuk Bayramlar, Marmar haykallar, Maktablar, Sobor ibodatlari, Ritsarlar turniri.

---

# 87. SHOHONA BAYRAMLAR (FESTIVALS)

Kuzgi Hosil Bayrami, Qishki Yule tantanalari. Fuqarolar baxti 100% ga chiqadi, nikohlar va yangi tug'ilishlar keskin ortadi.

---

# 88. RITSARLAR TURNIRI (ROYAL TOURNAMENT)

Kamonchilar otishuvi, qilichbozlik duellari, ot ustidagi nayza jangi (Jousting). G'olib ritsarlar qirollik shon-shuhratini yuksaltiradi.

---

# 89. TA’LIM VA SHAHAR MAKTABI

Tier III'da ochiladi. Shahar bolalari savod chiqaradi va usta hunarmandlik asoslarini tezroq o'rganadi.

---

# 90. USTA VA SHOGIRD AN’ANASI

Har bir Master usta o'zining noyob retseptlari va mahoratini yosh shogirdiga meros qilib qoldiradi.

---

# 91. DINIY VA MA’NAVIY INSHOOTLAR

Kichik ibodatxona (Chapel), Shahar cherkovi (Church), Buyuk Sobor (Great Cathedral).

---

# 92. FUQAROLARNING TABIIY VA NOTABIIY O‘LIMI (MORTALITY & GOMPERTZ-MAKEHAM MODEL)

Voxel Lord: Feudal Realm dunyosida har bir inson umri cheklangan. Shahar aholisi o'lmas robotlar emas — ular tabiiy ravishda keksayadi, kasallik yoki jarohatdan vafot etadi. Aholining o'limi demografik balansni, oilaviy ruhiyatni va shahar iqtisodiyoti davomiyligini belgilovchi asosiy omillardan biridir.

### 92.1. Gompertz-Makeham O'lim Ehtimoli Matematik Tenglamasi (Mortality Hazard Rate)

Keksa fuqarolarning (50 yoshdan oshgan) tabiiy qarish va vafot etish xavfi biologik demografiyada qabul qilingan Gompertz-Makeham o'lim qonuniyati asosida har bir o'yin kuni tongida hisoblanadi:

$$\lambda(Age) = \alpha + \beta \cdot e^{\gamma \cdot (Age - 50)}$$

Bunda kalibrlangan koeffitsiyentlar:
- $\alpha = 0.0001$: Tasodifiy biologik nosozliklar va baxtsiz hodisalarning yoshga bog'liq bo'lmagan bazaviy foni.
- $\beta = 0.0005$: Qarish boshlanishining bazaviy kuchi.
- $\gamma = 0.08$: Har yili qarish jadallashuvining eksponentsial ko'rsatkichi.
- **Kunlik O'lim Ehtimoli ($P_{death}(day)$):**
  $$P_{death}(day) = 1.0 - e^{-\lambda(Age)}$$

**Yosh Bo'yicha Tabiiy O'lim Jadvali:**
- **50 yosh:** $\lambda \approx 0.0006 \rightarrow P_{death}/kun \approx 0.06\%$ (Fasliga $\approx 0.4\%$).
- **60 yosh:** $\lambda \approx 0.0016 \rightarrow P_{death}/kun \approx 0.16\%$ (Fasliga $\approx 1.1\%$).
- **70 yosh:** $\lambda \approx 0.0029 \rightarrow P_{death}/kun \approx 0.29\%$ (Fasliga $\approx 2.0\%$).
- **75 yosh:** $\lambda \approx 0.0038 \rightarrow P_{death}/kun \approx 0.38\%$ (Fasliga $\approx 2.6\%$).
- **80+ yosh:** $\lambda > 0.0055 \rightarrow P_{death}/kun > 0.55\%$ (Yiliga $15\%$ dan ortiq tabiiy o'lim).

**Salomatlik va Gospital Ta'siri (Hazard Mitigation):**
Issiq, qulay tosh uylarda yashash, to'yimli go'shtli ratsion va shaharda yuqori malakali tabib mavjudligi o'lim xavfini quyidagi multiplikator bilan pasaytiradi:
$$\lambda_{actual} = \lambda(Age) \times \left(1.0 - 0.60 \times HospitalTier \times CleanlinessMult\right)$$
Ilg'or saroy sharoitida oqsoqollarning 80–85 yoshgacha yashash ehtimoli keskin ortadi.

---

### 92.2. Notabiiy O'lim Sabablari va Tibbiy Ekspertiza (Autopsy & Death Registry)

Har bir fuqaro vafot etganda, shahar Bailiff (Boshqaruvchisi) yoki Tabibi voqea joyiga kelib dastlabki ko'rikni (Autopsy) o'tkazadi va Royal Ledger daftari "Qazo Kitobi"ga rasmiy o'lim sababini qayd etadi:

1. **Keksalik (Old Age):** Gompertz-Makeham formulasiga ko'ra to'shakda tinch jon berish.
2. **Jangovar Qurbon (Slain in Battle):** Dushman qilichi, kamon o'qi yoki qamal toshidan olgan jarohatlari oqibatida.
3. **Yuqumli Vabo / O'lat (Plague / Infectious Disease):** Qora o'lat, vabo yoki kaltama asoratlaridan vafot etish.
4. **Ochlik va Suvsizlik (Starvation / Dehydration):** $Hunger = 100$ yoki $Thirst = 100$ holatida 48 soatdan ortiq qolib ketish.
5. **Qahraton Muzlash (Hypothermia / Freezing):** Qishda ko'chada boshpanasiz yoki isitilmagan kulbada tana harorati $28^\circ\text{C}$ dan pastga tushib ketishi.
6. **Shaxta va Ishlab Chiqarish Falokati (Cave-in / Crushed):** Shaxtada shift qulashi, yiqilgan ulkan daraxt tagida qolish yoki domna pechidagi portlash.
7. **Qotillik / Zahar (Homicide / Poison):** Shahardagi jinoyatchilar yoki josus xanjari bilan o'ldirilish.

---

### 92.3. O'lim Shok To'lqini va Shahar Ruhiyati (Death Shockwave Mechanics)

Fuqaro vafot etgan onda uning ijtimoiy aloqalari bo'yicha ruhiy zarba to'lqini tarqaladi:
- **Bevasi va Bolalari:** $-50$ Morale (1 fasl / 7 kun davomida so'nadi).
- **Aka-ukalari va Ota-onasi:** $-30$ Morale (4 kun davomida so'nadi).
- **Ustaxonadagi Hamkasblari:** $-15$ Morale (2 kun davomida ish unumi $-15\%$).
- **Shahar Aholisi:** Agar shahar himoyachisi bo'lgan ritsar jangda halok bo'lsa, butun shahar bo'ylab $-10$ Morale motam e'lon qilinadi.

---

# 93. KO‘CHADA QOLGAN JASADLARNING FOJIASI (UNBURIED CORPSES & MIASMA HAZARDS)

O'rta asr feodal dunyosida o'liklarga ehtirom ko'rsatilmasligi va jasadlarning ochiq osmon ostida qolib ketishi shahar hayotini bir necha kun ichida jahannamga aylantiruvchi biologik va ruhiy halokat manbaidir.

### 93.1. Jasadning Parchalanish Dinamikasi va Bosqichlari (48-Hour Decomposition Timeline)

O'ldirilgan yoki vafot etgan inson jasadi ko'milmasa, 48 soatlik real vaqt dinamikasida quyidagi bosqichlarni bosib o'tadi:

| Vaqt Oralig'i | Parchalanish Bosqichi | Tashqi Ko'rinish va Shader Vizuali | Morale Jarimasi (O'tgan fuqaroga) | Miasma va Yuqumlilik Xavfi |
|---|---|---|---|---|
| **0 – 6 soat** | Yangi Jasad (Fresh Corpse) | Rangi o'chgan, qon qotgan | $-15$ Morale | Miasma yo'q. Hashoratlar uchib kela boshlaydi. |
| **6 – 24 soat** | Shishish va Sassiq (Putrefaction) | Tana ko'karadi, qorin shishadi, yashil dog'lar | $-30$ Morale | $+10 \text{ Filth/soat}$, pashshalar to'dasi, ko'ngil aynishi (`Nausea`). |
| **24 – 48 soat**| Faol Chirish (Active Liquefaction) | Chiriyotgan to'qimalar, suyaklar ochiladi | $-45$ Morale | $+25 \text{ Filth/soat}$, 15m radiusda qora o'lat xavfi $+35\%$. |
| **48+ soat** | Zaharli Bio-Xavf (Contaminated Skeleton)| Qora chirindi, skelet suyaklari | $-60$ Morale | Yerosti suvlarini zaharlaydi, 25m quduqlar vabo o'chog'iga aylanadi. |

---

### 93.2. Yirtqichlar va Qarg'alar Bosqini (Scavenger Dynamics)

- **Qarg'alar To'dasi (Crows):**
  - Jasad 6 soatdan ortiq yotib qolsa, osmonda 5–12 ta qarg'a aylanib ucha boshlaydi.
  - Bu o'yinchi (Hukmdor) uchun vizual kompas signali bo'lib xizmat qiladi: osmonda aylanayotgan qarg'alar ko'ringan joyda ko'milmagan murda borligi ma'lum bo'ladi.
- **Yirtqich Bo'rilar Hujumi (Wolf Infiltration):**
  - Agar shahar devorlari tashqarisida yoki ochiq dalalarda 24 soatdan ortiq jasadlar qolib ketsa, chirigan go'sht hidi o'rmondagi yovvoyi bo'rilar to'dasini jalb qiladi.
  - Bo'rilar jasadlarni yeb to'ygach, kechalari shahar ichidagi tirik fuqarolarga va chorva mollariga hujum qila boshlaydi.

---

### 93.3. Fuqarolar Ruhiyati Kollapsi va Isyon Xavfi (Religious Despair & Riots)

- **Ajdodlar Ruhiga Hurmatsizlik:**
  Agar ko'chada 3 tadan ortiq jasad ko'milmay yotgan bo'lsa, fuqarolar o'z hukmdorini "La'natlangan zolim" deb hisoblaydi.
  - Cherkovdagi rohiblar shahar boshqaruviga qarshi va'z o'qiydi (Xalq dindorligi $-40\%$).
  - Fuqarolar "Bizni itlardek ko'chada qoldirishmoqchi" deb vahimaga tushadi va shahardan ommaviy qochish (Emigration) sur'ati 3 barobarga oshadi.

---

# 94. G‘ASSOL VA DAFN LOGISTIKASI (GRAVEDIGGER & MORTUARY LOGISTICS)

Shahar sanitariyasini va fuqarolar xotirjamligini saqlash uchun o'liklarni o'z vaqtida yig'ish va muqaddas dafn marosimlarini o'tkazuvchi maxsus kasb — **G'assol (Gravedigger & Undertaker)** faoliyati yo'lga qo'yiladi.

### 94.1. G'assolxona va Murdalar Logistikasi Infratuzilmasi

1. **G'assolxona (Undertaker's Shed / Mortuary):**
   - Shahar chetida, qabriston darvozasi yonida quriladigan bino.
   - Ichida tosh murda yuvish stoli, kafan va tobutlar zaxirasi, ohak bochkalari va belkuraklar saqlanadi.
2. **Murda Tashish Aravasi (Morgue Cart):**
   - 2 g'ildirakli, usti qora zig'ir brezent bilan yopilgan maxsus arava.
   - Bitta reysda 4 tagacha jasadni sig'dira oladi. Ustining yopiqligi jasad tashilayotganda ko'chadagi fuqarolarga vizual travma yetkazishning oldini oladi.
3. **G'assol Dispetcherlik Algoritmi:**
   - Shaharda o'lim sodir bo'lishi bilan tizim darhol Priority 600 (`Sanitation & Health`) toifasidagi `COLLECT_CORPSE` vazifasini ochadi.
   - G'assol o'z aravasini yetaklab jasad yotgan nuqtaga boradi, jasadni aravaga ortadi va qabristonga olib keladi.

---

### 94.2. Tobut Turlari va Hunarmandchilik Retseptlari (Coffin Crafting Table)

| Tobut / Kafan Nomi | Kerakli Materiallar | Ishlab Chiqarish Stoli | Miasmani To'sish | Fuqaro Oilasiga Ruhiy Taskin |
|---|---|---|---|---|
| **Oddiy Kafan (Linen Shroud)** | 2 Zig'ir Mato | To'quvchi / G'assolxona | $60\%$ (Vaqtinchalik) | $+5$ Morale |
| **Yog'och Tobut (Wooden Coffin)** | 4 Qoraqarag'ay Taxta + 2 Temir Mix | Duradgorxona | $100\%$ (To'liq to'sadi) | $+15$ Morale |
| **Tosh Sarkofag (Stone Sarcophagus)**| 6 Tarashlangan Tosh + 2 Marmar | Tosh Yo'nuvchi | $100\%$ (Abadiy saqlaydi) | $+35$ Morale (Qirollik ehtiromi)|

---

### 94.3. Dafn Marosimi va Qabrni Muqaddaslash (Burial Ritual & Sanctification)

To'liq dafn marosimi quyidagi 4 bosqichda amalga oshiriladi:
1. **Qabr Qazish:** G'assol shahar qabristoni zonasida $2\times1\times2$ o'lchamdagi voxel chuqurlik qaziydi (Mehnat vaqti: 45 soniya).
2. **Tobutni Tushirish:** Tobut qabr tubiga tushiriladi va ustiga tuproq voxellari qayta yopiladi.
3. **Qabrtosh O'rnatish (Headstone):** Yog'och xoch yoki o'ymakor tosh lavha o'rnatiladi. Toshda marhumning ismi, kasbi va yashagan yillari muhrlanadi.
4. **Ruhoniy Duosi va Muqaddaslash (`SanctifyGrave` Ritual):**
   - Cherkov ruhoniysi (Priest) qabr boshiga kelib muqaddas suv sepadi va duo o'qiydi.
   - **Qonli Oy Himoyasi (Anti-Necromancy Protection):**
     - Ruhoniy tomonidan muqaddaslangan qabrlardan hech qachon sharpalar, arvohlar yoki zombi skeletlari chiqmaydi.
     - Agar shahar chetidagi o'liklar shoshilinchda umumiy chuqurga (Mass Grave) ruhoniy duosisiz tashlansa, Qonli Oy (Blood Moon) reydi kechasida bu jasadlar yerdan tirilib, dushmanona o'liklar armiyasi (`Risen Skeletons`) sifatida shahar ichidan hujum boshlaydi!

---

# 95. MUQADDAS QABRISTON VA EPITAFLAR

Har bir qabr toshida fuqaroning ismi, kasbi, umr yillari va qilgan buyuk xizmatlari bitiladi.

---

# 96. MEROSXO‘RLIK (INHERITANCE)

Vafot etgan fuqaroning shaxsiy jamg'armasi va qurollari uning farzandlari yoki oilasiga o'tadi.

---

# 97. AJDODLAR MEROSI VA XOTIRA (ANCESTRAL LEGACY)

Obod tutilgan qabriston butun shaharga "Ajdodlar Duosi" xotirjamligini beradi. Qirollik o'z qahramonlarini unutmaydi.

---

# 98. DUNYONI TADQIQ ETISH (EXPLORATION)

Katta Dunyo Xaritasi tuman (Fog of War) bilan qoplangan bo'ladi. Hukmdor yoki otliq josuslar yangi hududlarni asta-sekin kashf qiladi.

---

# 99. DUNYO XARITASI (WORLD MAP)

Relyef, qishloqlar, qasirlar, yo'llar, ma'lum konlar, qo'shni fraktsiyalar chegaralari va xavfli hududlar ko'rsatiladi.

---

# 100. TOPSHIRIQLAR TIZIMI (QUESTS)

Asosiy qirollik topshiriqlari, shahar rivoji vazifalari, fuqarolarning shaxsiy iltimoslari, diplomatik topshiriqlar va boss ovlari.

---

# 101. DINAMIK VOQEALAR (DYNAMIC EVENTS)

Qochoqlar to'lqini, kutilmagan savdogarlar, qaroqchilar pistirmasi, shaxtada suv toshishi, saroyga oliyjanob mehmon kelishi.

---

# 102. HUKMDOR DAFTARI (ROYAL LEDGER — `TAB` TIZIMI)

Barcha davlat boshqaruvi: Aholi, Kasblar, Uylar, Oziq-ovqat, Ishlab chiqarish, Tashqi savdo, Armiya, Salomatlik, Qonunlar, Soliqlar, Chegaralar, Madaniyat.

---

# 103. SHOSHILINCH OGOHLANTIRISHLAR (ALERT SYSTEM)

`Info → Warning → Critical`.
Oziq-ovqat tanqisligi, Och fuqaro, Kasallik tarqalishi, Dushman bosqini, Yong'in, Kon gazining oshishi.

---

# 104. FOYDALANUVCHI INTERFEYSI (MINIMAL IMMERSIVE HUD)

Salomatlik, Chidamlilik, Tana harorati, Hotbar (8 slot), O'zaro ta'sir ko'rsatuvchi markerlar. Ekran ortiqcha raqamlar bilan to'ldirilmaydi.

---

# 105. BIRINCHI KUN VA O‘RGATISH (ONBOARDING)

1-qadam: Sovuqda omon qolish.  
2-qadam: Birinchi boshpana qurish.  
3-qadam: Xaloskor Gulxan yoqish.  
4-qadam: Birinchi sarson qochqinni qabul qilish.  
5-qadam: Unga ish berish.  
6-qadam: Birinchi qishloq tamalini qo'yish.

---

# 106. QIYINLIK DARAJASI (DIFFICULTY PRESETS)

- Hikoya (Story)
- Standart Feodal (Normal)
- Og'ir Kurash (Hard)
- Qora Qismat (Feudal Nightmare)
Maxsus sozlamalar: Reyd kuchi, vabo tarqalishi, qishki sovuq darajasi, resurslar mo'lligi.

---

# 107. QULAYLIK SOZLAMALARI (ACCESSIBILITY)

Tugmalarni erkin sozlash, UI masshtabi, Ko'rish burchagi (FOV), Subtitrlar, Kamerani tebranishini o'chirish, Rang ajratish rejimlari.

---

# 108. AUDIO VA MUSIQIY MUHIT

Biomlar shovqini, ob-havo tovushlari, ish shovqinlari (bolg'a urilishi, daraxt yiqilishi), jang musiqalari, bayram ohanglari, taverna liralari.

---

# 109. SAN’AT VA GRAFIKA YO‘NALISHI (ART DIRECTION)

Stylized Realistic Voxel Medieval. Blokli dunyo go'zalligi realistik yorug'lik, volumetric tuman, atmosferali ob-havo va silliq animatsiyalar bilan uyg'unlashadi.

---

# 110. KUN VA TUN SIKLI (DAY/NIGHT CYCLE)

Kunduzi faol mehnat. Tunda ko'rish masofasi qisqaradi, harorat tushadi, yirtqichlar va maxluqlar faollashadi.

---

# 111. O‘YINNI SAQLASH TIZIMI (SAVE SYSTEM)

Manual Save, Quick Save (`F5`), Kunlik tonggi avtomatik saqlash (Autosave).

---

# 112. SAVE FAYLI TARKIBI VA OPTIMALLASHTIRISH

Faqat o'zgargan voxel bloklari delta-formatida saqlanadi. Fuqarolar, bino chizmalari, iqtisodiy holat va qonunlar siqilgan JSON/Binary ko'rinishida yoziladi.

---

# 113. SAVE VERSIYALARI VA MIGRATSIYA

Har bir save fayl o'z versiyasiga ega bo'lib, o'yin yangilanishlari chiqqanda dunyo ma'lumotlarini buzmasdan yangi versiyaga o'tkazadi.

---

# 114. GODOT 4 DASTURIY ARXITEKTURASI

Voxel Lord: Feudal Realm o'yini Godot 4.3 Forward Plus renderlash dvijogiga asoslangan bo'lib, uning arxitekturasi modullilik, yuqori unumdorlik va ko'p oqimli hisob-kitoblar (Multithreaded computing) tamoyillariga tayanadi. O'yin tizimlari o'zaro zaif bog'langan (loosely coupled) holda EventBus (Signal avtomagistrali) va Autoload Singletonlari orqali boshqariladi.

### 114.1. Dasturiy Sahna Daraxti (Node Hierarchy & Scene Tree)

Dvigatel sahnasi quyidagi qat'iy iyerarxiya bo'yicha tuzilgan:

```
Main (Node3D)
├── Environment (WorldEnvironment, DirectionalLight3D)
├── VoxelWorld (Node3D)
│   ├── ChunkContainer (Node3D) — barcha faol 32x32x32 VoxelChunk instansiyalari
│   └── NavigationRegionContainer (Node3D) — dinamik o'zgaruvchi NavigationRegion3D qismlari
├── Entities (Node3D)
│   ├── Players (Node3D) — mahalliy va tarmoqdagi o'yinchilar
│   ├── Citizens (Node3D) — fuqarolar (LOD 0 va LOD 1 guruhlari)
│   └── Enemies (Node3D) — qaroqchilar va qamal qo'shinlari
├── Systems (Node)
│   ├── GasSimulationSystem (Node)
│   ├── GreenhouseThermalSystem (Node)
│   └── DiplomacyManager (Node)
├── NetworkSync (Node) — Steam P2P host-authoritative paket marshrutizatori
└── UILayer (CanvasLayer)
    ├── HUD (Control) — tezkor resurslar va asboblar paneli
    ├── RoyalLedger (Control) — shahar hisob-kitoblari va soliq daftari
    └── WorldMap (Control) — mintaqaviy xarita va diplomatiya interfeysi
```

### 114.2. Asosiy Autoload Singletonlar (Global Service Registry)

O'yinda 7 ta asosiy tizimli Autoload skriptlari global xizmat sifatida ro'yxatdan o'tgan:

1. **`GameManager` (`res://scripts/core/game_manager.gd`):** O'yin sessiyasini boshqarish, pauza, simulyatsiya tezligi ($1\times, 2\times, 5\times$), o'yin rejimi (Yagona qirollik yoki Feodal tarqoqlik) va saqlash/yuklash jarayonlarini nazorat qiladi.
2. **`ChunkManager` (`res://scripts/core/chunk_manager.gd`):** Dunyoning fazoviy venzel matritsasini ($32\times 32\times 32$ blokli chunklar) boshqaradi. O'yinchi atrofidagi $9\times 7\times 9$ faol mintaqani xotirada saqlaydi va fon oqimlarida yangi chunklarni yuklaydi.
3. **`GeologyManager` (`res://scripts/core/geology_manager.gd`):** Chuqur qatlamlarning mineral tarkibini, Gauss ehtimollik zichligi bo'yicha 24 ta mineralning paydo bo'lishini va shovqin generatsiyasini boshqaradi.
4. **`MinePhysicsServer` (`res://scripts/core/mine_physics_server.gd`):** Shaxta shiftining tayanch barqarorlik indeksini ($S_c$) hisoblaydi, ustunlar radiusi va xavfli qulash (cave-in) kaskadlarini simulyatsiya qiladi.
5. **`GreenhouseThermalSystem` (`res://scripts/core/greenhouse_thermal_system.gd`):** Issiqxonalarning termodinamik muvozanatini, geotermal bug' quvurlari issiqligini va Tundrada ekinlarni sovuqdan himoyalashni hisoblaydi.
6. **`NetworkPacketManager` (`res://scripts/network/network_packet_manager.gd`):** Steam P2P orqali uzatiluvchi barcha binar tarmoq paketlarini (`ClientInputPacket`, `VoxelDeltaModify`, `EntitySnapshot`, `CaveInEventPacket`) xom baytlarga o'rash va ochishni amalga oshiradi.
7. **`DiplomacyManager` (`res://scripts/diplomacy/diplomacy_manager.gd`):** 4 ta feodal fraktsiyalar bilan o'zaro munosabatlar, mavsumiy o'lpon hisob-kitoblari, karvonlar logistikasi va Casus Belli holatlarini boshqaradi.

---

# 115. SCRIPT VAZIFALARI (GDSCRIPT & C#)

Tizimda tillar vazifasiga ko'ra aniq taqsimlangan:
- **GDScript:** Yuqori darajadagi o'yin mantig'i, fuqarolar AI FSM holatlari, kvestlar, dialoglar, diplomatiya, iqtisodiy resurslar boshqaruvi va UI voqealari uchun qo'llaniladi.
- **C# / GDExtension:** Yuqori unumdorlik va chuqur xotira manipulyatsiyasi talab qiluvchi hisob-kitoblar — Greedy Voxel Meshing, fon oqimlarida 3D shovqin (FastNoiseLite) matritsalarini to'ldirish va yuzlab fuqarolarning binar yo'l topish so'rovlari uchun mo'ljallangan.

Quyida asosiy o'yin tizimlarining to'liq va ishlab chiqarishga tayyor GDScript implementatsiyalari keltirilgan:

### 115.1. Geologiya Menejeri (`res://scripts/core/geology_manager.gd`)

```gdscript
class_name GeologyManager
extends Node

## 3D chuqur qatlamlar geologiyasi va 24 ta mineralning fazoviy taqsimotini boshqaruvchi tizim.

@export var world_seed: int = 1337
var noise_strata: FastNoiseLite
var noise_veins: FastNoiseLite

var mineral_catalog: Dictionary = {}

func _ready() -> void:
	noise_strata = FastNoiseLite.new()
	noise_strata.seed = world_seed
	noise_strata.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	noise_strata.frequency = 0.015

	noise_veins = FastNoiseLite.new()
	noise_veins.seed = world_seed + 101
	noise_veins.noise_type = FastNoiseLite.TYPE_CELLULAR
	noise_veins.frequency = 0.04

	_register_all_minerals()

func _register_all_minerals() -> void:
	# 24 ta mineralning qatlam chegaralari, cho'qqi chuqurligi, sigma tarqalishi va bazaviy qiymati
	_add_mineral(1, "Topsoil", 0, -15, -2, 5.0, 1.00, 1, 0.05)
	_add_mineral(2, "Clay", 0, -35, -10, 8.0, 0.45, 2, 0.20)
	_add_mineral(3, "Peat", 0, -25, -8, 6.0, 0.35, 2, 0.30)
	_add_mineral(4, "Sandstone", -5, -60, -25, 15.0, 0.60, 3, 0.40)
	_add_mineral(5, "Limestone", -15, -90, -45, 20.0, 0.50, 4, 0.60)
	_add_mineral(6, "Halite", -20, -120, -60, 25.0, 0.30, 3, 2.50)
	_add_mineral(7, "Coal", -15, -180, -75, 35.0, 0.55, 4, 1.00)
	_add_mineral(8, "Copper Ore", -10, -110, -50, 22.0, 0.40, 5, 1.80)
	_add_mineral(9, "Tin Ore", -25, -130, -70, 24.0, 0.32, 5, 2.20)
	_add_mineral(10, "Sulfur", -40, -220, -120, 30.0, 0.25, 4, 3.00)
	_add_mineral(11, "Saltpeter", -30, -160, -90, 28.0, 0.22, 3, 3.50)
	_add_mineral(12, "Iron Ore", -45, -240, -130, 40.0, 0.45, 7, 4.00)
	_add_mineral(13, "Lead", -60, -210, -140, 35.0, 0.28, 6, 3.20)
	_add_mineral(14, "Zinc", -70, -230, -150, 35.0, 0.25, 6, 3.80)
	_add_mineral(15, "Nickel", -90, -260, -175, 38.0, 0.20, 8, 5.50)
	_add_mineral(16, "Marble", -50, -280, -160, 50.0, 0.30, 8, 6.00)
	_add_mineral(17, "Granite", -80, -350, -220, 65.0, 0.65, 10, 2.00)
	_add_mineral(18, "Silver Ore", -110, -280, -195, 35.0, 0.18, 8, 15.00)
	_add_mineral(19, "Gold Ore", -160, -340, -250, 40.0, 0.12, 10, 100.00)
	_add_mineral(20, "Platinum Ore", -220, -350, -290, 30.0, 0.06, 12, 220.00)
	_add_mineral(21, "Basalt", -250, -350, -320, 45.0, 0.50, 12, 3.00)
	_add_mineral(22, "Emerald", -120, -260, -190, 25.0, 0.04, 14, 180.00)
	_add_mineral(23, "Ruby", -180, -320, -260, 30.0, 0.03, 16, 280.00)
	_add_mineral(24, "Diamond", -280, -350, -330, 22.0, 0.015, 20, 500.00)

func _add_mineral(id: int, m_name: String, y_max: int, y_min: int, y_peak: int, sigma: float, prob_peak: float, hardness: int, val: float) -> void:
	mineral_catalog[id] = {
		"name": m_name, "y_max": y_max, "y_min": y_min,
		"y_peak": y_peak, "sigma": sigma, "prob_peak": prob_peak,
		"hardness": hardness, "base_value": val
	}

func sample_voxel_type(global_x: int, global_y: int, global_z: int) -> int:
	if global_y > 0:
		return 0 # Havo yoki yer usti qatlami
	if global_y >= -15:
		return 1 # Unumdor tuproq qatlami
	if global_y < -350:
		return 21 # Tub basalt / Bedrock

	var base_block: int = 17 # Granit matritsasi

	for m_id in mineral_catalog.keys():
		var data = mineral_catalog[m_id]
		if global_y <= data["y_max"] and global_y >= data["y_min"]:
			var depth_factor: float = exp(-pow(float(global_y - data["y_peak"]), 2.0) / (2.0 * pow(data["sigma"], 2.0)))
			var current_prob: float = data["prob_peak"] * depth_factor
			var n_val: float = (noise_veins.get_noise_3d(global_x, global_y, global_z) + 1.0) * 0.5
			if n_val < current_prob:
				return m_id

	return base_block
```

### 115.2. Shaxta Fizikasi Serveri (`res://scripts/core/mine_physics_server.gd`)

```gdscript
class_name MinePhysicsServer
extends Node

## Shaxta shiftining mustahkamligi, tayanch nurlari va o'pirilish fizikasini hisoblovchi avtoritar server.

signal cave_in_triggered(center_pos: Vector3i, radius: float)

const SUPPORT_RADII: Dictionary = {
	"wood_soft": 3.0,
	"wood_hard": 5.0,
	"stone_pillar": 7.5,
	"steel_arch": 11.0
}

const ROCK_TENSILE_K: Dictionary = {
	1: 0.20,  # Tuproq / Loy
	4: 0.55,  # Qumtosh
	5: 0.55,  # Ohaktosh
	16: 0.90, # Marmar
	17: 0.90, # Granit
	21: 1.00  # Basalt
}

var active_supports: Dictionary = {}

func register_support_beam(pos: Vector3i, beam_type: String) -> void:
	if SUPPORT_RADII.has(beam_type):
		active_supports[pos] = {
			"type": beam_type,
			"radius": SUPPORT_RADII[beam_type]
		}

func remove_support_beam(pos: Vector3i) -> void:
	active_supports.erase(pos)

func evaluate_ceiling_stability(pos: Vector3i, rock_type: int, unsupported_span: float) -> float:
	var k_rock: float = ROCK_TENSILE_K.get(rock_type, 0.50)
	var support_sum: float = 0.0

	for sup_pos in active_supports.keys():
		var sup_data = active_supports[sup_pos]
		var dist_sq: float = float(pos.distance_squared_to(sup_pos))
		var r: float = sup_data["radius"]
		if dist_sq <= (r * r):
			support_sum += (r * r) / (dist_sq + 0.1)

	var effective_support: float = max(1.0, support_sum)
	var depth: float = abs(float(pos.y))
	var denominator: float = 1.0 + (0.08 * pow(unsupported_span * 0.5, 2.0) * (1.0 + 0.35 * (depth / 100.0)))

	var stability_index: float = (k_rock * effective_support) / denominator
	return stability_index

func process_mined_voxel(pos: Vector3i, rock_type: int, unsupported_span: float) -> void:
	var ceiling_pos: Vector3i = pos + Vector3i(0, 1, 0)
	var stability: float = evaluate_ceiling_stability(ceiling_pos, rock_type, unsupported_span)
	if stability < 0.75:
		trigger_cave_in(ceiling_pos, 4.0)

func trigger_cave_in(center: Vector3i, radius: float) -> void:
	emit_signal("cave_in_triggered", center, radius)
```

### 115.3. Issiqxona Termodinamika Tizimi (`res://scripts/core/greenhouse_thermal_system.gd`)

```gdscript
class_name GreenhouseThermalSystem
extends Node

## Tundra biomidagi issiqxonalarning termodinamik muvozanati va ekinlar hosildorligini hisoblovchi tizim.

@export var ambient_temperature: float = -25.0
@export var solar_irradiance: float = 350.0

func calculate_greenhouse_temp(volume_m3: float, glass_area: float, insulated_wall_area: float, geothermal_vent_kw: float) -> float:
	var u_glass: float = 1.0 / 0.18 # 5.55 W/m2*K
	var u_wall: float = 1.0 / 1.60  # 0.625 W/m2*K

	var total_conductance: float = (glass_area * u_glass) + (insulated_wall_area * u_wall)
	var q_solar_watts: float = glass_area * solar_irradiance * 0.75
	var q_geo_watts: float = geothermal_vent_kw * 1000.0

	var total_heat_in: float = q_solar_watts + q_geo_watts
	var delta_t: float = total_heat_in / max(1.0, total_conductance)
	return ambient_temperature + delta_t

func get_crop_yield_multiplier(internal_temp: float) -> float:
	if internal_temp < 0.0:
		return 0.0 # Muzlab nobud bo'ldi
	elif internal_temp < 10.0:
		return 0.25 # Rivojlanish sust
	elif internal_temp < 18.0:
		return 0.65 # O'rtacha o'sish
	elif internal_temp <= 28.0:
		return 1.00 # Optimal hosil
	else:
		return 0.30 # Issiqdan so'ligan
```

### 115.4. Binar Tarmoq Paketlari Menejeri (`res://scripts/network/network_packet_manager.gd`)

```gdscript
class_name NetworkPacketManager
extends Node

## Steam P2P ko'p o'yinchili rejim uchun binar paketlarni ixcham qadoqlovchi va yechuvchi tizim.

enum PacketType {
	CLIENT_INPUT = 1,
	VOXEL_DELTA_MODIFY = 2,
	ENTITY_SNAPSHOT = 3,
	CAVE_IN_EVENT = 4,
	GAS_UPDATE = 5,
	CHUNK_STREAM = 6
}

static func pack_voxel_modify(chunk_pos: Vector3i, local_idx: int, block_type: int, meta: int, actor_id: int) -> PackedByteArray:
	var buf = StreamPeerBuffer.new()
	buf.big_endian = false
	buf.put_u8(PacketType.VOXEL_DELTA_MODIFY)
	buf.put_16(chunk_pos.x)
	buf.put_16(chunk_pos.y)
	buf.put_16(chunk_pos.z)
	buf.put_u16(local_idx)
	buf.put_u8(block_type)
	buf.put_u8(meta)
	buf.put_u8(actor_id)
	return buf.data_array

static func unpack_voxel_modify(data: PackedByteArray) -> Dictionary:
	var buf = StreamPeerBuffer.new()
	buf.big_endian = false
	buf.data_array = data
	var p_type = buf.get_u8()
	if p_type != PacketType.VOXEL_DELTA_MODIFY:
		return {}

	var chunk_pos = Vector3i(buf.get_16(), buf.get_16(), buf.get_16())
	var local_idx = buf.get_u16()
	var block_type = buf.get_u8()
	var meta = buf.get_u8()
	var actor = buf.get_u8()

	return {
		"chunk_pos": chunk_pos,
		"local_idx": local_idx,
		"block_type": block_type,
		"meta": meta,
		"actor_id": actor
	}
```

### 115.5. Diplomatiya Menejeri (`res://scripts/diplomacy/diplomacy_manager.gd`)

```gdscript
class_name DiplomacyManager
extends Node

## Fraktsiyalararo munosabatlar, o'lpon talablari va karvon sayohatlarini boshqaruvchi tizim.

signal tribute_demanded(faction_id: int, amount: int)
signal war_declared(faction_id: int, reason: String)

var factions: Dictionary = {
	1: {"name": "Coastal Merchants", "relation": 15, "power": 120.0, "aggression": 10},
	2: {"name": "Northern Warlords", "relation": -25, "power": 250.0, "aggression": 35},
	3: {"name": "Holy Sun Order", "relation": 5, "power": 180.0, "aggression": 15},
	4: {"name": "Steppe Horse Clans", "relation": 0, "power": 150.0, "aggression": 20}
}

func calculate_tribute(faction_id: int, player_power: float, player_treasury: float, player_pop: int, dist: float) -> int:
	var f_data = factions.get(faction_id)
	if not f_data:
		return 0

	var k_base: float = 50.0
	var d_max: float = 5000.0
	var power_ratio: float = pow(f_data["power"] / (player_power + 1.0), 1.35)
	var wealth_factor: float = pow(player_treasury, 0.55) + (0.1 * float(player_pop))
	var dist_factor: float = max(0.1, 1.0 - (dist / d_max))

	var raw_tribute: float = k_base * power_ratio * wealth_factor * dist_factor
	return int(round(raw_tribute))

func process_tribute_response(faction_id: int, accepted: bool) -> void:
	var f = factions.get(faction_id)
	if not f:
		return

	if accepted:
		f["relation"] = mini(100, f["relation"] + 12)
		f["aggression"] = 0
	else:
		f["aggression"] += 45
		f["relation"] = maxi(-100, f["relation"] - 35)
		if f["aggression"] >= 100:
			emit_signal("war_declared", faction_id, "Tribute Default")
```

---

# 116. VOXEL RENDERLASH SAMARADORLIGI

To'liq o'zgaruvchan 3D venzel dunyosida har bir blokni alohida kub sifatida chizish (naive cubic rendering) bitta $32\times 32\times 32$ chunk uchun 49,152 ta uchburchak hosil qilib, GPU renderlash konveyerini falajlaydi. Voxel Lord renderlashda ilg'or **Greedy Voxel Meshing** algoritmidan foydalanadi.

### 116.1. Greedy Meshing Algoritmi Ishlash Bosqichlari

1. **Yo'nalishli Ko'rinish Filtratsiyasi (Face Culling):** Har bir venzelning 6 ta tomoni (+X, -X, +Y, -Y, +Z, -Z) tekshiriladi. Faqat yonidagi qo'shnisi havo (`AIR`) yoki shaffof bo'lgan yuzalargina renderlash ro'yxatiga kiritiladi.
2. **2D Kesim Niqobini Shakllantirish (Slice Sweeping):** Chunkning har bir o'qi bo'ylab 32 ta qatlam kesimi hosil qilinadi. Har bir kesimda bir xil blok turiga va bitta teksturaga ega bo'lgan qo'shni yuzalar $32\times 32$ massivda binar belgilanadi.
3. **To'g'ri To'rtburchaklarni Birlashtirish (Greedy Merging):**
   - Algoritm birinchi band qilinmagan yuzani topadi va gorizontal o'q bo'yicha bir xil bloklar tugaguncha chiziq tortadi (kenglik $W$).
   - Keyin ushbu kenglikdagi chiziqni vertikal o'q bo'yicha pastga qarab, to'liq bir xil blokli qatorlar tugaguncha kengaytiradi (balandlik $H$).
   - Natijada $W \times H$ o'lchamli bitta yagona katta kvad (2 ta uchburchak) hosil bo'ladi.
   - Birlashtirilgan barcha venzellar "ishlangan" deb belgilanadi va jarayon davom etadi.
4. **Natijaviy Samaradorlik:** Ushbu algoritm poligonlar sonini $75\%$ dan $85\%$ gacha kamaytiradi (o'rtacha zich chunkda poligonlar soni 49,152 tadan 4,200 tagacha qisqaradi).

### 116.2. Vertex Packing va SurfaceTool Optimallashtirish

- **Uchlar Ma'lumotlarini Siqish (Vertex Packing):** Venzel koordinatalari $0$ dan $32$ gacha butun son bo'lganligi sababli, 32-bitli float o'rniga 8-bitli unsigned butun sonlar (`uint8`) ishlatiladi. Normal vektorlar va Tekstura ID ko'rsatkichi 16-bitli binar formatga joylanadi.
- **Yagona Draw Call:** Har bir chunk uchun barcha kvadlar Godotning `SurfaceTool` va `ArrayMesh` vositalari orqali yagona geometriya buferiga birlashtiriladi. Bitta chunk bitta GPU Draw Call orqali chiziladi.
- **WorkerThreadPool orqali Ko'p Oqimlilik:** Shovqin namunalari va mesh generatsiyasi Godot 4 ning `WorkerThreadPool` tizimi orqali fonga o'tkaziladi. Asosiy render oqimi (Main Thread) faqat tayyor bo'lgan mesh resursini GPU VisualServer ga topshiradi, bu esa kadr tushib ketishi (frame stutter) ning oldini oladi.
- **Teksturalar Massivi (Texture2DArray):** Barcha 24 ta mineral, tuproq, daraxt va qurilish teksturalari bitta `Texture2DArray` (qatlamli 2D tekstura) resursida saqlanadi. Bu shaderlarda tekstura almashish (texture bind switching) xarajatlarini butunlay yo'q qiladi.

---

# 117. O‘ZGARUVCHAN DUNYODA YO‘L TOPISH (NAVIGATION)

Statik dunyolarda qo'llaniladigan bir butun monolit NavMesh o'zgaruvchan venzel dunyosiga to'g'ri kelmaydi — har bir blok qazilganda butun dunyo navmeshini qayta hisoblash o'yinni qotirib qo'yadi. Voxel Lord dinamik, modulli va asinxron yo'l topish tizimini amalga oshiradi.

### 117.1. Bo'lingan Mintaqaviy NavMesh (Chunk-Partitioned Navigation)

- Dunyo $32\times 32\times 32$ o'lchamli har bir chunk bo'yicha alohida `NavigationRegion3D` nodlariga ajratilgan.
- Qo'shni chunklarning navmesh qirralari Godot 4 `NavigationServer3D` tomonidan chegarada avtomatik birlashtiriladi (Edge Connection Margin $= 0.1\text{m}$).
- Fuqarolar bir chunkdan ikkinchisiga hech qanday to'siqsiz, silliq harakatlanadi.

### 117.2. Asinxron Qayta Hisoblash (Asynchronous Dirty Re-baking)

- O'yinchi yoki fuqaro biror venzelni qaziganda yoki yangi blok qo'yganda:
  1. Faqat shu venzel joylashgan chunk (va agar blok chegarada bo'lsa, unga yondosh qo'shni chunk) "ifloslangan" (`dirty`) deb belgilanadi.
  2. Qayta hisoblash so'rovi fonga `WorkerThreadPool` ga yuboriladi.
  3. Fon oqimi `NavigationServer3D.region_bake_navigation_mesh()` funktsiyasini asinxron bajaradi.
  4. Yangi navmesh tayyor bo'lgach, navigatsiya serveriga almashtiriladi.
  5. Navigatsiya qayta qurilayotgan paytda fuqarolar eski navmesh keshidan foydalanib harakatni davom ettiradi (Double-buffered Navigation).

### 117.3. Fuqarolar Harakati va To'siqlarni Aylanib O'tish

- Fuqarolar `NavigationAgent3D` n ګرځi orqali harakatlanadi.
- **RVO2 Dinamik To'qnashuv Algoritmi:** Tor yo'llarda va ko'priklarda ikki fuqaro to'qnashib qolmasligi uchun RVO2 (Reciprocal Velocity Obstacles) orqali bir-birini avtomatik chetlab o'tadi.
- **Pog'onali Ko'tarilish (Step Traversal):** Fuqaro $1.0\text{ metr}$ balandlikdagi bitta venzel pog'onasiga sakrashsiz, tabiiy qadam bilan ko'tariladi. Tik devorlar uchun maxsus narvon (`Ladder`) va zinalar (`Stairs`) qo'llaniladi.
- **Tiqilib Qolishga Qarshi Nazoratchi (Anti-stuck Watchdog):** Agar fuqaro $3.0\text{ soniya}$ davomida mo'ljallangan nuqtaga qarab siljimasa, uning yo'li bekor qilinadi, to'siq atrofida yangi A* marshruti hisoblanadi.

---

# 118. AHOLI SUN’IY INTELLEKTI LOD TIZIMI (AI LOD)

Shaharda 200 dan ortiq fuqaro bir paytda yashaganda, ularning barchasini to'liq 3D skelet animatsiyasi va fizikasi bilan yurgizish CPU va GPU resurslarini tugatadi. Shu sababli 3 bosqichli sun'iy intellekt LOD tizimi joriy etilgan:

### 118.1. AI LOD Bosqichlari Matritsasi

| Parametr | LOD 0 (Yaqin Masofa) | LOD 1 (O'rta Masofa) | LOD 2 (Uzoq / Ko'rinmas Masofa) |
|---|---|---|---|
| **Kamera Masofasi** | $0\text{ m} \to 40\text{ m}$ | $40\text{ m} \to 120\text{ m}$ | $> 120\text{ m}$ yoki ko'rinishdan tashqarida |
| **Vizual Ko'rinish** | To'liq 3D model, kiyim va qurol meshlar | Vertex Animation Texture (VAT) shader | Vizual model sahnadan o'chiriladi ($0$ poligon) |
| **Animatsiya** | Skeletli suyak animatsiyasi, IK oyoq qadami | Soddalashtirilgan kadrma-kadr shader | Animatsiya hisoblanmaydi |
| **Fizika va Yo'l Topish**| To'liq CharacterBody3D, RVO2 avoidance | NavMesh agenti, harakat $10\text{ Hz}$ yangilanish | Matematik koordinata interpolyatsiyasi |
| **Ehtiyojlar Ticki** | Har soniyada real vaqt tekshiruvi ($60\text{ Hz}$) | Har $2.0$ soniyada tekshiruv ($0.5\text{ Hz}$) | Har $10.0$ soniyada statistik tekshiruv ($0.1\text{ Hz}$) |
| **Hisoblash yuki** | $100\%$ (To'liq individual simulyatsiya) | $15\%$ (Soddalashtirilgan) | $1\%$ (Sof statistik hisob-kitob) |

### 118.2. LOD 2 Statistik Simulyatsiya Mexanikasi

Uzoq dalalarda ishlayotgan dehqonlar yoki chuqur shaxtalardagi konchilar kamera ulardan uzoqlashganda `StatisticalCitizenSimulator` ga o'tkaziladi:
- Fuqaroning 3D tuguni (`Node3D`) xotirada qoladi, lekin sahnadan (`Tree`) vaqtinchalik chiqariladi.
- Uning ishi formulalar bilan hisoblanadi:
  $$P_{work}(t + \Delta t) = P_{work}(t) + \left(Skill_{craft} \cdot Efficiency_{station} \cdot \Delta t\right)$$
  $$Hunger(t + \Delta t) = Hunger(t) - \left(k_{hunger} \cdot \Delta t\right)$$
- Fuqaro o'z smenasini tugatgach, matematik koordinatasi uyiga ko'chiriladi.
- O'yinchi uning yoniga kelgan zahoti fuqaroning barcha holatlari (ochlik, charchoq, sumkasidagi narsalar) to'liq saqlangan holda darhol LOD 0 yoki LOD 1 holatida sahnada paydo bo'ladi (Seamless Materialization).

---

# 119. UNUMDORLIK NISHONLARI (PERFORMANCE TARGETS)

Voxel Lord o'yinining barcha arxitekturasi va renderlash zanjirlari quyidagi qat'iy apparat va unumdorlik talablariga muvofiq optimallashtiriladi:

### 119.1. Mo'ljallangan Tizim Talablari

- **Minimal Tizim Talabi (1080p @ 60 FPS, O'rta sozlamalar):**
  - GPU: Nvidia GeForce GTX 1660 (6GB) yoki AMD Radeon RX 580 (8GB).
  - CPU: Intel Core i5-8400 yoki AMD Ryzen 5 2600 (6 yadro, 3.4 GHz).
  - RAM: 8 GB DDR4.
- **Tavsiya Qilingan Tizim (1440p @ 120 FPS, Yuqori sozlamalar):**
  - GPU: Nvidia GeForce RTX 3060 (12GB) yoki AMD Radeon RX 6600 XT (8GB).
  - CPU: Intel Core i5-12400F yoki AMD Ryzen 5 5600X.
  - RAM: 16 GB DDR4/DDR5.

### 119.2. Aniq Miqdoriy Byudjet Me'yorlari

| Ko'rsatkich Nomi | Qat'iy Byudjet Chegarasi | Izoh va Sinov Shartlari |
|---|---|---|
| **Minimal Kadrlar Soni (FPS)** | $\ge 60\text{ FPS}$ | 200 ta fuqaro, yomg'ir/qor yog'ishi va qamal jangi paytida |
| **Kadr Hisoblash Vaqti (Frame Time)**| $\le 16.6\text{ ms}$ | Standart o'yin jarayonida barqaror $16.6\text{ ms}$ |
| **Maksimal Kadr Sakrashi (Peak Spike)**| $\le 35.0\text{ ms}$ | Katta tosh qal'a devori qulaganda yoki metan gazi portlaganda |
| **GPU Draw Calls Soni** | $< 180\text{ ta draw call}$ | Greedy Meshing va Texture2DArray orqali birlashtirilgan |
| **Video Xotira Sarfi (VRAM)** | $< 2.2\text{ GB}$ | Barcha chunk mesh buferlari va teksturalar yig'indisi |
| **Bir Paytdagi Faol Venzellar** | $\ge 100,000\text{ ta venzel}$ | O'yinchi kamerasida bir paytda chizilayotgan yuzalar |
| **Simulyatsiyadagi Aholi Soni** | $\ge 200\text{ nafar fuqaro}$ | Barcha LOD guruhlari (LOD 0, 1, 2) bo'yicha to'liq taqsimot |

---

# 120. DUNYO XARITASINI YUKLASH CHEGARALARI

$1000\times 1000$ blokli ulkan feodal xaritasida xotirani tejash va barqarorlikni ta'minlash uchun qat'iy asinxron Chunk Streaming tizimi ishlaydi.

### 120.1. Faol Chunklar Radiusi va Matritsasi

- O'yinchi kamerasi atrofida gorizontaliga $\pm 4$ ta chunk ($128\text{ metr}$ har bir tomonga) va vertikaliga $\pm 3$ ta chunk ($96\text{ metr}$ yuqori va pastga) yuklanadi.
- Umumiy faol mintaqa: $9 \times 7 \times 9 = 567$ ta chunk xotirada saqlanadi.
- O'yinchi harakatlanganda kamerasidan $5$ chunkdan ko'proq uzoqlashgan chekka chunklar xotiradan chiqariladi (unload), yangi yaqinlashgan chunklar esa fon oqimlarida yuklanadi.

### 120.2. Ob'ektlar Hovuzi (VoxelChunk Node Pool)

- Dinamik xotira ajratish (heap allocation) paytidagi qotishlarni bartaraf etish uchun 650 ta `VoxelChunk` nodidan iborat oldindan yaratilgan ob'ektlar hovuzi (`NodePool`) ishlatiladi.
- Bo'shatilgan chunklar o'chirilmaydi, balki tozalab qayta yangi koordinatalarga biriktiriladi. Bu esa Godot xotira tozalagichining (Garbage Collector) ishga tushishini nolga tushiradi.

### 120.3. LRU Kesh va Voxel Deltalarni Siqib Saqlash

- **O'zgarmagan Chunklar:** Agar procedural generatsiyadan so'ng o'yinchi chunkdagi bloklarni qazmagan bo'lsa, u diskka yozilmaydi; qayta yaqinlashganda dunyo urug'idan (`world_seed`) bir zumda qayta generatsiya qilinadi.
- **O'zgargan Chunklar (Voxel Deltas):** O'zgartirilgan bloklar RLE (Run-Length Encoding) va Zlib yordamida siqilib, saqlash fayliga faqat farqlar (deltalar) sifatida yoziladi.
- **Xotira Chegarasi (LRU Threshold):** Faol chunklar soni 700 tadan oshganda, eng uzoq vaqt murojaat qilinmagan (Least Recently Used) toza chunklar xotiradan majburiy haydaladi.

---

# 121. SIMULYATOR SINOVLARI (SIMULATION TESTING)

O'yin iqtisodiyoti, aholi demografiyasi, soliqlar va qishki omon qolish balansini tekshirish uchun o'yin oynasini ochmasdan, buyruqlar satrida ishlaydigan deterministik Headless simulyatsiya sinovlari tizimi mavjud.

### 121.1. Avtomatlashtirilgan Headless Sinovlar Tuzilishi

Sinovlar Godotning maxsus `--headless` rejimi hamda Python asosidagi `prototype_sim.py` va `tests/test_gdd_e2e.py` orqali ishga tushiriladi:
- **Deterministik Urug' (Fixed Seed):** Barcha sinovlar $Seed = 1337$ bilan ishga tushirilib, natijalar har safar $100\%$ bir xil va takrorlanuvchan bo'lishi kafolatlanadi.
- **Vaqtni Tezlashtirish (Fast-Forward Ticking):** 30 kunlik koloniya hayoti 1 soniyada, 100 kunlik qattiq qish sinovi esa 3 soniyada matematik hisoblab chiqiladi (10,000 simulyatsiya ticki grafik renderlashsiz o'tkaziladi).

### 121.2. Avtomatlashtirilgan Tekshiruv Shartlari (Assertions)

Sinov ssenariylari quyidagi mezonlar buzilganda darhol xatolik (failure) e'lon qiladi:
1. **Demografik Inqiroz:** Aholi soni hech qachon nolga tushmasligi shart ($Population > 0$).
2. **Ochlik Balansi:** 100 kunlik simulyatsiyada ochlikdan o'lim darajasi jami aholining $15\%$ idan oshmasligi kerak.
3. **Inflyatsiya va G'azna:** Pul emissiyasi va narxlar tebranishi yiliga $[-10\%, +25\%]$ koridorida saqlanishi shart.
4. **Shaxta Xavfsizligi:** Tayanch nurlari qo'yilgan zonalarda spontan qulashlar yuz bermasligi shart ($S_c \ge 1.0$).

---

# 122. MA’LUMOTLAR BILAN BOSHQARILUVCHI DIZAYN (DATA-DRIVEN)

Voxel Lord o'yinidagi barcha o'yin ob'ektlari dasturiy koddan to'liq ajratilgan bo'lib, Godot 4 ning `CustomResource` (`.tres`) fayllari orqali boshqariladi. Bu geym-dizaynerlarga dasturchilarsiz balansni o'zgartirish va mod yasovchilarga yangi kontent kiritish imkonini beradi.

### 122.1. Maxsus Resurs Klasslari Schemalari

1. **`ItemData` (`res://scripts/resources/item_data.gd`):**
   ```gdscript
   class_name ItemData
   extends Resource

   @export var item_id: StringName = &"item_iron_sword"
   @export var display_name: String = "Temir Qilich"
   @export var category: int = 2 # WEAPON
   @export var weight_kg: float = 1.8
   @export var stack_size: int = 1
   @export var max_durability: int = 250
   @export var base_value: int = 25 # Kumush tanga
   @export var quality_tier: int = 1
   ```

2. **`RecipeData` (`res://scripts/resources/recipe_data.gd`):**
   ```gdscript
   class_name RecipeData
   extends Resource

   @export var recipe_id: StringName = &"recipe_smelt_iron"
   @export var workstation_tier: int = 2 # Blast Furnace
   @export var craft_time_seconds: float = 8.0
   @export var inputs: Dictionary = {"iron_ore": 2, "coal": 1}
   @export var output_item: StringName = &"item_iron_ingot"
   @export var output_count: int = 1
   @export var required_skill_level: int = 15
   ```

3. **`MineralData` (`res://scripts/resources/mineral_data.gd`):**
   ```gdscript
   class_name MineralData
   extends Resource

   @export var mineral_id: int = 12
   @export var mineral_name: String = "Iron Ore"
   @export var strata_y_range: Vector2i = Vector2i(-45, -240)
   @export var peak_depth_y: int = -130
   @export var peak_probability: float = 0.45
   @export var hardness_hits: int = 7
   @export var drop_item_id: StringName = &"item_raw_iron_ore"
   ```

4. **`CropData` (`res://scripts/resources/crop_data.gd`):**
   ```gdscript
   class_name CropData
   extends Resource

   @export var crop_id: StringName = &"crop_wheat"
   @export var display_name: String = "Bug'doy"
   @export var growth_hours: float = 96.0
   @export var optimal_temp_c: float = 22.0
   @export var optimal_hydration: float = 0.15
   @export var base_yield: int = 12
   @export var harvest_item_id: StringName = &"food_wheat_sheaf"
   ```

---

# 123. MARKAZIY BALANS BAZASI (BALANCE CONFIG)

Barcha o'yin konstantalari yagona global konfiguratsiya resursida jamlangan bo'lib, o'yin ichida va ishlab chiqish paytida yagona haqiqat manbai (Single Source of Truth) vazifasini bajaradi.

### 123.1. Markaziy Balans Resursi (`res://scripts/core/balance_config.gd`)

```gdscript
class_name BalanceConfig
extends Resource

## O'yinning global iqtisodiy, ekologik va harbiy parametrlarining markaziy bazasi.

@export_group("Fuqarolar Ehtiyojlari")
@export var base_hunger_drain_per_hour: float = 4.16 # 24 soatda 100% ochlik
@export var base_thirst_drain_per_hour: float = 8.33 # 12 soatda 100% chanqoqlik
@export var base_warmth_drain_freezing: float = 12.5 # Qishki sovuqda sovish tezligi
@export var citizen_base_speed_m_s: float = 3.5

@export_group("Dehqonchilik va Oziq-ovqat")
@export var global_crop_growth_multiplier: float = 1.0
@export var arrhenius_q10_spoilage_factor: float = 2.0
@export var food_spoilage_reference_temp: float = 15.0

@export_group("Konchilik va Qurilish")
@export var mine_ceiling_collapse_threshold: float = 0.75
@export var natural_span_stress_factor: float = 0.08
@export var overburden_depth_scale: float = 0.35

@export_group("Diplomatiya va Soliqlar")
@export var tribute_base_coefficient: float = 50.0
@export var default_tax_efficiency: float = 0.85
@export var casus_belli_war_threshold: int = 100
```

### 123.2. Jonli Yangilanish (Hot-Reloading in Debug Builds)

Ishlab chiqish va balanslash bosqichida o'yinni o'chirib yoqmasdan parametrlar bilan tajriba o'tkazish uchun `BalanceConfig` drayveri Hot-Reload tizimiga ega:
- Fayl o'zgartirilganda Godotning `EditorFileSystem` yoki mustaqil `FileAccess` kuzatuvchisi buni aniqlaydi.
- `ResourceLoader.load("res://data/balance_config.tres", "", ResourceLoader.CACHE_MODE_REPLACE)` orqali yangi parametrlar xotiraga qayta yuklanadi.
- Barcha faol tizimlar (`ChunkManager`, `DiplomacyManager`, `GreenhouseThermalSystem`) yangilangan qiymatlarni darhol qabul qiladi.
- Debug konsolidan buyruqlar orqali qiymatlarni jonli o'zgartirish mumkin (Masalan: `cfg.global_crop_growth_multiplier = 2.5`).

---

# 124. QIROL BO‘LISH VA YAKUNIY G‘ALABA FARQI

Qirol bo'lish — o'yin o'rtasidagi yirik siyosiy bosqichdir. Yakuniy g'alaba (Victory) esa butun mintaqada abadiy meros qoldirish maqsadidir.

---

# 125. ENDGAME — 3 XIL BUYUK G‘ALABA YO‘LI

1. **Wonder of the Realm (Me'moriy Mo'jiza):** 10,000 o'yma tosh, 2,000 marmar, 500 oltin bezak va 150 vitraj oynadan iborat Asrlar Saroyi yoki Sobori.
2. **Realm Unification (Qit'ani Birlashtirish):** 6 ta biomda mustahkam poytaxtlar qurish, 5 ta Afsonaviy Bossni yengish va barcha raqib fraktsiyalarni birlashtirish.
3. **The Sovereign Guild (Iqtisodiy Monopoliya):** 100,000 Oltin Tanga xazinasi, Yirik Xalqaro Port va barcha savdo gildiyalarini iqtisodiy qaram qilish.

---

# 126. CHEKSIZ REJIM (ENDLESS REALM)

Buyuk g'alabadan keyin ham saltanat to'xtamaydi: o'yinchi o'z poytaxtini kengaytirishda, avlodlarni tarbiyalashda va ulkan feodal imperiyani boshqarishda davom etadi.

---

# 127. PLAYABLE MVP BOSQICHI

1 ta biom, bazaviy voxel mexanikasi, rudalar, qurilish, asbob yasash, 5–10 ta fuqaro, oddiy kasblar, non pishirish, bitta kichik qaroqchilar qarorgohi.

---

# 128. EARLY ACCESS 0.1 BOSQICHI

3 ta biom, 30 ta fuqaro, dehqonchilik, metallurgiya, bino chizmalari, qaroqchilar reydi, fasllar va bazaviy iqtisodiyot.

---

# 129. EARLY ACCESS 0.5 BOSQICHI

6 ta biom, 100 ta fuqaro, muntazam armiya, qamal mashinalari, vabo va sanitariya, qozixona, savdo karvonlari, dastlabki 3 ta boss.

---

# 130. RELEASE 1.0 (TO‘LIQ TALQIN)

Sulola va vorislik tizimi, barcha 5 ta afsonaviy boss, Ritsarlar turniri, tashqi diplomatiya, Buyuk Sobor me'moriy mo'jizasi, Steam P2P Co-op Multiplayer va yutuqlar (Achievements).

---

# 131. ASOSIY DIZAYN QOIDASI (KEY DESIGN RULE)

Har bir yangi funksiya quyidagi savolga ijobiy javob berishi shart:
> *“Bu mexanika o‘yinchining oddiy sarson-sargardondan buyuk qudratli feodal hukmdorgacha ko‘tarilish hissini kuchaytiradimi?”*

---

# 132. AMALIY ISHLAB CHIQISH NAVBATI (DEVELOPMENT PRIORITY)

* **P0 — Asos:** Voxel World, Character Controller, Inventar, Buyumlar, Save/Load.
* **P1 — Omon Qolish:** Crafting, Boshpana, Oziq-ovqat, Ob-havo.
* **P2 — Koloniya:** Citizen AI, Kasblar, Uylar, Logistika, Ishlab chiqarish.
* **P3 — Iqtisodiyot:** Tashqi savdo, Soliqlar, Resurs zanjirlari.
* **P4 — Harbiy:** Jang mexanikasi, Armiya, Reydlar, Voxel qamallari.
* **P5 — Jamiyat:** Oilalar, Sud va jazo, Sanitariya, Ta'lim, Madaniyat.
* **P6 — Qirollik:** Diplomatiya, Sulola, Qirollik qonunlari, Chegaralar.
* **P7 — Endgame & Co-op:** 5 ta Boss, Mo'jizalar, Steam P2P Multiplayer, G'alaba shartlari.

---

# YAKUNIY O‘YIN FORMULASI

**Survival → Settlement → Automation → Economy → Military → Politics → Kingdom → Dynasty → Legacy**

---

# VOXEL LORD: FEUDAL REALM

O‘yinning asosiy ruhiyati:
> Birinchi kuni o‘yinchi sovuq o‘rmonda yolg‘iz holda bitta daraxtni bolta bilan kesadi.
> Bir necha yil o‘tgach esa aynan shu joyda yuzlab odam yashaydigan ulkan tosh poytaxt qad ko'taradi.
> Uzoqda dalalar to'lqinlanadi.
> Konlardan aravalar ruda olib chiqadi.
> Temirchilar qilich yasaydi.
> Savdogarlar darvozadan kiradi.
> Bolalar maktabga boradi.
> Ritsarlar qal’a devorlarini qo‘riqlaydi.
> Sobor qo‘ng‘iroqlari yangraydi.
> Qabristonda o‘yinning dastlabki kunlarida o'yinchi bilan birga yashagan birinchi fuqarolarning qabr toshlari turadi.

Va o‘yinchi tushunadi:  
**bu qirollik unga tayyor berilmagan.**  
**Uning har bir g‘ishti, har bir oilasi va har bir tarixi o‘yin davomida o'z mehnati bilan paydo bo‘lgan.**
