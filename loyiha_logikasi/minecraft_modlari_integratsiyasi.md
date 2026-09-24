# Voxel Lord: Feudal Realm — Minecraft Modlaridan Olingan Mexanikalar va Integratsiya

Ushbu hujjat "Voxel Lord: Feudal Realm" o'yini uchun Minecraft ekotizimidagi eng sara va chuqur mexanikali modlardan saralab olingan tizimlar to'plamidir. Bu tizimlar quruq ko'chirish emas, balki bizning 1st-person feodal hukmdor va voxel koloniya arxitekturasiga to'liq moslashtirilgan.

---

## 1. MINECOLONIES — Aholi, Shahar Qurilishi va Logistika

MineColonies — shahar boshqaruvi va avtonom NPC simulyatsiyasining eng yetakchi namunasi. Undan quyidagi yadrolar olinadi:

### 1.1. Quruvchi Fuqaro (Builder Citizen) va Arxitektura Chizmalari (Blueprints)
- **Muammo**: Hukmdor har bir uy, devor yoki omborni o'zi kubikma-kubik qo'yib chiqishi zerikarli mikromenejmentga aylanadi.
- **Yechim (MineColonies andozasi)**:
  - Hukmdor dunyoga yarim shaffof (hologramma) bino qolipini joylashtiradi (masalan: "Tosh minorali darvoza", "Nonvoyxona", "Dehqon uyi").
  - Quruvchi kasbidagi fuqaro (`Builder`) ombordan kerakli resurslarni (yog'och, tosh g'isht, taxta) o'zi olib keladi va blokma-blok binoni qura boshlaydi.
  - Hukmdor esa faqat resurslar yetkazib berilishini va strategik joylashuvni nazorat qiladi.

### 1.2. Kuryer / Logist Fuqaro (Deliveryman / Hauler)
- Qasr kengaygani sari shaxtadan chiqqan rudani temirchiga, daladan o'rilgan bug'doyni tegirmon va nonvoyga qo'lda tashish imkonsiz bo'ladi.
- Maxsus **Kuryer** fuqarolar aravalar yoki qoplar bilan uzoq nuqtalardan markaziy omborga va ustaxonalarga resurslarni avtomatik tashiydi.

### 1.3. Kasbiy Mahorat va Tajriba (Proficiency Tiers)
- Fuqarolar ish jarayonida o'z sohasida tajriba to'playdi:
  - **Shogird (Apprentice)**: Ishlash tezligi 1.0x, resurs yo'qotish ehtimoli bor.
  - **Usta (Journeyman)**: Tezlik 1.5x, asboblar kamroq eskiradi.
  - **Bosh Usta (Master)**: Tezlik 2.2x, qo'shimcha nodir mahsulotlar yaratish imkoniyati (+15% sifat).

---

## 2. TERRAFIRMACRAFT (TFC) — Realistik Geologiya, Metallurgiya va Fasllar

TFC — tirik qolish va tabiiy qonuniyatlarning eng chuqur modidir. Undan olingan qismlar:

### 2.1. Shaxta Xavfsizligi va Geologik Qatlamlar (Cave-ins, Support Beams & Strata) — [Milestone 13 da to'liq integratsiya qilindi]
- **O'pirilish va Qulash Fizikasi (`GeologyManager` & `voxel_world.gd`)**:
  - Subterranean chuqurlikda (`Y <= 24`) strukturali tosh yoki rudalar qazilganda, agar 4 blok radiusda `SupportBeam` (tayanch to'sini) bo'lmasa, 35% ehtimollik bilan g'or shiftining o'pirilishi (`cave_in`) yuz beradi.
  - Shift toshlari qulab yerga tushadi (`COBBLESTONE` vayronasi hosil bo'ladi) va 4 metr atrofidagi barcha jonivorlar hamda hukmdorga 25-45 crush zarari yetkazadi.
  - Tayanch to'sini (`support_beam.glb`) gorizontal 4 blok va vertikal 3 bloklik to'liq xavfsizlik zonasini ta'minlaydi.
- **Geologik Razvedka Asbobi (`ProspectorPick` & `prospector_pick.glb`)**:
  - TerraFirmaCraft ning afsonaviy geolog cho'kichi. Tosh yuzasiga urilganda 12 bloklik sferik radiusdagi barcha rudalarni aniqlaydi va sezuvchanlik xabarlarini beradi:
    - `NONE`: "Ushbu qatlamda rudalar topilmadi."
    - `TRACES` (1-3 ruda): "Yaqin atrofda mis/temir izlari sezilmoqda."
    - `SAMPLE` (4-8 ruda): "Istiqbolli ruda namunasi topildi."
    - `RICH` (9-15 ruda): "Yaqin atrofda boy ruda tomiri joylashgan!"
    - `MOTHERLODE` (16+ ruda): "Katta va serhosil ona kon (motherlode) topildi!"
- **Yer Osti Ruda Vagonchasi (`MineCart` & `mine_cart.glb`)**:
  - Og'ir rudalarni tashish uchun 30 ta slotli vagoncha. Shaxtyor va Kuryer (`HAULER`) fuqarolar tomonidan itariladi.
  - Kon relslari (`mining_rail`) ustida 2.5 barobar tezroq harakatlanadi (`RAIL_SPEED_MULTIPLIER = 2.5`).
- **Geologik Qatlamlar va Minerallar**:
  - Yuqori Cho'kindi Qatlam (`Y >= 20`): Ko'mir (`coal`), Tosh tuzi (`rock_salt`).
  - O'rta Metamorfik Qatlam (`Y >= 10`): Temir (`iron`), Kumush (`silver`), Mis (`copper`).
  - Chuqur Magmatik Qatlam (`Y < 10`): Oltin (`gold`), Qimmatbaho yoqut va zumradlar (`gems`).

### 2.2. Oziq-ovqat Saqlanishi va Chirish (Food Preservation & Spoilage) — [Milestone 10 da to'liq integratsiya qilindi]
- Go'sht, sut va pishirilgan taomlar yozda ochiq havoda 3-4 kunda ayniydi.
- **Saqlash usullari**:
  - **Tuzlash (Curing/Salting)**: Konlardan olingan tosh tuz (`rock_salt`) bilan go'shtni tuzlash (saqlash muddati 8 barobar uzayadi).
  - **Dudlash (Smoking)**: Maxsus dudxona (`smoke_rack.glb`) yordamida eman yog'ochi bilan dudlash (5 barobar uzayadi).
  - **Yerto'la (Cellar)**: Yer ostidagi sovuq qorong'i xonalarda (`Y <= 22`, tosh tomli) saqlash (chirish tezligini 75% ga sekinlashtiradi).

---

## 3. TINKERS' CONSTRUCT — Modulli Qurol va Asboblar Tizimi

Klassik "oddiy temir qilich" o'rniga, qurollar alohida qismlardan yasaladi va ularning har biri alohida xususiyat beradi:

### 3.1. Qurol Anatomiyasi
1. **Tig' / Bosh qism (Blade / Head)**: Asosiy zarar va qazish tezligini belgilaydi.
   - *Temir*: Balanslashgan, o'rtacha o'tkir.
   - *Po'lat*: Yuqori zarar va o'tkirlik.
   - *Oltin*: Yuqori sehr o'tkazuvchanligi.
2. **Gardis / Bog'lovchi (Crossguard / Binding)**: Chidamlilik va maxsus himoyani belgilaydi.
3. **Dasta (Handle / Rod)**: Umumiy chidamlilik multiplikatori va silkinishni kamaytirish.

### 3.2. Sandon (Anvil)da Zarb Qilish
- Eritilgan temir va po'lat shunchaki dastgohda 1 soniyada qurolga aylanmaydi.
- Sandonda bolg'a bilan zarb qilinadi, so'ngra suv yoki moyda toblanadi (Quenching). Bu qurol sifatini (Quality: Common, Fine, Masterwork) oshiradi.

---

## 4. APOTHEOSIS & ENIGMATIC LEGACY — Sehirlar, Affikslar va Noyoblik

Foydalanuvchining aniq talabi: Oddiy sehirlar materiallar va mob droplaridan sehrgarlar tomonidan yasaladi, noyob afsonaviy narsalar faqatgina qaroqchilar va xazinalardan tushadi.

### 4.1. Sehirlar Tasnifi va Darajalari
Barcha sehirlar I dan V gacha darajaga ega bo'ladi:
- **Sharpness (O'tkirlik I-V)**: Kesuvchi qurollar uchun qo'shimcha jismoniy zarar.
- **Unbreaking (Mustahkamlik I-III)**: Qurol eskirish ehtimolini kamaytiradi.
- **Efficiency (Tezkorlik I-V)**: Kon va o'tin chopish tezligini oshiradi.
- **Protection (Himoya I-IV)**: Sovutlar uchun umumiy zararni pasaytirish.
- **Feather Falling (Yengil Qadam I-IV)**: Balandlikdan sakrashdagi zararni yo'qotish.
- **Power (Kuch I-V)**: Kamon o'qining uchish kuchi va zararini oshiradi.

### 4.2. Oddiy Sehirlarni Yasash (Sehrgar Laboratoriyasi)
- Shaharda **Sehrgar (Enchanter / Alchemist)** fuqarosi bo'ladi.
- Sehr tayyorlash uchun kerak bo'ladi:
  - *Sehrli Qog'oz / Runa*: Teridan tayyorlangan pergament + qimmatbaho tosh kukuni.
  - *Mob droplari*: Qaroqchilardan tushgan qon tomchisi, o'rgimchak ipi, zahar, bo'ri tishi.
  - *O'simliklar*: Yovvoyi dorivor giyohlar va ildizlar.
- Sehrgar ularni qaynatib, pergamentga sehrli runa bitadi. Hukmdor bu runani sandonda qurol yoki sovutga qo'shadi.

### 4.3. Noyob va Afsonaviy Sehrlar (Faqat Qaroqchilar Boshliqlari va Xazinalardan Tushadi)
Ushbu sehirlarni hech qaysi sehrgar yasay olmaydi, ular faqat dunyoda topiladi:
1. **`Dragon's Breath` (Ajdaho Nafasi)**: Har bir qilich zarbasida dushmanni 4 soniya olovda yondiradi.
2. **`Windstrider` (Shamol Hukmdori)**: Harakatlanish tezligini +30% ga oshiradi va suv ustida yurish imkonini beradi.
3. **`Vampiric Leech` (Qon So'rgich)**: Dushmanga berilgan zararning 15% miqdorida Hukmdorning jonini davolaydi.
4. **`Thunderstrike` (Yashin Urishi)**: Kamondan otilgan o'q tushgan yerga yashin chaqirib, atrofdagi barcha qaroqchilarga ommaviy zarar beradi.
5. **`Fortress Heart` (Qal'a Yuragi)**: Sovutga o'rnatilganda, Hukmdorning joni 25% dan pastga tushsa, 5 soniyaga barcha zararlarni 90% ga qaytaruvchi qalqon hosil qiladi.

---

## 5. FARMER'S DELIGHT — Feodal Qishloq Xo'jaligi va Oshxona

Oddiygina "non yeb qorin to'yg'azish" o'rniga, to'yimli va murakkab feodal taomlar:

### 5.1. Ekinlar Turfaligi
- Bug'doy (Wheat), Arpa (Barley), Karam (Cabbage), Piyoz (Onion), Sabzi (Carrot), Zaytun (Olive).
- Boyitilgan Qora Tuproq (`Rich Compost Soil`): Hayvon go'ngi va o'simlik qoldiqlaridan tayyorlanadi, ekinlar unda 2 barobar tezroq unib chiqadi.

### 5.2. Qozonda Qaynatilgan Taomlar (Cooking Pot Meals)
- **Qovurilgan Go'sht va Sabzavotlar**: Qorinni 40% ga to'yg'azadi va +20% chidamlilik beradi.
- **Qirollik Sho'rvasi (Hearty Stew)**: Qorinni to'liq to'yg'azadi, fuqarolarning ma'naviyatini +30 ga ko'taradi va 1 kun davomida sovuq qotishdan himoya qiladi (Thermal Resistance).

---

## 6. CREATE MOD — Suv va Shamol Mexanikasi (Feodal Avtomatizatsiya)

Medieval davrning haqiqiy muhandisligi:
1. **Suv Tegirmoni (Water Wheel)**: Daryo oqimiga o'rnatiladi. Aylanma harakat energiyasini venzelli g'ildiraklar orqali uzatadi.
2. **Shamol Tegirmoni (Windmill)**: Qir va tepaliklarda quriladi.
3. **Mexanik Bolg'a (Mechanical Trip Hammer)**: Suv yoki shamol kuchi bilan tinimsiz urilib, temir va ruda quymalarini qo'l mehnatini sarflamasdan yanchadi.
4. **Un Tegirmon Toshlari (Millstones)**: Bug'doyni sanoat darajasida unga aylantiradi.

---

## 7. AMALGA OSHIRILGAN AMALIY MODULLAR (Joriy Holat)
- [x] **Apotheosis & Enigmatic Legacy**: `EnchantmentManager` (`scripts/magic/enchantment_manager.gd`), `EnchanterTable` (`scripts/world/enchanter_table.gd`), `BanditWarlord` boss (`scripts/entities/bandit_warlord.gd`), afsonaviy affikslar (`dragons_breath`, `vampiric_leech`, `thunderstrike`, `windstrider`, `fortress_heart`).
- [x] **Create Mod**: `Windmill` (`scripts/world/windmill.gd` & `windmill.glb`) kinetik shamol tegirmoni, passiv 32 RPM aylanish va 2x un unumdorligi.
- [x] **Farmer's Delight**: `CookingPot` (`scripts/world/cooking_pot.gd` & `cooking_pot.glb`) quyma cho'yan qozon, multi-ingredient "Hearty Hunter Stew", "Vegetable Broth", "Noble Feast" taomlari (ochlik + issiqlik/gipotermiya qarshiligi).
- [x] **MineColonies Mudofaa Signali**: `Royal War Horn` (`war_horn.glb`), Hukmdor gorn chalishi bilan tinch aholining Qasr burchagiga (Bunker Zone) chekinishi va soqchilarning jangovar shay holatga o'tishi.
- [x] **MineColonies Bino Chizmalari (Blueprints)**: `BlueprintConstruction` (`scripts/world/blueprint_construction.gd`) yarim shaffof (hologramma) golografik bino joylashtirish, bosqichma-bosqich material yetkazish va avtomatik vokselli bino qurilishi.
- [x] **MineColonies Quruvchi Fuqaro (`Role.BUILDER`)**: Fuqaro omborlardan kerakli resurslarni olib, chizmalar ustida bolg'alab qurilishni amalga oshiradi.
- [x] **MineColonies Logist Kuryer (`Role.HAULER`)**: `wheelbarrow.glb` g'ildirakli arava bilan jihozlangan maxsus kuryer; uzoq nuqtalardan resurslarni qirollik omboriga tashiydi va qurilish maydonlariga material yetkazadi.
- [x] **RimWorld "Do Until X" Ishlab Chiqarish Limitlari**: `SupplyChain` va `CraftingMenu` da resurslar tugab ketishining oldini oluvchi kvotalar (`DO_UNTIL_X`, `DO_FOREVER`, `PAUSED`).
- [x] **Tinkers' Construct Sandon (Modular Anvil)**: `Anvil` (`scripts/world/anvil.gd` & `anvil.glb`) ikki shoxli temirchilik sandoni, modulli qurol yasash (Tig' / Gardis / Dasta kombinatsiyasi: Temir, Po'lat, Oltin, Qattiq yog'och, Teri), zarb qilish va sifat multiplikatorlari.
- [x] **TerraFirmaCraft Oziq-ovqat Saqlash & Sovuq Yerto'la**: `FoodPreservationManager` (`scripts/economy/food_preservation_manager.gd` & `smoke_rack.glb`), go'shtni tosh tuzi bilan tuzlash (8x saqlash muddati), dudxonada dudlash (5x saqlash muddati) va yer osti tabiiy sovuq yerto'lasida chirishni 75% ga kamaytirish.
- [x] **Create Mod Suv G'ildiragi (Kinetic Water Wheel)**: `WaterWheel` (`scripts/world/water_wheel.gd` & `water_wheel.glb`), 24 RPM, 256 Stress Units (SU) kinetik quvvat tarmog'i, daryo oqimi va kanallardan passiv aylanma mexanik energiya ishlab chiqarish.
- [x] **Create Mod Mexanik Tegirmon Toshlari (Millstone)**: `Millstone` (`scripts/world/millstone.gd` & `millstone.glb`), 32 SU quvvat sarflaydi, bug'doyni inson omilisiz avtomatik ravishda 200% unumdorlikda (1 bug'doy -> 2 non) un va rasionga aylantiradi.
- [x] **Create Mod Sanoat Mexanik Bolg'asi (Mechanical Trip Hammer)**: `TripHammer` (`scripts/world/trip_hammer.gd` & `trip_hammer.glb`), 64 SU quvvat sarflaydi, temir va mis rudalarini avtomatik yanchib maydalaydi (`crushed_iron`), domna pechida eritilganda 2 barobar ko'p temir quyma beradi (1 ruda -> 2 quyma).
- [x] **Farmer's Delight Organik Kompost Qutisi (Compost Bin)**: `CompostBin` (`scripts/world/compost_bin.gd` & `compost_bin.glb`), o'simlik va oziq-ovqat chiqindilaridan (4 ta chiqindi -> 1 ta o'g'it) boyitilgan qora tuproq (`rich_soil_compost`) o'g'iti ishlab chiqarish.
- [x] **Farmer's Delight Almashlab Ekish va Tuproq Unumdorligi (Crop Rotation Engine)**: `CropManager` (`scripts/world/crop_manager.gd`), ko'p turli ekinlar (Bug'doy, Karam, Piyoz, Sabzi), boyitilgan tuproqda 2x unib chiqish, almashlab ekishda +25% tezlik va hosil bonusi, monomadaniyatli tuproq toliqishiga qarshi chora.
- [x] **Farmer's Delight Oshxona Qirqish Taxtasi (Cutting Board)**: `CuttingBoard` (`scripts/world/cutting_board.gd` & `cutting_board.glb`), oshpazlik pichog'i bilan sabzavot va go'shtlarni maydalash (`sliced_cabbage`, `minced_beef`, `diced_onion`) hamda qozonda elita taomlar ("Rich Cabbage Stew", "Shepherd's Pie") pishirish.
- [x] **TerraFirmaCraft Geologiya va O'pirilish Fizikasi**: `GeologyManager` (`scripts/world/geology_manager.gd`), yer osti qulash fizikasi (`cave_in`), tayanch to'sinlari (`support_beam.glb`), geologik razvedka cho'kichi (`prospector_pick.glb`), yer osti vagonchasi (`mine_cart.glb`), kon relslari va xavfsizlik chirog'i (`mining_lantern.glb`).
- [x] **Apotheosis Boss Affikslari & Chempion Modifikatorlari**: `ApotheosisManager` (`scripts/magic/apotheosis_manager.gd`), qaroqchilar boshlig'iga (`BanditWarlord`) protsedural nomlar va unvonlar berish, 6 ta o'limli affiks (`INFERNAL`, `ARMORED`, `SWIFT`, `VAMPIRIC`, `TEMPEST`, `TITAN`), maxsus zararlar va jarohat qaytarish (lifesteal).
- [x] **Apotheosis Qimmatbaho Toshlarni Qirqish va Soket Tizimi (Lapidary & Sockets)**: `GemCuttingTable` (`scripts/world/gem_cutting_table.gd` & `gem_cutting_table.glb`), xom yoqut, sapfir, topaz va chuqurlik toshlarini qirqish, qurol va sovutlarga soket (slot) ochib toshlarni o'rnatish, yechib olish, hamda g'alaba kubogi (`boss_trophy.glb` - qirollik ma'naviyatiga +10).
- [x] **3D Blender 5.2 Modellar**: Jami 34 ta to'liq modellashtirilgan va import qilingan GLB 3D aktivlar (`gem_cutting_table.glb` va `boss_trophy.glb` qo'shildi).




