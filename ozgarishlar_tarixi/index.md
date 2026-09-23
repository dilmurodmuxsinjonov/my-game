# O'zgarishlar tarixi

## 2026-09-23 — Unreal migratsiyasi boshlandi

- GDD talablarini bosqichma-bosqich amalga oshirish rejasi va bajarilish daftari yaratildi.
- Unreal yo'nalishi, C++ yadro, yagona inventar, versiyalangan save va tekshiruv mezonlari tanlandi.
- Dastlabki Godot prototipi va foydalanuvchining showcase fayllari saqlandi.
- Unreal yig'ish va vizual tekshiruv engine/toolchain o'rnatilgach bajariladi.

## 2026-09-23 — Milestone 9: MineColonies Chizmalar, Quruvchi/Kuryer Fuqarolar va RimWorld Kvotalari
- **MineColonies Chizmalari (`BlueprintConstruction`)**: Golografik yarim shaffof ko'rinish, resurslar hisoblagichi, 3D holat paneli va yakunlanganda avtomatik vokselli binoni dunyoga o'rnatish.
- **Quruvchi Fuqaro AI (`Citizen.Role.BUILDER`)**: Omborlardan materiallarni avtomatik olib, qurilish chizmasi ustida bosqichma-bosqich ishlash va binoni yakunlash.
- **Kuryer / Logist Fuqaro AI (`Citizen.Role.HAULER`)**: `wheelbarrow.glb` g'ildirakli arava bilan jihozlangan fuqaro; 10 tagacha yuk ko'tarish, uzoq nuqtalardan markazga resurs tashish va qurilish maydonlariga material yetkazish.
- **RimWorld-style "Do Until X" Kvotalari**: `SupplyChain` va `CraftingMenu` da har bir mahsulot (Non, Asboblar, Qurollar, Temir quymalar) uchun rejimlar (`DO_FOREVER`, `DO_UNTIL_X`, `PAUSED`) va chegaralarni boshqarish.
- **Yangi 3D Modellar (Blender 5.2)**: `wheelbarrow.glb` (107 KB) va `architect_desk.glb` (31 KB) yaratildi va sinovdan o'tkazildi (jami 22 ta 3D aktiv).
- **Avtomatlashgan Testlar**: 33 ta test 100% muvaffaqiyat bilan o'tdi. Godot Engine ishga tushishi va skriptlar komplyatsiyasi tasdiqlandi.

