"""
Django sozlamalari - Django Shablon Loyihasi uchun

Bu fayl Django loyihasining asosiy sozlamalarini o'z ichiga oladi.
Barcha sozlamalar to'liq izohlangan va o'zbek tilida tushuntirilgan.

Ma'lumotlar bazasi sozlamalari:
- SQLite (standart, ishlab chiqish uchun)
- PostgreSQL (ishlab chiqarish uchun tavsiya etiladi)
- MySQL (alternativ variant)

Sozlamalarni o'zgartirish uchun tegishli qismlarni izohdan chiqaring.
"""

from pathlib import Path
import os

# ============================================================================
# ASOSIY YO'LLAR VA KATALOGLAR
# ============================================================================

# Loyihaning asosiy katalogi (BASE_DIR)
# Bu o'zgaruvchi loyihaning ildiz katalogini ko'rsatadi
# Barcha boshqa yo'llar shu katalogga nisbatan hisoblanadi
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================================
# XAVFSIZLIK SOZLAMALARI
# ============================================================================

# MUHIM: Ishlab chiqarishda (production) bu kalitni maxfiy saqlang!
# Bu kalit sessiyalar, cookielar va boshqa xavfsizlik funksiyalari uchun ishlatiladi
# Haqiqiy loyihada bu qiymatni environment variable orqali olish kerak
SECRET_KEY = 'django-insecure-bu-kalitni-ishlab-chiqarishda-almashtiring-123456789'

# DEBUG rejimi - faqat ishlab chiqish (development) uchun True bo'lishi kerak
# Ishlab chiqarishda (production) ALBATTA False qilish kerak!
DEBUG = True

# Ruxsat etilgan hostlar ro'yxati
# Ishlab chiqarishda bu yerga domen nomlarini qo'shing
# Masalan: ['example.com', 'www.example.com']
ALLOWED_HOSTS = ['*']  # Ishlab chiqishda barcha hostlarga ruxsat


# ============================================================================
# O'RNATILGAN ILOVALAR (INSTALLED APPS)
# ============================================================================

INSTALLED_APPS = [
    # Django'ning standart ilovalari
    'django.contrib.admin',        # Admin panel
    'django.contrib.auth',         # Autentifikatsiya tizimi
    'django.contrib.contenttypes', # Kontent turlari freymvorki
    'django.contrib.sessions',     # Sessiyalar boshqaruvi
    'django.contrib.messages',     # Xabarlar freymvorki
    'django.contrib.staticfiles',  # Statik fayllar boshqaruvi
    
    # Bizning yaratgan ilovamiz
    # Bu yerda loyihaning barcha custom ilovalari ro'yxatlanadi
    'asosiy_app',  # Asosiy funksionallik uchun ilovamiz
]


# ============================================================================
# MIDDLEWARE SOZLAMALARI
# ============================================================================

# Middleware - so'rovlar va javoblarni qayta ishlovchi komponentlar
# Ular ketma-ketlikda ishga tushadi (yuqoridan pastga)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',       # Xavfsizlik
    'django.contrib.sessions.middleware.SessionMiddleware', # Sessiyalar
    'django.middleware.common.CommonMiddleware',           # Umumiy funksiyalar
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF himoyasi
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Autentifikatsiya
    'django.contrib.messages.middleware.MessageMiddleware',    # Xabarlar
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Clickjacking himoyasi
]


# ============================================================================
# URL VA SHABLON SOZLAMALARI
# ============================================================================

# Asosiy URL konfiguratsiya fayli
ROOT_URLCONF = 'config.urls'

# Shablon (template) sozlamalari
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Shablonlar qidirilishi kerak bo'lgan kataloglar
        'DIRS': [BASE_DIR / 'templates'],  # Loyiha darajasidagi shablonlar
        'APP_DIRS': True,  # Har bir app ichidagi templates papkasini qidirish
        'OPTIONS': {
            'context_processors': [
                # Context processorlar - barcha shablonlarda mavjud bo'lgan o'zgaruvchilar
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # request obyekti
                'django.contrib.auth.context_processors.auth', # user obyekti
                'django.contrib.messages.context_processors.messages', # xabarlar
            ],
        },
    },
]

# WSGI ilovasi - ishlab chiqarish serverida ishlatiladi
WSGI_APPLICATION = 'config.wsgi.application'


# ============================================================================
# MA'LUMOTLAR BAZASI SOZLAMALARI
# ============================================================================

# VARIANT 1: SQLite (standart, ishlab chiqish uchun)
# SQLite - oddiy, faylga asoslangan ma'lumotlar bazasi
# Kichik va o'rta loyihalar uchun yetarli
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Ma'lumotlar bazasi fayli
    }
}

# VARIANT 2: PostgreSQL (ishlab chiqarish uchun tavsiya etiladi)
# PostgreSQL - kuchli, ishonchli va masshtablanadigan ma'lumotlar bazasi
# Ishlab chiqarishda eng ko'p ishlatiladigan variant
# Foydalanish uchun quyidagi qatorlarni izohdan chiqaring va yuqoridagi SQLite ni izohga oling
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'loyiha_nomi',           # Ma'lumotlar bazasi nomi
        'USER': 'postgres',              # Foydalanuvchi nomi
        'PASSWORD': 'parol123',          # Parol
        'HOST': 'localhost',             # Server manzili
        'PORT': '5432',                  # Port (standart 5432)
    }
}
"""

# VARIANT 3: MySQL/MariaDB (alternativ variant)
# MySQL - keng tarqalgan, tez va oson sozlanadigan ma'lumotlar bazasi
# Foydalanish uchun quyidagi qatorlarni izohdan chiqaring va yuqoridagi SQLite ni izohga oling
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'loyiha_nomi',           # Ma'lumotlar bazasi nomi
        'USER': 'root',                  # Foydalanuvchi nomi
        'PASSWORD': 'parol123',          # Parol
        'HOST': 'localhost',             # Server manzili
        'PORT': '3306',                  # Port (standart 3306)
        'OPTIONS': {
            'charset': 'utf8mb4',        # UTF-8 kodlash (emoji uchun ham)
        },
    }
}
"""


# ============================================================================
# PAROL TEKSHIRISH SOZLAMALARI
# ============================================================================

# Parol validatorlari - foydalanuvchi parollarini tekshirish uchun qoidalar
AUTH_PASSWORD_VALIDATORS = [
    {
        # Parol juda oddiy bo'lmasligi kerak
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Parol kamida 8 ta belgidan iborat bo'lishi kerak
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        # Parol juda keng tarqalgan parollardan bo'lmasligi kerak
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Parol faqat raqamlardan iborat bo'lmasligi kerak
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ============================================================================
# XALQAROLASHTIRISH (INTERNATIONALIZATION)
# ============================================================================

# Til sozlamalari
LANGUAGE_CODE = 'uz'  # O'zbek tili (uz-latn yoki uz ham ishlatish mumkin)

# Vaqt zonasi
TIME_ZONE = 'Asia/Tashkent'  # O'zbekiston vaqt zonasi

# Xalqarolashtirish yoqilganmi
USE_I18N = True  # Tarjimalar uchun

# Vaqt zonalarini ishlatish
USE_TZ = True  # Vaqt zonalarini avtomatik boshqarish


# ============================================================================
# STATIK FAYLLAR (CSS, JavaScript, Rasmlar)
# ============================================================================

# Statik fayllar URL manzili
# Brauzerda statik fayllarga murojaat qilish uchun ishlatiladi
# Masalan: /static/css/style.css
STATIC_URL = '/static/'

# Statik fayllar joylashgan kataloglar
# Bu yerda loyiha darajasidagi statik fayllar saqlanadi
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Asosiy statik fayllar katalogi
]

# Statik fayllar to'planadigan katalog (collectstatic buyrug'i uchun)
# Ishlab chiqarishda barcha statik fayllar shu yerga to'planadi
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ============================================================================
# MEDIA FAYLLAR (Foydalanuvchi yuklagan fayllar)
# ============================================================================

# Media fayllar URL manzili
MEDIA_URL = '/media/'

# Media fayllar saqlanadigan katalog
# Foydalanuvchilar tomonidan yuklangan barcha fayllar shu yerda saqlanadi
MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================================
# DEFAULT PRIMARY KEY SOZLAMASI
# ============================================================================

# Modellar uchun standart primary key turi
# Django 3.2+ versiyalarida tavsiya etiladi
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================================
# AUTENTIFIKATSIYA SOZLAMALARI
# ============================================================================

# Login va logout dan keyin yo'naltiriladigan sahifalar
LOGIN_REDIRECT_URL = 'bosh_sahifa'      # Login dan keyin
LOGOUT_REDIRECT_URL = 'bosh_sahifa'     # Logout dan keyin
LOGIN_URL = 'kirish'                     # Login sahifasi


# ============================================================================
# QOSHIMCHA SOZLAMALAR
# ============================================================================

# Email sozlamalari (ixtiyoriy)
# Email yuborish uchun kerakli sozlamalar
# Ishlab chiqishda konsolga chiqarish uchun:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Ishlab chiqarishda SMTP orqali yuborish uchun:
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sizning@email.com'
EMAIL_HOST_PASSWORD = 'sizning_parolingiz'
"""

# Sessiya sozlamalari
SESSION_COOKIE_AGE = 1209600  # 2 hafta (sekundlarda)
SESSION_SAVE_EVERY_REQUEST = False  # Har bir so'rovda sessiyani saqlash

# CSRF sozlamalari
CSRF_COOKIE_HTTPONLY = False  # JavaScript orqali CSRF tokenga kirish
CSRF_COOKIE_SECURE = False    # Ishlab chiqishda False, production da True

# Xavfsizlik sozlamalari (production uchun)
# Ishlab chiqarishda quyidagi sozlamalarni yoqing:
"""
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
"""
