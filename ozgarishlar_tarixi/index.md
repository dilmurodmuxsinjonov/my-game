# O'zgarishlar tarixi

## 2026-09-23 — Unreal migratsiyasi boshlandi

- GDD talablarini bosqichma-bosqich amalga oshirish rejasi va bajarilish daftari yaratildi.
- Unreal yo'nalishi, C++ yadro, yagona inventar, versiyalangan save va tekshiruv mezonlari tanlandi.
- Dastlabki Godot prototipi va foydalanuvchining showcase fayllari saqlandi.
- Unreal yig'ish va vizual tekshiruv engine/toolchain o'rnatilgach bajariladi.

## 2026-09-25 — Milestone 18: Tinkers' Construct Smeltery Multiblok Pechi, Qotishmalar va Quyish Tizimi
- **Tinkers' Construct Smeltery Pechi (`SmelteryController` & `smeltery_controller.glb`)**: O'tga chidamli g'ishtlar (`seared_brick`) dan quriladigan 36 birlik sig'imli suyuq metall idishi:
  - Lava va ko'mir yoqilg'isi bilan 1600°C gacha qizdirish.
  - Xom rudalarni 2x ko'paytiruvchi eritish (1 ta ruda -> 2 birlik suyuq metall).
- **Metallurgik Qotishma Tizimi (`AlloyManager`)**:
  - *Bronza*: 3 Mis + 1 Qalay -> 4 Suyuq Bronza ($\ge 950$°C).
  - *Tozalangan Po'lat*: 1 Temir + 1 Uglerod/Ko'mir gazi -> 1 Suyuq Po'lat ($\ge 1450$°C).
  - *Qirollik Elektrumi*: 1 Oltin + 1 Kumush -> 2 Suyuq Elektrum ($\ge 1000$°C).
- **Quyish Havzasi (`CastingBasin` & `casting_basin.glb`)**: 9 birlik suyuq metallni qabul qilib, sovutgandan keyin yaxlit qattiq metall bloklarini (`bronze_block`, `iron_block`, `steel_block`) beradi.
- **Qolip Stoli (`CastingTable` & `casting_table.glb`)**: Almashtiriladigan qoliplar (Ingot, Qilich tig'i, Cho'kich boshi, Bolta boshi) orqali metallni isrof qilmasdan to'g'ridan-to'g'ri qurol-asbob qismlariga quyish.
- **Yangi 3D Modellar (Blender 5.2)**: `smeltery_controller.glb` (132 KB), `casting_basin.glb` (25 KB), `casting_table.glb` (27 KB) yaratildi (jami **46 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 46 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **61 ta test 100% muvaffaqiyat bilan o'tdi** (0.009s).

## 2026-09-25 — Milestone 17: MineColonies Shahar Kengashi, Qirollik Xazinasi va Garnizon Soqchilar Posti
- **MineColonies Shahar Kengashi (`TownHall` & `town_hall_desk.glb`)**: Koloniya ma'muriy markazi va hududiy chegaralar yadrosi:
  - 4 ta rivojlanish bosqichi: Hamlet (32m radius, 8 aholi) -> Village (48m radius, 20 aholi) -> Township (64m radius, 45 aholi) -> Royal City (96m radius, 100 aholi).
  - Fuqarolar reyestri, turar-joy kvotalari va kasb taqsimoti boshqaruvi.
- **Qirollik Xazinasi Xazinaxonasi (`TreasuryVault` & `treasury_vault.glb`)**: Kuchaytirilgan temir tasmali xazina qutisi:
  - Har kunlik feodal soliq yig'ish (soliq stavkasiga qarab aholi kayfiyatiga (morale) ta'sir: past soliq ma'naviyatni oshiradi, yuqori soliq norozilik keltirib chiqaradi).
  - Garnizon harbiylari va soqchilarning kunlik oylik maoshi to'lovi; agar xazina bo'shasa, garnizon soqchilari ish tashlaydi va mudofaa 50% ga zaiflashadi.
  - Bayram subsidiyalari: 50 ta oltin sarflab shahar bayrami o'tkazish orqali butun aholiga +20 morale bonusi taqdim etiladi.
- **Garnizon Soqchilar Posti (`GuardPost` & `guard_post.glb`)**: Halberdlar va qalqonlar raki bilan jihozlangan mudofaa stansiyasi:
  - 16 metr mudofaa radiusi va soqchilar saflanish bonusi (+15 mudofaa balli har bir navbatchi soqchi uchun).
  - Qaroqchilar va bosqinchilar yaqinlashganda avtomatik jangovar xavf signali chalinishi.
- **Yangi 3D Modellar (Blender 5.2)**: `town_hall_desk.glb` (30 KB), `treasury_vault.glb` (148 KB), `guard_post.glb` (33 KB) yaratildi (jami **43 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 43 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **58 ta test 100% muvaffaqiyat bilan o'tdi** (0.007s).

## 2026-09-24 — Milestone 16: Create Mod Konveyer Lentasi, Gravitatsion Truba va Sanoat Shtamplash Pressi
- **Create Mod Kinetik Konveyer Lentasi (`ConveyorBelt` & `conveyor_belt.glb`)**: Kinetik vallar yordamida 2.0 m/s tezlikda harakatlanuvchi mexanik charm lenta (16 SU sarflaydi); resurslarni qo'l mehnatisiz avtomatik ravishda stanoklar, ruda konlari va omborlar o'rtasida tashiydi.
- **Create Mod Gravitatsion Truba va Voronka (`Chute` & `chute.glb`)**: Tabiiy og'irlik kuchi asosida (0 SU talab qiladi) 4 ta narsa/soniya tezlikda resurslarni yuqori qavatdan pastdagi stanoklarga tashuvchi metall truba; don siloslaridan to'g'ridan-to'g'ri tegirmon toshlariga bug'doy uzatadi.
- **Create Mod Sanoat Shtamplash Pressi (`MechanicalPress` & `mechanical_press.glb`)**: Kinetik eksentrik porshen bilan jihozlangan og'ir metallurgik press (48 SU sarflaydi):
  - Temir quyma -> Qalin ritsar plastinasi (`iron_sheet`).
  - Mis quyma -> Tom yopish va quvurlar uchun mis tunukasi (`copper_sheet`).
  - Oltin quyma -> Qirollik oltin tangalari zarb qilish (`gold_coins` — 1:10 nisbatda).
- **Yangi 3D Modellar (Blender 5.2)**: `conveyor_belt.glb` (53 KB), `chute.glb` (15 KB), `mechanical_press.glb` (27 KB) yaratildi (jami **40 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 40 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi.
- **Avtomatlashgan Testlar**: Jami **55 ta test 100% muvaffaqiyat bilan o'tdi** (0.009s).

## 2026-09-24 — Milestone 15: TerraFirmaCraft Bloomery Domna Pechi, Piroliz Ko'mir Chuquri va Bronza Quyish
- **TerraFirmaCraft Piroliz Ko'mir Chuquri (`CharcoalPit` & `charcoal_pit.glb`)**: Yog'och xodalari usti loy va tuproq qatlami bilan germetik yopilgan holatda sekin tutab yonadi (kislorodsiz piroliz); 4 ta yog'ochdan 4 ta yuqori haroratli yog'och ko'miri (`charcoal`) ishlab chiqariladi. Agar chuqur ochiq qolsa, o'tinlar kulga aylanadi (`ash`).
- **TerraFirmaCraft Bloomery Qaytarish Pechi (`Bloomery` & `bloomery.glb`)**: O'tga chidamli tosh va loydan yasalgan shaft domna pechi; 1200°C - 1450°C haroratda temir rudasini yog'och ko'mirdan olingan gazlar bilan qaytaradi va shlakli g'ovak metall to'pi — **Temir Blumi (`iron_bloom`)** ni beradi.
- **Blumni Sandonda Zarb Qilish va Qotirish (`Anvil` va `TripHammer`)**: G'ovakli temir blumini sandonda bolg'alab, suyuq silikat shlakni chiqarish orqali toza **Bolg'alangan Temir Quyma (`wrought_iron_ingot`)** olinadi; Create modining kinetik mexanik bolg'asi (`TripHammer`) esa bu jarayonni avtomatik ravishda inson aralashuvisiz bajaradi.
- **Sopol Tigel va Bronza Qotishmasi Quyish (`Crucible` & `crucible.glb`)**: O'tga chidamli loy tigelda mis va qalay 87.5% / 12.5% nisbatda eritilib suyuq bronza tayyorlanadi; so'ngra oldindan pishirilgan sopol qoliplarga (`ceramic_mold`) quyilib, bronza qilich tig'i (`cast_bronze_blade`), cho'kich (`cast_bronze_pickaxe`) va bolta boshlari yasaladi.
- **Yangi 3D Modellar (Blender 5.2)**: `bloomery.glb` (331 KB), `charcoal_pit.glb` (146 KB), `crucible.glb` (326 KB) yaratildi (jami **37 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 37 ta aktiv, yangi domna pechlari va metallurgiya inshootlari bilan `assets/showcase_realm.png` da qayta render qilindi.
- **Avtomatlashgan Testlar**: Jami **52 ta test 100% muvaffaqiyat bilan o'tdi** (0.009s).

## 2026-09-24 — Milestone 14: Apotheosis Boss Chempion Affikslari, Qimmatbaho Toshlar va Soket Tizimi
- **Apotheosis Boss Affikslari & Chempion Modifikatorlari (`ApotheosisManager` & `bandit_warlord.gd`)**: Qaroqchilar boshlig'i (`BanditWarlord`) endi protsedural nomlar va unvonlar bilan paydo bo'ladi (masalan, *Gorath the Flameborn*, *Kaelen the Bloodthirsty*); 6 ta halokatli chempion affiksi:
  - `INFERNAL`: +35% o't zarari va zarbada nishonni yondirish.
  - `ARMORED`: 50% qo'shimcha sovut va 30% to'g'ridan-to'g'ri jismoniy zararni yutish.
  - `SWIFT`: +40% yugurish va hujum tezligi.
  - `VAMPIRIC`: Yetkazilgan zararning 25% miqdorida o'z sog'lig'ini tiklash (lifesteal).
  - `TEMPEST`: Har 6 soniyada yerga yashin chaqirib elektr to'lqini tarqatish.
  - `TITAN`: +100% qo'shimcha HP, orqaga surilishga (knockback) 100% immunitet.
- **Qimmatbaho Toshlarni Qirqish Dastgohi (`GemCuttingTable` & `gem_cutting_table.glb`)**: Lapidariya dastgohi orqali xom yoqut, sapfir, topaz va chuqurlik toshlarini qirqilgan qimmatbaho toshlarga aylantirish (`cut_ruby`, `cut_sapphire`, `cut_topaz`, `cut_deep_gem`).
- **Qurol va Sovut Soketlari (Gem Socketing System)**: Qurollar va sovutlarga 3 tagacha soket o'rnatish; kesilgan yoqut (+12 jangovar zarar), sapfir (+25 chidamlilik), topaz (+20% hujum tezligi) va chuqurlik toshi (+35 HP & vampirik so'rish) beradi.
- **G'alaba Kubogi (`boss_trophy.glb`)**: Bandit Warlord mag'lub etilganda tushadi; Hukmdor qasriga o'rnatilganda butun qirollik aholisining ma'naviyatini +10 ga oshiradi.
- **Yangi 3D Modellar (Blender 5.2)**: `gem_cutting_table.glb` (115 KB) va `boss_trophy.glb` (109 KB) yaratildi (jami **34 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 34 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi.
- **Avtomatlashgan Testlar**: Jami **48 ta test 100% muvaffaqiyat bilan o'tdi** (0.014s). Godot 4.7.2 dvigateli xatosiz yuklandi.

## 2026-09-24 — Milestone 13: TerraFirmaCraft Geologiya, Shaxta O'pirilishi va Ruda Qatlamlari
- **TerraFirmaCraft Geologiya va O'pirilish Fizikasi (`GeologyManager` & `voxel_world.gd`)**: Yer ostida (`Y <= 24`) tayanch to'sinlarisiz tosh va ruda qazilganda 35% ehtimollik bilan g'or shiftining o'pirilishi (`cave_in`) yuz beradi; shift toshlari to'kilib qulagan vayronaga (`COBBLESTONE`) aylanadi va 4 metr radiusdagi barchaga 25-45 crush zarari yetkazadi.
- **Tayanch To'sinlari Aurası (`support_beam.glb`)**: Har bir tayanch to'sini gorizontal 4 blok va vertikal 3 bloklik xavfsizlik aurasini hosil qiladi, o'pirilish xavfini 0% ga tushiradi.
- **Geologik Razvedka Cho'kichi (`ProspectorPick` & `prospector_pick.glb`)**: Tosh qatlamiga urilganda 12 blok radiusdagi barcha rudalarni skanerlash va sezgirlik darajasini ko'rsatish (`NONE`, `TRACES`, `SAMPLE`, `RICH`, `MOTHERLODE`).
- **Yer Osti Ruda Vagonchasi (`MineCart` & `mine_cart.glb`)**: 30 ta og'ir ruda yuk hajmi, kon relslari (`mining_rail`) bo'ylab 2.5 barobar tezroq harakatlanish va omborga yuk to'kish.
- **Shaxtyor Xavfsizlik Chirog'i (`mining_lantern.glb`)**: Yopiq jez korpusli yoritish chirog'i.
- **Yangi 3D Modellar (Blender 5.2)**: `prospector_pick.glb` (24 KB), `mine_cart.glb` (80 KB), `mining_lantern.glb` (266 KB) yaratildi (jami 32 ta GLB model).
- **Yangi Qirollik Dioramasi**: Barcha 32 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi.
- **Avtomatlashgan Testlar**: Jami 45 ta test 100% muvaffaqiyat bilan o'tdi. Godot 4.7.2 dvigateli xatosiz yuklandi.

## 2026-09-24 — Milestone 12: Farmer's Delight Qishloq Xo'jaligi, Boy Tuproq va Oshpazlik Tizimi
- **Farmer's Delight Kompost Qutisi (`CompostBin` & `compost_bin.glb`)**: Organik chiqindilar (chirigan ovqat, barglar, o'simlik qoldiqlari) dan 4 ta sarflab, 1 ta yuqori unumdor o'g'it (`rich_soil_compost`) tayyorlash stansiyasi.
- **Ekinlar Almashlab Ekish va Dinamik Unumdorlik (`CropManager`)**: Bug'doy, karam, piyoz, sabzi ekinlarining to'liq hayotiy sikli. Boyitilgan tuproqda 2x tezroq o'sish; almashlab ekish rotatsiyasi (almashinish) +25% o'sish tezligi va +1 hosil bonusi; ketma-ket bir xil ekin ekish (monokultura) esa o'sishni 20% ga sekinlashtiradi va -1 hosil jarimasi beradi.
- **Oshpazlik Kesish Taxtasi (`CuttingBoard` & `cutting_board.glb`)**: Oshxona satiri (cleaver) bilan ingredientlarni professional maydalash: Karam -> 2x To'g'ralgan karam (`sliced_cabbage`), Xom go'sht -> 2x Qiyma (`minced_beef`), Piyoz -> 2x To'g'ralgan piyoz (`diced_onion`).
- **Gourmet Retseptlar (`SupplyChain`)**: Boyitilgan Karamli Sho'rva (`cabbage_stew`) va To'yimli Cho'pon Pirogi (`shepherd_pie`) pishirish logikasi.
- **Yangi 3D Modellar (Blender 5.2)**: `compost_bin.glb` (46 KB) va `cutting_board.glb` (24 KB) yaratildi (jami 29 ta yuqori sifatli GLB model).
- **Yangi Qirollik Dioramasi**: Barcha 29 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi.
- **Avtomatlashgan Testlar**: Jami 41 ta test 100% muvaffaqiyat bilan o'tdi. Godot 4.7.2 dvigateli xatosiz yuklandi.

## 2026-09-24 — Milestone 11: Create Mod Suv G'ildiragi, Mexanik Tegirmon va Sanoat Bolg'asi
- **Create Mod Suv G'ildiragi (`WaterWheel` & `water_wheel.glb`)**: Daryo oqimi va flume kanallaridan 24 RPM va 256 SU (Stress Units) mexanik energiya ishlab chiqarish, 8 metr radiusdagi mashinalarga kinetik quvvat ulash.
- **Mexanik Tegirmon Toshlari (`Millstone` & `millstone.glb`)**: 32 SU quvvat sarflaydi; aylanma granit toshlar orqali bug'doyni avtomatik ravishda 200% unumdorlikda (1 bug'doy -> 2 non) un va rasionga aylantiradi.
- **Sanoat Mexanik Bolg'asi (`TripHammer` & `trip_hammer.glb`)**: 64 SU quvvat sarflaydi; eksentrik vallar yordamida temir va mis rudalarini avtomatik yanchib maydalaydi (`crushed_iron`), domna pechida eritilganda 2 barobar ko'p temir quyma beradi (1 ruda -> 2 quyma).
- **Yangi 3D Modellar (Blender 5.2)**: `water_wheel.glb` (119 KB), `millstone.glb` (36 KB), `trip_hammer.glb` (40 KB) yaratildi (jami 27 ta GLB model).
- **Yangi Qirollik Dioramasi**: Barcha 27 ta aktiv, suv kanali va kinetik agregatlar ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi.
- **Avtomatlashgan Testlar**: Jami 38 ta test 100% muvaffaqiyat bilan o'tdi. Godot 4.7.2 dvigateli toza initsializatsiya qilindi.

## 2026-09-23 — Milestone 10: Tinkers' Construct Sandon (Modular Anvil) va TerraFirmaCraft Oziq-ovqat Saqlash
- **Tinkers' Construct Sandon (`Anvil`)**: Ikki shoxli haqiqiy temirchilik sandoni, interaktiv modulli qurol yasash (Tig' / Gardis / Dasta), po'lat va temir qotishmalari, xarakteristikalar hisobi (Zarar, Chidamlilik, Tezlik) va sandonda zarb qilish.
- **TerraFirmaCraft Oziq-ovqat Saqlash (`FoodPreservationManager`)**: Go'sht va oziq-ovqatlarning vaqt o'tishi bilan aynishi/chirishi, Tosh tuzi (`rock_salt`) bilan tuzlash (8x saqlash muddati), Dudxona (`smoke_rack.glb`) yordamida dudlash (5x saqlash muddati) va Yer osti sovuq yerto'lasida (`Y <= 22`, tosh tomli) chirish tezligini 75% ga kamaytirish.
- **Yangi 3D Modellar (Blender 5.2)**: `anvil.glb` (175 KB) va `smoke_rack.glb` (38 KB) yaratildi (jami 24 ta GLB model).
- **Yangi Qirollik Dioramasi**: Barcha 24 ta aktiv ishtirokidagi yuqori aniqlikdagi diorama `assets/showcase_realm.png` da render qilindi.
- **Avtomatlashgan Testlar**: Jami 35 ta test 100% muvaffaqiyat bilan o'tdi (barcha 24 ta model yaxlitligi, modulli qurol matematikasi, TFC saqlash algoritmlari).

## 2026-09-23 — Milestone 9: MineColonies Chizmalar, Quruvchi/Kuryer Fuqarolar va RimWorld Kvotalari
- **MineColonies Chizmalari (`BlueprintConstruction`)**: Golografik yarim shaffof ko'rinish, resurslar hisoblagichi, 3D holat paneli va yakunlanganda avtomatik vokselli binoni dunyoga o'rnatish.
- **Quruvchi Fuqaro AI (`Citizen.Role.BUILDER`)**: Omborlardan materiallarni avtomatik olib, qurilish chizmasi ustida bosqichma-bosqich ishlash va binoni yakunlash.
- **Kuryer / Logist Fuqaro AI (`Citizen.Role.HAULER`)**: `wheelbarrow.glb` g'ildirakli arava bilan jihozlangan fuqaro; 10 tagacha yuk ko'tarish, uzoq nuqtalardan markazga resurs tashish va qurilish maydonlariga material yetkazish.
- **RimWorld-style "Do Until X" Kvotalari**: `SupplyChain` va `CraftingMenu` da har bir mahsulot (Non, Asboblar, Qurollar, Temir quymalar) uchun rejimlar (`DO_FOREVER`, `DO_UNTIL_X`, `PAUSED`) va chegaralarni boshqarish.
- **Yangi 3D Modellar (Blender 5.2)**: `wheelbarrow.glb` (107 KB) va `architect_desk.glb` (31 KB) yaratildi va sinovdan o'tkazildi (jami 22 ta 3D aktiv).
- **Avtomatlashgan Testlar**: 33 ta test 100% muvaffaqiyat bilan o'tdi. Godot Engine ishga tushishi va skriptlar komplyatsiyasi tasdiqlandi.

