# Voxel Lord: Feudal Realm — E2E Test Infrastructure Specification

**Document Maqomi:** End-to-End Test Infrastructure & Quality Assurance Specification  
**Maqsad:** "Voxel Lord: Feudal Realm" Master Game Design Document (`MASTER_GDD.md`) va uning tizim prototiplarini qat'iy, avtomatlashtirilgan 4 bosqichli (4-Tier) sifat tekshiruvi orqali verifikatsiya qilish.  
**Bog'langan Hujjatlar:** `ORIGINAL_REQUEST.md`, `PROJECT.md`, `MASTER_GDD.md`, `tests/test_gdd_e2e.py`  
**Muallif / Rol:** QA & E2E Test Writer  

---

## 1. Test Falsafasi (Test Philosophy)

O'yin dizayni hujjati (`MASTER_GDD.md`) oddiy g'oyalar to'plami emas, balki bevosita Godot 4.3 dvigatelida kodlanadigan **ishlab chiqarish arxitekturasi spetsifikatsiyasi (Production Specification)** dir. Shu sababli, test infratuzilmasi hujjatni dasturiy ta'minot kodidek qat'iy tekshiradi.

### 1.1. Opaque-Box & Requirement-Driven
- **Tashqi talablarga tayanish:** Testlar faqat `ORIGINAL_REQUEST.md` va `PROJECT.md` dagi qat'iy talablardan kelib chiqadi. Hujjat ichidagi yuzaki matnlarga ko'r-ko'rona moslashmaydi.
- **Zero Placeholder qoidasi:** Hujjatda birorta ham qoralamalik belgisi (`TBD`, `TODO`, `...`, `va boshqalar`) bo'lishiga yo'l qo'yilmaydi. Har bir tizim to'liq yechimga ega bo'lishi shart.
- **Matematik qat'iylik:** Har bir iqtisodiy, demografik, harbiy va fizik formula chegara qiymatlari (boundary), ekstremal sharoitlar va barqarorlik (stability) nuqtai nazaridan tekshiriladi.

---

## 2. To'rt Bosqichli Test Metodologiyasi (4-Tier Methodology)

Test arxitekturasi 4 darajali qatlamga bo'lingan:

```
+-----------------------------------------------------------------------+
|  Tier 4: Real-World Simulation (Formulalar simulyatsiyasi & Math)     |
+-----------------------------------------------------------------------+
|  Tier 3: Cross-Feature Integration (Tizimlararo bog'liqlik & Schema)  |
+-----------------------------------------------------------------------+
|  Tier 2: Boundary & Corner Conditions (Jadvallar, Chegaralar, Format) |
+-----------------------------------------------------------------------+
|  Tier 1: Feature Coverage (133 Bo'lim to'liqligi & Zero Placeholders) |
+-----------------------------------------------------------------------+
```

### Tier 1: Xususiyat Qamrovi (Feature Coverage)
- **133 ta bo'lim mavjudligi:** `MASTER_GDD.md` dagi barcha 0 dan 132 gacha bo'lgan asosiy bo'lim sarlavhalari (`# 0.` dan `# 132.` gacha) mavjudligi tekshiriladi.
- **Tarkib yetarliligi:** Har bir bo'lim bo'sh emasligi, mazmunli spetsifikatsiyaga egaligi tekshiriladi.
- **Placeholder taqiqi:** Hujjat matnida `TBD`, `TODO`, `...`, yoki `va boshqalar` kabi noaniq, chala iboralar mutlaqo yo'qligi qat'iy assert qilinadi.

### Tier 2: Chegara va Burchak Shartlari (Boundary & Corner Conditions)
- **Markdown jadvallari formati:** Barcha tizim jadvallari (Ruda, Qurol, Asbob, Ekin, Oziq-ovqat, Qo'shin va h.k.) to'g'ri Markdown jadvali tuzilishiga (Header, Separator `|---|`, Ma'lumot qatorlari) egaligi tekshiriladi.
- **Ustunlar va kataklar yaxlitligi:** Birorta qatorda kataklar bo'sh qolmasligi, ustunlar soni mos kelishi talab qilinadi.
- **Raqamli diapazonlar va o'lchov birliklari:** 
  - Ekin o'sish soatlari: $24 \le \text{ticks} \le 500$ soat;
  - Qurol mustahkamligi: $\text{durability} > 0$;
  - Ziyon miqdori: $FinalDamage \ge 0$;
  - Bozor elastikligi narx chegarasi: $[0.2 \times P_{base}, 5.0 \times P_{base}]$.

### Tier 3: Tizimlararo Integratsiya va Muvofiqlik (Cross-Feature Integration)
- **Geologiya ↔ Metallurgiya:** Geologik katalogda ko'rsatilgan rudalar (masalan, Temir, Mis, Qalay, Oltin) eritish retseptlarida mavjudligi.
- **Qishloq xo'jaligi ↔ Oziq-ovqat ↔ Ratsion:** Ekinlar jadvalidagi hosillar oziq-ovqat zanjiriga kirishi, oziq-ovqatlar esa fuqarolar ratsioni va saqlanish (preservation) tizimi bilan bog'langanligi.
- **Qurollar ↔ Zirhlar ↔ Jang turlari:** Qurollarning zarba turlari (Slash, Pierce, Blunt) zirhlarning zarba qaytarish va yutish matritsasi bilan 1:1 muvofiqligi.
- **Fuqaro AI ↔ Ehtiyojlar ↔ Kasblar:** FSM holatlari (Walk, Work, Eat, Sleep, Fight, Flee, Socialize, Heal, Transport, Rest) ehtiyojlar pasayishi va vazifalar ustuvorligi bilan bog'langanligi.

### Tier 4: Real-World Simulyatsiya va Matematik Tekshiruv (Real-World Simulation)
Hujjatda keltirilgan barcha differensial va algebraik formulalar Python testlarida bevosita hisoblab chiqiladi:
1. **Ekin o'sish formulasi (Crop Growth Ticks):** Tuproq namligi va harorat parabolasi ostida o'sish tezligi hisobi.
2. **Arrhenius oziq-ovqat aynishi (Food Spoilage):** $Q_{10} = 2.0$ qoidasi bo'yicha harorat oshganda buzilish tezlashishi va qutilar/muzxona koeffitsiyentlari.
3. **Dinamik Bozor Narxi (Market Pricing):** Talab va taklif nisbati elastikligi ($\gamma=1.25$) hamda narx chegaralari ($0.2\times$ va $5.0\times$).
4. **Jang ziyonini hisoblash (Combat Damage):** `(BaseDamage * Skill * Quality * Hit - ArmorDeflection) * (1 - Absorption)` formulasi bo'yicha turli zirh va qurollarning o'zaro ta'siri.
5. **Kon shiftining barqarorligi ($S_c$):** $S_c = K_{rock} \times \frac{R_{sup}}{Span}$ formulasi, tayanch ustunlarining radiusi va o'pirilish ($S_c < 0.75$) shartlari.
6. **Issiqxona termodinamik muvozanati (Greenhouse Thermodynamics):** Tundrada geotermal bug' va tashqi sovuqlik o'rtasidagi statsionar issiqlik muvozanati harorati.

---

## 3. To'liq 32 Xususiyatlar Inventari va Test Matritsasi

| # | Xususiyat Nomi | Asosiy Bo'limlar | Test Tier | Test Funksiyasi / Verifikatsiya Kriteriyasi |
|---|---|---|---|---|
| 1 | R1: Crop Growth Ticks & Agriculture | Sec 36–39 | Tier 1, 2, 4 | `test_tier4_crop_growth_simulation`, Ekin jadvali, harorat chegaralari |
| 2 | R1: Soil Fertility Decay & Rotation | Sec 40–42 | Tier 1, 2, 3 | N-P-K nutrient depletion matrix, 4-dala almashlab ekish yaxlitligi |
| 3 | R1: Food Spoilage & Preservation Math | Sec 43–45 | Tier 1, 2, 4 | `test_tier4_arrhenius_spoilage_simulation`, $Q_{10}=2.0$ aynish hisobi |
| 4 | R1: Multi-Tier Processing Chains | Sec 46–48 | Tier 1, 2, 3 | Xomashyo → Yarim tayyor → Tayyor mahsulot balansi ($100\%$ mass saqlanish) |
| 5 | R1: Dynamic Market Pricing & Economy | Sec 49–52 | Tier 1, 2, 4 | `test_tier4_dynamic_pricing_bounds`, Narx elastikligi va qisqichlari |
| 6 | R1: Items, Quality & Tools | Sec 10–13 | Tier 1, 2, 3 | Asboblar progressiyasi, chidamlilik (durability), 6 sifat darajasi |
| 7 | R2: Citizen Demographics & Lifecycle | Sec 14–17 | Tier 1, 2, 4 | Gompertz-Makeham o'lim formulasi, demografik balans |
| 8 | R2: 10-State Citizen AI FSM | Sec 19 | Tier 1, 2, 3 | 10 ta FSM holati, o'tish shartlari va interruptlar to'liqligi |
| 9 | R2: Granular Needs Drain Formulas | Sec 18 | Tier 1, 4 | Hunger, Thirst, Warmth, Fatigue differensial pasayish tezliklari |
| 10 | R2: Normalized Morale System | Sec 21, 74 | Tier 1, 2, 4 | `[-100, +100]` normalizatsiyasi, 21 ta holat effekti balansi |
| 11 | R2: Job Priority Weighting Utility | Sec 20 | Tier 1, 4 | Utility skoring funksiyasi, 7 darajali ustuvorlik |
| 12 | R2: Housing Quality Scoring Metrics | Sec 17 | Tier 1, 2 | 0–100 shkala bo'yicha qulaylik, maydon, issiqlik bahosi |
| 13 | R2: Health, Epidemics & Sanitation | Sec 75–77 | Tier 1, 2 | Qora o'lat tarqalish ehtimoli, kasallanish va davolanish vaqti |
| 14 | R3: Universal Damage Calculations | Sec 53–56 | Tier 1, 4 | `test_tier4_combat_damage_mitigation`, Skill va Quality ko'paytmasi |
| 15 | R3: Armor Mitigation Charts | Sec 57–58 | Tier 1, 2, 4 | Slash, Pierce, Blunt uchun defleksiya va yutish foizlari |
| 16 | R3: 3D Ranged Ballistics Physics | Sec 59–60 | Tier 1, 4 | Gravitatsiya, shamol og'ishi, kinetik energiya formulasi |
| 17 | R3: Military Morale System | Sec 61, 71 | Tier 1, 4 | Talafot shoki, komandir halokati vahima radiusi, chekinish |
| 18 | R3: Siege Engines & Voxel Destruction | Sec 65–66 | Tier 1, 2, 4 | Boshbuloq, katapulta portlash radiusi, venzel buzilish energiyasi |
| 19 | R3: Structural Stability & Bosses | Sec 70–72 | Tier 1, 2 | Osilib turgan venzel massasi chegarasi, 5 ta boss parametrlari |
| 20 | R4: Complete 24-Mineral Geological Catalog | Sec 27, 30 | Tier 1, 2, 3 | 24 ruda qatlam chuqurligi (0 dan -350m gacha), qattiqlik $H$ |
| 21 | R4: Mine Ceiling Stability & Cave-ins | Sec 31–33 | Tier 1, 4 | `test_tier4_mine_ceiling_stability`, $S_c$ indeksi, o'pirilish sharti |
| 22 | R4: Subterranean Gas & Ventilation Math | Sec 34–35 | Tier 1, 4 | $CH_4, CO_2, H_2S, CO$ to'planish tezligi va shamollatish oqimi |
| 23 | R4: 6-Biome Ecological Master Matrix | Sec 67–68 | Tier 1, 2, 3 | 6 ta biom harorat/yog'ingarchilik diapazoni, o'sish koeffitsiyenti |
| 24 | R4: Tundra Greenhouse Thermodynamics | Sec 69 | Tier 1, 4 | `test_tier4_greenhouse_thermodynamics`, Issiqlik yo'qotish va balans |
| 25 | R5: Feudal Factions & Diplomacy | Sec 83–85 | Tier 1, 2 | 4 fraksiya arxetipi, munosabatlar shkalasi (-100 dan +100 gacha) |
| 26 | R5: Tribute & Trade Logistics | Sec 84, 85 | Tier 1, 4 | Karvon yo'li tezligi, soliq to'lov talabi, savdo marshruti foydasi |
| 27 | R5: Espionage Mechanics | Sec 85 | Tier 1, 2 | Josuslik operatsiyalari muvaffaqiyat ehtimoli formulasi |
| 28 | R5: Steam P2P Co-op Network Protocol | Sec 114–118 | Tier 1, 2 | 20Hz tick, 11-baytli voxel delta, 10-baytli entity snapshot formati |
| 29 | R5: Concrete Godot 4 GDScript Classes | Sec 119–123 | Tier 1, 3 | GeologyManager, MinePhysicsServer, Greenhouse, Packet sinflari |
| 30 | Kingdom Pillars, Laws & Culture | Sec 0–9, 78–82 | Tier 1, 2 | 5 asosiy ustun, sulola davomiyligi, qonunlar kodeksi |
| 31 | Exploration, World Systems & UI/Saves | Sec 86–113 | Tier 1, 2 | Dunyo xaritasi, TAB boshqaruv oynasi, Save fayl JSON/binary strukturasi |
| 32 | Full Document Consistency & Verification | Barcha 133 bo'lim | Tier 1–4 | To'liq yakuniy tekshiruv, 0 ta qoldiq placeholder, sinxronlik |

---

## 4. Test Arxitekturasi va Katalogni Tashkil Etish

### 4.1. Fayllar Tuzilishi
```
voxel-lord/
├── MASTER_GDD.md               # Asosiy Game Design Document (Sinaluvchi hujjat)
├── prototype_sim.py            # Iqtisodiy va demografik prototip kodi
├── TEST_INFRA.md               # Ushbu test infratuzilmasi hujjati
├── TEST_READY.md               # Test natijalari va tayyorgarlik hisoboti
└── tests/
    ├── __init__.py             # Test to'plami moduli
    └── test_gdd_e2e.py         # 4-bosqichli avtomatlashtirilgan test kodi
```

### 4.2. Test Ishga Tushirish Ko'rsatmalari (Execution Instructions)

Standart Python 3.10+ yordamida testlarni ishga tushirish:

```powershell
# 1. Barcha testlarni to'liq ishga tushirish (Verifikatsiya)
python tests/test_gdd_e2e.py

# 2. Python unittest moduli orqali verbose rejimda:
python -m unittest tests/test_gdd_e2e.py -v

# 3. Muayyan bosqichni alohida tekshirish:
# Masalan, faqat Tier 4 (Matematik simulyatsiyalar):
python -m unittest tests.test_gdd_e2e.TestGDD_Tier4_Simulations -v
```

### 4.3. Natijalarni Baholash Qoidalari (Pass / Fail Criteria)
- **Muvaffaqiyat (PASS):** Formula hisob-kitoblari matematik jihatdan aniq ishlaydi, jadval tuzilishi to'g'ri, sectionlar to'liq.
- **Kutilgan qisman xatolar (Expected Failures on unexpanded milestones):** Kengaytirish jarayonida hali to'liq yakunlanmagan bo'limlar bo'yicha Tier 1 placeholder tekshiruvi aniqlagan nuqsonlar (masalan, matnda uchragan `va boshqalar` jumlasi) test tomonidan to'xtovsiz qayd qilinadi va orkestrator hamda implementor agentlarga eskalatsiya qilinadi.
