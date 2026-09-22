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

# 14. AHOLINING PAYDO BO‘LISHI

1. **Signal Fire (Xaloskor Gulxan):** Dastlabki sarson-sargardonlarni jalb qiladi.
2. **Captive Rescue (Asirlarni Qutqarish):** Qaroqchilar lageridagi tutqunlarni ozod qilish.
3. **Village Bell (Shahar Qo'ng'irog'i):** Farovon shahar migrant va ustalarni chaqiradi.
4. **River Docks (Daryo Porti):** Yollanma ishchilar va sayohatchilar kelishi.
5. **Generations (Tug'ilish):** Baxtli oilalar nikohi va bolalar dunyoga kelishi.

---

# 15. MIGRATSIYA VA KETISH (EMIGRATION)

Aholi shaharni tashlab ketish sabablari:
- uzoq davom etgan ochlik;
- boshpana yetishmasligi;
- xavfsizlik pastligi (doimiy reydlar);
- yuqori soliqlar (>30%);
- davolanmagan vabo va kasallik;
- zolimona hukmronlik.

---

# 16. OILA VA QARINDOSHLIK TIZIMI

Har bir fuqaro: `Partner, Parents, Children, Siblings, Household` aloqalariga ega.
Nikoh ehtimoliga yosh, uy mavjudligi, ma'naviy ruhiyat (morale) va xavfsizlik ta'sir qiladi.

---

# 17. UY-JOY TALABLARI (HOUSING)

Uy parametrlari:
- **Capacity (Sig'im)**
- **Beds (To'shaklar)**
- **Warmth (Issiqlik - Pechka)**
- **Privacy (Shaxsiy hudud)**
- **Beauty (Go'zallik va bezaklar)**
- **Safety (Mustahkam devorlar)**
Uy sifati to'g'ridan-to'g'ri unumdorlik va tug'ilishga ijobiy ta'sir ko'rsatadi.

---

# 18. FUQAROLAR EHTIYOJLARI (CITIZEN NEEDS)

Food, Water, Sleep, Warmth, Safety, Housing, Social, Entertainment, Health.

---

# 19. CITIZEN AI ARXITEKTURASI

1. **High-Level Planner:** Kun tartibi va nima qilish kerakligini rejalashtiradi.
2. **Finite State Machine (FSM):**
   `Walk, Work, Eat, Sleep, Fight, Flee, Socialize, Heal, Transport, Rest`.

---

# 20. VAZIFALAR USTUVORLIGI (TASK PRIORITY)

`Critical → High → Normal → Low`.
- Yong'in o'chirish = Critical.
- Jasadlarni yig'ish = High.
- Shaharni bezatish = Low.

---

# 21. KASBLAR TIZIMI (JOB ROLES)

Farmer, Lumberjack, Miner, Builder, Hauler, Blacksmith, Carpenter, Hunter, Fisherman, Cook, Baker, Brewer, Tailor, Merchant, Doctor, Alchemist, Teacher, Guard, Soldier, Knight, Gravedigger, Priest, Bard va boshqalar.

---

# 22. DIPLOMATIYA, RAQIB FRAKTSIYALAR VA MULTIPLAYER (CO-OP)

## 22.1. Qo'shni AI Qirolliklar va Fraktsiyalar
Dunyo procedural generatsiya qilinayotganda turli biomlarda mustaqil AI lordlar va neytral fraktsiyalar paydo bo'ladi:
* **Savdogar Gildiyalari (Merchant Guilds):** Qirg'oq bo'yi va tekisliklarda joylashgan. Noyob resurslarga (ziravorlar, maxsus shisha, ekzotik matolar) ega. Monopoliya va erkin savdoni xohlaydi.
* **Harbiy Feodallar (Warlords):** Tog'li va o'rmonli hududlardagi agressiv qo'shnilar. Chegarasini doimiy kengaytiradi va o'lpon talab qiladi.
* **Diniy Ordenlar (Theocratic Orders):** Qat'iy diniy qoidalarga tayanadi. Buyuk Sobor qursangiz ittifoqchi, qora joduga berilsangiz "bid'atchi" deb urush ochadi.

## 22.2. Savdo va Diplomatiya Tizimi
Tier 3 Elchixona (Embassy) binosi orqali Dunyo Xaritasi interfeysida boshqariladi:
* **Karvon Yo'llari (Trade Routes):** Ikki tomonlama savdo shartnomasi, ot-aravali qatnovlar. O'yinchi karvonlarni qaroqchilardan himoya qiladi.
* **Diplomatik Harakatlar:**
  * **O'lpon (Tribute):** Hujumni to'xtatish yoki hurmat qozonish uchun har mavsum to'lov.
  * **Ittifoq (Alliance):** Umumiy dushmanga qarshi birlashish, qamalda yordam chaqirish.
  * **Josuslik (Espionage):** Raqib qasri omboriga o't qo'yish yoki tungi qamalda darvozani ichkaridan ochish.

## 22.3. Chegara To'qnashuvlari va Urush Mexanikasi
* **Voxel Qamallari (Destructible Voxel Sieges):** AI va o'yinchi trebuchetlar, katapultalar va taranlar (Battering Ram) yordamida tosh devorlarni jismonan buzib kiradi.
* **Hududni Bosib Olish:** Raqib Asosiy Zali (Great Hall) egallansa va AI Lord yengilsa, o'sha yer barcha infratuzilmasi bilan tobelikka o'tadi.
* **Asirlar Tizimi:** Mag'lub lordlar zindonga tashlanadi — katta tovon puli talab qilish, qatl etish yoki vassalga aylantirish mumkin.

## 22.4. Multiplayer va Co-op Rejimi (Steam P2P 2–4 O'yinchi)
* **Yagona Taxt (Shared Kingdom / Co-op):** Do'stlar bitta shahar-davlatni birgalikda boshqaradi:
  * *1-O'yinchi (Hukmdor):* Iqtisodiyot, binolar loyihasi, soliqlar va diplomatiya.
  * *2-O'yinchi (Bosh Qomondon):* Kazarma, qo'shin tayyorlash va jangovar yurishlar.
  * *3-O'yinchi (Bosh Usta):* Konchilik tarmog'i, chuqur shaxtalar va metallurgiya zanjiri.
* **Feodal Tarqoqlik (Rival Kingdoms / PvPvE):** O'yinchilar bitta katta xaritaning turli burchaklarida o'z qasrlarini quradi — ittifoq tuzishi yoki konlar uchun o'zaro qamal urushlari olib borishi mumkin.
* **Texnik Yechim:** Host-Authoritative Client-Server arxitekturasi. Dunyo simulyatsiyasi va NPC AIsi Hostda hisoblanadi, boshqa o'yinchilarga holat paketlari uzatiladi.

---

# 23. MAHORAT TIZIMI (SKILL SYSTEM)

Har bir kasbda 0–100 daraja:
`Novice (Yangi) → Apprentice (Shogird) → Journeyman (Usta yordamchisi) → Expert (Mutaxassis) → Master (Buyuk Usta)`.
Master ustalar yangi avlod shogirdlarini o'qitish huquqiga ega.

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

# 27. DUNYO GENERATSIYASI VA 6 ASOSIY BIOM

1. **Unumdor Tekislik:** Dehqonchilik unumi +50%, minerallar kam.
2. **Qalin O‘rmon:** Mo'l yog'och va yovvoyi hayvonlar, yirtqichlar xavfi.
3. **Tog‘lik:** Boy minerallar va tosh zaxirasi, qiyin relyef.
4. **Botqoqlik:** Torf, noyob dorivor giyohlar, zax va kasallik xavfi.
5. **Tundra:** Doimiy sovuq, ekinlar o'smaydi, go'sht muzlab aynimaydi, geotermal issiqxonalar zarur.
6. **Dasht (Arid Steppe):** Yaylovlar, tosh tuzi, suv manbalari tanqis.

---

# 28. VOXEL WORLD TEXNIK PARAMETRLARI

- **Masshtab:** 1 voxel = 1 metr³.
- **Chunk:** 32 × 32 × 32 voxel bloklari.
- **Chunk Streaming:** O'yinchi atrofida asinxron yuklanadi.

---

# 29. VOXEL LOD (LEVEL OF DETAIL)

- Yaqin chunklar: To'liq voxel kolliziya va greedy meshing.
- O'rta masofa: Soddalashtirilgan yuzalar.
- Uzoq masofa: Relyef balandlik xaritasi (Terrain LOD).

---

# 30. YER QATLAMLARI VA STRATALAR

- **0 → -30m:** Tuproq va loy qatlami (Soil & Clay).
- **-30 → -100m:** Ko'mir, Mis va Qalay qatlami.
- **-100 → -200m:** Temir, Kumush va Oltingugurt qatlami.
- **-200 → -350m:** Oltin, Qimmatbaho javohirlar (Ruby, Diamond).
- **-350m+:** Magma, Obsidian va Tub Qoya (Bedrock).

---

# 31. SHAXTALAR VA KONCHILIK MEXANIZMLARI

Shaxta xavfsizligi va logistikasi:
- Yog'och tirgaklar (Support Beams);
- Shamollatish shaxtalari (Ventilation Shafts);
- Ruda aravachalari (Mine Carts & Rails);
- Chuqur liftlar (Hoists & Winches);
- Konchilar chiroqlari (Lanterns).

---

# 32. SHAXTA O‘PIRILISHI (CAVE-IN)

Tirgaklar o'rnatilmasa, shiftning mustahkamlik koeffitsiyenti (Ceiling Stability) pasayadi va voxel qulashi ro'y beradi. Konchilar jarohatlanadi, tunnellar yopilib qoladi.

---

# 33. METAN GAZI VA PORTLASH (UNDERGROUND GAS)

Chuqur qatlamlarda zaharli gaz cho'ntaklari paydo bo'ladi. Shamollatish quvurlari bo'lmasa, gaz zaharlanishi yoki mash'ala olovidan portlash yuz beradi.

---

# 34. 20+ GEOLOGIK MINERALLAR

Stone, Clay, Limestone, Marble, Granite, Basalt, Coal, Peat, Salt (Halite), Sulfur, Saltpeter, Copper, Tin, Lead, Zinc, Nickel, Iron, Silver, Gold, Platinum, Ruby, Emerald, Sapphire, Diamond.

---

# 35. METALLURGIYA ZANJIRI

`Ruda qazish → Rudani maydalash → Domna pechida eritish → Quymalar (Ingots) → Qotishmalar (Bronza, Po'lat) → Temirchilik bosqoni → Tayyor qurol/asbob`.

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

# 53. JANG TIZIMI (COMBAT MECHANICS)

Light Attack, Heavy Attack, Block, Parry (Qaytarish), Dodge (Chetlanish), Stamina, Armor, Stagger (Muvozanatni yo'qotish).

---

# 54. ZARAR HISOBLASH FORMULASI (DAMAGE)

`FinalDamage = (BaseDamage × SkillModifier × WeaponQuality × HitModifier) - ArmorProtection`.

---

# 55. SOVUTLAR VA ZARAR TURLARI

Sovutlar: Matoli kiyim, Qalin charm, Zanjir sovut, To'liq temir zirh (Plate Armor).
Zarar turlari: Kesuvchi (Slash), Sanchuvchi (Pierce), Maydalovchi (Blunt).

---

# 56. MASOFADAN JANG (RANGED COMBAT)

Oddiy va kompozit kamonlar, og'ir arbaletlar (Crossbows). Fizik gravitatsiya va shamol ta'siri.

---

# 57. HARBIY FAZILATLAR (WARRIOR TRAITS)

Jasorat (Bravery), Kuch (Strength), Chaqqonlik (Agility), Ko'rish o'tkirligi (Vision), Intizom (Discipline).

---

# 58. ASKARLARNI O‘QITISH VA RUTBALAR

`Ko'ngilli Yangi Askar → Xalq Lashkari (Militia) → Professional Piyoda → Tajribali Veteran → Elita Ritsar`.

---

# 59. HARBIY SAFLAR VA BUYRUQLAR (FORMATIONS)

Buyruqlar: Ortidan ergashish (Follow), O'rnida turish (Hold), Himoyalanish (Defend), Hujum (Attack), Chekinish (Retreat).
Saflar: Saf (Line), Qalqon Devori (Shield Wall), Kolonna (Column), Otliqlar Hujumi (Cavalry Charge).

---

# 60. JANGOVAR RUH (MILITARY MORALE)

Komandir o'lsa saf buziladi va askarlar qochadi. G'alaba qozonilsa jangovar ruh va tajriba keskin oshadi.

---

# 61. QAMAL TEXNIKASI (SIEGE ENGINES)

Devor yoruvchi taran (Battering Ram), qamal narvonlari, tosh otuvchi katapultalar va og'ir trebuchetlar. Voxel devorlar to'g'ridan-to'g'ri parchalanadi.

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

Og'irlik, mustahkamlik va tayanch masofasi (Support Distance). Tayanchsiz qoldirilgan og'ir tosh tomlar o'z og'irligi ostida qulab tushadi.

---

# 66. YONG‘IN XAVFI VA O‘CHIRISH (FIRE HAZARD)

Yog'och va somon tomlar chaqmoq yoki olovdan tez alangalanadi. Fuqarolar darhol chelaklar bilan suv tashib yong'inni o'chiradi.

---

# 67. DINAMIK OB-HAVO

Bahorgi jala va sellar, yozgi jazirama va qurg'oqchilik, kuzgi tumanlar, qishki qor bo'roni va sovuq.

---

# 68. TANA HARORATI VA GIPOTERMIYA

Har bir personajda BodyTemperature mavjud. Qattiq sovuqda issiq kiyimsiz va pechkali uysiz yurgan fuqaro muzlab halok bo'ladi.

---

# 69. TABIIY VA YIRTQICH DUSHMANLAR

Bo'rilar to'dasi, ayiqlar, qaroqchilar, g'or kalamushlari, gigant zaharli o'rgimchaklar.

---

# 70. QONLI OY REYDLARI (BLOOD MOON)

Har 15–20 kunda yuz beruvchi keng ko'lamli qaroqchilar va maxluqlar hujumi. Kuch o'yinchi shahrining boyligi va aholisiga qarab mutanosib oshib boradi.

---

# 71. DUNYONING 5 AFSONAVIY BOSSI (CANONICAL 5 BOSSES)

1. **Qonli Tirnoq (Alpha Bear):** O'rmon xo'jayini (Tier II).
2. **Temir Soqol Valdemar (Warlord):** Qaroqchilar sarkardasi (Tier III).
3. **Zulmat Onasi (Broodmother):** Chuqur g'orlar malikasi (Tier III–IV).
4. **Qoya Kolossi (Crag Colossus):** Tog'li hududlar giganti (Tier IV).
5. **Muz Qanoti (Frost Wyvern):** Shimoliy tundraning afsonaviy vishali (Late Tier IV).

---

# 72. BOSS PROGRESSIYASI

Har bir boss o'z bosqichida ochiladi va mag'lub etilganda noyob mukofotlar va unvonlar keltiradi.

---

# 73. JAROHAT VA SALOMATLIK STATUSLARI

Health, Qon ketishi (Bleeding), Og'riq (Pain), Suyak sinishi (Fracture), Yuqumli yiringlash (Infection).

---

# 74. TABOBAT VA GOSPITAL TIZIMI

Bog'lov materiallari (Bandage), dorivor damlamalar, Tabib (Doctor), Gospital va Alkimyoviy malhamlar.

---

# 75. YUQUMLI KASALLIKLAR MEXANIKASI

Yuqish zanjiri: `Kontakt → Inkubatsiya → Belgilar → Tuzalish / O'lim`. Tarqalish sabablari: iflos suv, buzilgan taom, ko'milmagan jasadlar, kalamushlar.

---

# 76. SHAHAR SANITARIYASI

Chiqindi chuqurlari, toza ichimlik suvi ta'minoti, jasadlarni o'z vaqtida yig'ish, kalamushlarga qarshi mushuklar va itlar boqish.

---

# 77. QORA O‘LAT VA KARANTIN (THE BLACK PLAGUE)

Epidemiya boshlanganda:
Karantin e'lon qilish, O'lat Tabibi (Plague Doctor) jalb qilish, kasalxona izolatsiyasi, vabo gulxanida kiyimlarni yoqish.

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

Dushman (Hostile), Sovuq (Unfriendly), Neytral (Neutral), Do'stona (Friendly), Ittifoqchi (Allied), Vassal (Qaram tobe).

---

# 84. DIPLOMATIK SHARTNOMALAR

Savdo bitimi, Hujum qilmaslik pakti, Mudofaa ittifoqi, Nikoh diplimatiyasi, O'lpon to'lash, Sulh yoki Urush e'lon qilish.

---

# 85. HUDUD CHEGARALARI (TERRITORY CONTROL)

Qorovul minoralari (Watchtowers) qurish orqali hududni o'z mulkiga qo'shib olish. Kengayish uchun yetarli aholi va ma'muriy boshqaruv kuchi talab qilinadi.

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

# 92. FUQAROLARNING TABIIY VA NOTABIIY O‘LIMI

O'lim sabablari: Keksalik (Old Age), Jang maydoni, Kasallik, Ochlik, Qahraton sovuq, Shaxtadagi baxtsiz hodisa.

---

# 93. KO‘CHADA QOLGAN JASADLARNING FOJIASI

Jasad ko'milmay qolsa, shahar sanitariyasi yemirilib, fuqarolar chuqur ruhiy tushkunlikka tushadi va vabo xavfi kuchayadi.

---

# 94. G‘ASSOL VA DAFN LOGISTIKASI (GRAVEDIGGER)

O'liklar aravasi (Morgue Cart) bilan jasadlarni yig'ib, tobut yoki kafanda qabristonga yetkazuvchi maxsus xizmatchi.

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

- **Core:** `GameManager`, `TimeManager`, `EventBus`, `SaveManager`.
- **World:** `WorldManager`, `ChunkManager`, `VoxelGenerator`, `WeatherManager`.
- **Entities:** `Citizen`, `Player`, `Animal`, `Enemy`, `Boss`.
- **AI:** `TaskManager`, `JobManager`, `CitizenBrain`, `FactionAI`.
- **Economy:** `ItemDatabase`, `InventorySystem`, `ProductionManager`, `TradeManager`.
- **Settlement:** `BuildingManager`, `HousingManager`, `TerritoryManager`, `CultureManager`.
- **Combat:** `CombatManager`, `ProjectileSystem`, `SiegeSystem`.
- **UI:** `HUD`, `RoyalLedger`, `WorldMap`, `DialogueManager`.

---

# 115. SCRIPT VAZIFALARI (GDSCRIPT & C#)

- **GDScript:** O'yin mantig'i, kvestlar, personajlar muloqoti, UI boshqaruvi.
- **C# / GDExtension:** Yuqori unumdorlik talab qiluvchi Voxel Meshing, Greedy algoritmlari, ko'p sonli aholining yo'l topish hisob-kitoblari.

---

# 116. VOXEL RENDERLASH SAMARADORLIGI

Face Culling, Greedy Meshing, Fon oqimlarida (Background Threads) chunk yaratish. Asosiy render oqimi (Main Thread) hech qachon qotib qolmasligi shart.

---

# 117. O‘ZGARUVCHAN DUNYODA YO‘L TOPISH (NAVIGATION)

Statik NavMesh ishlamaydi. Har bir chunk o'zining dinamik NavigationRegion3D qismiga ega bo'ladi. Voxel buzilganda yoki qo'yilganda faqat shu mintaqa yangilanadi.

---

# 118. AHOLI SUN’IY INTELLEKTI LOD TIZIMI (AI LOD)

- Yaqin fuqarolar: To'liq 3D animatsiya va individual fizik hisob-kitob.
- O'rta masofa: Soddalashtirilgan yo'l topish.
- Uzoq masofa: Statistik simulyatsiya (Fermer dalada matematik ishlaydi, kadrma-kadr render qilinmaydi).

---

# 119. UNUMDORLIK NISHONLARI (PERFORMANCE TARGETS)

- Ekran: 1080p / 1440p.
- FPS: Minimal 60 FPS, Ideal 120 FPS.
- Sinov me'yori: 100–150 ta faol fuqaro, yirik tosh qal'a, qor bo'roni va faol ishlab chiqarish paytida.

---

# 120. DUNYO XARITASINI YUKLASH CHEGARALARI

1000×1000 masshtabdagi dunyo bir paytda to'liq chizilmaydi — qat'iy asinxron Chunk Streaming tizimi ishlaydi.

---

# 121. SIMULYATOR SINOVLARI (SIMULATION TESTING)

`prototype_sim.py` vositasi orqali: 30 kunlik balans, 100 kunlik qishki omon qolish, aholi o'sishi, vabo epidemiyasi va soliq bosimi matematik tekshiriladi.

---

# 122. MA’LUMOTLAR BILAN BOSHQARILUVCHI DIZAYN (DATA-DRIVEN)

Barcha qurollar, binolar, retseptlar, ekinlar va qonunlar qattiq kodlanmasdan, JSON va Godot Custom Resource fayllarida saqlanadi.

---

# 123. MARKAZIY BALANS BAZASI (BALANCE CONFIG)

Hosil ko'paytiruvchilari, soliq narxlari, askarlar oyligi va fuqarolarning non iste'moli yagona balans faylida boshqariladi.

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
