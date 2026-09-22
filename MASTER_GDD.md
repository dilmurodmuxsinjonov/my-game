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

# 10. ITEM TIZIMI

Har bir ashyo quyidagi atributlarga ega:
`ItemID, Name, Category, Weight, StackSize, Durability, Quality, Value, Rarity, Tags`.

---

# 11. ITEM QUALITY (BUYUM SIFATI)

Quality darajalari:
`Poor → Common → Fine → Masterwork → Royal → Legendary`
Yuqori sifat qurol zararini, asbob tezligini, kiyim mustahkamligini va savdo narxini oshiradi.

---

# 12. ASBOBLAR PROGRESSIYASI (TOOL PROGRESSION)

`Stone (Tosh) → Copper (Mis) → Bronze (Bronza) → Iron (Temir) → Steel (Po'lat) → Damascus Steel (Damashq Po'lati) → Runic / Legendary (Runik)`.

---

# 13. CRAFTING (YASASH) TIZIMI

1. **Hand Crafting:** Oddiy mayda vositalar va mash'alalar.
2. **Workstation Crafting:** Temirchilik, Duradgorlik, Tegirmon, Nonvoyxona, To'quvchilik, Alkimyo dastgohlari.
3. **Citizen Production:** O'yinchi retsept va kvota belgilaydi, fuqarolar avtomatik ishlab chiqaradi.

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

# 36. DEHQONCHILIK VA EKINLAR

Urug' → Yumshoq tuproq → Namlik → Harorat → O'sish davri → Begona o'tlar/kasalliklar → Hosilni yig'ish.

---

# 37. TUPROQ UNUMDORLIGI VA ALMASHINLAB EKISH

Tuproq unumdorligi (Fertility) har hosildan keyin pasayadi. Bir maydonga doimiy bir xil ekin ekish man etiladi. Almashlab ekish (Bug'doy → Mosh/Dukkakli → Bedapoya) va chirindi o'g'it unumdorlikni tiklaydi.

---

# 38. SUG‘ORISH TIZIMI (IRRIGATION)

Daryo yoki buloq → Ariqlar va kanallar → Sug'oriladigan polizlar. Sug'orish hosildorlikni +40% ga oshiradi.

---

# 39. CHORVACHILIK (LIVESTOCK)

Chicken (Tuxum, Pat), Sheep (Jun, Go'sht), Cow (Sut, Teri), Pig (Go'sht, Yog'), Horse (Minish, Arava tortish).

---

# 40. OZIQ-OVQAT AYNISH MUDDATLARI

- Xom go‘sht/baliq: 2–3 kun;
- Sut: 1–2 kun;
- Sabzavot va mevalar: 5–7 kun;
- Non: 6–8 kun;
- Don va bug'doy: 1–2 yil.

---

# 41. SAQLASH USULLARI (FOOD PRESERVATION)

1. **Tuzlash (Salting):** Halite tuzi yordamida 1 yilgacha saqlash.
2. **Dudlash (Smoking):** Dudxonada dudlangan qazi va baliqlar (20–30 kun, baxt +15%).
3. **Quritish (Drying):** Qoqi mevalar va quritilgan qo'ziqorinlar.
4. **Muzxona / Podval (Cold Cellar):** Qishki muz bloklari bilan sovitiladigan ombor.

---

# 42. OMBORXONALAR VA MAXSUS FILTRLAR

- Granary: Don va un;
- Cold Cellar: Oziq-ovqatlar;
- Armory: Qurol-yarog' va sovutlar;
- Warehouse: Qurilish materiallari va xomashyo.

---

# 43. YUK TASHISH LOGISTIKASI (HAULING & RESERVATION)

Bir ashyoni ikki fuqaro bir vaqtda talashmasligi uchun Item Reservation tizimi ishlaydi. Ustuvorlik asosida aravalar yuk tashiydi.

---

# 44. YO‘LLAR VA TRANSPORT SAMARADORLIGI

- **Tuproq yo'l:** Harakat tezligi +15%.
- **Tosh yotqizilgan ko'cha:** Tezlik +35%.
- **Qirollik shoh ko'chasi:** Tezlik +60%, aravalar maksimal tezlikda harakatlanadi.

---

# 45. IQTISODIYOT ASOSI

`Xomashyo ishlab chiqarish → Qayta ishlash → Tayyor mahsulot → Iste'mol / Ichki bozor / Eksport`.

---

# 46. BUG‘DOY VA NON ZANJIRI

`Bug‘doy ekish → O'roq bilan o'rish → Shamol/Suv tegirmoni (Un) → Nonvoyxona (Non) → Aholi ta'minoti`.

---

# 47. TEMIR VA QUROL ZANJIRI

`Temir rudasi + Ko'mir → Eritish pechi → Temir quyma → Temirchilik ustaxonasi → Bolg'a, o'roq, qilich, nayzalar`.

---

# 48. VALYUTA TIZIMI

100 Kumush Tanga (Silver) = 1 Oltin Tanga (Gold).
Kundalik ichki savdo va xizmatlar kumushda, yirik davlat xaridlari, soliqlar va xalqaro savdo oltinda yuritiladi.

---

# 49. BOZOR MEXANIKASI VA DINAMIK NARXLAR

Narx = `BaseValue × Supply (Taklif) × Demand (Talab) × Reputation (Obro')`. Ortiqcha mahsulot arzonlashadi, taqchil resurs qimmatlashadi.

---

# 50. SAVDO KARVONLARI

Karvonlar shaharga oziq-ovqat, ekzotik matolar, qurol-aslahalar va noyob minerallar olib keladi va mahalliy ortiqcha mollarni sotib oladi.

---

# 51. SOLIQ QONUNCHILIGI (TAX SYSTEM)

Hukmdor soliqlarni 0% dan 40% gacha belgilaydi:
- Past soliq (<10%): Fuqarolar juda xursand, ammo xazina sekin to'ladi.
- O'rtacha soliq (10–20%): Muvozanatli holat.
- Yuqori soliq (>25%): Xazina tez to'ladi, biroq xalq ruhiyati tushadi, jinoyat va qochishlar (emigratsiya) ortadi.

---

# 52. FUQAROLAR RUHIYATI (MORALE)

Ko'rsatkich: 0–100.
Faktorlar: Taom xilma-xilligi, issiq uy, xavfsizlik, dam olish maskanlari, adolatli soliqlar, o'lim va kasalliklar yo'qligi, bayramlar.

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
