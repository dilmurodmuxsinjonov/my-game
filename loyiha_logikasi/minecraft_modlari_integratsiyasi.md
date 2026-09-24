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

### 1.4. Shahar Kengashi (Town Hall), Qirollik Xazinasi (Treasury Vault) va Garnizon Soqchilar Posti (Guard Post) — [Milestone 17 da to'liq integratsiya qilindi]
- **Shahar Kengashi va Hududiy Chegaralar (`town_hall.gd`, `town_hall_desk.glb`)**:
  - Koloniya markazi va hududiy boshqaruv yadrosi. Qishloq darajalari:
    - *Hamlet (Qishloqcha)*: 32m radius, 8 nafar fuqaro chegarasi.
    - *Village (Qishloq)*: 48m radius, 20 nafar fuqaro chegarasi.
    - *Township (Shaharcha)*: 64m radius, 45 nafar fuqaro chegarasi.
    - *Royal City (Qirollik Shahri)*: 96m radius, 100 nafar fuqaro chegarasi.
  - Fuqarolarni ro'yxatga olish, turar-joy hajmi chegaralari va avtomatlashtirilgan kasbiy taqsimot.
- **Qirollik Xazinaxonasi (`treasury_vault.gd`, `treasury_vault.glb`)**:
  - Oltin va kumush tangalar xazinasi. Kunlik feodal soliqlarni yig'ish, fuqarolar kayfiyatiga (morale) ta'sir, garnizon soqchilarining maoshi to'lovi va bayram subsidiyalari. Agar xazina soqchilar maoshini to'lay olmasa, garnizon ish tashlaydi (mudofaa 50% ga pasayadi).
- **Garnizon Soqchilar Posti (`guard_post.gd`, `guard_post.glb`)**:
  - 16 metr mudofaa radiusi, halberd va qalqonli soqchilar saflanish bonusi (+15 mudofaa balli har bir soqchi uchun) va bosqinchi banditlar yaqinlashganda ogohlantirish signali.

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

### 2.3. Bloomery Domna Pechi, Piroliz Ko'mir Chuquri va Qolipga Quyish (Bloomery, Charcoal Pit & Crucible Casting) — [Milestone 15 da to'liq integratsiya qilindi]
- **Yopiq Piroliz Ko'mir Chuquri (`CharcoalPit` & `charcoal_pit.glb`)**:
  - Haqiqiy o'rta asrlarda temirni oddiy o'tin bilan eritib bo'lmaydi (harorat yetmaydi). Maxsus yuqori kaloriyali yog'och ko'miri (`charcoal`) talab qilinadi (1450°C gacha yonadi).
  - Yog'och xodalari yer osti chuquriga yoki tepalikka taxlanib, usti nam loy va tuproq qatlami bilan germetik yopiladi (`is_sealed = true`).
  - Kislorodsiz sekin tutab yonish (piroliz) jarayonida 4 ta log yog'ochdan 4 ta sifatli toza ko'mir olinadi. Agar chuqur ochiq qolsa, barcha o'tin kulga aylanadi (`ash`).
- **Bloomery Qaytarish Pechi (`Bloomery` & `bloomery.glb`)**:
  - O'tga chidamli tosh va loydan qurilgan baland shaft pechi. Havoni majburiy puflagich (bellows) tuyere orqali kiritadi.
  - 1200°C - 1450°C haroratda temir oksidlarini qaytarib, shlak bilan aralash g'ovakli metall to'pini — **Temir Blumi (`iron_bloom`)** ni hosil qiladi (2 ta temir rudasi + 2 ta ko'mir -> 1 ta temir blumi).
- **Blumni Sandonda Zarb Qilish va Qotirish (`Anvil` va `TripHammer`)**:
  - Qaynoq g'ovakli blumni sandonda og'ir bolg'a bilan tinimsiz urib, ichidagi suyuq silikat shlak siqib chiqariladi va zich, toza **Bolg'alangan Temir Quyma (`wrought_iron_ingot`)** olinadi.
  - Create Mod ning avtomatik kinetik mexanik bolg'asi (`TripHammer`) esa bu jarayonni inson omilisiz avtomatlashtiradi!
- **O'tga Chidamli Sopol Trogel va Qolipga Quyish (`Crucible` & `crucible.glb`)**:
  - Rangli metallar (Mis va Qalay) nisbatan past haroratda eriydi.
  - Sopol tigel pech ustiga qo'yiladi: 7 ta mis + 1 ta qalay qo'shilib, 8 ta suyuq bronza (`molten_bronze`) qotishmasi eritiladi (87.5% Cu, 12.5% Sn).
  - So'ngra oldindan pishirilgan sopol qoliplarga (`ceramic_mold`) quyilib, to'g'ridan-to'g'ri bronza qilich tig'i (`cast_bronze_blade`), cho'kich boshi (`cast_bronze_pickaxe`) yoki bolta quyiladi.

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

### 3.3. Suyuq Metall Eritish Pechi (Smeltery), Qolip Stoli (Casting Table) va Quyish Havzasi (Casting Basin) — [Milestone 18 da to'liq integratsiya qilindi]
- **Tinkers' Smeltery Multiblok Nazoratchisi (`SmelteryController`, `smeltery_controller.glb`)**:
  - O'tga chidamli tosh g'ishtlar (`seared_brick`) dan barpo etiladigan yuqori hajmli suyuq metall qozoni (36 birlik sig'im).
  - Lava yoki yuqori kaloriyali ko'mir yordamida 1600°C gacha qiziydi.
  - Xom rudalarni 2 barobar ko'proq metall hosil qilgan holda eritadi (1 ta ruda -> 2 ta suyuq birlik).
- **Metallurgik Qotishma Tizimi (`AlloyManager`)**:
  - *Bronza*: 3 birlik Mis + 1 birlik Qalay -> 4 birlik Suyuq Bronza ($\ge 950$°C).
  - *Tozalangan Po'lat*: 1 birlik Temir + 1 birlik Uglerod/Ko'mir gazi -> 1 birlik Suyuq Po'lat ($\ge 1450$°C).
  - *Elektrum (Qirollik oltin qotishmasi)*: 1 birlik Oltin + 1 birlik Kumush -> 2 birlik Suyuq Elektrum ($\ge 1000$°C).
- **Quyish Havzasi (`CastingBasin`, `casting_basin.glb`)**:
  - 9 birlik suyuq metallni qabul qiladi va sovutish vaqtidan so'ng yaxlit qattiq metall blokini (`bronze_block`, `iron_block`, `steel_block`) beradi.
- **Qolip Stoli (`CastingTable`, `casting_table.glb`)**:
  - Almashtiriladigan sopol va bronza qoliplarni o'z ichiga oladi:
    - *Ingot qolipi (1 birlik)*: Metall quymalari quyish.
    - *Qilich tig'i qolipi (2 birlik)*: Qilich tig'ini to'g'ridan-to'g'ri bir xil aniqlikda quyish.
    - *Cho'kich boshi qolipi (3 birlik)*: Kon cho'kichi boshini quyish.
    - *Bolta boshi qolipi (3 birlik)*: O'tinchi boltasi boshini quyish.

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
5. **Mexanik Konveyer Lentasi (Mechanical Conveyor Belt & `conveyor_belt.glb`)**: Kinetik vallar orqali 2.0 m/s tezlikda harakatlanuvchi mustahkam charm lenta (16 SU sarflaydi); shaxtadan chiqqan rudalarni, domna pechi quymalarini va un qoplarini fuqarolarsiz avtomatik ustaxonalarga tashiydi.
6. **Gravitatsion Voronka va Truba (Gravity Chute & `chute.glb`)**: Tabiiy tortishish kuchi hisobiga 4 ta narsa/soniya tezlikda vertikal pastga resurslarni tushirib beruvchi voronkali jez/temir truba (0 SU talab qiladi); baland silos omboridan donni to'g'ridan-to'g'ri tegirmon toshiga uzatadi.
7. **Sanoat Mexanik Pressi (Mechanical Press & `mechanical_press.glb`)**: Og'ir eksentrik porshenli shtamplash pressi (48 SU sarflaydi); temir quymalarni og'ir ritsar sovuti plastinalariga (`iron_sheet`), mis quymalarini tomlar uchun tunukalarga (`copper_sheet`), va oltin quymalarini qirollik oltin tangalariga (`gold_coins` — 1 oltin quyma = 10 ta tanga) shtamplab zarb qiladi!

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
- [x] **TerraFirmaCraft Bloomery Domna Pechi**: `Bloomery` (`scripts/world/bloomery.gd` & `bloomery.glb`), 1200°C - 1450°C yuqori haroratli kimyoviy qaytarish pechi, temir rudasi va yog'och ko'miridan g'ovakli temir blumi (`iron_bloom`) ishlab chiqarish.
- [x] **TerraFirmaCraft Piroliz Ko'mir Chuquri**: `CharcoalPit` (`scripts/world/charcoal_pit.gd` & `charcoal_pit.glb`), yer osti tuproq va loy bilan germetik yopilgan piroliz chuquri, 4 ta o'tindan 4 ta toza yuqori haroratli yog'och ko'miri (`charcoal`) tayyorlash.
- [x] **TerraFirmaCraft Sopol Tigel va Qolipga Bronza Quyish**: `Crucible` (`scripts/world/crucible.gd` & `crucible.glb`), mis va qalayni 88/12 nisbatda eritib suyuq bronza tayyorlash va sopol qoliplarga quyib qurol/asbob tig'larini quyish.
- [x] **Blum Zarb Qilish va Avtomatlashtirish**: `Anvil` va `TripHammer` orqali temir blumini bolg'alab silikat shlakni chiqarish va zich bolg'alangan temir quymalar (`wrought_iron_ingot`) ishlab chiqarish.
- [x] **Create Mod Mexanik Konveyer Lentasi (Conveyor Belt)**: `ConveyorBelt` (`scripts/world/conveyor_belt.gd` & `conveyor_belt.glb`), 16 SU quvvat sarflaydi, 2.0 m/s tezlikda resurslarni stanoklar va omborlar o'rtasida avtomatik tashish.
- [x] **Create Mod Gravitatsion Truba (Gravity Chute)**: `Chute` (`scripts/world/chute.gd` & `chute.glb`), 0 SU energiya talab qiluvchi tortishish kuchi trubasi, 4 ta narsa/soniya tezlikda yuqoridagi don siloslaridan pastdagi tegirmon toshlariga resurslarni tushirish.
- [x] **Create Mod Sanoat Shtamplash Pressi (Mechanical Press)**: `MechanicalPress` (`scripts/world/mechanical_press.gd` & `mechanical_press.glb`), 48 SU quvvat sarflaydi, temir quymalardan sovut plastinalari (`iron_sheet`), mis tunukalari (`copper_sheet`) va oltin quymalardan qirollik oltin tangalarini (`gold_coins` — 1:10) shtamplab zarb qilish.
- [x] **MineColonies Shahar Kengashi & Qirollik Xazinasi (Town Hall & Treasury)**: `TownHall` (`town_hall_desk.glb`), `TreasuryVault` (`treasury_vault.glb`), `GuardPost` (`guard_post.glb`) — 4 ta rivojlanish darajasi (Hamlet -> Royal City), feodal soliqlar va garnizon oyliklari.
- [x] **Tinkers' Construct Suyuq Metall Pechi & Quyish Tizimi (Smeltery & Casting)**: `SmelteryController` (`smeltery_controller.glb`), `AlloyManager`, `CastingBasin` (`casting_basin.glb`), `CastingTable` (`casting_table.glb`) — 36 birlik suyuq metall qozoni, Bronza, Po'lat va Elektrum qotishmalari, quyish havzasi va asbob qoliplari.
- [x] **Tashqi Qirollik O'lponi va Logistika Outpostlari (Crown Tribute & Outposts)**: `CrownTribute` (`tax_sheriff_cart.glb`), `Outpost` (`outpost_banner.glb`), `FuneralPyre` (`funeral_pyre.glb`) — Tashqi soliq bosimi, uzoq kon logistikasi va sanitariya gulxani.
- [x] **3D Blender 5.2 Modellar**: Jami **49 ta to'liq modellashtirilgan va import qilingan GLB 3D aktivlar**.

---

## 8. O'XSHASH JANR GIGANTLARIDAN OLINGAN LOGISTIKA VA IQTISODIYOT (Medieval Dynasty, Bellwright, Manor Lords, RimWorld)

### 8.1. Tashqi Qirollik O'lponi va Qirol Noibi (Royal Crown Tribute & Sheriff) — [Medieval Dynasty / Bellwright]
- **Muammo**: O'yinda tashqi iqtisodiy bosim bo'lmasa, hukmdor cheksiz resurs yig'ib tezda zerikib qoladi.
- **Yechim (`CrownTribute` & `tax_sheriff_cart.glb`)**:
  - Har mavsum (7 o'yin kuni) oxirida poytaxtdan Qirol Noibi (Crown Sheriff) qurollangan karvonda tashrif buyuradi.
  - O'lpon bazaviy to'lov (40 oltin) + har bir bino uchun 5 oltin + har bir fuqaro uchun 2 oltindan iborat.
  - Agar xazinada pul bo'lmasa va 2 marta o'lpon to'lanmasa, Qirollik jazo ekspeditsiyasi (Crown Punitive Expedition) qo'shin tortib keladi va qasrni qamal qiladi.

### 8.2. Uzoq Masofali Kon Outposti va Karvon Tizimi (Outpost & Pack Caravan) — [Bellwright / Manor Lords]
- **Muammo**: 500-1000m uzoqlikdagi tog' shaxtalariga fuqarolarni har kuni qasrdan piyoda qatnatish vaqtni behuda sarflaydi.
- **Yechim (`Outpost` & `outpost_banner.glb`)**:
  - Kon yonida kichik chegara posti o'rnatiladi. Konchilar shu yerda tunab qoladi.
  - Qazilgan ruda Outpost mahalliy omborida to'planadi (minimal chegara: 10 ta ruda).
  - Me'yor to'plangach, avtomatik ravishda otli yuk karvoni yo'lga chiqib markaziy qasr omboriga yetkazadi.

### 8.3. Muqaddas Jasad Yoqish Gulxani va Epidemiya Qarshiligi (Funeral Pyre) — [RimWorld / Going Medieval]
- **Muammo**: Katta jang yoki kasallik paytida o'nlab jasadlarni bittalab ko'mishga vaqt yetmaydi; ochiqda qolgan murdalar shahar bo'ylab kasallik (miasma) tarqatadi.
- **Yechim (`FuneralPyre` & `funeral_pyre.glb`)**:
  - Tosh platformali marosim o'chog'i. Jasadlar o'tin bilan birga muqaddas olovda yondiriladi.
  - Sanitariya tozalanadi, epidemiya xavfi yo'qoladi, marhumlar ehtirom qilingani uchun aholi ruhiyatiga +10 morale beriladi va Qonli Oyda zombi tirilishi xavfi 0% ga tushiriladi.

---

## 9. Manor Lords & Bellwright Integratsiyasi — Fuqaro Lashkarlari, Qurollar Zaxiraxonasi va Hovli Qo'shimchalari (Milestone 20)

### 9.1. Qurollar Zaxiraxonasi va Fuqarolarni Safarbar Qilish (Militia Armory) — [Manor Lords / Bellwright]
- **Muammo**: Bosqin paytida oddiy dehqonlar himoyasiz qolib o'lib ketadi yoki jangga qo'shilmaydi.
- **Yechim (`MilitiaArmory` & `armory_rack.glb`)**:
  - Og'ir eman yog'ochidan yasalgan qurol-yarog' ustuni (`armory_rack`). Nayzalar, qalqonlar, temir dubulg'alar va yoylar zaxiralanadi.
  - `muster_squad()`: Hukmdor xavf tug'ilganda fuqarolarni zudlik bilan harbiy xizmatga chaqiradi. Fuqarolar ombordan nayza, qalqon va dubulg'a olib qurollanadi (HP +40, Armor +25, Attack +18).
  - `demobilize_squad()`: Jangdan so'ng askarlar qurollarini armoryga qaytarib topshiradi va o'z ishlariga qaytadi. Omon qolgan faxriylar shahar ruhiyatini oshiradi.

### 9.2. Dehqon Xonadoni Hovli Qo'shimchalari (Burgage Plot Extensions) — [Manor Lords]
- **Muammo**: Shahar uylari faqat yotoqxona vazifasini o'taydi, oilalar mustaqil oziq-ovqat ishlab chiqarmaydi.
- **Yechim (`BurgagePlot` & `burgage_coop.glb`)**:
  - Har bir dehqon xonadoni o'z hovlisiga maxsus ishlab chiqarish tarmog'ini o'rnatishi mumkin:
    - `CHICKEN_COOP`: Har kuni passiv 3 ta yangi tuxum va 1 ta pat beradi.
    - `GOAT_PEN`: Har kuni passiv 2 ta teri va 1 ko'za yangi sut beradi.
    - `VEGETABLE_GARDEN`: Sabzi, karam va piyoz hosili beradi.
  - Ratsion xilma-xilligi (+15 oilaviy baxt) va Qirollik g'aznasiga qo'shimcha yer solig'i (+1 tanga/kun) ta'minlanadi.

### 9.3. Harbiy Jang Mashqi Mankeni (Combat Training Dummy) — [Bellwright / Kingdom Come]
- **Muammo**: Harbiy tajribasi bo'lmagan yangi askarlar jang maydonida tez sarosimaga tushadi va zarba bera olmaydi.
- **Yechim (`TrainingDummy` & `training_dummy.glb`)**:
  - Somon bilan to'ldirilgan va temir dubulg'a kiydirilgan yog'och manken (`training_dummy.glb`).
  - Askar va fuqarolar qilich, nayza yoki kamon bilan mankenga zarba berib `melee_skill` yoki `archery_skill` mahoratini 50 ballgacha (Veteran Levy darajasi) oshiradi.
  - Manken mustahkamligi 200 zarba; eskiganda 2 ta yog'och va 1 ta charm tasma bilan qayta ta'mirlanadi.

