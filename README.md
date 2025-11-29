# Django Shablon Loyihasi

![Django](https://img.shields.io/badge/Django-5.2-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.0-cyan)
![License](https://img.shields.io/badge/License-MIT-yellow)

**To'liq funksional, o'zbekcha izohlangan Django loyihasi shabloni**

Bu loyiha Django freymvorki asosida yaratilgan to'liq funksional veb-ilova shablonidir. Barcha asosiy imkoniyatlar tayyor holda va to'liq o'zbek tilida izohlangan.

## 📋 Mundarija

- [Xususiyatlar](#xususiyatlar)
- [Texnologiyalar](#texnologiyalar)
- [O'rnatish](#ornatish)
- [Ishga tushirish](#ishga-tushirish)
- [Loyiha strukturasi](#loyiha-strukturasi)
- [Ma'lumotlar bazasi sozlamalari](#malumotlar-bazasi-sozlamalari)
- [Admin panel](#admin-panel)
- [Foydalanish bo'yicha qo'llanma](#foydalanish-boyicha-qollanma)
- [Hissa qo'shish](#hissa-qoshish)
- [Litsenziya](#litsenziya)

## ✨ Xususiyatlar

### Asosiy funksiyalar

- ✅ **To'liq o'zbekcha izohlar** - Barcha kodlar va dokumentatsiya o'zbek tilida
- ✅ **Zamonaviy dizayn** - Tailwind CSS bilan responsive dizayn
- ✅ **Autentifikatsiya tizimi** - Kirish, ro'yxatdan o'tish, profil boshqaruvi
- ✅ **CRUD operatsiyalari** - To'liq Create, Read, Update, Delete funksiyalari
- ✅ **Django Signals** - Avtomatik ishlov berish uchun signallar tizimi
- ✅ **Admin panel** - To'liq sozlangan va o'zbekcha admin panel
- ✅ **Formalar va validatsiya** - Xavfsiz va validatsiyalangan formalar
- ✅ **Ko'p ma'lumotlar bazasi** - SQLite, PostgreSQL, MySQL uchun tayyor
- ✅ **Media va statik fayllar** - Rasmlar va fayllar boshqaruvi
- ✅ **Qidiruv va filtrlash** - Mahsulotlarni qidirish va filtrlash
- ✅ **Pagination** - Sahifalash tizimi
- ✅ **Sharh tizimi** - Foydalanuvchilar sharh qoldirishi mumkin
- ✅ **Reyting tizimi** - Mahsulotlar uchun reyting

### Modellar

1. **Kategoriya** - Mahsulotlar kategoriyalari
2. **Mahsulot** - Asosiy mahsulot ma'lumotlari
3. **Sharh** - Foydalanuvchilar sharhlari
4. **Profil** - Foydalanuvchi profili (User modeliga qo'shimcha)

## 🛠 Texnologiyalar

- **Backend**: Django 5.2
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Ma'lumotlar bazasi**: SQLite (standart), PostgreSQL, MySQL
- **Python**: 3.11+
- **Icons**: Font Awesome 6.4

## 📦 O'rnatish

### 1. Loyihani klonlash

```bash
git clone https://github.com/sizning-username/django-shablon.git
cd django-shablon
```

### 2. Virtual muhit yaratish

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kerakli paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

Agar `requirements.txt` fayli bo'lmasa, quyidagi paketlarni o'rnating:

```bash
pip install django pillow mysqlclient psycopg2-binary
```

### 4. Ma'lumotlar bazasini sozlash

Standart holatda SQLite ishlatiladi. Boshqa ma'lumotlar bazasini sozlash uchun `config/settings.py` faylini tahrirlang.

### 5. Migratsiyalarni qo'llash

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Superuser yaratish

```bash
python manage.py createsuperuser
```

Foydalanuvchi nomi, email va parolni kiriting.

### 7. Statik fayllarni to'plash (ixtiyoriy)

```bash
python manage.py collectstatic
```

## 🚀 Ishga tushirish

### Development server

```bash
python manage.py runserver
```

Brauzerda ochish: http://localhost:8000

### Admin panelga kirish

http://localhost:8000/admin/

Yaratgan superuser ma'lumotlaringiz bilan kiring.

## 📁 Loyiha strukturasi

```
django_shablon/
├── config/                 # Asosiy loyiha sozlamalari
│   ├── settings.py        # Django sozlamalari (o'zbekcha izohlar bilan)
│   ├── urls.py            # Asosiy URL marshrutlari
│   ├── wsgi.py            # WSGI konfiguratsiyasi
│   └── asgi.py            # ASGI konfiguratsiyasi
├── asosiy_app/            # Asosiy ilova
│   ├── models.py          # Ma'lumotlar bazasi modellari
│   ├── views.py           # View funksiyalari va classlari
│   ├── forms.py           # Django formalar
│   ├── admin.py           # Admin panel sozlamalari
│   ├── signals.py         # Django signallari
│   ├── urls.py            # Ilova URL marshrutlari
│   ├── apps.py            # Ilova konfiguratsiyasi
│   ├── templates/         # HTML shablonlar
│   │   └── asosiy_app/
│   │       ├── bosh_sahifa.html
│   │       ├── mahsulotlar.html
│   │       ├── mahsulot_batafsil.html
│   │       ├── kirish.html
│   │       ├── royxatdan_otish.html
│   │       ├── profil.html
│   │       ├── profil_tahrirlash.html
│   │       ├── haqida.html
│   │       └── aloqa.html
│   └── migrations/        # Ma'lumotlar bazasi migratsiyalari
├── templates/             # Umumiy shablonlar
│   └── base.html         # Asosiy shablon (header, footer)
├── static/               # Statik fayllar (CSS, JS, rasmlar)
├── media/                # Foydalanuvchi yuklagan fayllar
├── manage.py             # Django boshqaruv fayli
├── requirements.txt      # Python paketlar ro'yxati
├── README.md            # Bu fayl
└── db.sqlite3           # SQLite ma'lumotlar bazasi (yaratilgandan keyin)
```

## 🗄 Ma'lumotlar bazasi sozlamalari

### SQLite (standart)

Hech narsa o'zgartirish shart emas. Loyiha avtomatik SQLite ishlatadi.

### PostgreSQL

`config/settings.py` faylida quyidagi qismni izohdan chiqaring:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'loyiha_nomi',
        'USER': 'postgres',
        'PASSWORD': 'parol123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

PostgreSQL o'rnatish:

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

### MySQL

`config/settings.py` faylida quyidagi qismni izohdan chiqaring:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'loyiha_nomi',
        'USER': 'root',
        'PASSWORD': 'parol123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

MySQL o'rnatish:

```bash
# Ubuntu/Debian
sudo apt-get install mysql-server

# macOS
brew install mysql
```

## 👨‍💼 Admin panel

Admin panelda quyidagilarni boshqarish mumkin:

- **Kategoriyalar** - Mahsulot kategoriyalarini qo'shish, tahrirlash, o'chirish
- **Mahsulotlar** - Mahsulotlarni to'liq boshqarish
- **Sharhlar** - Sharhlarni ko'rish, tasdiqlash, o'chirish
- **Profillar** - Foydalanuvchi profillarini boshqarish
- **Foydalanuvchilar** - Django'ning standart foydalanuvchi boshqaruvi

### Admin panel xususiyatlari

- O'zbekcha interfeys
- Qidiruv va filtrlash
- Inline tahrirlash
- Bulk actions (bir nechta obyektga bir vaqtda amal qilish)
- Rasmlarni preview ko'rish
- Custom metodlar va hisob-kitoblar

## 📖 Foydalanish bo'yicha qo'llanma

### Yangi kategoriya qo'shish

1. Admin panelga kiring
2. "Kategoriyalar" bo'limiga o'ting
3. "Kategoriya qo'shish" tugmasini bosing
4. Ma'lumotlarni to'ldiring va saqlang

### Yangi mahsulot qo'shish

1. Admin panelga kiring
2. "Mahsulotlar" bo'limiga o'ting
3. "Mahsulot qo'shish" tugmasini bosing
4. Barcha maydonlarni to'ldiring:
   - Nomi
   - Slug (avtomatik yaratiladi)
   - Kategoriya
   - Tavsif
   - Narx va chegirma narxi
   - Rasm
   - Miqdor va holat
5. Saqlang

### Foydalanuvchi ro'yxatdan o'tish

1. Bosh sahifada "Ro'yxatdan o'tish" tugmasini bosing
2. Formani to'ldiring
3. Avtomatik tizimga kirasiz va profil yaratiladi

### Sharh qoldirish

1. Tizimga kiring
2. Mahsulot sahifasiga o'ting
3. Sharh formasi orqali sharh va baho qoldiring
4. Sharh moderatsiyadan o'tgandan keyin ko'rinadi

## 🔧 Sozlamalar

### DEBUG rejimi

Ishlab chiqish (development) uchun:
```python
DEBUG = True
```

Ishlab chiqarish (production) uchun:
```python
DEBUG = False
ALLOWED_HOSTS = ['example.com', 'www.example.com']
```

### Email sozlamalari

`config/settings.py` faylida email sozlamalarini o'zgartiring:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sizning@email.com'
EMAIL_HOST_PASSWORD = 'sizning_parolingiz'
```

### Til va vaqt zonasi

```python
LANGUAGE_CODE = 'uz'  # O'zbek tili
TIME_ZONE = 'Asia/Tashkent'  # O'zbekiston vaqt zonasi
```

## 📝 Kerakli komandalar

### Migratsiyalar

```bash
# Yangi migratsiya yaratish
python manage.py makemigrations

# Migratsiyalarni qo'llash
python manage.py migrate

# Migratsiyalarni ko'rish
python manage.py showmigrations
```

### Superuser

```bash
# Yangi superuser yaratish
python manage.py createsuperuser

# Parolni o'zgartirish
python manage.py changepassword username
```

### Shell

```bash
# Django shell ochish
python manage.py shell

# IPython shell (agar o'rnatilgan bo'lsa)
python manage.py shell -i ipython
```

### Test

```bash
# Barcha testlarni ishga tushirish
python manage.py test

# Ma'lum bir ilovani test qilish
python manage.py test asosiy_app
```

### Statik fayllar

```bash
# Statik fayllarni to'plash
python manage.py collectstatic

# Statik fayllarni tozalash
python manage.py collectstatic --clear
```

### Ma'lumotlar bazasi

```bash
# Ma'lumotlar bazasini tozalash
python manage.py flush

# Ma'lumotlar bazasini dump qilish
python manage.py dumpdata > backup.json

# Ma'lumotlar bazasini tiklash
python manage.py loaddata backup.json
```

## 🚀 Production uchun tayyorlash

### 1. SECRET_KEY ni o'zgartirish

```python
# config/settings.py
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
```

### 2. DEBUG ni o'chirish

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

### 3. Xavfsizlik sozlamalari

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 4. Statik fayllarni to'plash

```bash
python manage.py collectstatic --noinput
```

### 5. Gunicorn o'rnatish

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 6. Nginx sozlash (ixtiyoriy)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🤝 Hissa qo'shish

Hissa qo'shmoqchimisiz? Ajoyib! Quyidagi qadamlarni bajaring:

1. Loyihani fork qiling
2. Yangi branch yarating (`git checkout -b feature/yangi-xususiyat`)
3. O'zgarishlaringizni commit qiling (`git commit -am 'Yangi xususiyat qo'shildi'`)
4. Branch ga push qiling (`git push origin feature/yangi-xususiyat`)
5. Pull Request yarating

## 📄 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil ma'lumot uchun [LICENSE](LICENSE) faylini ko'ring.

## 📞 Aloqa

Savollar yoki takliflar bo'lsa, iltimos bog'laning:

- Email: info@example.com
- Telegram: @example
- GitHub Issues: [Issues sahifasi](https://github.com/sizning-username/django-shablon/issues)

## 🙏 Minnatdorchilik

- Django jamoasiga ajoyib freymvork uchun
- Tailwind CSS jamoasiga chiroyli CSS freymvorki uchun
- O'zbek dasturchilar hamjamiyatiga qo'llab-quvvatlash uchun

---

**Omad tilaymiz! 🚀**

Agar bu loyiha sizga yoqsa, ⭐ star bering!
