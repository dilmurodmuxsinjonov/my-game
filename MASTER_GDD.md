# MASTER GAME DESIGN DOCUMENT (GDD)
# "Voxel Lord: Feudal Realm" 👑

> **Hujjat Maqomi:** To'liq Texnik Loyiha (Specification 1.1 — Yangilangan)  
> **Janr:** Birinchi Shaxs / Voxel Sandbox / O'rta Asrlar Koloniya Simulyatori (Colony Sim & Strategy)  
> **Dvigatel:** Godot Engine 4.3+ (Forward+ / GDScript & C#)  
> **Platforma:** PC (Steam / Windows, Linux)  
> **Biznes Model:** Pullik Indie Reliz ($14.99 – $19.99), Early Access  

---

## MUNDARIJA
1. [O'yin Konsepsiyasi va Asosiy Falsafasi](#1-oyin-konsepsiyasi-va-asosiy-falsafasi)
2. [O'yinchi Boshlanishi va O'tmish Arxetiplari (Origins)](#2-oyinchi-boshlanishi-va-otmish-arxetiplari-origins)
3. [Aholining Real Paydo Bo'lishi va Bolalar Ulg'ayishi](#3-aholining-real-paydo-bolishi-va-bolalar-ulgayishi)
4. [Shaxsiy Mehnatdan Avtomatlashuvgacha (Hands-on to Automation)](#4-shaxsiy-mehnatdan-avtomatlashuvgacha-hands-on-to-automation)
5. [Feodal Mansab Zinapoyasi va Qirollikka 3 Xil Yo'l](#5-feodal-mansab-zinapoyasi-va-qirollikka-3-xil-yol)
6. [4 Ta Feodal Rivojlanish Bosqichi (Tech Tree Tiers 1–4)](#6-4-ta-feodal-rivojlanish-bosqichi-tech-tree-tiers-14)
7. [Biomlar Tizimi va Tundra Issiqxonalari](#7-biomlar-tizimi-va-tundra-issiqxonalari)
8. [Yer Chuqurligi Qatlamlari va Shaxta Mexanikasi](#8-yer-chuqurligi-qatlamlari-va-shaxta-mexanikasi)
9. [20+ Geologik Rudalar, Minerallar va Metallurgiya](#9-20-geologik-rudalar-minerallar-va-metallurgiya)
10. [Mahluqlar Tizimi, Oddiy Dushmanlar va 5 Ta Ulug'vor Boss](#10-mahluqlar-tizimi-oddiy-dushmanlar-va-5-ta-ulugvor-boss)
11. [Harbiy Tizim: Askarlarni Saralash, O'qitish va Ta'minot](#11-harbiy-tizim-askarlarni-saralash-oqitish-va-taminot)
12. [Sehr, Alkimyo va Runa Temirchiligi](#12-sehr-alkimyo-va-runa-temirchiligi)
13. [Boshqaruv Daftari (The Royal Ledger) va Zanjirli Iqtisodiyot](#13-boshqaruv-daftari-the-royal-ledger-va-zanjirli-iqtisodiyot)
14. [Qurilish Tizimi, Kattalik Darajalari va Masshtab](#14-qurilish-tizimi-kattalik-darajalari-va-masshtab)
15. [Godot 4 Texnik Arxitekturasi va Dasturiy Modullar](#15-godot-4-texnik-arxitekturasi-va-dasturiy-modullar)

---

## 1. O'YIN KONSEPSIYASI VA ASOSIY FALSAFASI

*Voxel Lord: Feudal Realm* — bu o'yinchini tayyor taxtga o'tqazib qo'ymaydigan, balki uni oddiy sarson qochqindan tortib, butun mintaqa tan oladigan Buyuk Qirol darajasigacha o'z mehnati bilan ko'tarilishga majbur qiluvchi chuqur birinchi shaxs koloniya simulyatoridir.

### 4 Ta Asosiy Ustun:
1. **Hukmdor Nigohi (First-Person Monarch):** O'yinchi osmondan qarab buyruq beruvchi emas, fuqarolari bilan birga yerda yuradi, kerak bo'lsa o'zi bug'doy o'radi, devor tiklaydi va kitob orqali davlatni boshqaradi.
2. **Mantiqiy Aholi va Zanjir (Living Citizens & Logistics):** Aholi havodan tushmaydi. Har bir odam qutqarilgan qochqin yoki yangi tug'ilgan go'dak.
3. **Voxel Erkinligi + Rejalar (Voxel Freedom & Blueprints):** Xohlagancha qo'lda blok qo'yish yoki Blueprint orqali quruvchi fuqarolarga qurdirish.
4. **Feodalizm va Shon-shuhrat (Feudal Ladder & Glory):** Sargardondan Qirolgacha 5 ta unvon va 3 xil toj kiyish yo'li.

---

## 2. O'YINCHI BOSHLANISHI VA O'TMISH ARXETIPLARI (ORIGINS)

| Arxetip | Boshlang'ich Holat | Afzalligi | Kamchiligi |
| :--- | :--- | :--- | :--- |
| **Surgun Ritsar** | Qilich, eski zanjir sovut, qalqon | Dastlabki yirtqich va qaroqchilardan qo'rqmaydi, jangovar mahorati yuqori | Dehqonchilik va qurilishdan bexabar, asboblar yasashni bilmaydi |
| **Xonavayron Savdogar**| 25 ta kumush tanga, bo'sh aravacha, xarita | Sayyor karvonlar bilan savdoda 25% chegirma, resurslarni tez baholaydi | Jang qilishni bilmaydi, joni kam, qurol ko'tara olmaydi |
| **Qochoq Ovchi** | Kamon, 20 ta o'q, bolta, tuzoqlar | O'rmonda omon qolish, ovchilik va o'tin kesishda 2 barobar tez | Hech qanday sarmoyasi yo'q, xalqaro diplomatiyaga qobiliyatsiz |

---

## 3. AHOLINING REAL PAYDO BO'LISHI VA BOLALAR ULG'AYISHI

### 3.1. Aholining 5 Ta Mantiqiy Manbasi
1. **Gulxan Nuri (The Signal Fire):** Tepalikdagi olov tutuniga kelgan och sarsonlar (har 2–3 kunda 1 kishi).
2. **Qafaslardan Qutqaruv (Captive Rescue):** Qaroqchilar lagerlaridagi asir hunarmandlarni ozod qilish.
3. **Qishloq Qo'ng'irog'i (The Village Bell):** Bronza qo'ng'iroq sadosi va shahar boyligi tufayli ko'chib keluvchi oilalar.
4. **Daryo Pristani (River Docks):** Daryo oqimi bo'ylab qayiqlarda keluvchi yollanma hunarmandlar.
5. **Nikoh & Tug'ilish (Generations):** Baxtli fuqarolar oila qurib farzand ko'rishadi.

### 3.2. Bolalar Ulg'ayishi Zanjiri:
* **Chaqaloq (0–3 yosh):** Faqat ona suti, iliq uy va xavfsizlik talab qiladi.
* **Kichik bola (4–10 yosh):** Ko'chada o'ynaydi, yengil yordam beradi (tovuq tuxumini yig'ish, meva terish).
* **Shogird (11–15 yosh):** Usta temirchi, novvoy yoki fermerga shogird tushadi va hunar o'rganadi.
* **Voyaga yetgan fuqaro (16+ yosh):** To'laqonli askar, konchi yoki hunarmandga aylanadi.

---

## 4. SHAXSIY MEHNATDAN AVTOMATLASHUVGACHA (HANDS-ON TO AUTOMATION)

O'yinda shaxsiy mehnat va boshqaruv o'rtasida ajoyib evolyutsiya bor:
* **Dastlab (Odam kam paytda):** O'yinchi shaxsan o'zi:
  * Dalaga ketmon uradi, paqirda suv tashib ekinlarni sug'oradi va o'radi.
  * O'rmondan qo'y, sigir, tovuqlarni olib kelib, yem beradi va juftlashtiradi.
  * O'zi bolta bilan o'tin chopadi, shaxtada tosh qaziydi.
* **Aholi ko'paygach (Feodal Avtomatlashuv):**
  * Vazifalar fuqarolarga topshiriladi: Fermer dalani o'zi sug'oradi, Chorvador podani boqadi, Novvoy non yopadi.
  * Hukmdor faqat strategiya va rivojlanishga e'tibor qaratadi (lekin istalgan vaqtda o'zi ham dalaga chiqishi mumkin!).

---

## 5. FEODAL MANSAB ZINAPOYASI VA QIROLLIKKA 3 XIL YO'L

* **0-daraja: Sargardon (Wanderer)** — 1 kishi. Omon qoluvchi.
* **1-daraja: Oqsoqol (Camp Elder)** — 3–8 kishi. Birinchi qo'nalg'a.
* **2-daraja: Baron (Lord / Baron)** — 10–30 kishi. Birinchi yog'och qal'a va shaxsiy bayroq.
* **3-daraja: Graf / Gersog (Count / Duke)** — 30–80 kishi. Tosh qal'a, armiya va soliqlar.
* **4-daraja: QIROL (Sovereign King)** — 100+ kishi. Butun mintaqa hukmdori.

### Qirollikka 3 Xil Yo'l:
1. **Qilich Yo'li (Fotih / Warlord):** Mintaqadagi barcha qaroqchi qal'alarni qamal qilib yoqib yuborish va kuch bilan toj kiyish.
2. **Oltin Yo'li (Savdo / Merchant King):** Xazinaga 10,000 oltin yig'ish, barcha neytral yerlarni sotib olish.
3. **Xalq Mehri Yo'li (Adolatli Qirol):** Buyuk Sobor qurish, yo'qolgan Ajdodlar Tojini topish va xalq mehrini 95%+ ga yetkazish.

---

## 6. 4 TA FEODAL RIVOJLANISH BOSQICHI (TECH TREE TIERS 1–4)

* **Tier 1: Qochqinlar Qo'nalg'asi (3–8 kishi):** Kulbalar, aravacha, gulxan, oddiy quduq. Dehqon, o'rmonchi, yukchi.
* **Tier 2: Hunarmandlar Qishlog'i (8–25 kishi):** Tegirmon, nonvoyxona, temirchilik, yog'och devor, **Chorva Molxonasi**.
  * *Chorvadorlik:* Qo'y (jun $\to$ issiq kiyim), Sigir (teri $\to$ sovut/sut), Tovuq (patlar $\to$ o'qlar/tuxum), Otlar (chavandozlik).
* **Tier 3: Feodal Qal'asi (25–60 kishi):** Tosh devorlar, qorovul minorasi, kazarma, taverna, kasalxona, bozor. Farmonlar (Edicts).
* **Tier 4: Mustahkam Qirollik (60–150+ kishi):** Qirollik Saroyi, Zarbxona, Balista/Katapulta minoralari, Buyuk Sobor, Ritsarlar.

---

## 7. BIOMLAR TIZIMI VA TUNDRA ISSIQXONALARI

| Biom | Afzalliklari (Pros) | Kamchiliklari (Cons) | Strategik Yechim |
| :--- | :--- | :--- | :--- |
| **Unumdor Tekislik** | Dehqonchilik +50%, daryo suvi, oson qurilish | Tabiiy to'siq yo'q, yog'och va ruda kam | Shahar atrofiga tosh devorlar tortish |
| **Qalin O'rmon** | Cheksiz yog'och, ov hayvonlari, yovvoyi asal | Yer tozalash qiyin, yirtqichlar ko'p | Qishloq chetiga doimiy gulxan va tuzoqlar |
| **Qoyali Tog'lik** | Barcha rudalar xazinasi, yengilmas mudofaa | Ekin o'smaydi (-80%), qulash xavfi, qahraton | Vodiydan oziq-ovqat import qilish, terrasalar |
| **Zax Botqoqlik** | Torf (yoqilg'i), loy, botqoq temiri, dori o'tlar | Kasalliklar ko'p, uylar zaxdan tez chiriydi | Doimiy Tabib saqlash, tosh poydevor qurish |
| **Qorli Tundra** | Go'sht muzlab buzilmaydi, qimmatbaho mo'ynalar | Shafqatsiz sovuq, ochiq havoda dehqonchilik 0% | **Maxsus Isitiladigan Issiqxona qurish!** |
| **Qurg'oqchil Dasht**| Cheksiz yaylovlar, tuz konlari, kvars qumi | Ichimlik suvi taqchilligi, katta daraxtlar yo'q | Chuqur quduqlar va tosh/loy arxitekturasi |

### Tundra Maxsus Isitiladigan Issiqxonasi (Heated Greenhouse)
* Shisha gumbaz (kvars eritish), tosh poydevor, ko'mir pechi va mo'rilar (yoki geotermal qaynoq buloq).
* Qishki ekinlar: Sholg'om, qora javdar, qizilcha va dorivor Muzlik guli.

---

## 8. YER CHUQURLIGI QATLAMLARI VA SHAXTA MEXANIKASI

* **[0m dan -30m gacha] 1-Qatlam (Tuproq va Loy):** Gil, torf, shag'al, quduqlar poydevori.
* **[-30m dan -100m gacha] 2-Qatlam (Toshlar va Bronza):** Ko'mir, mis, qalay, tuz, gematit.
* **[-100m dan -200m gacha] 3-Qatlam (Temir va Zaharli G'orlar):** Magnetit, rux, kumush, oltingugurt, metan gazi. Shamollatgich quvurlari zarur.
* **[-200m dan -350m gacha] 4-Qatlam (Abadiy Zulmat va Javohirlar):** Oltin, platina, olmos, yoqut, zumrad.
* **[-350m va pastda] 5-Qatlam (Magma va Bedrock):** Lava, obsidian, geotermal issiqlik, dunyo tubi.
* **Shaxta Mexanizatsiyasi:** Yog'och tirgaklar (struts), Shaxta Lifti va ruda yuk aravachalari (Minecart Hoist).

---

## 9. 20+ GEOLOGIK RUDALAR, MINERALLAR VA METALLURGIYA

1. **Qurilish:** Ohaktosh (ohak/sement), Loy (pech g'ishtlari), Marmar (saroy ustunlari), Granit/Bazalt (qamalga chidamli tosh).
2. **Yoqilg'i & Kimyo:** Ko'mir, Torf, **Tosh Tuzi** (go'shtni tuzlab saqlash), Oltingugurt, Selitra (porox va olovli o'qlar).
3. **Rangli Metallar:** Mis + Qalay = Bronza; Qo'rg'oshin (og'ir qamal toshlari); Rux (Latun/Brass); Nikel (zanglamas po'lat).
4. **Qora Metallar:** Gematit/Magnetit (Temir); Po'lat (Domna pechi); Damashq Po'lati (afsonaviy ritsar quroli).
5. **Javohirlar:** Kumush, Oltin, Platina, Yoqut, Zumrad, Safir, Olmos.

---

## 10. MAHLUQLAR TIZIMI, ODDIY DUSHMANLAR VA 5 TA ULUG'VOR BOSS

### 10.1. Oddiy Dushmanlar
* **Bo'rilar to'dasi:** Kechalari hujum qiladi, gulxandan qo'rqadi.
* **Qaroqchi o'g'rilar:** Tunda omborni talaydi.
* **G'or kalamushlari (-30m):** Vabo va isitma tarqatadi.
* **Ipak o'rgimchaklari (-100m):** To'r otadi; pishiq kamon iplari beradi.
* **Ko'r maxluqlar (-200m):** Tovushga qarab hujum qiladi.
* **Qonli Oy (Blood Moon):** Har 15–20 kunda uyushgan katta qamal to'lqini.

### 10.2. 5 Ta Ulug'vor Epic Boss:
1. **O'rmon Bossi — «Qonli Tirnoq» (Alpha Bear):** *Mukofot:* Hukmdor Mantiyasi (+20% xalq hurmati).
2. **Qamal Bossi — «Temir Soqol» Valdemar (Warlord):** *Mukofot:* Feodal Gerb Nizomi (Baronlik unvoni) va Damashq qilichi.
3. **G'or Bossi — «Zulmat Onasi» (Broodmother: -150m):** *Mukofot:* Titan Ipak (afsonaviy kamonlar uchun).
4. **Tog' Bossi — Qoya Kolossi (Crag Colossus):** *Mukofot:* «Yer Yuragi» Kristali (avtomatik aravachalar quvvati).
5. **Muzlik Bossi — «Muz Qanoti» (Frost Wyvern):** *Mukofot:* Muz Yadrosi (oziq-ovqatlarni abadiy saqlovchi artefakt).

---

## 11. HARBIY TIZIM: ASKARLARNI SARALASH, O'QITISH VA TA'MINOT

### 11.1. Shaxsiy Fazilatlar (Attributes)
* **Jasorat (Bravery):** Qo'rqoqlik vs Qahramonlik.
* **Kuch (Strength):** Og'ir po'lat sovut va qurollarni ko'tarish qobiliyati.
* **Chaqqonlik & Ko'rish (Vision/Agility):** Kamon va arbalet aniqligi.
* **Intizom (Discipline):** Tungi soqchilik va buyruqlarni bekamu-ko'st bajarish.

### 11.2. O'qitish Zanjiri (Barracks Pipeline)
1. **Chaqiriluvchi (Recruit):** Yog'och qilich bilan somon manekenlarda 3 kunlik mashq.
2. **Ixtisoslashuv:** Kamonchi, Qalqonli nayzachi, Og'ir piyoda.
3. **Ritsarlar Akademiyasi:** Jangovar otlar ustida nayza urishish va saf buzish.
4. **Faxriylik (Veterancy):** Har bir omon qolgan jang tajriba beradi; faxriylar qo'rqmaydi.

### 11.3. Ta'minot va Narx:
* Askar dalada ishlamaydi: kuniga **2 ta to'yimli non + go'sht** va haftalik **kumush tanga maosh** talab qiladi.
* Maosh to'lanmasa ruhiyat tushadi, askar qochib ketishi yoki qo'zg'olon ko'tarishi mumkin.

---

## 12. SEHR, ALKIMYO VA RUNA TEMIRCHILIGI

### 12.1. Alkimyo va Eliksirlar (Qozonxona)
* **Hayot Sharobi (Healing):** Og'ir yarador askarni darhol davolaydi.
* **Tosh Teri (Stoneskin):** 5 daqiqa davomida jismoniy zararni 50% ga kamaytiradi.
* **Hosildorlik Damlamasi (Fertility):** Ekinlarni bir kechada pishiradi.
* **Yunon Olovi (Alchemical Fire):** O'chmas qamal olovi.

### 12.2. Runa Temirchiligi (Enchanting)
* **Olov Runasi:** Dushman sovutini qizdirib o't qo'yadi.
* **Buzilmaslik Runasi:** Asbob va qurollar hech qachon sinmaydi.
* **Shamol Runasi:** Kamon o'qlari 2 barobar uzoqroqqa to'g'ri uchadi.
* **Yengillik Runasi:** Po'lat sovutli ritsarga yengil yugurish imkonini beradi.

### 12.3. Shohona Marosimlar va Munajjim Minorasi
* **Yomg'ir Chaqirish:** Qurg'oqchilikda ekinlarni qutqarish.
* **Quyosh Nuri:** Tundrada qahraton bo'ronni eritish.
* **Nurli Qalqon (Sanctuary Ward):** Qonli Oyda shahar darvozasini 30 daqiqa yopib turuvchi nurli gumbaz.
* **Munajjim Minorasi (Observatory):** Yulduzlarga qarab dushman hujumini 3–5 kun oldin xabar beradi.

---

## 13. BOSHQARUV DAFTARI (THE ROYAL LEDGER) VA ZANJIRLI IQTISODIYOT

* **Daftar Menyusi (`Tab` tugmasi):** Fuqarolar ro'yxati, ombor balansi, soliq siyosati va farmonlar.
* **Zanjirli Ishlab Chiqarish:**
  $$\text{Bug'doy} \to \text{Tegirmon (Un)} \to \text{Pech (Non)} \to \text{Aholi to'qligi}$$
  $$\text{Ruda} + \text{Ko'mir} \to \text{Temir quyma} \to \text{Asboblar (Ish unumi +50\%) & Qurollar}$$
* **Farovonlik Formulasi:**
  $$\text{Morale} = \frac{\text{Oziq-ovqat xilma-xilligi} + \text{Uylar sifati} + \text{Xavfsizlik}}{3} - \text{Soliq}$$

---

## 14. QURILISH TIZIMI, KATTALIK DARAJALARI VA MASSHTAB

### 14.1. Ikki Xil Qurilish Rejimi
* **Erkin Voxel Rejimi:** Qo'lda blok qo'yish (kichik tuzatishlar, interyer).
* **Blueprint Rejimi (`B` tugmasi):** Shaffof gologramma bloklar bilan reja chizish. Quruvchi fuqarolar ombordan g'isht tashib binoni tiklaydi.
* **Struktura Chidamliligi (Gravity):** Keng tosh shiftlar ostiga yog'och yoki tosh to'sinlar qo'yilishi shart.

### 14.2. Binolar Kattalik Darajalari:
* **Kichik (3x3 dan 5x5 gacha):** Chayla, quduq, soqchi budkasi.
* **O'rtacha (7x7 dan 10x10 gacha):** Novvoyxona, tegirmon, temirchilik, 2 qavatli oilaviy uy, taverna.
* **Katta (15x15 dan 20x20 gacha):** Kazarma, markaziy ombor, chorva molxonasi.
* **Monumental (30x30 dan 60x60+ gacha):** Qirollik Saroyi, Buyuk Sobor, Qal'a Keep.

### 14.3. Hudud va Shahar Masshtablari:
1. **Qo'nalg'a (Homestead):** 50x50 blok (1–5 kishi).
2. **Qishloqcha (Hamlet):** 100x100 blok (6–15 kishi).
3. **Katta Qishloq (Village):** 200x200 blok (16–35 kishi).
4. **Feodal Shaharcha (Town):** 400x400 blok (35–80 kishi).
5. **Qirollik Poytaxti (Metropolis):** 800x800 – 1000x1000 blok (80–200+ kishi).
* *Chegarani Kengaytirish:* Qorovul minorasi qurilib, askar tayinlangach, atrofidagi 50–70 blok yer rasman davlatga qo'shiladi.

---

## 15. GODOT 4 TEXNIK ARXITEKTURASI VA DASTURIY MODULLAR

* **Face Culling & Greedy Meshing:** `scripts/core/voxel_chunk.gd` — ko'rinmaydigan blok yuzalarini birlashtirib 120+ FPS ta'minlash.
* **Aholi FSM & Yo'l topish:** `scripts/entities/citizen.gd` — NavigationAgent3D yordamida dinamik yo'l topish.
* **Iqtisodiyot va Ta'minot:** `scripts/economy/supply_chain.gd` — resurslar sarfi va kundalik hisob-kitob.
* **Boshqaruv UI:** `scripts/ui/royal_ledger.gd` — Hukmdor daftari interfeysi.
* **Simulyator:** `prototype_sim.py` — 30 kunlik avtomatlashtirilgan iqtisodiy sinov vositasi.
