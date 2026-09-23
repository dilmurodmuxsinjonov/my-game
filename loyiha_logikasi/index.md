# Loyiha logikasi

Voxel Lord — o'yinchi jismonan ishtirok etadigan feodal koloniya simulyatori. Asosiy sikl: resurs topish → boshpana qurish → oziq-ovqat → fuqarolar mehnati → iqtisodiyot → mudofaa → davlat boshqaruvi.

Unreal Engine dunyoni va boshqaruvni ko'rsatadi; C++ yadro bloklar, inventar va vaqtning yagona holatini saqlaydi. Bitta buyum IDsi barcha retsept, ombor, qazish va save tizimlarida ishlatiladi. Amallar avval tekshiriladi, keyin to'liq qo'llanadi.

Ma'lumot modeli: world(seed, generator_version), chunk(x,y, block_deltas), player(transform, inventory), calendar(minutes), citizen(id, role, job, needs), realm(treasury, laws). Dastlab tashqi ma'lumotlar bazasi kerak emas; mahalliy versiyalangan fayl yetarli. Tafsilotlar: `../implementation_plan.md`.
