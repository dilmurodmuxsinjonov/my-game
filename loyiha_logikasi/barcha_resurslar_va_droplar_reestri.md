# Voxel Lord: Feudal Realm — To'liq Resurslar, Mahsulotlar va Droplar Reestri

Ushbu reestr o'yindagi barcha ashyolar, tabiiy boyliklar, taomlar, mob droplari va sehirlarning to'liq katalogidir. Har bir elementning qayerdan olinishi yoki nima orqali tayyorlanishi qat'iy belgilangan.

---

## 1. TABIIY RUDALAR VA XOMASHYOLAR

| Ashyo Nomi | Qayerdan Olinadi / Qaziladi | Qatlam Chuqurligi | Ishlatilishi / Maqsadi |
| :--- | :--- | :--- | :--- |
| **Yog'och (Logs)** | O'rmon daraxtlarini bolta bilan chopish | Yer yuzasi | Taxta, qurilish, asbob dastasi, ko'mir tayyorlash |
| **Ko'mir Rudasi (Coal Ore)** | Tog' qoyalari va yerosti shaxtalari | $Y < 25$ | Pech yoqilg'isi, mash'ala, metall eritish |
| **Mis Rudasi (Copper Ore)** | Sayoz yerosti qatlamlari | $Y < 20$ | Mis quymasi, dastlabki qozonlar va qurollar |
| **Temir Rudasi (Iron Ore)** | O'rta yerosti qatlamlari | $Y < 15$ | Temir quymasi, mustahkam qurollar, sovutlar, asboblar |
| **Oltin Rudasi (Gold Ore)** | Chuqur yerosti qatlamlari | $Y < 8$ | Oltin quymasi, tanga zarb qilish, sehr o'tkazgich |
| **Chuqur Gavharlar (Deep Gems)** | Abissal eng chuqur g'orlar | $Y < 5$ | Sehrli runalar, noyob zargarlik, elita savdosi |
| **Loy (Clay)** | Daryo va ko'l qirg'oqlari | Yer yuzasi | G'isht quyish, koshin, sopol idishlar |
| **Tosh Tuz (Rock Salt)** | Shaxta tuz tomirlari yoki Savdo karvoni | $Y < 12$ | Go'shtni tuzlash, uzoq muddatli oziq-ovqat saqlash |

---

## 2. QURILISH MATERIALLARI VA TOSHLAR

| Material Nomi | Qanday Tayyorlanadi / Olinadi | Foydalaniladigan Dastgoh | Xususiyati / Vazifasi |
| :--- | :--- | :--- | :--- |
| **Oddiy Tosh (Cobblestone)** | Tosh bloklarini cho'kichda qazish | Cho'kich | Oddiy devorlar, o'choq asosi, poydevor |
| **Tosh G'isht (Stone Bricks)** | Tosh + Ko'mirni pechda pishirish | Eritish Pechi (`Furnace`) | Qal'a devorlari, minoralar, yuqori chidamlilik |
| **Taxta (Wood Planks)** | 1 dona yog'ochdan 4 dona taxta | Qo'lda / Duradgorlik dastgohi | Uy pollari, eshiklar, mebellar, sandiqlar |
| **Shaxta To'sini (Support Beam)** | 2 Yog'och + 1 Tosh | Duradgorlik dastgohi | 4 blok radiusda g'or o'pirilishining oldini oladi |
| **Yog'och To'siq (Wooden Palisade)**| 4 dona Yog'och | Duradgorlik dastgohi | Qal'a atrofini o'rash uchun o'tkir qoziqli to'siq |
| **Tishli Devor (Stone Battlement)**| 4 dona Tosh G'isht | Duradgorlik dastgohi | Kamonchilar o'q uzishi uchun maxsus mudofaa parapeti |
| **Mustahkam Darvoza (Wooden Gate)**| 4 Yog'och + 2 Temir quyma | Duradgorlik dastgohi | Ochilib-yopiladigan, qamalga chidamli qal'a eshigi |
| **Shisha Blok (Glass)** | Qumni eritish pechida qizdirish | Eritish Pechi | Derazalar, issiqxonalar qurish |

---

## 3. O'SIMLIKLAR, EKINLAR VA MEVALAR

| O'simlik Nomi | Urug'i Qayerdan Olinadi | O'sish Sharoiti | Olinadigan Mahsulot |
| :--- | :--- | :--- | :--- |
| **Bug'doy (Wheat)** | Yovvoyi o'tlarni o'rishdan tushadi | Nam tuproqda (suvdan $\le 4$ blok) | Bug'doy boshoqlari (un, non, pivo) |
| **Karam (Cabbage)** | O'rmon chetidagi yovvoyi butalardan | Nam unumdor tuproq | Karam boshlari (sho'rvalar, tuzlama) |
| **Sabzi (Carrot)** | Qaroqchilar lagerlaridagi omborlardan | Unumdor yumshoq tuproq | To'yimli xom sabzi, qovurmalar uchun |
| **Piyoz (Onion)** | Daryo vodiysidagi yovvoyi o'tlardan | Nam tuproq | Ziravor, dori-darmon, go'shtli ovqatlar |
| **Zig'ir / Tolali O't (Flax)** | Tekislik o'tloqlaridan | O'rtacha nam tuproq | Zig'ir tolasi (Linen ip, kiyim, kamon ipi) |
| **Dorivor Giyohlar (Medicinal Herbs)**| Tog' etaklari va o'rmon soyasidan | Tabiiy o'sadi | Malhamlar, davolovchi damlamalar |

---

## 4. YEGULIKLAR VA PISHIRILGAN TAOMLAR

| Taom Nomi | Kerakli Masalliqlar | Qayerda Pishiriladi | Foydasi va Effektlari |
| :--- | :--- | :--- | :--- |
| **Pishirilgan Non (Bread)** | Bug'doy uni + Suv | O'choq / Nonvoyxona | 30% ochlikni qondiradi, asosiy oziq-ovqat |
| **Pishirilgan Go'sht (Steak)** | Xom go'sht + Olov | Gulxan (`Campfire`) | 45% ochlikni qondiradi, +10 Jon |
| **Tuzlangan Go'sht (Salted Meat)** | Xom go'sht + Tosh tuz | Omborxona | 35% ochlik, 30 kun aynamaydi |
| **Qal'a Sho'rvasi (Hearty Stew)** | Go'sht + Sabzi + Piyoz + Karam | Qozon (`Cooking Pot`) | 100% ochlik, +40 Jon, 1 kun sovuqdan himoya |
| **Sabzavotli Dimlama (Veggie Stew)**| Sabzi + Karam + Kartoshka | Qozon | 70% ochlik, dehqonlarga +20 ma'naviyat |

---

## 5. DUSHMAN VA HAYVONLARDAN TUSHADIGAN DROPLAR (MOB DROPS)

| Dushman / Jonivor | Qayerda Uchraydi | Tushadigan Droplar (Loot) | Ehtimollik |
| :--- | :--- | :--- | :--- |
| **Kiyik / Bo'rsiq (Deer/Game)** | O'rmonlarda | Xom go'sht (1-2), Teri (1-2) | 100% |
| **Qaroqchi Bosqinchi (Bandit Raider)** | Reydlar va lagerlarda | Qon tomchisi (1), Temir parchalari (1), 2-4 Tanga | 100% |
| **Qaroqchi Kamonchi (Bandit Archer)** | Kuzatuv minoralarida | Kamon ipi (1), O'qlar (3-6), Teri qalpoq | 80% |
| **Qaroqchi Boshlig'i (Bandit Warlord)** | Katta reydlar oxirida | Po'lat quyma, **Noyob Sehrli Runa**, 25 Tanga | 100% (Kafolatlangan) |
| **Yovvoyi Bo'ri (Wolf)** | Qorong'i changalzorlarda | Bo'ri tishi (1), Qalin yung (1-2) | 90% |

---

## 6. QUROL, SOVUT VA ASBOBLAR TIZIMI

| Asbob / Qurol | Kerakli Materiallar | Zarba / Himoya | Xususiyati |
| :--- | :--- | :--- | :--- |
| **Temir Qilich** | 3 Temir quyma + 1 Yog'och dasta | 35 Jismoniy Zarar | Tezkor yaqin jang quroli |
| **Yog'ochkesar Boltasi** | 2 Temir quyma + 1 Yog'och dasta | 24 Zarar / O'tin 2x | Daraxtlarni tez chopish va og'ir zarba |
| **Konchi Cho'kichi** | 3 Temir quyma + 1 Yog'och dasta | 16 Zarar / Ruda 2.5x | Tosh va qattiq rudalarni oson qazish |
| **Ov Kamoni (Hunting Bow)** | 3 Qattiq yog'och + 2 Zig'ir ip | 45 Uzoq Masofa Zarari | 36 m/s parabolik o'q uzish |
| **Zirhli Temir Sovut (Chestplate)**| 8 Temir quyma + 2 Teri | +40% Zarar Qaytarish | Jismoniy zarbani sezilarli pasaytiradi |
| **Temir Dubulg'a (Iron Helmet)** | 5 Temir quyma | +15% Bosh Himoyasi | Boshga tushadigan kritik zarbalarni to'sadi |

---

## 7. SEHIRLAR VA RUNALAR TIZIMI

### 7.1. Oddiy Sehirlar (Sehrgar Labaratoriyasida Yasaladi)
*Sehrgar fuqaro ularni mob droplari, qog'oz va o'tlardan tayyorlaydi:*
- **O'tkirlik (Sharpness I-V)**: Qilich zararini har darajada +15% ga oshiradi. (Retsept: Qon tomchisi + Tosh kukun + Pergament).
- **Mustahkamlik (Unbreaking I-III)**: Asbob sinish ehtimolini 50% ga kamaytiradi. (Retsept: Bo'ri tishi + Temir kukun).
- **Himoya (Protection I-IV)**: Sovutning zarar qaytarish foizini oshiradi. (Retsept: Qalin teri + Dorivor giyoh).
- **Kuch (Power I-V)**: Kamon o'qining uchish tezligi va kuchini oshiradi. (Retsept: O'rgimchak ipi + Bo'ri tishi).

### 7.2. Noyob va Qadimiy Sehirlar (Faqat Bosslar va Sandiqlardan Tushadi)
*Bularni tayyorlab bo'lmaydi, faqatgina qaroqchilar boshliqlarini mag'lub etib topish mumkin:*
- 🔥 **Ajdaho Nafasi (`Dragon's Breath`)**: Dushmanga zarba berganda, uni 4 soniya olovda yondiradi.
- ⚡ **Yashin Urishi (`Thunderstrike`)**: Kamon o'qi tushgan yerga yashin chaqirib, atrofdagi barcha dushmanlarga ommaviy zarar yetkazadi.
- 🩸 **Qon So'rgich (`Vampiric Leech`)**: Berilgan har bir zararning 15% miqdorida Hukmdorning jonini to'ldiradi.
- 🌪️ **Shamol Qadami (`Windstrider`)**: Etikka o'rnatilganda, yugurish tezligini +30% ga oshiradi va daryo/suv yuzasida cho'kmasdan yurish imkonini beradi.
- 🛡️ **Qal'a Yuragi (`Fortress Heart`)**: Jon 25% dan pasayganda, 5 soniyaga 90% barcha zararlarni qaytaruvchi sehrli to'siq hosil qiladi.
