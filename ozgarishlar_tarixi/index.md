# O'zgarishlar tarixi

## 2026-09-23 — Unreal migratsiyasi boshlandi

- GDD talablarini bosqichma-bosqich amalga oshirish rejasi va bajarilish daftari yaratildi.
- Unreal yo'nalishi, C++ yadro, yagona inventar, versiyalangan save va tekshiruv mezonlari tanlandi.
- Dastlabki Godot prototipi va foydalanuvchining showcase fayllari saqlandi.
- Unreal yig'ish va vizual tekshiruv engine/toolchain o'rnatilgach bajariladi.

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

