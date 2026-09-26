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

---

## 10. Going Medieval & RimWorld Integratsiyasi — Tabibxona, Malhamlar va Jarrohlik To'shagi (Milestone 21)

### 10.1. Giyohshunos va Alkimyogar Dastgohi (Apothecary Bench) — [Going Medieval / RimWorld]
- **Muammo**: Jangdan yaralanib qaytgan askarlar qon ketishi yoki yiringli infeksiya tufayli halok bo'ladi.
- **Yechim (`ApothecaryBench` & `apothecary_bench.glb`)**:
  - Tosh hovoncha, alembik kolba va dorivor giyohlar osilgan dastgoh (`apothecary_bench.glb`).
  - **Steril bint (`sterile_bandage`)**: 1 mato + 1 giyoh $\rightarrow$ 2 ta bint (qon ketishini darhol to'xtatadi, +15 HP).
  - **Dorivor malham (`herbal_poultice`)**: 2 giyoh + 1 toza suv $\rightarrow$ 1 ta malham (yiringli yara infeksiyasini davolaydi, +30 HP).
  - **Vabo ziddizahari (`plague_antidote`)**: 3 giyoh + 1 sarimsoq $\rightarrow$ 1 ta ziddizahar (og'ir kasallik va infeksiyani bir zumda yo'qotadi, +45 HP).

### 10.2. Shifoxona Jarrohlik To'shagi va Dori Qutisi (Infirmary Bed & Medicine Chest) — [RimWorld]
- **Muammo**: Oddiy uyda yotgan yaradorlar juda sekin sog'ayadi va infeksiya kuchayib ketadi.
- **Yechim (`InfirmaryBed`, `infirmary_bed.glb` & `medicine_chest.glb`)**:
  - Toza choyshabli shifoxona to'shagi (`infirmary_bed.glb`) va dori-darmon qutisi (`medicine_chest.glb`).
  - Tabib nazorati ostida sog'ayish tezligi daqiqasiga 4.0 HP gacha oshadi.
  - Bemor to'liq sog'ayib chiqqanda tibbiy g'amxo'rlik uchun aholi ruhiyatiga +8 morale qo'shiladi.

---

## 11. Medieval Dynasty & Valheim Integratsiyasi — Asalarichilik, Asal Sharobi va Mum Shamlar (Milestone 22)

### 11.1. Somonli Asalari Uyasi va Ekinlarni Changlatish (Apiary Beehive) — [Medieval Dynasty / Valheim]
- **Muammo**: Ekinlar faqat o'g'it bilan cheklanib qolgan va qishki yorug'lik hamda asal mahsulotlari manbai yo'q.
- **Yechim (`ApiaryBeehive` & `beehive_skep.glb`)**:
  - Har kuni passiv ravishda 3 ta **Asalari mumi katagi (`honeycomb`)** va 2 ta **Toza mum (`beeswax`)** beradi.
  - **Changlatish aurasi (18m radius)**: Uya atrofidagi barcha ekinlarning o'sish tezligini avtomatik ravishda **+20% ga (1.20x)** oshiradi.

### 11.2. Asal Sharobi Bochkasi va Mum Shamdonlar (Mead Fermenter & Candelabra) — [Valheim]
- **Muammo**: Qahraton qishda fuqarolar sovuqdan aziyat chekadi, shaxtalar va qasr xonalarini tutunsiz yoritish vositasi kerak.
- **Yechim (`MeadFermenter`, `mead_fermenter.glb` & `candle_candelabra.glb`)**:
  - **Oltin Asal Sharobi (`honey_mead`)**: 2 ta honeycomb + 1 toza suv + 1 bug'doy $\rightarrow$ 2 ko'za asal sharobi (Aholiga +15 morale va qishki sovuqqa +25.0 issiqlik bardoshliligi beradi).
  - **Mum Shamlar (`beeswax_candle`)**: 2 ta mum $\rightarrow$ 3 ta sham (`candle_candelabra.glb` orqali qasr va yer osti shaxtalarini yoritadi).

---

## 12. Stronghold & Mount & Blade II: Bannerlord Integratsiyasi — Qasr Mudofaasi, Mangonel Katapultasi, Qaynoq Smola Qozoni va O'tkir Panjara Darvoza (Milestone 23)

### 12.1. Mangonel Katapultasi va Yong'inli Toshlar (`SiegeEngine` & `catapult.glb`) — [Stronghold / Mount & Blade II]
- **Muammo**: Dushman daryo narigi tomonida yoki uzoq masofada tosh devorlar ortida to'planib qolganida o'q-yoy yetib bormaydi.
- **Yechim (`SiegeEngine` & `catapult.glb`)**:
  - Qattiq eman xodalaridan yasalgan, og'ir qarshi toshli Mangonel artilleriyasi (`catapult.glb`).
  - Masofa chegarasi: 15 metrdan 65 metrgacha ballistik traektoriya.
  - Asosiy tosh zarbasi: 120 ball to'g'ridan-to'g'ri maydalovchi zarar va 12 metr radiusdagi zarba to'lqini.
  - **Olovli tosh (`fire_boulder`)**: +50 yong'in zarari qo'shilib, umumiy zarba 170 ballga yetadi va yog'och istehkomlarni kul qiladi.

### 12.2. Qaynoq Qora Smola (Pitch) Qozoni (`PitchCauldron` & `pitch_cauldron.glb`) — [Stronghold "Pour Oil!"]
- **Muammo**: Dushman piyodalari qasr darvozasi tagiga to'planib, devorni buzishga uringanda yuqoridan ularni to'xtatish qiyin bo'ladi.
- **Yechim (`PitchCauldron` & `pitch_cauldron.glb`)**:
  - Darvoza arki yoki devor bo'g'ziga o'rnatilgan cho'yan qozon (`pitch_cauldron.glb`).
  - Qozondan quyilgan yonuvchi qora smola pastda 6 metrlik qaynoq ko'lmak hosil qiladi:
    - 15 soniya davomida har soniyada 40 DPS olov zarari (jami 600 ball zarba salohiyati).
    - Raqiblar harakatlanish tezligini 60% ga (0.40x) sekinlashtiruvchi to'siq effekti.
  - 5 marta quyish zaxirasi; har to'kilishdan so'ng 45 soniyada qayta qaynaydi.

### 12.3. Mustahkam O'tkir Temir Panjara Darvoza (Portcullis Gate) (`PortcullisGate` & `portcullis_gate.glb`) — [Mount & Blade II / Stronghold Gatehouse]
- **Muammo**: Oddiy yog'och darvozalar devorbuzar rammalar zarbasiga dosh bera olmay tez sinadi.
- **Yechim (`PortcullisGate` & `portcullis_gate.glb`)**:
  - Temir uchi o'tkirlangan qalin eman panjarasi va yuk ko'tarish richagi/chig'iri (`portcullis_gate.glb`).
  - 500 mustahkamlik balli (HP): devorbuzar va bolg'a zarbalariga qarshi -50% chidamlilik (blunt resistance), kamon o'qlariga -80% qaytarish defleksiyasi.
  - **Tuzoq ezish zarari (Trap Crush)**: Darvoza tepadan pastga tashlanganda, ostida qolgan barcha bosqinchilarga 80 ball crushing zarbasi beriladi.

---

## 13. Manor Lords & Medieval Dynasty Integratsiyasi — Chorvachilik, Og'ir Xo'kizlar Logistikasi, Qo'y Juni va Qishki Ozuqa Oxuri (Milestone 24)

### 13.1. Og'ir Yog'och Molxona va Xo'kizlar Logistikasi (`PastureBarn` & `pasture_barn.glb`) — [Manor Lords / Medieval Dynasty]
- **Muammo**: Katta qasrlar va soborlar qurilishida uzoq o'rmonlardan og'ir yog'och xodalarini qo'lda tashish kolonistlar ish unumdorligini falaj qiladi.
- **Yechim (`PastureBarn` & `pasture_barn.glb`)**:
  - Somon boloxonali, eman ustunli molxona va hayvonlar bo'lmasi (`pasture_barn.glb`).
  - **Ishchi Xo'kizlar (`draft_oxen`)**: Xo'kizga bo'yinturuq bog'lab, bir safarda birdaniga 4 ta og'ir yog'och xodasini 1.8x tezlik bilan qurilish maydoniga yetkazadi.
  - **Sog'in Sigirlar (`dairy_cows`)**: Har kuni ozuqa bilan ta'minlanganda 4 ko'za yangi sut (`milk_jug`) ishlab chiqaradi. Ozuqa bo'lmaganda mahsuldorlik 0 ga tushadi.

### 13.2. Qo'yxona va Qishki Jun Kiyim To'qish (`SheepPasture` & `sheep_pen.glb`) — [Going Medieval / Medieval Dynasty]
- **Muammo**: Qahraton qishda va qor bo'ronlarida fuqarolar gipotermiya (muzlash) tufayli kasal bo'lib o'ladi.
- **Yechim (`SheepPasture` & `sheep_pen.glb`)**:
  - Chipta to'siqli qo'y qo'rasi, boshpana va jun qirqish kursisi (`sheep_pen.glb`).
  - Har 2 kunda qo'ylardan 8 ta toza qo'y juni (`raw_wool`) qirqib olinadi.
  - **Issiq Jun Nimcha (`woolen_tunic`)**: 2 ta jun $\rightarrow$ 1 ta qalin jun nimcha. Qishki sovuqqa +35.0 issiqlik bardoshliligi beradi va aholi kayfiyatiga +10 baxtiyorlik (morale) qo'shadi.

### 13.3. Qishki Ozuqa Oxuri va Ochlikdan Qirilib Ketish (`FeedingTrough` & `feeding_trough.glb`) — [RimWorld / Medieval Dynasty]
- **Muammo**: Qishda yer yuzasini qor qoplaganda yaylovlardagi yashil o't muzlaydi va hayvonlar ochiq havoda oziqlana olmaydi.
- **Yechim (`FeedingTrough` & `feeding_trough.glb`)**:
  - 40 birlik somon va silos sig'imiga ega qalin yog'och oxur (`feeding_trough.glb`).
  - Harorat $5^\circ\text{C}$ dan pastga tushganda mollar o'tlay olmaydi va har bir hayvon kuniga 1 ta zaxira somon iste'mol qiladi.
  - Agar oxur bo'shab qolsa, ogohlantirish signali chalinadi va chorva ochlikdan nobud bo'la boshlaydi.

---

## 14. Ko'p Biomli Voksel Olam, Qaroqchilar Turlari va Relyef Harakati Fizikasi (Milestone 25)

### 14.1. Relyef Balandligi, Daryo Vodiylari va 3D Simplex G'orlar (`BiomeManager`, `VoxelWorld`)
- **Muammo**: Bir xil tekis voksel olam o'yin jarayonini zerikarli qiladi va qidiruv (exploration) qiziqishini so'ndiradi.
- **Yechim (`BiomeManager` & `VoxelWorld`)**:
  - Namlik (moisture) va harorat (temperature) ko'rsatkichlari bo'yicha 4 xil tabiiy biom:
    - **Plains (Yashil tekislik)**: Qishloq xo'jaligi va bug'doyzorlar uchun unumdor tuproq ($Y \approx 10$).
    - **Deep Forest (Qorong'i qalin o'rmon)**: Qurilish uchun eman va qarag'ay xodalariga boy hudud ($Y \approx 12$).
    - **Highlands (Baland tog'lar va qoyalar)**: Tosh, granit va ruda qazib olish uchun tog'li qiyaliklar ($Y > 18$).
    - **River Valley (Dengiz sathidan past daryo vodiysi)**: Suv tegirmonlari va baliqchilik uchun daryo ($Y < 6$), qirg'og'ida qum bloklari.
  - **3D Simplex Cave Carving**: 3D shovqin funksiyasi orqali tog'lar ostida tabiiy chuqur g'orlar va yerosti yo'laklari o'yiladi (noise > 0.65 bo'shliq hosil qiladi).

### 14.2. Qaroqchilar Jangovar Turlari va Istehkomlar (`BanditArchetype`, `BanditCamp`, `bandit_tent.glb`, `spiked_barricade.glb`, `loot_chest.glb`)
- **Muammo**: Bir xil statsga ega dushmanlar taktik jangni oddiy chertish (hack-and-slash) ga aylantirib qo'yadi.
- **Yechim**:
  - **Qalqonchi (`Shieldbearer`)**: Katta temir qalqon bilan saf tortadi; frontal hujumlarning 75% ini bloklaydi, kamon o'qlarini esa 90% qaytaradi. Orqadan va yonboshdan zarba berish talab qilinadi.
  - **O'qchi Mergan (`Raider Archer`)**: 15–25m masofadan ballistik o'q yog'diradi. O'yinchi yaqinlashganda (<6m) chekinish (kiting retreat) manevrini bajaradi.
  - **Berserker (`Raider Berserker`)**: Qattiq po'lat boltalar bilan qurollangan; 6 metr masofadan sakrab hujum qiladi, +50% tezlik va 24 ball og'ir zirh teshar (armor-piercing) zarar beradi.
  - **Qaroqchilar Qarorgohi (`bandit_tent.glb`)**: Bosqinchilar markaziy qarorgohi.
  - **Tikanli Yog'och Barrikada (`spiked_barricade.glb`)**: Yugurib kelib urilgan hujumchilarga 20 ball aks-zarar beradi.
  - **O'lja Sandig'i (`loot_chest.glb`)**: Qarorgoh tozalanganda ochiladigan sandiq: oltin tangalar, temir quymalar va oziq-ovqat zaxirasi.

### 14.3. Relyefga Bog'liq Harakatlanish va To'dalanish (Boids) Ajralishi (`GridPathfinder3D`)
- **Muammo**: Birliklar bitta nuqtada bir-birining ichiga kirib ketishi (unit stacking) va yo'llardan foydalanmasligi.
- **Yechim (`GridPathfinder3D`)**:
  - **Tosh To'shalgan Yo'llar (`paved road`)**: +20% tezlik bonusi (1.20x) berib, qishloq ichidagi logistikani tezlashtiradi.
  - **Daryo va Suv Havzalari**: 50% suzish qarshiligi (0.50x sekinlashuv).
  - **Flocking Boids Separation**: Yaqin turgan jangchilar o'rtasida 1.2m radiusda itaruvchi kuch vektori hisoblanib, birliklarning tabiiy saf tortishi ta'minlanadi.

---

## 15. Medieval Dynasty & Bellwright Integratsiyasi — Ovchilik Kulbasi, Eman Po'stlog'i Teri Oshlash va Mo'yna Quritish Dastgohi (Milestone 26)

### 15.1. Qalin O'rmon Ovchilik Kulbasi va Yovvoyi Jonivorlar Ekolgiyasi (`HuntingLodge` & `hunting_lodge.glb`)
- **Muammo**: Yangi paydo bo'lgan o'rmon va tog'li biomlarda yovvoyi kiyiklar, qoplonlar va yovvoyi cho'chqalar (boars) mavjud bo'lsada, qishloq faqat dehqonchilik va qoramolga bog'lanib qolishi.
- **Yechim (`HuntingLodge` & `hunting_lodge.glb`)**:
  - Eman va qarag'ay xodalaridan qurilgan, kiyik shoxi bilan bezatilgan ovchilik kulbasi (`hunting_lodge.glb`).
  - Kulbaga 3 tagacha malakali ovchi tayinlanadi.
  - Biom ekologiyasi multiplikatori:
    - **Deep Forest**: 1.5x kiyik va cho'chqa ovi mahsuldorligi.
    - **Highlands**: 1.2x tog' echkilari va bo'rilar ovi.
    - **Plains / River Valley**: 0.8x - 1.0x standart ov.
  - **Kamonchilar Boshpanasi (`archery_blind`)**: Ovchilar hosildorligini +35% ga oshiradi va yovvoyi cho'chqalarning qonli hujumi xavfini 15% dan 3% ga (80% ga kamaytirish) tushiradi.
  - Kunlik hosil: To'yimli kiyik go'shti (`raw_venison`), xom terilar (`raw_hide`), hayvon yog'i (`tallow` - sham va sovun uchun) va mayin quyon/tulki mo'ynasi (`raw_pelt`).

### 15.2. Eman Po'stlog'i Teri Oshlash Qadog'i (`TanneryVat` & `tannery_vat.glb`) — [Medieval Dynasty / Vintage Story]
- **Muammo**: Oddiy xom terilar tezda chiriydi va ulardan mustahkam harbiy sovutlar yoki og'ir arava egar-jabduqlari yasab bo'lmaydi.
- **Yechim (`TanneryVat` & `tannery_vat.glb`)**:
  - Temir chambaraklar bilan mustahkamlangan eman bochkasi va yog'och qirish dastgohi (`tannery_vat.glb`).
  - O'tinchi o'rmondan eman po'stlog'i (`oak_bark` — tabiiy tannin) yig'adi.
  - Oshlash formulasi: 2 ta xom teri + 1 ta eman po'stlog'i + 1 chelak suv $\rightarrow$ 2 ta mustahkam oshlangan qattiq charm (`cured_leather`).
  - **Feodal Hunarmandchilik Ehtiyojlari**:
    - **Gambeson / Charm Sovut**: 4 ta oshlangan charm + 2 ta jun.
    - **Xo'kiz Jabdug'i (`ox_harness`)**: 3 ta charm + 2 ta temir quyma (og'ir xodalarni tortish uchun).
    - **Mergan Sadoqi (Quiver)**: 2 ta charm.

### 15.3. Mo'yna Quritish Dastgohi va Qishki Mo'ynali Qimmatbaho Chopon (`FurDryingRack` & `fur_drying_rack.glb`)
- **Muammo**: Qahraton qishda oddiy jun kiyimlar ham kuchli qor bo'ronlaridan (blizzard) to'liq asray olmaydi va qishloqda yuqori tabaqa zodagonlar uchun eksport mahsuloti yetishmaydi.
- **Yechim (`FurDryingRack` & `fur_drying_rack.glb`)**:
  - 4 ta mo'yna sig'imli A-simon yog'och quritish ramkasi (`fur_drying_rack.glb`).
  - Xom mo'ynalar 20 soniya davomida tortilib quritiladi va mayin ishlov berilgan mo'yna (`cured_fur`) ga aylanadi.
  - **Mo'ynali Qishki Shohona Chopon (`fur_cloak`)**:
    - 3 ta ishlov berilgan mo'yna + 1 ta jun kiyim $\rightarrow$ 1 ta mo'ynali chopon.
    - **Effektlari**: +50.0 sovuqqa bardoshlilik (har qanday qor bo'roniga 100% immunitet), zodagonlar ruhiyatiga +15 baxtiyorlik va savdogar karvonlariga 15 oltin tanga qiymatida sotish salohiyati!

---

## 16. Medieval Dynasty & Going Medieval Integratsiyasi — Qishloq Suv Qudug'i, Akveduk Sug'orish va O't O'chirish Logistikasi (Milestone 27)

### 16.1. Tosh Quduq va Aholi Chanqog'i Mexanikasi (`WaterWell` & `water_well.glb`) — [Medieval Dynasty / RimWorld]
- **Muammo**: Shaharcha o'sib borishi bilan aholi ichimlik suvisiz qolib, chanqoqlik va gipohidratsiya tufayli ish unumdorligi pasayadi; shuningdek yog'och binolar yong'inga qarshi himoyasiz qoladi.
- **Yechim (`WaterWell` & `water_well.glb`)**:
  - Daryo toshlaridan terilgan, yog'och shingilli soyabon va chig'irli quduq (`water_well.glb`).
  - Yerosti suv qatlamidan har kuni avtomatik 8 chelak toza ichimlik suvi (`potable_water`) to'ldiradi (maksimal sig'im 24 chelak).
  - Har bir fuqaro kuniga 1 chelak suv iste'mol qiladi. Suv yetishmasa `Dehydrated` holati beriladi: -25% mehnat tezligi va -15 ruhiyat (morale) jarimasi.
  - **Yong'in O'chirish Zaxirasi**: Bino olov olganda quduqdan 4 chelak suv olinib, yong'in o'chiriladi.

### 16.2. Rim Me'morchiligi Akveduk Sug'orish Tizimi (`AqueductIrrigation` & `aqueduct_pipe.glb`) — [Going Medieval]
- **Muammo**: Daryodan uzoqda joylashgan unumdor dasht ekinzorlari yozgi qurg'oqchilikda (drought) 60% hosil yo'qotadi va quriydi.
- **Yechim (`AqueductIrrigation` & `aqueduct_pipe.glb`)**:
  - Tosh ustunli arka va yuqori suv o'zani bo'ylab oqadigan akveduk kanali (`aqueduct_pipe.glb`).
  - Daryo vodiysidan suv olib, har bir segment atrofida 8 metrlik to'liq namlik aurasini ta'minlaydi.
  - **Hosil Bonusi**: Sug'orilgan ekinlar +30% (1.30x) tezroq o'sadi va yozgi qurg'oqchilik qovjirashidan 100% himoyalanadi.
  - Mustahkamlik: 150 HP (yong'inga mutlaqo chidamli, qamal toshlari zarbasidan sinishi mumkin).

### 16.3. Zaxira Suv Bochkasi va Harbiy Suv Idishlari (`WaterCask` & `water_cask.glb`)
- **Muammo**: Uzoq masofali harbiy yurishlar va og'ir yog'och tashuvchi xo'kiz karvonlari qishloq qudug'idan uzoqlashganda chanqab zaiflashadi.
- **Yechim (`WaterCask` & `water_cask.glb`)**:
  - Maxsus yog'och taglikdagi, jez jo'mrakli 40 chelak sig'imli eman bochka (`water_cask.glb`).
  - Askar va kuryerlar uchun charm suv idishlari (`hydration_canteen`): Har bir jangchiga 2 chelak zaxira berilib, 24 soatlik to'liq chanqoq immuniteti bilan ta'minlanadi.

---

## 17. Valheim & Vintage Story Integratsiyasi — Yerosti Qadimiy Kriptasi, Sarkofag Qoldiqlari va Zulmat Labirintlari (Milestone 28)

### 17.1. Protsedural Qadimiy Tosh Kriptasi (`CryptDungeon` & `crypt_entrance.glb`) — [Valheim / Minecraft]
- **Muammo**: Er usti dunyosi to'liq o'rganilgach, o'yinchida xazina qidirish, unutilgan texnologiyalarni topish va xavfli yerosti labirintlariga sho'ng'ish (dungeon delving) ehtiyoji yuzaga keladi.
- **Yechim (`CryptDungeon` & `crypt_entrance.glb`)**:
  - Tog'lik hududlar (Highlands) etagida va chuqur g'orlarda ($Y < 12$) qadimiy o'yma tosh peshtoqli, zanglagan panjarali daxma kirishi (`crypt_entrance.glb`).
  - Protsedural ko'p xonali tuzilma: Kirish vestibyuli, ustunli galereyalar, qopqonli yo'laklar va shohona dafn xonalari (`Burial Chamber`).
  - Yerosti optik tuman va to'liq zulmat okluziyasi (0.05 ambient light).
  - Sarkofaglar bezovta qilinganda daxma qo'riqchilari (`CryptSkeletonKnight`, `CryptDraugr`) uyg'onishi va pistirma hujumlari.

### 17.2. O'yma Ohaktosh Sarkofagi va Qadimiy Yodgorliklar (`AncientSarcophagus` & `stone_sarcophagus.glb`) — [Vintage Story]
- **Muammo**: Standart yog'och sandiqlardan oddiy resurslar chiqishi yerosti ekspeditsiyalarining qiymatini pasaytiradi; daxmalar o'ziga xos qadimiy sirlarga ega bo'lishi kerak.
- **Yechim (`AncientSarcophagus` & `stone_sarcophagus.glb`)**:
  - Ustida ritsarning tosh qiyofasi o'yilgan og'ir ohaktosh sarkofag (`stone_sarcophagus.glb`).
  - **Lom bilan ochish mexanikasi (`prying`)**: Og'ir tosh qopqoqni qo'lda surish 12%/sek, temir lom (`iron_crowbar`) bilan esa 2.2x tezlikda (26.4%/sek) ochiladi.
  - **Qopqonlar**: Zaharli nayzalar (`POISON_DARTS` - 25 zarar) yoki shiftdan tosh yog'ilishi; o'g'rilik mahorati (Rogue skill >= 40) orqali zararsizlantiriladi.
  - **Nodir Yodgorliklar (Relics)**:
    - Qadimiy Damashq Po'lati Chizmasi (`ancient_steel_schematic` - 45 oltin, unutilgan metallurgiya texnologiyasi).
    - Qirol Aldenning Muhrli Uzugi (`lost_king_signet` - 60 oltin, +20 qirollik nufuzi, vassallar bilan munosabatga +15 diplomatiya).
    - Qadimiy Oltin Tangalar (`ancient_coins`).

### 17.3. Temir Devor Mash'ali va Zulmat Qo'rquvi Nazorati (`DungeonCrawlerManager` & `wall_sconce.glb`)
- **Muammo**: Chuqur yerostidagi cheksiz zulmat o'yinchi va soqchilar ruhiyatiga (sanity) salbiy ta'sir ko'rsatib, vahima va jangga layoqatsizlik keltirib chiqaradi.
- **Yechim (`DungeonCrawlerManager` & `wall_sconce.glb`)**:
  - Qadimiy daxma devorlariga o'rnatilgan temir mash'aldon (`wall_sconce.glb`).
  - Mash'ala yoqilganda 7.5 metr radiusda iliq yorug'lik aurasini beradi (240 soniya yonish muddati).
  - **Ruhiyat va Qo'rquv Balansi**: Yorug'likda ruhiyat tiklanadi (+1.5/sek); qop-qorong'uda esa ruhiyat pasayadi (-2.0/sek). Ruhiyat 25% dan tushganda `Fear Debuff` (-30% jangovar aniqlik va qochish xavfi) faollashadi.
  - Topilgan barcha relikviyalar qasr xazinasiga olib kelinib, feodal boylik va texnologiyalarga almashtiriladi.

---

## 18. Manor Lords & Bellwright Integratsiyasi — Yo'l To'shash Tizimi, Ko'cha Chiroqlari va Logistika Ko'rsatkichlari (Milestone 29)

### 18.1. Bosqichma-bosqich Yo'l To'shash va Harakatlanish Bonusi (`RoadNetwork` & `paved_road_tile.glb`) — [Manor Lords]
- **Muammo**: Loy va tuproq yo'llarda fuqarolar, g'ildirakli aravalar va og'ir yog'och tashuvchi xo'kizlar sekin harakatlanadi; natijada ishlab chiqarish zanjirlarida xomashyo yetishmasligi yuzaga keladi.
- **Yechim (`RoadNetwork` & `paved_road_tile.glb`)**:
  - Modular tosh qoplama plitkasi (`paved_road_tile.glb`), chekkalarida drenaj ariqchalari va mustahkam bordyurlar.
  - **Yo'l Bosqichlari (Tiers)**:
    - **Dirt Path** (Tuproq so'qmoq): +10% tezlik (1.10x), yo'l qidirish narxi 0.90x.
    - **Gravel Road** (Shaqaltosh yo'l): +25% tezlik (1.25x), yo'l qidirish narxi 0.75x.
    - **Cobblestone Paved** (Tosh to'shalgan shohona yo'l): +50% tezlik (1.50x), yo'l qidirish narxi 0.50x (sun'iy intellekt piyodalarni avtomatik tosh yo'lga yo'naltiradi).
  - **Og'ir Aravalar Yeyilishi (Wear & Tear)**: Xo'kiz va yuk aravalari o'tganda yo'l asta-sekin yeyiladi; tosh yo'llar 2.4 barobar chidamli bo'lib, tosh quyish orqali ta'mirlanadi.

### 18.2. Shahar Ko'cha Chirog'i va Tungi Xavfsizlik Aurasi (`StreetLamp` & `street_lamp.glb`) — [Going Medieval / Bellwright]
- **Muammo**: Tunda aholi punktlari qorong'ilikka cho'madi; fuqarolar qo'rquv tufayli ko'chaga chiqmaydi, qaroqchilar va o'g'rilar omborxonalarga bemalol suqilib kiradi.
- **Yechim (`StreetLamp` & `street_lamp.glb`)**:
  - O'yma tosh poydevor ustidagi naqshinkor bolg'alangan temir ustun va shisha fonus (`street_lamp.glb`).
  - **Avtomatlashgan Tungi Sensor**: Shom tushganda (18:00) avtomatik yonadi va tongda (06:00) o'chadi.
  - **Ozuqa Moyi / Yog' Sarfi**: 1 birlik hayvon yog'i (`tallow` — ovchilikdan olinadi) 3 kechalik to'liq yorug'likni ta'minlaydi.
  - **Jinoyatchilikka Qarshi Qalqon**: 9.0 metr yorug'lik radiusi ichidagi har qanday o'g'ri va pistirmachi qaroqchini fosh qiladi va qochishga majbur qiladi.

### 18.3. Chorraha Ko'rsatkichi va Tranzit Koridori Ustuvorligi (`LogisticsWaypoint` & `road_signpost.glb`)
- **Muammo**: Katta feodal shaharlarda kuryerlar va xachirlar chalkash yo'llarda adashib, uzoq aylanma yo'llar orqali resurs tashiydi.
- **Yechim (`LogisticsWaypoint` & `road_signpost.glb`)**:
  - Chorrahalarga o'rnatiladigan o'yma yog'och yo'l ko'rsatkichi (`road_signpost.glb`) — "Market Square", "Castle Keep", "Iron Mine" yo'nalishlari.
  - **Magistral Koridor Bonusi**: Ustuvor belgilangan yo'nalish bo'ylab o'tuvchi kuryer va yuk tashuvchilar yuk ko'tarish hajmiga +15% unumdorlik bonusi oladi.
  - **Harbiy Yig'ilish Nuqtasi (Muster Point)**: Xavf paytida fuqaro lashkarlari aynan shu chorrahaga to'planish signali beriladi.

---

## 19. Medieval Dynasty & Farmer's Delight Integratsiyasi — Tosh Shamol Tegirmoni, Un Silosi va Nonvoyxona (Milestone 30)

### 19.1. Kinetik Shamol Tegirmoni (`StoneWindmill` & `stone_windmill.glb`) — [Medieval Dynasty / Create]
- **Muammo**: Daryo oqimidan uzoqdagi tepalik qishloqlarida suv g'ildiragi qurib bo'lmaydi va bug'doyni qo'lda yanchish behuda ishchi kuchini sarflaydi.
- **Yechim (`StoneWindmill` & `stone_windmill.glb`)**:
  - Konussimon tosh minorali, yog'och shingilli aylanuvchi tomi va 4 ta tuval parrakli shamol tegirmoni (`stone_windmill.glb`).
  - **Atmosfera Shamol Kuchini Hisoblash**: Balandlik ($Y > 10$) va bo'ronli ob-havoga qarab shamol tezligi 0.5x dan 1.8x gacha o'zgaradi.
  - **Kinetik Quvvat Ishlab Chiqarish**: Bazaviy 384 Stress Units (SU) quvvat beradi.
  - **200% Un Hosildorligi**: 1 bug'doy $\rightarrow$ 2 qop toza un (`wheat_flour`), qo'l tegirmoniga nisbatan 3 barobar tezroq yanchiladi.

### 19.2. Ko'tarilgan Namlikdan Himoyalangan Un Donxonasi (`FlourSilo` & `flour_silo.glb`)
- **Muammo**: Yanchilgan un qoplari oddiy yerto'la yoki omborxona polida zax tortib, mog'orlaydi va hasharotlar (weevil) tushishi oqibatida 40-50% yo'qotiladi.
- **Yechim (`FlourSilo` & `flour_silo.glb`)**:
  - Yer sathidan 1 metr ko'tarilgan 4 ta mustahkam tirgakli, temir chambarakli yog'och bochka va shifer tomli donxona (`flour_silo.glb`).
  - **Sig'im**: 120 qop un.
  - **Mog'or va Chirishga Qarshi Himoya**: Germetik qopqoq tufayli tabiiy namlik ta'siridagi chirishni 85% ga kamaytiradi.
  - **Gravitatsion Pastki Jo'mrak**: Aravalar va nonvoylar unni to'g'ridan-to'g'ri tagidagi voronka orqali bir lahzada to'ldirib oladi.

### 19.3. Gumbazli Qizil G'ishtli Nonvoyxona Pechi va Shohona Nonlar (`BakerOven` & `baker_oven.glb`) — [Farmer's Delight / Manor Lords]
- **Muammo**: Xom ekinlar yoki oddiy bo'tqalar aholi ochligini to'liq qondirolmaydi, charchoqni ketkazmaydi va qirollik ma'naviyatiga bonus bermaydi.
- **Yechim (`BakerOven` & `baker_oven.glb`)**:
  - Tosh poydevorli, gumbazsimon qizil g'ishtli non pechi, qizigan cho'g'li o'choq va nonvoy kuragi (`baker_oven.glb`).
  - **Termal Akkumulyatsiya (220°C)**: O'tin bilan qizdiriladi; harorat 180°C dan oshganda non pishirish boshlanadi.
  - **Non Pishirish Retseptlari**:
    - **Qora Javdar Noni (`rye_bread`)**: 2 un + 1 suv $\rightarrow$ 3 ta to'yimli non (+45 to'qlik, +10 mehnat energiyasi).
    - **Shohona Shirin Briyosh (`royal_brioche`)**: 2 un + 1 sut + 1 asal $\rightarrow$ 3 ta elita non (+70 to'qlik, +15 qirollik ruhiyati).

---

## 20. Vintage Story, Valheim & Teardown Integratsiyasi — Realistik PBR Teksturalar, Triplanar Sheyder, Konstruktiv Yuk Fizikasi va Atmosfera Realizmi (Milestone 31)

### 20.1. Ko'p Qatlamli PBR Voksel Teksturalari va Triplanar Sheyder (`voxel_pbr_triplanar.gdshader`) — [Vintage Story]
- **Muammo**: Standart UV proyeksiyasi tik qoyalar, g'orlar va vertikal voksel devorlarida teksturani cho'zib, xunuk va sun'iy ko'rinish beradi; shuningdek bitta oddiy albedo xaritasi zamonaviy yorug'lik effektlarini qo'llab-quvvatlamaydi.
- **Yechim (`voxel_pbr_triplanar.gdshader` & `voxel_atlas_*.png`)**:
  - **12 ta Tabiiy Blok Uchun PBR Tekstura To'plami**: Stone, dirt, grass_top, grass_side, oak_log, oak_planks, cobblestone, brick, sand, water, iron_ore, gold_ore.
  - **Uchta 256x192 PBR Atlasi**:
    - `voxel_atlas_albedo.png` — Tabiiy rang va mikro-rang o'zgarishlari.
    - `voxel_atlas_normal.png` — Tangent-space relef sirtlari ($\frac{\partial h}{\partial x}, \frac{\partial h}{\partial y}$ gradientli normallar).
    - `voxel_atlas_roughness.png` — Yaltiroqlik va mikrog'adir-budurlik koeffitsientlari.
  - **Triplanar Proyeksiya**: Dunyo koordinatalari bo'yicha $X, Y, Z$ tekisliklariga proyeksiyalanadi va devor burchaklarida $N^4$ darajali vaznlar bilan silliq birlashtiriladi (zero UV distortion).
  - **Dinamik Yomg'ir Ho'lligi (`rain_wetness`)**: Yomg'ir paytida sirt qorayadi, roughness 0.08 gacha pasayadi va ko'lmak yaltiroqligi (specular 0.85) paydo bo'ladi.
  - **Qishki Qor Qoplami (`snow_accumulation`)**: Qor bo'ronida tepaga qaragan yuzalarga ($N_y > 0.6$) tabiiy qor qatlami yotqiziladi.

### 20.2. Konstruktiv Yuk Ko'tarish Fizikasi va Qulash Dinamikasi (`StructuralIntegrityManager` & `masonry_buttress.glb`) — [Valheim / 7 Days to Die]
- **Muammo**: Minecraft uslubidagi havoda muallaq turuvchi tosh va tuproq bloklari o'yin realizmini yo'qotadi va qal'a qamallarining strategik chuqurligini cheklaydi.
- **Yechim (`StructuralIntegrityManager` & `masonry_buttress.glb`)**:
  - **Gorizontal Konsol (Cantilever) Chegaralari**:
    - Poydevor / Bedrock: Cheksiz ($\infty$).
    - Temir blok: 8 metr.
    - Tosh va g'isht: 6 metr.
    - Qoplama tosh (`cobblestone`): 5 metr.
    - Yog'och va taxta: 4 metr.
    - Tuproq: 1 metr.
    - Qum: 0 metr (darhol o'piriladi).
  - **Gotika Uslubidagi Uchuvchi Tirgak (`masonry_buttress.glb`)**:
    - Og'ir tosh devorlar va peshtoqlar yoniga o'rnatilgan gotik tirgak maksimal gorizontal oraliqqa **+3 metr** qo'shimcha mustahkamlik beradi (tosh konsol 6m dan 9m gacha uzayadi).
  - **BFS Barqarorlik Tahlili va Voksel Qulashi**:
    - Poydevor tayanchi uzilgan bloklar darhol kinetik gravitatsiya bo'lagi (`falling rubble`) ga aylanadi.
    - Qulagan 2600 kg tosh bloki 10 metr balandlikdan 14.0 m/s tezlikda tushib, 255 kJ kinetik energiya bilan pastdagi inshootlar va dushmanlarga halokatli zarba beradi.

### 20.3. Atmosfera Quyosh Harorati va Volumetrik Tuman (`EnvironmentRealismManager` & `weather_vane.glb`, `barometer_station.glb`) — [Vintage Story]
- **Muammo**: O'yinda kunduz va kecha faqat oddiy yorug'lik intensivligi bilan ifodalanadi, haqiqiy quyosh spektri va havo bosimi o'zgarishlari hisobga olinmaydi.
- **Yechim (`EnvironmentRealismManager` & Fixturalar)**:
  - **Quyosh Kelvin Harorati Grafigi (Tanner Helland Algoritmi)**:
    - Tong (06:00): 4750K (iliq oltin nurlar).
    - Tush (12:00): 6500K (neytral oppoq quyosh).
    - Botish (18:00): 2600-3400K (qizg'ish-sariq shafaq).
    - Yarim tun (00:00): 12000K (sovuq ko'kish yulduz va oy shu'lasi).
  - **Volumetrik Reley Tumani**:
    - Ochiq havo (`clear`): zichlik 0.005, tarqalish 0.15.
    - Tuman (`mist`): zichlik 0.035, tarqalish 0.40.
    - Yomg'ir (`rain`): zichlik 0.065, tarqalish 0.65.
    - Qor bo'roni (`blizzard`): zichlik 0.120, tarqalish 0.85.
  - **Mis Xo'rozli Shamol Yo'naltirgichi (`weather_vane.glb`)**: Shamol vektori va shamol tezligini vizual ko'rsatadi.
  - **Devorga O'rnatiladigan Simobli Barometr (`barometer_station.glb`)**: Atmosfera bosimining pasayishini kuzatib, 3 soat oldin bo'ron xavfidan ogohlantiradi.

### 20.4. Haqiqiy Aerodinamik Ballistika va Shamol Ta'siri (`BallisticRealism`) — [Mount & Blade / ArmA]
- **Muammo**: Kamon va arbalet o'qlari tekis parabolik traektoriya bo'ylab uchadi, havo qarshiligi, balandlik va shamol ta'siri hisoblanmaydi.
- **Yechim (`BallisticRealism`)**:
  - **Barometrik Havo Zichligi**: $\rho(y) = 1.225 \cdot e^{-y / 8500}$ kg/m³ (tog' cho'qqisida havo siyraklashib, o'q uzoqroq masofaga uchadi).
  - **Aerodinamik Qarshilik**: $\vec{F}_d = -\frac{1}{2} \rho |\vec{v}_{rel}| \vec{v}_{rel} C_d A$.
  - **Yon Shamol Ta'siri (Crosswind Drift)**: Shamol vektori hisobiga o'q o'z yo'nalishidan og'adi.
  - **Kinetik Zirh Teshib O'tish**:
    - Bodkin o'qi 50 m/s tezlikda 62.5 J kinetik energiya va 1.4x penetratsiya koeffitsienti bilan mato kamzulni (gambeson, 20 armor) teshib o'tadi, lekin to'liq po'lat sovutdan (65 armor) aks etib sachrab ketadi.












