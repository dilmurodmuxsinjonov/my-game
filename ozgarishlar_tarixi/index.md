# O'zgarishlar tarixi

## 2026-09-29 — Milestone 45: Feudal Quest & Progression Ledger, Dynamic Citizen Dialogue, and Monarch Renown System (Issue #52)
- **6-Bosqichli Tarixiy Feodal Kvestlar Zanjiri (`scripts/quests/quest_manager.gd`)**:
  - *I. Foundations of the Realm*: Yog'och va tosh bloklarini qazib olish, fuqaroning kasbiy burchini tayinlash (+100 Renown, "Lord of the Frontier" unvoni).
  - *II. Bread & Iron*: Norfolk ekinzorlarini shudgorlash, oltin bug'doy yetishtirish va domnada temir eritish (+250 Renown, "Baron of the Realm" unvoni).
  - *III. High-Pressure Industry*: Bug' va og'ir metallurgiya tumanini ziyorat qilish, o'choqni qizdirish, mexanik buyumlar yasash (+450 Renown, "Count of the Trade Lands" unvoni).
  - *IV. Maritime Trade Fleet*: Dengiz portini ko'zdan kechirish, savdo aravasi bilan ayirboshlash, savdo flotini barpo etish (+700 Renown, "Duke of High Metallurgy" unvoni).
  - *V. Renaissance Clockwork*: Rasadxonadagi Praga astronomik soatini tekshirish, yerosti kon temiryo'l tarmog'ini o'rganish (+1000 Renown).
  - *VI. The Sovereign Coronation*: Qirollik jang karnayini chalish, chegara qaroqchilarini daf etish, 2,500 Renown to'plab Oliy Qirollik tojini kiyish va olam g'alabasiga erishish (`realm_victory_achieved`).
- **Interaktiv Fuqarolar Muloqot Tizimi (`scripts/entities/citizen_dialogue.gd`)**:
  - Har qanday fuqaroga `E` tugmasini bosganda ochiluvchi feodal dialog oynasi.
  - 7 ta kasb bo'yicha tarixiy dialoglar (dehqon, o'tinchi, konchi, novvoy, temirchi, soqchi, erkin fuqaro).
  - Qishki iqlim, ochlik va past ma'naviyat bo'yicha moslashuvchan nutq.
  - Monarx amallari: "Yangi pishgan non ulashish (+15 Ma'naviyat)", "Monarx Ilhomi (+5 Ma'naviyat)", "Vazifani o'zgartirish".
- **Qirollik Solnomasi va Kvest Jurnali (`scripts/ui/quest_journal.gd`)**:
  - `J` tezkor tugmasi orqali ochiluvchi hashamatli qirollik daftari.
  - Joriy monarx unvoni, umumiy nufuz balli, faol kvest vazifalari `[✓]` va `[○]` ko'rinishida, shuningdek aholi va tumanlar statistikasi.
- **Standalone Simulyator Yangilanishi (`tools/interactive_play_simulator.py`)**:
  - Yangi `quests` / `journal` va `talk [smith|farmer|guard|baker]` interaktiv buyruqlari.
- **Avtomatlashgan Testlar To'plami (`tests/test_quest_dialogue_progression.py`)**:
  - Jami **350 ta test 100% muvaffaqiyat bilan o'tdi** (0.65s).

## 2026-09-29 — Milestone 44: Save/Load Persistensiya Tizimi, O'yin Ichidagi Pause & Sozlamalar Menyusi va Dinamik Akustik Atmosfera (Issue #50)
- **Sparse Delta Voksel Persistensiya va Holatni Saqlash (`scripts/core/save_system.gd`)**:
  - **Sparse Voxel Delta Serialization**: Butun olamning 131,072 ta blokini saqlash o'rniga faqat o'yinchi tomonidan o'zgartirilgan (o'yilgan, qo'yilgan, shudgorlangan) bloklar `modified_voxels` lug'atida kuzatiladi va saqlanadi. Bu fayl hajmini 95%+ ga kamaytiradi (bir necha kilobayt) va saqlash/yuklash tezligini bir zumda amalga oshiradi.
  - **Monarx Hayotiy Ko'rsatkichlari & Inventar**: Koordinatalar (X, Y, Z), rotatsiya, salomatlik, chidamlilik, ochlik, tana issiqligi, faol hotbar uyasi va to'liq 8 uyali inventar saqlanadi va qayta tiklanadi.
  - **Iqtisodiy Omborlar va Fuqarolar**: Yog'och, tosh, temir, bug'doy, non zahiralari, fuqarolarning rollari, ma'naviyati va joylashuvi, shuningdek sutka vaqti va fasl ma'lumotlari to'liq serializatsiya qilinadi.
  - **Kriptografik SHA-256 Nazorat Summasi (Checksum)**: Har bir saqlangan fayl SHA-256 heshi bilan imzolanadi va yuklash jarayonida faylning buzilmaganligi va butunligi avtomatik tekshiriladi.
  - **Tezkor Saqlash va Yuklash (QuickSave / QuickLoad)**: `F5` tugmasi orqali tezkor saqlash va `F9` tugmasi orqali tezkor yuklash.
- **Interaktiv O'yin Ichidagi Pause va Sozlamalar Menyusi (`scripts/ui/pause_menu.gd`)**:
  - **Medieval UI Dizayn**: Yarim shaffof gotik fon, oltin hoshiyalar va tugmalar.
  - **5 Ta Ko'rinish (Panel Views)**:
    - *Asosiy Pause Menyusi*: O'yinni davom ettirish, saqlash, yuklash, sozlamalar, boshqaruv yo'riqnomasi, ish stolidan chiqish.
    - *Saqlash Slotlari Menyusi*: 1, 2, 3-slotlar va QuickSave uyasi.
    - *Yuklash Slotlari Menyusi*: Mavjud slotlar ro'yxati va vaqt ko'rsatkichlari.
    - *Sozlamalar Menyusi*: Sichqoncha sezgirligi (Mouse Sensitivity), Ko'rish burchagi (FOV), Master Ovoz balandligi va To'liq ekran rejimi (Fullscreen toggle).
    - *Feodal Boshqaruv Qo'llanmasi (Controls Guide)*: Harakat, jang, voksel amallari va tezkor tugmalar ro'yxati.
  - **Kursor va Vaqt Nazorati**: ESC bosilganda o'yin `SceneTree.paused` rejimiga o'tadi va kursor avtomatik ko'rsatiladi; qaytganda esa kursor yashirilib o'yin davom etadi.
- **Dinamik Akustik Atmosfera va Protsedurali Ovoz Dvigateli (`scripts/world/audio_manager.gd`)**:
  - **26 Ta Blok Turi Uchun Akustik Qadam Tovushlari (Surface Footstep System)**: O'yinchi qaysi voksel bloki (o't, tosh, yog'och, loy, suv, qor, temir rels) ustida yurganiga qarab alohida chastotali tovushlar eshitiladi; yugurganda tovush qadami tezlashadi va ovoz kuchi 1.2x ga oshadi.
  - **Protsedurali Sintez SFX**: Kirka bilan tosh sindirish (640 Hz), bolta bilan yog'och chopish (280 Hz), qilich silkitish (880 Hz), monarx xavf karnayi (146.8 Hz D3), blok o'rnatish (210 Hz), hunarmandlik muvaffaqiyati (587.3 Hz D5) va tugma bosish ovozlari.
  - **8 Ta Tuman Akustik Manzarasi va Kunduz/Tun Rejimi**: Qirollik qal'asi, Shahar maydoni, Bug' zavodi, Port, Shaxta, Rasadxona, Ekinzor va Qabriston uchun xos rezonans va muhit tovushlari; kechasi va kunduzi avtomatik almashinuvchi tovushlar.
- **Tizimlarning O'zaro Integratsiyasi (`scripts/core/game_manager.gd`, `scripts/entities/player.gd`, `scenes/main.tscn`)**:
  - O'yinchi harakatlari, blok qo'yish/olish, tezkor saqlash/yuklash va sozlamalarni qo'llash to'liq zanjirda bog'landi.
  - Standalone simulyator `tools/interactive_play_simulator.py` da yangi `save`, `load`, `audio`, `pause` buyruqlari bilan boyitildi.
- **Avtomatlashgan Testlar To'plami (`tests/test_save_audio_pause_systems.py`)**:
  - Jami **325 ta test 100% muvaffaqiyat bilan o'tdi** (0.60s).

## 2026-09-28 — Milestone 43: Infinite Work — To'liq Olam Montaji, 1-Shaxs Interaktiv Kontrolleri va Standalone O'yin Relizi (Issue #48)
- **112 Ta 3D Modelning 8 Ta Tarixiy Feodal Tumanga To'liq Integratsiyasi (`scripts/world/world_assembler.gd`)**:
  - **1. Qirollik Qal'asi (Citadel)**: `portcullis_gate.glb`, `drawbridge_platform.glb`, `drawbridge_winch.glb`, 4 ta `watchtower.glb`, `masonry_buttress.glb`, `spiked_barricade.glb`, `trebuchet_siege.glb`, `battering_ram.glb`, `siege_tower.glb`, `catapult.glb`, `pitch_cauldron.glb`, `guard_post.glb`, `armory_rack.glb`, `training_dummy.glb`, `war_horn.glb`, `outpost_banner.glb`.
  - **2. Shahar va Bozor Maydoni (Town Square)**: `town_hall_desk.glb`, `treasury_vault.glb`, `architect_desk.glb`, `water_well.glb`, `burgage_coop.glb`, `caravan_cart.glb`, `tax_sheriff_cart.glb`, `wheelbarrow.glb`, `crate.glb`, `loot_chest.glb`, `paved_road_tile.glb`, `road_signpost.glb`, `street_lamp.glb`, `wall_sconce.glb`, `candle_candelabra.glb`, `citizen.glb`.
  - **3. Bug' va Og'ir Metallurgiya Zavodi (Steam & Forge Quarter)**: `steam_boiler.glb`, `steam_engine_drive.glb`, `centrifugal_governor.glb`, `furnace.glb`, `furnace_tuyere.glb`, `mechanical_bellows.glb`, `industrial_trip_hammer.glb`, `smeltery_controller.glb`, `bloomery.glb`, `anvil.glb`, `crucible.glb`, `casting_basin.glb`, `casting_table.glb`, `charcoal_pit.glb`, `mechanical_press.glb`, `drive_shaft.glb`, `bevel_gearbox.glb`, `mechanical_clutch.glb`, `conveyor_belt.glb`, `chute.glb`.
  - **4. Dengiz Savdo Porti va Slipvey Doki (Harbor & Docks)**: `drydock_slipway.glb`, `fluyt_cargo_ship.glb`, `quayside_crane.glb`, `treadwheel_crane.glb`, `water_cask.glb`.
  - **5. Yerosti Shaxtasi va Bug' Temiryo'l Tarmog'i (Mining Rail District)**: `mine_locomotive.glb`, `mine_cart.glb`, `rail_switch.glb`, `hopper_unloader.glb`, `mine_dewatering_pump.glb`, `mine_ventilator.glb`, `mining_capstan.glb`, `support_beam.glb`, `mining_lantern.glb`.
  - **6. Uyg'onish Davri Rasadxonasi (Observatory Complex)**: `astronomical_clock.glb`, `armillary_sphere.glb`, `celestial_orrery.glb`, `barometer_station.glb`, `weather_vane.glb`, `enchanter_table.glb`, `gem_cutting_table.glb`.
  - **7. Norfolk 4-Yillik Ekinzorlari va Qishloq Xo'jaligi (Agriculture)**: `windmill.glb`, `stone_windmill.glb`, `water_wheel.glb`, `millstone.glb`, `baker_oven.glb`, `flour_silo.glb`, `pasture_barn.glb`, `sheep_pen.glb`, `feeding_trough.glb`, `beehive_skep.glb`, `mead_fermenter.glb`, `hunting_lodge.glb`, `fur_drying_rack.glb`, `smoke_rack.glb`, `tannery_vat.glb`, `apothecary_bench.glb`, `medicine_chest.glb`, `infirmary_bed.glb`, `campfire.glb`, `cooking_pot.glb`, `cutting_board.glb`, `workbench.glb`, `compost_bin.glb`, `aqueduct_pipe.glb`.
  - **8. Chegara Istehkomlari va Qadimiy Qabriston (Wilderness & Frontier)**: `crypt_entrance.glb`, `stone_sarcophagus.glb`, `funeral_pyre.glb`, `runestone.glb`, `bandit_tent.glb`, `bandit.glb`, `bandit_warlord.glb`, `boss_trophy.glb`.
- **1-Shaxs Monarx Boshqaruvi va Jonli Realizm Telemetriyasi (`scripts/entities/player.gd` & `scripts/ui/hud.gd`)**:
  - **Harakat va Boshqaruv**: WASD harakatlanish, Space sakrash, Shift sprint, sichqoncha bilan ko'rish, sichqoncha chap tugmasi (LMB) bilan blok o'yish, o'ng tugma (RMB) bilan blok o'rnatish.
  - **Tezkor Tugmalar**: `E` — interaksiya/hunarmandlik, `C` — hunarmandlik menyusi, `L` — qirollik daftari, `H` — harbiy xavf karnayi, `F1` — realizm debug paneli, `F2` — 8 ta tuman bo'ylab tezkor teleportatsiya (fast travel).
  - **Jonli Blok Tekshiruvi (Inspect Tooltip)**: Krest qaratilgan har qanday voksel va binoning mustahkamligi, bosim kuchlanishi ($\sigma_c$), harorati (°C) va tuproq NPK (Azot, Fosfor, Kaliy) foizlarini ko'rsatuvchi intellektual panel.
- **Standalone Ishga Tushirish Fayllari (One-Click Launchers)**:
  - **`run_game.bat`**: Windows batch skripti — tizimdagi Godot 4.3 dvigatelini avtomatik topadi yoki winget orqali o'rnatishni taklif qiladi va darhol o'yin oynasini ochadi.
  - **`run_game.ps1`**: PowerShell skripti — pre-flight tekshiruvlar, testlarni yurgizish va loyihani ishga tushirish imkoniyati.
  - **`tools/interactive_play_simulator.py`**: Standalone to'liq interaktiv Python-simulyatori — foydalanuvchi Godot o'rnatilmagan holatda ham bevosita terminal orqali olamda kezishi, blok o'yishi, domna yoqishi va trebyushedan o't ochishi mumkin.
- **Avtomatlashgan Testlar**: Jami **300 ta test 100% muvaffaqiyat bilan o'tdi** (0.574s).

## 2026-09-28 — Milestone 42: Total Realism Architecture — Fizika, Termodinamika, Metabolizm/Agronomiya, PBR Render va Feodal Iqtisodiyot (Issue #44 & #46)
- **1-Ustun: Konstruktiv Barqarorlik va Voksel Fizikasi (Structural Integrity & Voxel Physics)**:
  - **Graf Asosidagi Bosim/Cho'zilish Kuchlanishi Modeli (`scripts/world/structural_integrity.gd`)**: Diskret graf yo'nalishli tahlili orqali voksel bloklarining vertikal va lateral yuk ko'tarish qobiliyati ($\sigma_c = \frac{\sum W}{A}$ va $\sigma_t$). Ohaktosh (Limestone: 15 MPa), Granit (Granite: 45 MPa), Pishgan g'isht (Fired Brick: 12 MPa), Eman to'sini (Oak Beam: 8 MPa) va Konstruksion temir (Structural Iron: 65 MPa) uchun haqiqiy fizik chegaralar joriy etildi.
  - **Dinamik Qulash Kaskadlari (Overhang Collapse Cascades)**: Ruxsat etilgan tayanch radiusidan oshib ketgan kantileverlar va ortiqcha yuklangan ustunlar halokati ("ghost blocks" muammosisiz) tosh/yog'och parchalariga aylanib yerga qulaydi.
  - **Yerosti Geologik Bosimi va G'orlar Qulashi (`scripts/world/geology_manager.gd`)**: Chuqur shaxta gorizontlarida litostatik bosim ($P = \rho \cdot g \cdot h$) hisobi; mustahkamlovchi yog'och ustunlarsiz (mine timbers) qazilganda g'or qulashi (cave-in) va metan to'planishi mexanikasi.
  - **Haqiqiy Ballistika va Snaryad Fizikasi (`scripts/physics/ballistic_realism.gd`, `scripts/combat/projectile.gd`, `scripts/combat/siege_engine.gd`)**: O'qlar, ballista nayzalari va trebyushe snaryadlari uchun aerodinamik qarshilik ($F_d = \frac{1}{2} \rho v^2 C_d A$), gravitatsion tushish va shamol shabadasi og'ishi hisobi; kinetik energiyaga asoslangan voksel sindirish ($E_k = \frac{1}{2} m v^2$).
- **2-Ustun: Panjarali Termodinamika va Gidravlika (Grid-Based Thermodynamics & Fluid Hydraulics)**:
  - **3D Uyali Avtomat (Cellular Automata) Issiqlik O'tkazuvchanligi (`scripts/world/thermodynamic_engine.gd`, `scripts/core/voxel_chunk.gd`)**: Furye qonuni ($\frac{\partial T}{\partial t} = \alpha \nabla^2 T$) asosida har bir voksel o'z qo'shnilari bilan issiqlik almashadi; har xil materiallar uchun issiqlik sig'imi va o'tkazuvchanlik koeffitsientlari (temir: 0.12, tosh: 0.05, yog'och: 0.02, havo: 0.01).
  - **Mo'ri Tortish Konveksiyasi (Chimney Draft Buoyancy)**: Enclosed havo shaxtalari va vertikal mo'rilarda Bernulli effekti va suzuvchanlik bosimi ($v = \sqrt{2gH \frac{T_{in} - T_{out}}{T_{in}}}$) orqali kislorod oqimi kuchaytirilib, domna pechlarida 1400°C gacha issiqlik ta'minlanadi.
  - **Olov Tarqalishi va Yonuvchanlik**: Yonuvchan vokellar (yog'och, somon, ko'mir) tutashish harorati va kislorod mavjudligiga qarab o'z-o'zidan yonadi va o't o'chiruvchi suv/qum bilan so'ndiriladi.
  - **Hajm Saqlanish Gidravlikasi va Sug'orish (`scripts/world/fluid_hydraulics.gd`, `scripts/world/aqueduct_irrigation.gd`)**: Suv saqlanish qonuniga amal qiluvchi, bosim va sath tenglashuviga asoslangan gidravlika; akveduklar, tosh ariqlar va gidravlik qiya oqimlar orqali ekinzorlarni namlash.
  - **Muzlash va Erish Fazaviy O'tishlari**: Ambient harorat $T \le 0^\circ\text{C}$ ga tushganda suv qatlamlari mustahkam ustida yurish mumkin bo'lgan muz bloklariga aylanadi va bahorda asta-sekin erib suvga aylanadi.
- **3-Ustun: Biologik Metabolizm, Oziqlanish va NPK Agronomiya (Biological Survival, Nutrition & NPK Agronomy)**:
  - **Ko'p Bosqichli Metabolik Byudjet (`scripts/entities/metabolism_component.gd`)**: Fuqarolarning jismoniy faolligiga qarab soatlik kaloriya sarfi (dam olishda 75 kcal/h, og'ir qazishda 350 kcal/h) va 3 ta makroelement ustuni: Uglevodlar (Carbohydrates — energiya), Oqsillar (Proteins — to'qima tiklanishi va mushak kuchi), Vitaminlar (Vitamins — immunitet).
  - **Fiziologik Xastaliklar va Patologiyalar**: Vitamin C yetishmovchiligida singa (scurvy: milk qonashi, -40% ish unumi), oqsil tanqisligida mushak atrofiyasi va immunitet pasayishi, sovuq havoda gipotermiya va titroq.
  - **Oziq-ovqat Chirishi va Saqlash Dinamikasi (`scripts/economy/food_preservation_manager.gd`)**: Arrenius kimyoviy kinetikasi asosida harorat va namlikka qarab buzilish vaqti; muzxona (cellar), tuzlash (salting), quritish (curing), dudlash (smoking) va sirkalash (pickling) orqali saqlash muddatini 10x-20x gacha uzaytirish.
  - **NPK Tuproq Agronomiyasi va Ekin Almashlab Ekish (`scripts/world/agronomy_soil_manager.gd`)**: Tuproqdagi Azot (N), Fosfor (P) va Kaliy (K) elementlarini alohida kuzatish; bug'doy, javdar, dukkaklilar (azot to'plovchi) va sholg'om almashlab ekish (4-year Norfolk crop rotation) hamda kompost/kul bilan tuproqni qayta tiklash.
- **4-Ustun: Fotorealistik PBR Sirtlar va Dinamik Atmosfera (Photorealistic PBR Surfaces & Dynamic Atmosphere)**:
  - **6-Kanalli Triplanar POM Voksel Shaderi (`assets/shaders/voxel_pbr_complete.gdshader`)**: Albedo, Normal (tangent-space), Roughness, Metallic, Ambient Occlusion va Height/Displacement xaritalari yordamida chuqur relyefli Parallax Occlusion Mapping (POM); voksel qirralarida choklar va tekstura cho'zilishining to'liq bartaraf etilishi.
  - **Organik Materiallar Uchun Subsurface Scattering (SSS)**: Inson terisi, barglar, mum va mevalar uchun nur tarqalishi modeli.
  - **Dinamik Atrof-muhit va Iqlim Effektlari (`scripts/world/atmosphere_controller.gd`)**: Yog'ingarchilikda tosh va yog'och yuzalarida realistik suv plyonkasi va nur sinishi (wetness roughness attenuation); sovuqda gorizontal voksel yuzalarida protsedurali qor qatlami to'planishi; Quyosh balandligi ($\alpha$) bo'yicha dinamik volumetrik tuman va Rayleigh/Mie optik nurlanishi.
- **5-Ustun: Tarixiy Feodal Ijtimoiy-Iqtisodiyoti va Logistika Friksiyasi (Historical Feudal Socio-Economics & Logistics Friction)**:
  - **5 Ta Ijtimoiy Tabaqa Huquqlari va Xartiyalari (`scripts/economy/feudal_charter_manager.gd`)**: Krepostnoylar (Serfs), Erkin dehqonlar (Yeomen), Gildiya hunarmandlari (Artisans), Ruhoniylar (Clergy) va Zodagonlar (Nobility); har bir tabaqaning soliq stavkalari, huquqlari va qo'zg'olon ko'tarish xavfi (unrest/strike threshold).
  - **Transport Ishqalanishi va Yo'l Infratuzilmasi (`scripts/economy/road_network.gd`, `scripts/economy/trade_caravan.gd`)**: Qoplamasiz loy yo'llar aravachalar tezligini -50% ga pasaytiradi, shag'al yo'l +15% tezlashtiradi, yo'nilgan tosh magistral esa +40% tezlik va kamroq charchoq ta'minlaydi.
  - **Dinamik Ko'p Bozorli Narx Shakllanishi (`scripts/economy/market_economy_manager.gd`)**: Shahar bozorlari o'rtasida elastik talab-taklif narxlari, qishki g'alla narxi sakrashi, qaroqchilik xavfi mukofoti (risk premium) va inflyatsion muvozanat.
- **MASTER_GDD.md To'liq Integratsiyasi**: Barcha 5 ta ustun uchun to'liq matematik tenglamalar, balans jadvallari, GDScript arxitektura namunalari bilan 6,994 qatorgacha boyitildi.
- **Avtomatlashgan Testlar**: Barcha **280 ta test 100% muvaffaqiyat bilan o'tdi** (0.348s), 10,000 Monte-Karlo iteratsiyasi va 141 ta balans jadvali to'liq tekshirildi.

## 2026-09-28 — Milestone 41: Barcha 3D Modellarni Alohida Detalizatsiya Qilish va Yuqori Sifatli PBR Skinlarni Yangilash (Issue #42)
- **Rasadxona Kompleksi 3D Detallari va Materiallari (`tools/generate_milestone40_models.py`)**:
  - **Praga Astronomik Soati (`astronomical_clock.glb`)**: Gotik tosh minora arxitekturasi, plint mouldings, ustunlar va tepasidagi gotik gable toj; 24 soatlik tilla astrolyabiya siferblati, stereografik koordinata halqalari (Saraton, Ekvator, Tog' echkisi), 12 burj yulduz tugunlariga ega ekssentrik zodiak kamari, alanga nurlariga ega Quyosh ko'rsatkichi, kumush/qora aylanuvchi Oy shari, pastki 12 oylik pergament taqvim siferblati, qo'shaloq bronza qo'ng'iroqlar va zarba bolg'alari, foliot va verge muvozanat mexanizmi hamda osilgan qo'rg'oshin og'irliklar.
  - **Uchoyoqli Armillyar Sfera (`armillary_sphere.glb`)**: Yevropa yong'oq yog'ochidan o'yilgan kabriol oyoqlar va bronza panja-shar oyoqchalari, aylanuvchi tayanch kvadranti; 360° darajalarga bo'lingan va 8 yo'nalishli kompas guli bilan ta'minlangan gorizont halqasi, konsentrik meridianga, ekvator, qutb va tropik halqalar, 23.44° qiya ekliptika burj kamari, markazdagi oltin qit'alarga ega lapis lazuli Yer shari hamda ko'rish teshiklariga ega qutb o'qi.
  - **Episiklik Sayyoralar Orreriysi (`celestial_orrery.glb`)**: Sakkizburchakli qizil yog'och shkaf (boiserie panellari va tilla hoshiyalar bilan), fil suyagi tutqichli qo'l buragich (crank), sakkizburchakli tilla taqvim palubasi, tishli g'ildiraklar klasteri (alohida modellashtirilgan tishlar va engillashtirilgan 4 tirgakli disklar), 12 ta toj nurlariga ega oltin Quyosh, Merkuriy, Venera, Yer va aylanuvchi kumush Oy halqasi, Mars (qutb muz qoplami bilan), Yupiter (4 ta Galiley yo'ldoshlari bilan) hamda Saturn (ikkita konsentrik planar halqalar bilan).
- **Yuqori Bosimli Bug' Quvvati Kompleksi Detallari va Materiallari (`tools/generate_milestone39_models.py`)**:
  - **Ko'p Quvurli Bug' Qozoni (`steam_boiler.glb`)**: Shamot o'tga chidamli g'isht devorlari va ohak choklari, sovitish panjaralari, ilmoqlari va aylanuvchi jez qulfiga ega cho'yan o'choq eshigi; ichida 5.0 emissiya kuchi bilan yonayotgan cho'g'li ko'mir olovi (glowing embers); jami 72 ta oltiburchakli parchin mixlar (hex rivets) bilan qoplangan 3 ta temir halqali jez baraban, konussimon tutun kamerasi, mis tojli baland mo'ri va tortish richagi, bimetallik manometr (sifon ilmog'i bilan), suv sathi shisha naychasi hamda ikkita prujinali/yukli xavfsizlik klapanlari.
  - **Gorizontal Statsionar Bug' Dvigateli (`steam_engine_drive.glb`)**: Sanoat to'q yashil (British Racing Green) cho'yan bedplate, silliqlangan yorqin po'lat relslar va 4 burchakdagi poydevor bolt-gaykalari; tilla jez lentalar va qisqichlar bilan tortilgan sayqallangan tik (teak) yog'och stavalari bilan izolyatsiyalangan silindr; 8 tadan boltli bronza silindr qopqoqlari, krosskopf qutisi va bronza sirpanuvchi tagliklar (slippers) hamda jez moydoncha; dengiz uslubidagi bronza vkladishlar va ponalar bilan mahkamlangan shatun; ikkita muvozanatlovchi qarshi og'irlikka ega tirsakli val (crankshaft); 6 ta oval tirgakli 1.8 metrli quyma cho'yan maxovik (flywheel) va ko'rinib turgan shponka; podshipnik stoykalari va shisha tomchili moylagichlar.
  - **Sentrifugal Uayt Regulyatori (`centrifugal_governor.glb`)**: Klassik yo'nilgan (fluted) cho'yan ustun, poydevor konus tishli uzatmasi (miter bevel gears) va tasmali shkiv; silliqlangan po'lat shpindel, oyna kabi sayqallangan massiv jez sharlar, shpindel bo'ylab sirpanuvchi bronza yoqa va og'ir bronza disk; bo'g'inli richaglar, drossel yelkasiga uzatuvchi rostlanuvchi shtanga (turnbuckle) va gardishli (flanged) drossel klapan korpusi.
- **Dengiz Porti va Kema Qurilishi Detallari va Materiallari (`tools/generate_milestone38_models.py`)**:
  - **Kema Qurg'oq Verfi / Slipvey Doki (`drydock_slipway.glb`)**: Dengizga nishab eman yog'och balkalari va ho'l yaltiroq moylangan temir relslar; pog'onali kil bloklari, tekislovchi ponalar va bort tirgovichlari; qurilayotgan kemaning egrilangan kili, forstiven va axterstiveni, 7 juft egrilangan qovurg'a ramkalari (futtocks), qavatli oraliq to'sinlar va bort plankalari; ikki qavatli ishchi ko'priklari va to'siqlari; tosh o'choq ustidagi cho'g'lar va qaynayotgan qora smola (pitch) qozoni.
  - **Ohaktosh Poydevorli Port Krani (`quayside_crane.glb`)**: Sakkizburchakli yo'nilgan ohaktosh pirs poydevori, po'lat tasmalar bilan mahkamlangan eman machta va qiya tirgovichlar; buriluvchi thrust podshipnik; 45° qiya eman strela, burama rostlagichli (turnbuckle) temir tyagalar va ikkita blok g'ildiraklari; granit toshlar bilan to'ldirilgan orqa ballast qutisi; ikkita yog'och tutqichli richag va tishli reduktorli kabel barabani; po'lat ilgak (cargo hook) va 4 oyoqli arqon ilmog'i bilan osilgan temir burchakli yog'och yuk qutisi.
  - **Golland Savdo Flyoyti (`fluyt_cargo_ship.glb`)**: Noksimon tumblehome korpusi, suv ostidagi korroziyaga qarshi yashil mis qoplama (copper sheathing) chizig'i; karvel uslubida qoplangan eman bortlar va smolalangan choklar; baland kema orqa kasri (transom), tilla o'ymakor bezaklar, kabina oynalari va issiq nur taratuvchi brass navigatsiya chirog'i; qarag'ay paluba, brezent bilan yopilgan yuk lyuklari, shturval g'ildiragi, binnakl kompas shkafi, shpil (capstan) vinchi, langar; 3 ta machta (Grot, Fok, Bizan), to'liq yelkanlar majmuasi (kvadrat va lotin), vanti va ko'tarilish narvonlari (ratlines) hamda bugshprit.
- **Showcase Renderlar va Diorama**: Barcha renderlar (`showcase_observatory.png`, `showcase_steam_power.png`, `showcase_harbor_and_navy.png`, `showcase_realm.png`) eng qulay kamera burchaklari va yoritish bilan to'liq yangilandi.
- **Avtomatlashgan Testlar**: Barcha **205 ta test 100% muvaffaqiyat bilan o'tdi** (0.314s).

## 2026-09-27 — Milestone 40: Create Mod, Renaissance Astronomy & Clockwork Science Buyuk Imperiya Soatli Rasadxonasi: Astronomik Soat, Armillyar Sfera va Sayyoralar Orreriysi (Issue #39)

- GDD talablarini bosqichma-bosqich amalga oshirish rejasi va bajarilish daftari yaratildi.
- Unreal yo'nalishi, C++ yadro, yagona inventar, versiyalangan save va tekshiruv mezonlari tanlandi.
- Dastlabki Godot prototipi va foydalanuvchining showcase fayllari saqlandi.
- Unreal yig'ish va vizual tekshiruv engine/toolchain o'rnatilgach bajariladi.

## 2026-09-27 — Milestone 40: Create Mod, Renaissance Astronomy & Clockwork Science Buyuk Imperiya Soatli Rasadxonasi: Astronomik Soat, Armillyar Sfera va Sayyoralar Orreriysi (Issue #39)
- **Praga Uslubidagi Minorali Astronomik Soat (`AstronomicalClock` & `astronomical_clock.glb`)**:
  - Tosh va qora marmar bezakli gotik minora ramkasi, 24 soatlik oltin rim raqamli astrolyabiya siferblati, 12 burj (zodiak) halqasi, aylanuvchi yarim-kumush/yarim-qora oy fazasi shari va qo'shaloq bronza qo'ng'iroqli foliot soat harakati (`astronomical_clock.glb`).
  - Vaqt va taqvim: 1 real soniya = 1 o'yin daqiqasi ($dt = 1.0$); 28 kunlik yil (4 fasl, har fasl 7 kun).
  - Qonli Oy (Blood Moon) erta ogohlantirish: 27-kun 20:00 da (ofatdan 24 soat oldin) avtomatik bong urib qirollik mudofaasini ogohlantirish.
  - Tortish og'irligi: 1,440 daqiqa (24 soat) avtonom quvvat yoki 16 SU kinetik quvvat bilan uzluksiz avtomatik buralish.
- **Aylanuvchi Guruch Armillyar Sfera (`ArmillarySphere` & `armillary_sphere.glb`)**:
  - O'ymakor yong'oq yog'och uchoyoq (tripod), 360° gorizont halqasi, meridiangacha bo'lgan konsentrik aylanuvchi guruch doiralar, 23.4° qiyalikdagi ekliptika burj kamari va lapis lazuli yer shari (`armillary_sphere.glb`).
  - Astronomik hisob-kitoblar: Quyosh balandligi ($\alpha$) va og'ishini ($\delta$) o'lchash; 3 kun oldindan qattiq qahraton ayoz (`HARD_FROST_WARNING`) va yozgi qurg'oqchilikni bashorat qilish.
  - Yulduzlar Navigatsiya Xaritasi (`celestial_chart`): 60s kuzatuv natijasida yaratiladi; dengiz savdo kemalariga (Milestone 38 Fluyt) berilganda safar tezligini +30% ga, savdo daromadini +50% ga oshiradi va bo'ronlarda adashish xavfini 0% ga tushiradi.
- **Soatli Mexanik Sayyoralar Orreriysi (`CelestialOrrery` & `celestial_orrery.glb`)**:
  - Sakkizburchakli qizil daraxt shkafi, silliqlangan guruch stol, markaziy oltin Quyosh va atrofida aylanuvchi 5 ta sayyora (Merkuriy, Venera, Yer+Oy, Mars, Saturn) dan iborat episiklik planetariy (`celestial_orrery.glb`).
  - Kinetik quvvat: 16 SU va 16–64 RPM tezlikda valdan quvvatlanib, orbital tezliklarda harakatlanish.
  - Astrologik Rezonanslar: Jang qorishmasi (+20% jangovar ma'naviyat, +25% eritish unumi), Hunarmand qorishmasi (+25% baxtiyorlik, +30% hunarmandlik tezligi) va Buyuk Sayyoralar Paradi (Grand Conjunction: +50% qirollik ishlab chiqarishi, 2x hosildorlik).
- **Yangi 3D Modellar (Blender 5.2)**: `astronomical_clock.glb` (390 KB), `armillary_sphere.glb` (447 KB), `celestial_orrery.glb` (256 KB) yaratildi (jami **112 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 112 ta aktiv ishtirokidagi kengaytirilgan diorama `assets/showcase_realm.png` da muvaffaqiyatli render qilindi.
- **Avtomatlashgan Testlar**: Jami **205 ta test 100% muvaffaqiyat bilan o'tdi** (0.308s).

## 2026-09-27 — Milestone 39: Create Mod, Vintage Story & Thermal Expansion Yuqori Bosimli Bug' Quvvati: Bug' Qozoni, Statsionar Bug' Dvigateli va Sentrifugal Regulyator (Issue #37)
- **Ko'p Quvurli Yuqori Bosimli Bug' Qozoni (`SteamBoiler` & `steam_boiler.glb`)**:
  - O'tga chidamli shamot g'ishtli o'choq (refractory firebox), jez qozon barabani (brass drum) mustahkamlovchi halqalar bilan, suv sathi oynasi (sight glass), bimetallik monometr va ikkita prujinali xavfsizlik klapani (`steam_boiler.glb`).
  - Termodinamik model: 12 bar optimal ishchi bosimi, 15 bar xavfsizlik purkashi (popoff relief), 20 bar falokatli portlash chegarasi (catastrophic explosion limit).
  - Bug' generatsiyasi: 850°C haroratda daqiqasiga 9 litr suv bug'latib, 512 dan 2,048 SU ekvivalentidagi to'yingan bug' oqimini uzatish.
- **Gorizontal Statsionar Bug' Dvigateli (`SteamEngineDrive` & `steam_engine_drive.glb`)**:
  - Quyma temir bedplate, yog'och plankalar bilan izolyatsiyalangan gorizontal silindr, krosskopf yo'naltiruvchilari, shatun va 1.8 metrli 6 tirgakli massiv maxovik g'ildirak (`steam_engine_drive.glb`).
  - Mexanik quvvat: 12 bar bug' bosimi va 1.0 drossel ochilishida to'liq 1,024 SU va 64 RPM kinetik quvvat generasiyasi.
  - Dinamik inersiya: 450 kg og'irlikdagi aylanuvchi maxovik g'ildirak tork tebranishlarini yutadi va yuk to'satdan ortganda mexanizmlarni silliq ushlab turadi.
- **Sentrifugal Uayt Regulyatori (`CentrifugalGovernor` & `centrifugal_governor.glb`)**:
  - James Watt tamoyiliga asoslangan quyma temir ustun, aylanuvchi vertikal shpindel, ikkita massiv jez sharlar, suriluvchi yoqa (sliding collar) va drossel richagi (`centrifugal_governor.glb`).
  - Avtomatik PID tezlik nazorati: Aylanish tezligi ($\Omega$) ortganda markazdan qochma kuch sharlarni kengaytiradi ($\theta \propto \Omega^2$), yoqani yuqoriga ko'taradi va drossel klapanini yopadi; yuk oshganda esa klapanni ochib barqaror 64 RPM tezlikni ushlab turadi.
- **Yangi 3D Modellar (Blender 5.2)**: `steam_boiler.glb` (116 KB), `steam_engine_drive.glb` (128 KB), `centrifugal_governor.glb` (134 KB) yaratildi (jami **109 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 109 ta aktiv ishtirokidagi kengaytirilgan diorama `assets/showcase_realm.png` da muvaffaqiyatli render qilindi.
- **Avtomatlashgan Testlar**: Jami **201 ta test 100% muvaffaqiyat bilan o'tdi** (0.193s).

## 2026-09-27 — Milestone 38: Anno 1404, Port Royale & Vintage Story O'rta Asr Dengiz Porti va Kema Qurilishi: Slipvey Dok, Port Krani va Flyoyt Savdo Kemasi (Issue #35)
- **Sohildagi Kema Qurish Slipvey Doki (`DrydockSlipway` & `drydock_slipway.glb`)**:
  - Dengizga -7° nishablikdagi moylangan skidlar, kil bloklari, 2 qavatli iskala va smola qozoni (`drydock_slipway.glb`).
  - 4 bosqichli kema qurilishi: Kil qo'yish (60s), qovurg'a ramkalari (90s), bort qoplash va smolalash (120s), yelkan va outfitting (90s).
  - 4 nafar kema duradgori birgalikda ishlaganda 360s jarayon atigi 144 soniyada (2.5x tezlik) yakunlanib, kema tantanali suvga tushiriladi (`LAUNCHED`).
- **Tosh Poydevorli Port Jib Krani (`QuaysideCrane` & `quayside_crane.glb`)**:
  - Sakkizburchakli ohaktosh poydevor (barbette), buriluvchi eman mast, 45° qiya strela va toshli ballast qutisi (`quayside_crane.glb`).
  - 2,500 kg (2.5 tonna) ko'tarish quvvati; 48 SU kinetik drayv (1.2 m/s, 45°/s burilish) yoki 2 ta dok ishchisi (0.4 m/s).
  - Port tranzit samaradorligi: kemalarni yukdan bo'shatish vaqtini 65% ga qisqartiradi (5 daqiqadan 1.75 daqiqaga).
- **Okean Savdo Kemasi Golland Flyoyti (`FluytCargoShip` & `fluyt_cargo_ship.glb`)**:
  - Noksimon egri bortli eman korpusi, baland kema orqa kasri, kvadrat va lotin yelkanlar majmuasi (`fluyt_cargo_ship.glb`).
  - 80 slotli ulkan tryum; shamol burchagiga ko'ra yelkan aerodinamikasi (broad reach da 6.5 tugun / 3.34 m/s).
  - Chet el savdo portlari (Ganza / Janubiy Xalifalik) bilan avtomatlashgan savdo qatnovlari.
- **Yangi 3D Modellar (Blender 5.2)**: `drydock_slipway.glb`, `quayside_crane.glb`, `fluyt_cargo_ship.glb` yaratildi (jami **106 ta GLB model**!).
- **Yangi Qirollik Dioramasi**: Barcha 106 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **140 ta engine testi** (umumiy **197 ta test**) 100% muvaffaqiyat bilan o'tdi.


## 2026-09-27 — Milestone 37: Create Mod, Railcraft & Vintage Story Shaxta Temiryo'l Logistikasi: Tishli Bug' Parovozi, Temiryo'l Strelkasi va Bunker Tushirgichi (Issue #33)
- **Tor Koleyli Kichik Shaxta Bug' Parovozi (`MineLocomotive` & `mine_locomotive.glb`)**:
  - Gorizontal silindrik qora temir qozon (boiler), mis bug' gumbazi (steam dome), dastro'mollar (coupling rods) bilan bog'langan 4 ta shpilli g'ildiraklar, ochiq kabina va ko'mir bunkeri (`mine_locomotive.glb`).
  - Tortish quvvati: 8,500 N gacha kuch, 6 ta vagonetkani (7,200 kg yuk) tortish imkoniyati.
  - Termodinamika va tezlik: 8 bar ish bosimi, 12 bar xavfsizlik klapani (popoff valve), 4.5 m/s (16.2 km/h) tranzit tezligi.
- **Mexanik Ikki Yo'nalishli Temiryo'l Strelkasi (`RailSwitch` & `rail_switch.glb`)**:
  - Quyma po'lat krestovina (frog), ostryaklar (switch points), cho'yan yukli zvenoli dastak va rotatsion signal fonari (`rail_switch.glb`).
  - Ikki yo'nalish: `STRAIGHT` (yashil signal) va `DIVERGING` (sariq signal, 2.5 m/s tezlik chegarasi).
  - 0.6 soniyada silliq o'tish; po'lat g'ildiraklar ustida bo'lganda qulflanish (interlocking); prujinali mexanizm (spring switch) bilan relsdan chiqishdan 100% himoyalangan.
- **Avtomatlashgan Estakada Bunker Tushirgichi (`HopperUnloader` & `hopper_unloader.glb`)**:
  - Rel'slar ostidagi teskari piramidasimon po'lat voronka, yo'l chetidagi prujinali richaglar (trip levers) va roliklar (`hopper_unloader.glb`).
  - Vagonetka ostidagi tushirish lyukini avtomatik urib ochish: 12 dona/s evakuatsiya tezligi (30 ta rudani 2.5 soniyada to'liq to'kib yuboradi).
  - 120 dona sig'imli qabul bunkeri va nov orqali pastdagi konveyer/pechga 8 dona/s tezlikda uzluksiz ruda quyish.
- **Yangi 3D Modellar (Blender 5.2)**: `mine_locomotive.glb`, `rail_switch.glb`, `hopper_unloader.glb` yaratildi (jami **103 ta GLB model**!).
- **Yangi Qirollik Dioramasi**: Barcha 103 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **136 ta engine testi** (umumiy **193 ta test**) 100% muvaffaqiyat bilan o'tdi.


## 2026-09-27 — Milestone 36: Georgius Agricola (*De Re Metallica*), Vintage Story & Create Mod Yerosti Kon Muhandisligi: Drenaj Suv Nasosi, Shamollatish Ventilyatori va Shaxta Lebyodkasi (Issue #31)
- **Vertikal Zanjirli Sump Drenaj Nasosi (`MineDewateringPump` & `mine_dewatering_pump.glb`)**:
  - Suv yig'iladigan chuqur (sump pit) ustidagi baland eman headframe portali, uzluksiz mis chelaklar zanjiri, tishli sproket va yuqori yog'och nov (`mine_dewatering_pump.glb`).
  - Kinetik quvvat: 48 SU quvvat sarfi (minimal 16 RPM).
  - Drenaj tezligi: daqiqasiga 150 litr suv chiqarish.
  - Chuqur gorizontlar ($Y \le 16$) grunt sizishini (100 L/min) to'liq bartaraf etib, sof 50 L/min quritish sur'atini ta'minlaydi (`is_sump_dry = true`).
- **Sentrifugali Markazdan Qochma Shaxta Ventilyatori (`MineVentilator` & `mine_ventilator.glb`)**:
  - Shilliqqurt shaklidagi radial korpus (snail-shell casing), bronza turbina, havo so'ruvchi markaziy bo'g'iz va konus truba (`mine_ventilator.glb`).
  - Kinetik quvvat: 32 SU quvvat va 20 RPM ish rejimi.
  - Toza havo yetkazish: 24 metr radiusda soniyasiga 0.75 m³ toza havo oqimi.
  - Zaharli va portlovchi gazlarni ($CH_4$, $CO_2$, $H_2S$) 95% ga kamaytirib, dimiqish va shaxta portlash xavfini bartaraf etadi.
- **Og'ir Shaxta Tik Nishi Lebyodkasi (Mining Capstan Winch) (`MiningCapstan` & `mining_capstan.glb`)**:
  - Vertikal eman baraban, pastki bronza konussimon tishli uzatma (bevel gear), xavfsizlik tishli ilmgichi (ratchet and pawl) va yo'naltiruvchi g'ildirak (`mining_capstan.glb`).
  - Yuk ko'tarish quvvati: 30° nishablikda 1,500 kg (1.5 tonna) tosh va ruda yuklangan vagonetkalar.
  - Ikki rejim: Kinetik drayv (40 SU bilan 1.0 m/s) yoki 4 kishilik konchi brigadasi bilan qo'lda aylantirish (0.35 m/s).
  - Prujinali tishli qulf (pawl) bilan avariyaviy pastga qulash xavfidan 100% himoyalangan.
- **Yangi 3D Modellar (Blender 5.2)**: `mine_dewatering_pump.glb`, `mine_ventilator.glb`, `mining_capstan.glb` yaratildi (**Yubiley 100 ta GLB model**!).
- **Yangi Qirollik Dioramasi**: Barcha 100 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **132 ta engine testi** (umumiy **189 ta test**) 100% muvaffaqiyat bilan o'tdi.


## 2026-09-27 — Milestone 35: Create Mod, TerraFirmaCraft & Vintage Story Og'ir Metallurgiya Quymaxonasi: Mexanik Bosqon, Domna Forzonkasi va Kinetik Bolg'a (Issue #29)
- **Kinetik Ekssentrikli Mexanik Charm Bosqon (`MechanicalBellows` & `mechanical_bellows.glb`)**:
  - Qo'shaloq garmonikasimon buklanuvchi charm kamera, eman ramka va orqa valga o'rnatilgan quyma temir ekssentrik kamshturgich (`mechanical_bellows.glb`).
  - Kinetik quvvatga ulanish: 32 SU sarf (minimal 12 RPM).
  - Majburiy havo oqimi: soniyasiga 0.45 m³ siqilgan kuchli havo oqimi hosil qiladi.
  - Harorat sakrashi (1550°C): o'choq haroratini 1100°C dan 1550°C gacha ko'tarib, cho'yan (`pig_iron`), yuqori uglerodli po'lat (`blister_steel`) va tigel qotishma po'latlarini (`crucible_steel`) eritishni to'liq avtomatlashtirish.
- **Domna Pechi Mis Forzonkasi va Stexiometrik Klapan (`FurnaceTuyere` & `furnace_tuyere.glb`)**:
  - Pech devorini teshib kiruvchi qizil mis naycha, sovutish g'ilofi, shomot gardishi va kapalaksimon klapan (`furnace_tuyere.glb`).
  - Havo klapani (0.75 - 0.92) orqali yonish stexiometriyasini muvozanatlash: +25% metall hosildorligi (shlak kamayadi).
  - Manometr orqali o'choq ichidagi dinamik bosimni uzluksiz o'lchash.
- **Suv Quvvatli Katta Sanoat Tilt-Bolg'asi (Helve Hammer) (`IndustrialTripHammer` & `industrial_trip_hammer.glb`)**:
  - Katta quyma temir sandon, 800 kg li eman dastali og'ir po'lat bolg'a va 3 ta egri temir barmoqli aylanuvchi taqsimlash vali (`industrial_trip_hammer.glb`).
  - 24 RPM tezlikda 3 ta barmoq har daqiqada 48 marta kuchli zarba (har 1.25 soniyada 450 Joul) beradi.
  - G'ovakli doma temirini zichlash: 4 zarbada temir quymasini (`iron_bloom`) sof temir zagotovkaga (`wrought_iron_billet`) aylantiradi.
  - Sovut plitalari va qurollar yoyish: 3 zarbada zagotovkani ikkita tekis temir plastinaga (`iron_plate`) yoyadi (5 barobar tez va nol inson mehnati bilan).
- **Yangi 3D Modellar (Blender 5.2)**: `mechanical_bellows.glb`, `furnace_tuyere.glb`, `industrial_trip_hammer.glb` yaratildi (jami **97 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 97 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **128 ta engine testi** (umumiy **185 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 34: Stronghold & Mount & Blade II Og'ir Qamal Qurollari: Gravitatsion Trebyushe, Zirhli Devorbuzar va Hujum Minorasi Belfri (Issue #27)
- **Qarshi Toshli Gravitatsion Trebyushe (`TrebuchetSiege` & `trebuchet_siege.glb`)**:
  - Uchburchakli mustahkam eman fermasi, bronza vkladishli po'lat markaziy val va 12 tonnalik tosh to'ldirilgan qarshi yuk qutisi (`trebuchet_siege.glb`).
  - Uzoq masofali ballistika: 40 metrdan 140 metrgacha qamrov.
  - 3 xil snaryad: Og'ir tosh boulderi (320 zarar, 8m shockwave), yonuvchi qora smola (240 zarar + 12 fire DPS, 10m burn), o'latli mol murdasi (biologik urush, 15m radiusda -30 morale).
  - O'qlash: 3 ta muhandis bilan qo'lda 15.0s, kinetik val bilan avtomatik 4.5s (80 SU).
- **Zirhli G'ildirakli Qo'chqor Boshli Devorbuzar (`BatteringRam` & `battering_ram.glb`)**:
  - To'rtta quyma zanjirga osilgan qalin eman daraxti tanasi va cho'yan qo'chqor boshli zarba uchligi (`battering_ram.glb`).
  - Mayatnik tebranishi: har 3.2 soniyada 180 ball kinetik zarba.
  - Ho'l charm (rawhide) ikki nishabli boshpana: 80% o'qlarni qaytarish va 50% qaynoq smola olovini so'ndirish.
- **Ko'chma Ko'p Qavatli Hujum Minorasi Belfri (`SiegeTower` & `siege_tower.glb`)**:
  - 8 metr balandlikdagi 3 qavatli yog'och minora; o'qchi slitlari va tepasida osma shturm ko'prigi (corvus bridge) (`siege_tower.glb`).
  - 6 ta askar tomonidan 0.6 m/s tezlikda devorga suriladi; 2 soniyada temir tirnoqli ko'prik parapetga tashlanadi.
  - 8 ta saralangan qilichboz desantni 4 soniyada (2 troop/s) devorga yopirilib tushirish; 70% o'qdan himoya hordingi.
- **Yangi 3D Modellar (Blender 5.2)**: `trebuchet_siege.glb`, `battering_ram.glb`, `siege_tower.glb` yaratildi (jami **94 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 94 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **124 ta engine testi** (umumiy **181 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 33: Stronghold & Medieval Engineering Qasr Xandaq Ko'prigi Chig'iri, Ko'tarma Darvoza va G'ildirakli Shaxta Krani (Issue #25)
- **Qasr Xandag'i Ko'tarma Ko'prik Chig'iri (`DrawbridgeController` & `drawbridge_winch.glb`)**:
  - A-simon og'ir eman ustunli chig'ir, tishli po'lat baraban va qo'sh richagli aylantirish g'ildiragi (`drawbridge_winch.glb`).
  - Qo'shaloq rejim: 2 ta soqchi yordamida qo'lda ko'tarish 12.0s (7.5 deg/s); kinetik val uzatmasi orqali shiddatli ko'tarish 3.5s (25.7 deg/s, 64 SU quvvat).
- **Og'ir Eman Ko'tarma Ko'prik Platformasi va Zanjir Fizikasi (`drawbridge_platform.glb`)**:
  - 6m x 4m qalin eman taxtalaridan iborat, temir kamar va piramidasimon mixlar bilan mustahkamlangan ko'tarma platforma (`drawbridge_platform.glb`).
  - Qo'shaloq soxta temir zanjirlar (har biri 800 HP mustahkamlik).
  - Qamal to'plari zanjirlarni uzganda erkin qulash va pastdagi dushman piyodalarini bosib qoluvchi 120 ball ezuvchi zarar (Crush Damage).
- **Katta G'ildirakli Vertikal Shaxta Krani (`CargoCrane` & `treadwheel_crane.glb`)**:
  - 2.6 metrli ichki qadam bosuvchi g'ildirak (treadwheel), vertikal gantry ustuni va egilgan ko'tarish balkasi (derrick jib) ga ega kran (`treadwheel_crane.glb`).
  - 40 metrgacha vertikal chuqurlikdan 1,200 kg yuk sig'imi (30-uyali ruda vagonetkasi yoki 4 ta katta kesilgan tosh bloki).
  - Vertikal logistika tranzit vaqtini 70% ga (0.30x) qisqartirish.
  - Ishchi soniyasiga 0.15 charchoq sarflaydi; kinetik valga ulanganda fuqaro mehnatisiz avtomatlashtiriladi.
- **Yangi 3D Modellar (Blender 5.2)**: `drawbridge_winch.glb`, `drawbridge_platform.glb`, `treadwheel_crane.glb` yaratildi (jami **91 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 91 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **120 ta engine testi** (umumiy **177 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 32: Create Mod & Vintage Story Kinetik Transmissiya, Vallar, Burchakli Tishli Quti va Mexanik Mufta (Issue #23)
- **Graf Asosidagi Kinetik Tarmoq Hal Qiluvchisi (`KineticNetworkManager`)**:
  - BFS grafigi orqali barcha ulangan manbalar, vallar va dastgohlarni aniqlash.
  - Quvvat ($\sum SU_{capacity}$) va yuklanish ($\sum SU_{consumed}$) balansini hisoblash.
  - Yuklanish me'yordan oshganda avtomatik tarmoq bloklanishi (Overload Stalling) va $RPM \to 0.0$ to'xtashi.
- **Chiziqli Kinetik Val va O'qlar (`DriveShaft` & `drive_shaft.glb`)**:
  - 1x1 venzel o'lchamli sayqallangan po'lat val, tishli gardishlar va dub podshipnik kronshteyni (`drive_shaft.glb`).
  - 16 metrgacha oraliq tayanchsiz erkin quvvat uzatish (0 SU sarfi).
  - Devor va pol ichidan o'tuvchi himoyalangan (`EncasedShaft`) rejim.
- **90-Gradusli Konussimon Tishli Quti (`BevelGearbox` & `bevel_gearbox.glb`)**:
  - To'rt tomonlama chiqish o'qlariga ega quyma temir korpus va 45° bronza tishli charxlar (`bevel_gearbox.glb`).
  - Aylanish yo'nalishini 90 darajaga burish va yo'nalishni teskarilash (`Invert`) imkoniyati.
- **Mexanik Friktsion Mufta va Richag (`MechanicalClutch` & `mechanical_clutch.glb`)**:
  - Ikkita friktsion disk va qo'l richagi orqali pastki zanjirlarni uzish va ulash.
  - Yuk tashlash (Load Shedding): bloklangan tarmoqni zudlik bilan qayta faollashtirish.
- **Yangi 3D Modellar (Blender 5.2)**: `drive_shaft.glb`, `bevel_gearbox.glb`, `mechanical_clutch.glb` yaratildi (jami **88 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 88 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **116 ta engine testi** (umumiy **173 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 31: Vintage Story & Valheim Realistik PBR Teksturalar, Triplanar Sheyder, Konstruktiv Yuk Fizikasi va Atmosfera Realizmi (Issue #21)
- **Realistik PBR Voksel Teksturalari va Triplanar Sheyder (`voxel_pbr_triplanar.gdshader` & `voxel_atlas_*.png`)**:
  - 12 ta tabiiy blok uchun procedural PBR teksturalar (Albedo, Tangent Normal, Roughness).
  - Uchta 256x192 birlashtirilgan PBR atlas: `voxel_atlas_albedo.png`, `voxel_atlas_normal.png`, `voxel_atlas_roughness.png`.
  - Dunyo koordinatalari bo'yicha triplanar proyeksiyalash (tik qoyalarda cho'zilishni nolga tushiradi).
  - Dinamik yomg'ir suvi ho'lligi (`rain_wetness`, specular 0.85) va qishki qor to'planishi (`snow_accumulation`).
- **Konstruktiv Yuk Ko'tarish Fizikasi va Qulash Dinamikasi (`StructuralIntegrityManager` & `masonry_buttress.glb`)**:
  - Gorizontal konsol (cantilever) chegaralari: Bedrock $\infty$, Tosh 6m, G'isht 6m, Yog'och 4m, Tuproq 1m, Qum 0m.
  - Gotika uslubidagi uchuvchi tosh tirgak (`masonry_buttress.glb`): konsol oraliq masofasiga +3 metr qo'shimcha tayanchni ta'minlaydi.
  - Tayanchsiz qolgan voksellarning fizik gravitatsiya qoldiqlari (`falling rubble`) sifatida qulashi va 255 kJ kinetik zarba berishi.
- **Atmosfera Quyosh Harorati va Volumetrik Tuman (`EnvironmentRealismManager` & `weather_vane.glb`, `barometer_station.glb`)**:
  - Quyosh Kelvin harorati: Tongda 4750K, tushda 6500K, shafaqda 2600K, tunda 12000K.
  - Tanner Helland qora tana nurlanishi spektri bo'yicha tabiiy yorug'lik rangini hisoblash.
  - Volumetrik Reley va Mi tuman zichliklari (ochiq havo 0.005 dan qor bo'roni 0.120 gacha).
  - Mis xo'rozli shamol yo'naltirgichi (`weather_vane.glb`) va devoriy simobli barometr stantsiyasi (`barometer_station.glb`).
- **Haqiqiy Aerodinamik Ballistika va Shamol Ta'siri (`BallisticRealism`)**:
  - Barometrik havo zichligi: $\rho(y) = 1.225 \cdot e^{-y / 8500}$ kg/m³.
  - Aerodinamik qarshilik $\vec{F}_d = -\frac{1}{2} \rho |\vec{v}_{rel}| \vec{v}_{rel} C_d A$ va yon shamol ta'sirida traektoriya og'ishi (crosswind drift).
  - Kinetik energiya va zirh penetratsiyasi (bodkin o'qi gambesonni teshib o'tadi, to'liq po'lat plitadan sachraydi).
- **Yangi 3D Modellar (Blender 5.2)**: `weather_vane.glb`, `barometer_station.glb`, `masonry_buttress.glb` yaratildi (jami **85 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 85 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **112 ta engine testi** (umumiy **169 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 30: Medieval Dynasty & Farmer's Delight Shamol Tegirmoni, Un Silosi va Nonvoyxona (Issue #19)
- **Kinetik Shamol Tegirmoni (`StoneWindmill` & `stone_windmill.glb`)**:
  - Konussimon tosh minora va 4 ta tuval parrakli aylanma shamol tegirmoni (`stone_windmill.glb`).
  - Dinamik shamol tezligi: balandlik va bo'ronli havoga qarab 0.5x dan 1.8x gacha o'zgaradi.
  - 384 SU mexanik kinetik quvvat ishlab chiqarish.
  - 200% un hosildorligi: 1 bug'doy $\rightarrow$ 2 qop toza un (`wheat_flour`).
- **Ko'tarilgan Namlikdan Himoyalangan Un Donxonasi (`FlourSilo` & `flour_silo.glb`)**:
  - 4 ta tirgakli, temir chambarakli yog'och donxona (`flour_silo.glb`).
  - Sig'imi: 120 qop un.
  - Germetik saqlash: namlik va zararkunandalar tufayli un chirishini 85% ga kamaytiradi.
  - Gravitatsion pastki tushirish voronkasi orqali aravalarga tezkor un to'ldirish.
- **Gumbazli Qizil G'ishtli Nonvoyxona Pechi (`BakerOven` & `baker_oven.glb`)**:
  - Qizdirilgan o'choqli, gumbazli g'isht pech va nonvoy kuragi (`baker_oven.glb`).
  - Termal akkumulyatsiya (220°C): 180°C dan oshganda non pishirish boshlanadi.
  - Retseptlar: Qora javdar noni (2 un + 1 suv $\rightarrow$ 3 non, +45 to'qlik, +10 energiya) va Shohona briyosh (2 un + 1 sut + 1 asal $\rightarrow$ 3 non, +70 to'qlik, +15 ruhiyat).
- **Yangi 3D Modellar (Blender 5.2)**: `stone_windmill.glb`, `flour_silo.glb`, `baker_oven.glb` yaratildi (jami **82 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 82 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **108 ta engine testi** (umumiy **165 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 29: Manor Lords & Bellwright Yo'l To'shash, Ko'cha Chiroqlari va Logistika Koridorlari (Issue #17)
- **Bosqichma-bosqich Yo'l To'shash Tizimi (`RoadNetwork` & `paved_road_tile.glb`)**:
  - Modular tosh plitka (`paved_road_tile.glb`), drenaj va chekka bordyurlar.
  - Yo'l qatlamlari: Dirt Path (+10% tezlik), Gravel Road (+25% tezlik), Cobblestone Paved (+50% tezlik, yo'l narxi 0.50x).
  - Sun'iy intellekt va fuqarolarni avtomatik ravishda qoplangan magistral yo'llarga yo'naltirish.
  - Og'ir aravalar va xo'kizlar harakatidan yeyilish mexanikasi hamda tosh bilan ta'mirlash.
- **Shahar Ko'cha Chirog'i va Tungi Xavfsizlik Aurasi (`StreetLamp` & `street_lamp.glb`)**:
  - O'yma tosh asos, temir ustun va shisha fonus (`street_lamp.glb`).
  - Shomdan tonggacha (18:00 - 06:00) avtomatik yonish sensori.
  - Hayvon yog'i (`tallow`) zaxirasi: 1 tallow = 3 kechalik yorug'lik.
  - 9.0m yorug'lik radiusi: tungi jinoyatchilik va o'g'rilikni fosh qilib, qochirish qalqoni.
- **Chorraha Ko'rsatkichi va Tranzit Koridori Ustuvorligi (`LogisticsWaypoint` & `road_signpost.glb`)**:
  - O'yma yog'och yo'l ko'rsatkichi (`road_signpost.glb`) — "Market Square", "Castle Keep", "Iron Mine".
  - Magistral koridori: ustuvor yo'nalishdagi kuryerlar yuk hajmiga +15% unumdorlik bonusi.
  - Harbiy yig'ilish nuqtasi (Muster Point) vazifasi.
- **Yangi 3D Modellar (Blender 5.2)**: `paved_road_tile.glb`, `street_lamp.glb`, `road_signpost.glb` yaratildi (jami **79 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 79 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **104 ta engine testi** (umumiy **161 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 28: Valheim & Vintage Story Yerosti Tosh Kriptasi, Sarkofag Qoldiqlari va Ekspeditsiya Zulmati (Issue #15)
- **Protsedural Qadimiy Tosh Kriptasi (`CryptDungeon` & `crypt_entrance.glb`)**:
  - Tog'liklar va chuqur qatlamlarda ($Y < 12$) o'yma tosh daxma kirishi (`crypt_entrance.glb`).
  - Protsedural ko'p xonali tuzilma: Kirish vestibyuli, ustunli galereyalar va shohona dafn zallari.
  - Yerosti to'liq zulmat okluziyasi (0.05 ambient light) va optik tuman zichligi (0.04 fog density).
  - Sarkofaglar ochilganda daxma qo'riqchilari (`CryptSkeletonKnight`, `CryptDraugr`) ning uyg'onishi va pistirma hujumi.
- **O'yma Ohaktosh Sarkofagi va Nodir Yodgorliklar (`AncientSarcophagus` & `stone_sarcophagus.glb`)**:
  - Ustida ritsar qiyofasi o'yilgan og'ir ohaktosh sarkofag (`stone_sarcophagus.glb`).
  - Lom bilan ochish (`prying`): Oddiy qo'lda 12%/s, temir lom bilan 2.2x tezlik (26.4%/s).
  - Qopqonlar: Zaharli nayzalar (`POISON_DARTS` - 25 zarar), o'g'rilik mahorati (Rogue skill >= 40) orqali zararsizlantirish.
  - Nodir yodgorliklar: Qadimiy Damashq Po'lati Chizmasi (45 oltin qiymat), Qirol Aldenning Muhrli Uzugi (+20 nufuz, +15 vassallar bilan aloqa) va qadimiy oltin tangalar.
- **Temir Devor Mash'ali va Ekspeditsiya Ruhiyati (`DungeonCrawlerManager` & `wall_sconce.glb`)**:
  - Forged iron devor mash'aldoni (`wall_sconce.glb`), 7.5m yorug'lik radiusi va 240s yonish muddati.
  - Ruhiyat va qo'rquv: Zulmatda ruhiyat yo'qolishi (-2.0/s), 25% dan pasayganda `Fear Debuff` (-30% jangovar aniqlik va qochish xavfi). Mash'ala atrofida ruhiyatning tiklanishi (+1.5/s).
  - Topilgan relikviyalarni qasr xazinasiga topshirish va daromadga aylantirish.
- **Yangi 3D Modellar (Blender 5.2)**: `crypt_entrance.glb`, `stone_sarcophagus.glb`, `wall_sconce.glb` yaratildi (jami **76 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 76 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **100 ta engine testi** (umumiy **157 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 27: Medieval Dynasty & Going Medieval Suv Logistikasi, Qishloq Qudug'i, Akveduk Sug'orish va O't O'chirish (Issue #13)
- **Tosh Quduq va Aholi Chanqog'i Mexanikasi (`WaterWell` & `water_well.glb`)**:
  - Daryo toshlaridan terilgan, yog'och shingilli soyabon va chig'irli quduq (`water_well.glb`).
  - Yerosti suv qatlamidan har kuni avtomatik 8 chelak toza ichimlik suvi (`potable_water`) to'ldiradi (maksimal sig'im 24 chelak).
  - Har bir fuqaro kuniga 1 chelak suv iste'mol qiladi. Suv yetishmasa `Dehydrated` holati beriladi: -25% mehnat tezligi va -15 ruhiyat (morale) jarimasi.
  - Yong'in o'chirish zaxirasi: Bino olov olganda quduqdan 4 chelak suv olinib, yong'in o'chiriladi.
- **Rim Me'morchiligi Akveduk Sug'orish Tizimi (`AqueductIrrigation` & `aqueduct_pipe.glb`)**:
  - Tosh ustunli arka va yuqori suv o'zani bo'ylab oqadigan akveduk kanali (`aqueduct_pipe.glb`).
  - Daryo vodiysidan suv olib, har bir segment atrofida 8 metrlik to'liq namlik aurasini ta'minlaydi.
  - Hosil Bonusi: Sug'orilgan ekinlar +30% (1.30x) tezroq o'sadi va yozgi qurg'oqchilik qovjirashidan 100% himoyalanadi.
  - Mustahkamlik: 150 HP (yong'inga mutlaqo chidamli, qamal toshlari zarbasidan sinishi mumkin).
- **Zaxira Suv Bochkasi va Harbiy Suv Idishlari (`WaterCask` & `water_cask.glb`)**:
  - Maxsus yog'och taglikdagi, jez jo'mrakli 40 chelak sig'imli eman bochka (`water_cask.glb`).
  - Askar va kuryerlar uchun charm suv idishlari (`hydration_canteen`): Har bir jangchiga 2 chelak zaxira berilib, 24 soatlik to'liq chanqoq immuniteti bilan ta'minlanadi.
- **Yangi 3D Modellar (Blender 5.2)**: `water_well.glb`, `aqueduct_pipe.glb`, `water_cask.glb` yaratildi (jami **73 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 73 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **96 ta engine testi** (umumiy **153 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 26: Medieval Dynasty & Bellwright Ovchilik Kulbasi, Eman Po'stlog'i Teri Oshlash va Mo'yna Quritish Dastgohi (Issue #11)
- **O'rmon va Tog' Ovchilik Kulbasi (`HuntingLodge` & `hunting_lodge.glb`)**:
  - Malakali ovchilar tayinlash (3 tagacha); Deep Forest (1.5x) va Highlands (1.2x) biomlarida yovvoyi kiyik va cho'chqa ovi mahsuldorligi.
  - Kamonchilar Boshpanasi (`archery_blind`): Hosildorlikka +35% bonus va yovvoyi hayvonlar hujumi jarohatini 15% dan 3% ga tushirish.
  - Kunlik hosil: To'yimli kiyik go'shti (`raw_venison`), xom teri (`raw_hide`), hayvon yog'i (`tallow`) va xom mo'yna (`raw_pelt`).
- **Eman Po'stlog'i Teri Oshlash Qadog'i (`TanneryVat` & `tannery_vat.glb`)**:
  - 2 xom teri + 1 eman po'stlog'i (`oak_bark` tannin) + 1 chelak suv $\rightarrow$ 2 mustahkam oshlangan charm (`cured_leather`).
  - Feodal hunarmandchilik: Gambeson sovuti (4 charm + 2 jun), Ishchi xo'kiz jabdug'i (3 charm + 2 temir quyma) va mergan sadoqi.
- **Mo'yna Quritish Dastgohi va Shohona Chopon (`FurDryingRack` & `fur_drying_rack.glb`)**:
  - A-simon quritish ramkasida xom mo'ynalarni tortib quritish (20 soniya per pelt $\rightarrow$ `cured_fur`).
  - Qishki Shohona Mo'ynali Chopon (`fur_cloak`): 3 cured fur + 1 woolen tunic (+50 sovuqqa bardoshlilik, +15 zodagonlar baxtiyorligi va 15 oltin tanga bozor narxi).
- **Yangi 3D Modellar (Blender 5.2)**: `hunting_lodge.glb`, `tannery_vat.glb`, `fur_drying_rack.glb` yaratildi (jami **70 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 70 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **92 ta engine testi** (umumiy **149 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-27 — Milestone 25: Ko'p Biomli Voksel Olam, Qaroqchilar Turlari (Archetypes) va Relyef Harakati Fizikasi (Issue #9)
- **Ko'p Biomli Relyef Generatsiyasi va 3D G'orlar (`BiomeManager` & `VoxelWorld`)**:
  - 4 xil tabiiy biom: Yashil tekisliklar (`Plains`), Qalin o'rmon (`Deep Forest`), Baland qoyali tog'lar (`Highlands`) va Dengiz sathidan past daryo vodiylari (`River Valley`, $Y < 6$).
  - 3D Simplex Cave noise: qoyalar ichida tabiiy yerosti g'orlari va o'tish yo'laklari (noise > 0.65 havo bo'shliqlari o'yadi).
  - Voksel sirtining biomga mos blok turlari: unumdor tuproq/o't, tog' qoyasi toshlari, va daryo tubi/qirg'og'idagi qum bloklari.
- **Qaroqchilar Taktik Turlari va Istehkomlar (`BanditArchetype`, `BanditCamp`, `bandit_tent.glb`, `spiked_barricade.glb`, `loot_chest.glb`)**:
  - Qalqonchi (`Shieldbearer`): Og'ir temir qalqon bilan saf tortib, frontal yaqin jang zarbalarini 75% qaytaradi, kamon o'qlarini 90% defleksiya qiladi. Flank yoki orqadan zarba berish talab etiladi.
  - O'qchi Mergan (`Raider Archer`): 15–25m masofadan ballistik o'q yog'diradi. O'yinchi yaqinlashganda (<6m) "Kiting Retreat" harakati bilan chekinadi.
  - Berserker (`Raider Berserker`): 6m masofadan sakrab hujum qiladi (leap attack), +50% harakat tezligi va 24 ball zirhni inkor qiluvchi (armor-piercing) zarar beradi.
  - Qaroqchilar Qarorgohi Chodiri (`bandit_tent.glb`), Tikanli Barrikada (`spiked_barricade.glb` - urilganlarga 20 aks-zarar beradi) va O'lja Sandig'i (`loot_chest.glb` - oltin, temir va ozuqa beradi).
- **Relyef Harakatlanish Tezligi va Boids Ajralishi (`GridPathfinder3D`)**:
  - Tosh to'shalgan yo'llar: +20% tezlik bonusi (1.20x).
  - Daryo va suv havzalari: 50% suzish qarshiligi (0.50x sekinlashuv).
  - Flocking Boids Separation: 1.2m radiusdagi jangchilar va fuqarolar o'rtasida to'qnashuv itarish kuchlari hisoblanib, birliklarning bir-biriga yopishib qolishining (unit stacking) oldi olinadi.
- **Yangi 3D Modellar (Blender 5.2)**: `bandit_tent.glb`, `spiked_barricade.glb`, `loot_chest.glb` yaratildi (jami **67 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 67 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **88 ta engine testi** (umumiy **145 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-26 — Milestone 24: Manor Lords & Medieval Dynasty Chorvachilik, Xo'kizlar Logistikasi, Qo'y Juni va Qishki Ozuqa Oxuri (Issue #7)
- **Og'ir Yog'och Molxona va Xo'kizlar Logistikasi (`PastureBarn` & `pasture_barn.glb`)**:
  - Ishchi Xo'kizlar (`draft_oxen`): Bir safarda 4 ta og'ir xodani 1.8x tezlik bilan qurilishga yetkazib, logistika tirbandligini bartaraf etish.
  - Sog'in Sigirlar (`dairy_cows`): Kuniga 4 ko'za yangi sut (`milk_jug`) sog'ib olish.
- **Qo'yxona va Qishki Jun Kiyim To'qish (`SheepPasture` & `sheep_pen.glb`)**:
  - Qo'ylardan har 2 kunda 8 ta toza qo'y juni (`raw_wool`) qirqish.
  - Qalin Jun Nimcha (`woolen_tunic`): 2 ta jun $\rightarrow$ 1 ta nimcha (+35 qishki sovuqqa bardoshlilik va +10 baxtiyorlik).
- **Qishki Ozuqa Oxuri va Muzlash Mexanikasi (`FeedingTrough` & `feeding_trough.glb`)**:
  - 40 birlik somon/silos sig'imli oxur; havo harorati $5^\circ\text{C}$ dan tushganda mollarni qishki ozuqa bilan ta'minlash.
- **Yangi 3D Modellar (Blender 5.2)**: `pasture_barn.glb`, `sheep_pen.glb`, `feeding_trough.glb` yaratildi (jami **64 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 64 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **84 ta engine testi** (umumiy **141 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-26 — Milestone 23: Stronghold & Mount & Blade II Qasr Qamal Mudofaasi, Mangonel Katapultasi, Qaynoq Smola Qozoni va O'tkir Panjara Darvoza (Issue #5)
- **Mangonel Katapultasi va Yong'inli Toshlar (`SiegeEngine` & `catapult.glb`)**:
  - 15m dan 65m gacha ballistik masofada dushman saflarini o'qqa tutish.
  - 120 ball to'g'ridan-to'g'ri zarba va 12 metr radiusdagi zarba to'lqini.
  - Olovli tosh (`fire_boulder`): +50 qo'shimcha yong'in zarbasi (jami 170 ball).
- **Qaynoq Qora Smola Qozoni (`PitchCauldron` & `pitch_cauldron.glb`)**:
  - Darvoza arki mudofaasi: 6 metr radiusda 15 soniya davomida 40 DPS (jami 600 zarba salohiyati) olov ko'lmagi.
  - Raqiblar harakat tezligini 60% ga (0.40x) sekinlashtirish.
  - 5 ta zaryad zaxirasi va 45 soniyalik qayta qaynash sikli.
- **Mustahkam O'tkir Temir Panjara Darvoza (`PortcullisGate` & `portcullis_gate.glb`)**:
  - 500 mustahkamlik HP, devorbuzar va bolg'a zarbalariga -50% chidamlilik, o'q-yoylarga -80% defleksiya.
  - Tuzoq ezish (Trap Crush): Darvoza tushirilganda ostidagi bosqinchilarga 80 crushing zarbasi beradi.
- **Yangi 3D Modellar (Blender 5.2)**: `catapult.glb` (450 KB), `pitch_cauldron.glb` (331 KB), `portcullis_gate.glb` (211 KB) yaratildi (jami **61 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 61 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **80 ta engine testi** (umumiy **137 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-25 — Milestone 22: Medieval Dynasty & Valheim Asalarichilik, Asal Sharobi va Mum Shamlar (Issue #3)
- **Somonli Asalari Uyasi va Changlatish (`ApiaryBeehive` & `beehive_skep.glb`)**:
  - Har kuni passiv 3 ta asalari mumi katagi (`honeycomb`) va 2 ta toza mum (`beeswax`) ishlab chiqarish.
  - 18 metr radiusdagi ekinlarni changlatib, o'sish tezligini +20% ga (1.20x) oshirish.
- **Asal Sharobi Bochkasi va Mum Shamdon (`MeadFermenter`, `mead_fermenter.glb` & `candle_candelabra.glb`)**:
  - Oltin Asal Sharobi (`honey_mead`): 2 honeycomb + 1 toza suv + 1 bug'doy $\rightarrow$ 2 ko'za sharob (+15 morale va qishki sovuqqa +25 issiqlik bardoshliligi).
  - Mum Shamlar (`beeswax_candle`): 2 ta mum $\rightarrow$ 3 ta sham (tutunsiz ichki va yer osti yoritish).
- **Yangi 3D Modellar (Blender 5.2)**: `beehive_skep.glb` (541 KB), `mead_fermenter.glb` (330 KB), `candle_candelabra.glb` (79 KB) yaratildi (jami **58 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 58 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **76 ta engine testi** (umumiy **133 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-25 — Milestone 21: Going Medieval & RimWorld Tabibxona, Dorivor Malhamlar va Shifoxona To'shagi (Issue #1)
- **Giyohshunos va Alkimyogar Dastgohi (`ApothecaryBench` & `apothecary_bench.glb`)**:
  - Steril bint (`sterile_bandage`): 1 mato + 1 dorivor giyoh $\rightarrow$ 2 ta bint (qon ketishini darhol to'xtatadi, +15 HP).
  - Dorivor malham (`herbal_poultice`): 2 giyoh + 1 toza suv $\rightarrow$ 1 ta malham (yara infeksiyasini davolaydi, +30 HP).
  - Vabo ziddizahari (`plague_antidote`): 3 giyoh + 1 sarimsoq $\rightarrow$ 1 ta ziddizahar (infeksiya va qon ketishni bir zumda bartaraf etadi, +45 HP).
- **Shifoxona Jarrohlik To'shagi va Dori Qutisi (`InfirmaryBed`, `infirmary_bed.glb` & `medicine_chest.glb`)**:
  - Yarador askar va kasal fuqarolarni shifoxonaga yotqizish (`admit_patient()`), tabib nazorati ostida sog'ayish tezligini daqiqasiga 4.0 HP gacha oshirish.
  - Sog'ayib chiqqan fuqarolar uchun aholi ruhiyatiga +8 morale bonusi.
- **Yangi 3D Modellar (Blender 5.2)**: `apothecary_bench.glb` (155 KB), `infirmary_bed.glb` (23 KB), `medicine_chest.glb` (44 KB) yaratildi (jami **55 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 55 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **72 ta engine testi** (umumiy **129 ta test**) 100% muvaffaqiyat bilan o'tdi.

## 2026-09-25 — Milestone 20: Manor Lords & Bellwright Militsiya Zaxiraxonasi, Burgage Hovli Qo'shimchalari va Jang Mashqi Mankeni
- **Qurollar Zaxiraxonasi va Fuqaro Lashkarlari (`MilitiaArmory` & `armory_rack.glb`)**: Manor Lords va Bellwright andozasidagi harbiy safarbarlik tizimi:
  - Og'ir eman yog'ochidan qurol-yarog' javoni (nayza, qalqon, dubulg'a, yoy va o'qlar zaxirasi).
  - Hukmdor buyrug'i bilan dehqonlarni harbiy guruhga safarbar qilish (`muster_squad()`), ularni qurollantirib jangovar kuchga aylantirish (HP +40, Armor +25, Melee Attack +18).
  - Jang tugagach qurollarni zaxiraxonaga qaytarib topshirish va dehqonlarni tinch mehnatga qaytarish (`demobilize_squad()`).
- **Dehqon Xonadoni Hovli Qo'shimchalari (`BurgagePlot` & `burgage_coop.glb`)**: Manor Lords andozasidagi hovli xo'jaligi:
  - Tovuq katagi (`CHICKEN_COOP`): Har kuni passiv 3 ta tuxum va 1 ta pat ishlab chiqarish.
  - Echkixona (`GOAT_PEN`): Har kuni passiv 2 ta teri va 1 ko'za sut berish.
  - Sabzavot polizi (`VEGETABLE_GARDEN`): Sabzi, karam va piyoz hosili berish.
  - Oila a'zolari baxtiyorligini oshirish (+15) va Xazinaga qo'shimcha yer solig'i (+1 tanga/kun) to'lash.
- **Harbiy Jang Mashqi Mankeni (`TrainingDummy` & `training_dummy.glb`)**: Bellwright andozasidagi jangovar mashg'ulot obyekti:
  - Askarlar va fuqarolar zarba berib `melee_skill` va `archery_skill` mahoratini oshiradi (har zarbaga +2 XP, 50 ballgacha).
  - Manken mustahkamligi 200 zarba; singanda 2 ta yog'och va 1 ta charm tasma bilan qayta ta'mirlanadi.
- **Yangi 3D Modellar (Blender 5.2)**: `armory_rack.glb` (569 KB), `burgage_coop.glb` (306 KB), `training_dummy.glb` (338 KB) yaratildi (jami **52 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 52 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **68 ta test 100% muvaffaqiyat bilan o'tdi** (0.009s).

## 2026-09-25 — Milestone 19: Tashqi Qirollik O'lponi (Crown Tribute) va Kon Outpost Karvon Logistikasi
- **Tashqi Qirollik O'lponi va Sherif Aravasi (`CrownTribute` & `tax_sheriff_cart.glb`)**: Medieval Dynasty va Bellwright andozasidagi tashqi moliyaviy bosim:
  - Mavsumiy Qirol Noibi (Crown Sheriff) tashrifi; bino va aholi soniga mutanosib feodal o'lpon undirish.
  - Agar 2 mavsum ketma-ket to'lanmasa, Qirollik jazo ekspeditsiyasi (Crown Punitive Expedition) qo'shin tortib keladi.
- **Chekka Kon va O'rmon Outposti (`Outpost` & `outpost_banner.glb`)**: Bellwright va Manor Lords andozasidagi frontier lageri:
  - 500-1000m uzoqlikdagi tog' shaxtalarida ishlovchilar uchun tunash va oraliq bufer ombori.
  - 10 ta ruda to'plangach, avtomatik ravishda otli karvon jo'natilib poytaxt xazinasiga resurslarni yetkazadi.
- **Muqaddas Jasad Yoqish Gulxani (`FuneralPyre` & `funeral_pyre.glb`)**: RimWorld va Going Medieval andozasidagi sanitariya inshooti:
  - Qamal yoki vabodan so'ng o'liklarni yondirib tozalash (o'tin sarflaydi), 30 metr radiusda epidemiya va kasallik (miasma) xavfini yo'qotadi, sharafli dafn uchun aholiga +10 morale beradi.
- **Yangi 3D Modellar (Blender 5.2)**: `outpost_banner.glb` (23 KB), `tax_sheriff_cart.glb` (90 KB), `funeral_pyre.glb` (98 KB) yaratildi (jami **49 ta GLB model**).
- **Yangi Qirollik Dioramasi**: Barcha 49 ta aktiv ishtirokidagi diorama `assets/showcase_realm.png` da qayta render qilindi va brainga saqlandi.
- **Avtomatlashgan Testlar**: Jami **64 ta test 100% muvaffaqiyat bilan o'tdi** (0.009s).

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

