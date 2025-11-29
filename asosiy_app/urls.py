"""
URLs - URL marshrutlari

Bu faylda asosiy_app ilovasining barcha URL marshrutlari aniqlanadi.
Har bir URL ma'lum bir view ga yo'naltiriladi.
"""

from django.urls import path
from . import views

# ============================================================================
# URL MARSHRUTLARI
# ============================================================================

urlpatterns = [
    # Asosiy sahifa
    # URL: /
    path('', views.bosh_sahifa, name='bosh_sahifa'),
    
    # Mahsulotlar ro'yxati
    # URL: /mahsulotlar/
    path('mahsulotlar/', views.MahsulotlarListView.as_view(), name='mahsulotlar'),
    
    # Mahsulot batafsil
    # URL: /mahsulot/<slug>/
    # Masalan: /mahsulot/yangi-telefon/
    path('mahsulot/<slug:slug>/', views.MahsulotDetailView.as_view(), name='mahsulot_batafsil'),
    
    # Sharh qo'shish
    # URL: /mahsulot/<slug>/sharh-qoshish/
    path('mahsulot/<slug:mahsulot_slug>/sharh-qoshish/', views.sharh_qoshish, name='sharh_qoshish'),
    
    # Kategoriya bo'yicha mahsulotlar
    # URL: /kategoriya/<id>/
    # Masalan: /kategoriya/1/
    path('kategoriya/<int:kategoriya_id>/', views.kategoriya_mahsulotlar, name='kategoriya_mahsulotlar'),
    
    # Qidiruv
    # URL: /qidiruv/
    path('qidiruv/', views.qidiruv, name='qidiruv'),
    
    # Autentifikatsiya
    # Ro'yxatdan o'tish
    # URL: /royxatdan-otish/
    path('royxatdan-otish/', views.royxatdan_otish, name='royxatdan_otish'),
    
    # Tizimga kirish
    # URL: /kirish/
    path('kirish/', views.kirish, name='kirish'),
    
    # Tizimdan chiqish
    # URL: /chiqish/
    path('chiqish/', views.chiqish, name='chiqish'),
    
    # Profil
    # URL: /profil/
    path('profil/', views.profil, name='profil'),
    
    # Profil tahrirlash
    # URL: /profil/tahrirlash/
    path('profil/tahrirlash/', views.profil_tahrirlash, name='profil_tahrirlash'),
    
    # Haqida
    # URL: /haqida/
    path('haqida/', views.haqida, name='haqida'),
    
    # Aloqa
    # URL: /aloqa/
    path('aloqa/', views.aloqa, name='aloqa'),
]

"""
URL NOMENKLATURASI:

1. URL nomlarida faqat kichik harflar ishlatiladi
2. So'zlar tire (-) bilan ajratiladi
3. O'zbek tilida yoziladi
4. name parametri Python o'zgaruvchi nomlariga mos keladi (snake_case)

Masalan:
- URL: /royxatdan-otish/
- name: royxatdan_otish

Bu standartlarga rioya qilish kodni o'qishni va boshqarishni osonlashtiradi.
"""
