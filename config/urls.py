"""
URL konfiguratsiyasi - Django Shablon Loyihasi

Bu fayl loyihaning barcha URL marshrutlarini belgilaydi.
Har bir URL ma'lum bir view funksiyasiga yoki classiga yo'naltiriladi.

URL marshrutlari:
- Admin panel
- Asosiy app URL lari
- Media va statik fayllar (development rejimida)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ============================================================================
# ASOSIY URL MARSHRUTLARI
# ============================================================================

urlpatterns = [
    # Admin panel URL i
    # Admin panelga kirish: http://localhost:8000/admin/
    path('admin/', admin.site.urls),
    
    # Asosiy app ning barcha URL larini ulash
    # Bu yerda asosiy_app/urls.py faylidagi barcha marshrutlar ulanadi
    # Masalan: http://localhost:8000/, http://localhost:8000/mahsulotlar/ va h.k.
    path('', include('asosiy_app.urls')),
]

# ============================================================================
# MEDIA VA STATIK FAYLLAR UCHUN URL LAR (DEVELOPMENT REJIMI)
# ============================================================================

# Faqat DEBUG=True bo'lganda (development rejimida) ishlaydi
# Ishlab chiqarishda (production) media fayllar web server orqali xizmat qiladi
if settings.DEBUG:
    # Media fayllar uchun URL marshrutlarini qo'shish
    # Foydalanuvchi yuklagan fayllar (rasmlar, hujjatlar va h.k.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Statik fayllar uchun URL marshrutlarini qo'shish
    # CSS, JavaScript, rasmlar va boshqa statik fayllar
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ============================================================================
# ADMIN PANEL SOZLAMALARI
# ============================================================================

# Admin panel sarlavhalarini o'zgartirish
admin.site.site_header = "Django Shablon - Admin Panel"
admin.site.site_title = "Django Shablon"
admin.site.index_title = "Boshqaruv Paneli"
