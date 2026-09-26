# O'zgarishlar tarixi

## 2026-09-23 — Unreal migratsiyasi boshlandi

- GDD talablarini bosqichma-bosqich amalga oshirish rejasi va bajarilish daftari yaratildi.
- Unreal yo'nalishi, C++ yadro, yagona inventar, versiyalangan save va tekshiruv mezonlari tanlandi.
- Dastlabki Godot prototipi va foydalanuvchining showcase fayllari saqlandi.
- Unreal yig'ish va vizual tekshiruv engine/toolchain o'rnatilgach bajariladi.

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

