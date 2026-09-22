# Voxel Lord: Feudal Realm 👑

> **Steam uchun mo'ljallangan birinchi shaxs / Voxel Sandbox / Feodal Koloniya Simulyatori.**

---

## 🌟 O'yin Haqida
*Voxel Lord: Feudal Realm* — o'yinchiga o'z feodal davlatini blokma-blok qurish, fuqarolarga kasblar tayinlash, ishlab chiqarish zanjirlarini yo'lga qo'yish va shohlikni qaroqchilar hujumidan himoya qilish imkonini beruvchi mustaqil kompyuter o'yini.

---

## ⚙️ Asosiy Tizimlar va Arxitektura

1. **Voxel Engine (`scripts/core/voxel_chunk.gd`):**
   * 16x32x16 blok o'lchamli optimallashtirilgan chunklar.
   * **Face Culling** algoritmi: ko'rinmaydigan ichki blok yuzalari hisoblanmaydi, yuqori FPS ta'minlanadi.

2. **Aholi va AI (`scripts/entities/citizen.gd`):**
   * Fuqarolar uchun chekli avtomat (Finite State Machine).
   * Kasblar: Fermer, Novvoy, O'rmonchi, Konchi, Temirchi, Qorovul.
   * Ehtiyojlar: Oziq-ovqat, uyqu, ish, xavfsizlik.

3. **Ta'minot Zanjiri (`scripts/economy/supply_chain.gd`):**
   * Xom-ashyodan tayyor mahsulotgacha bo'lgan to'liq zanjir (Bug'doy $\to$ Tegirmon/Non $\to$ Fuqarolar iste'moli).
   * Asboblar eskirishi va davlat farovonlik ko'rsatkichi.

4. **Qirollik Daftari (`scripts/ui/royal_ledger.gd`):**
   * Hukmdorning asosiy boshqaruv interfeysi (`Tab` tugmasi).
   * Rollarni taqsimlash, kunlik balans va soliq siyosati.

---

## 🚀 Prototipni Sinash (Tezkor Start)

O'yinning iqtisodiy va logistika matematikasini tekshirish uchun tayyor terminal simulyatori:

```bash
cd C:\Users\dilmu\.gemini\antigravity\scratch\voxel-lord
python prototype_sim.py
```

Ushbu simulyator har kuni aholi nima yeyotgani, qancha mahsulot ishlab chiqarayotgani va qachon muhojirlar ko'chib kelishini real vaqtda hisoblab beradi.

---

## 🛠️ Godot 4 bilan ochish
1. [Godot Engine 4.3+](https://godotengine.org) ni yuklab oling.
2. `Import` tugmasini bosib, ushbu papkadagi `project.godot` faylini tanlang.
