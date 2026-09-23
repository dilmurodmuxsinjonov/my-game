# Texnik talablar va yechimlar

- Unreal Engine 5.8 target; aniq patch birinchi muvaffaqiyatli build'da qayd etiladi.
- Windows SDK va Epic moslik jadvalidagi MSVC/Visual Studio; dastlab Windows, keyin Linux.
- UE modullari: Core, CoreUObject, Engine, InputCore, ProceduralMeshComponent; PythonScriptPlugin va EditorScriptingUtilities faqat editor bootstrap uchun.
- Portable C++17 yadro uchun standart kutubxona; tashqi runtime paketi yo'q.
- Python 3 faqat yordamchi hujjat/test vositalari uchun. Blender'da tayyorlangan GLB'lar kelajakdagi art import manbasi; tayyor Unreal asset deb hisoblanmaydi.
- Muhit o'zgaruvchisi `UE_ROOT` engine ildizini ko'rsatadi. Tarmoq porti/API kaliti kerak emas.
- Kelajakdagi ko'p o'yinchili rejim server tasdiqlaydigan amallarga tayanadi; mijoz resurs miqdori va zararni mustaqil belgilamaydi.
- Save fayllari yuklanishdan oldin hajm, versiya, ID va koordinatalar bo'yicha tekshiriladi. Dastlabki prototip save formati production `.vlsa` bilan bir xil deb e'lon qilinmaydi.
- Engine/cache uchun D diskidan foydalanish rejalashtirilgan. O'rnatish, litsenziya qabul qilish va account login holati alohida qayd etiladi.
