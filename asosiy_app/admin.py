"""
Admin - Admin panel sozlamalari

Bu faylda modellarni admin panelda qanday ko'rsatish va boshqarish
kerakligi belgilanadi.

Admin panel - Django'ning eng kuchli xususiyatlaridan biri.
U orqali ma'lumotlar bazasini oson boshqarish mumkin.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Kategoriya, Mahsulot, Sharh, Profil

# ============================================================================
# KATEGORIYA ADMIN
# ============================================================================

@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    """
    Kategoriya modelini admin panelda boshqarish
    
    Bu class kategoriyalarni admin panelda qanday ko'rsatish va
    qanday funksiyalar bo'lishi kerakligini belgilaydi.
    """
    
    # Ro'yxatda ko'rsatiladigan ustunlar
    list_display = ['nomi', 'mahsulotlar_soni', 'faol', 'rasm_preview', 'yaratilgan_sana']
    
    # Filtr qilish uchun maydonlar (o'ng tomonda)
    list_filter = ['faol', 'yaratilgan_sana']
    
    # Qidiruv uchun maydonlar
    search_fields = ['nomi', 'tavsif']
    
    # Ro'yxatda tahrirlash mumkin bo'lgan maydonlar
    list_editable = ['faol']
    
    # Har bir sahifada nechta obyekt ko'rsatish
    list_per_page = 20
    
    # Tartiblash
    ordering = ['nomi']
    
    # Avtomatik to'ldiriladigan maydonlar (slug)
    prepopulated_fields = {}
    
    # Sanalar bo'yicha navigatsiya
    date_hierarchy = 'yaratilgan_sana'
    
    # O'qish uchun maydonlar (tahrirlash mumkin emas)
    readonly_fields = ['yaratilgan_sana', 'yangilangan_sana', 'rasm_preview']
    
    # Batafsil ko'rinishda maydonlarni guruhlash
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('nomi', 'tavsif', 'rasm', 'rasm_preview')
        }),
        ('Sozlamalar', {
            'fields': ('faol',)
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('yaratilgan_sana', 'yangilangan_sana'),
            'classes': ('collapse',)  # Yig'ilgan holda ko'rsatish
        }),
    )
    
    def rasm_preview(self, obj):
        """
        Rasmni kichik ko'rinishda ko'rsatish
        """
        if obj.rasm:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.rasm.url)
        return "Rasm yo'q"
    rasm_preview.short_description = 'Rasm'
    
    def mahsulotlar_soni(self, obj):
        """
        Kategoriyaga tegishli mahsulotlar sonini ko'rsatish
        """
        return obj.mahsulotlar_soni()
    mahsulotlar_soni.short_description = 'Mahsulotlar'


# ============================================================================
# MAHSULOT ADMIN
# ============================================================================

@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    """
    Mahsulot modelini admin panelda boshqarish
    """
    
    # Ro'yxatda ko'rsatiladigan ustunlar
    list_display = ['nomi', 'kategoriya', 'joriy_narx_display', 'chegirma_display', 
                    'miqdor', 'holat', 'mashhur', 'yangi', 'reyting', 'rasm_preview']
    
    # Filtr qilish uchun maydonlar
    list_filter = ['kategoriya', 'holat', 'mashhur', 'yangi', 'yaratilgan_sana']
    
    # Qidiruv uchun maydonlar
    search_fields = ['nomi', 'qisqacha_tavsif', 'toliq_tavsif', 'slug']
    
    # Ro'yxatda tahrirlash mumkin bo'lgan maydonlar
    list_editable = ['holat', 'mashhur', 'yangi']
    
    # Har bir sahifada nechta obyekt ko'rsatish
    list_per_page = 25
    
    # Tartiblash
    ordering = ['-yaratilgan_sana']
    
    # Avtomatik to'ldiriladigan maydonlar
    prepopulated_fields = {'slug': ('nomi',)}
    
    # Sanalar bo'yicha navigatsiya
    date_hierarchy = 'yaratilgan_sana'
    
    # O'qish uchun maydonlar
    readonly_fields = ['yaratilgan_sana', 'yangilangan_sana', 'korilganlar_soni', 
                       'rasm_preview', 'chegirma_foizi_display']
    
    # Batafsil ko'rinishda maydonlarni guruhlash
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('nomi', 'slug', 'kategoriya')
        }),
        ('Tavsif', {
            'fields': ('qisqacha_tavsif', 'toliq_tavsif')
        }),
        ('Narx va chegirma', {
            'fields': ('narx', 'chegirma_narxi', 'chegirma_foizi_display')
        }),
        ('Rasm', {
            'fields': ('rasm', 'rasm_preview')
        }),
        ('Ombor va holat', {
            'fields': ('miqdor', 'holat')
        }),
        ('Qo\'shimcha', {
            'fields': ('mashhur', 'yangi', 'reyting', 'korilganlar_soni', 'yaratuvchi')
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('yaratilgan_sana', 'yangilangan_sana'),
            'classes': ('collapse',)
        }),
    )
    
    # Kategoriya bo'yicha filtr
    autocomplete_fields = []
    
    # Tashqi kalitlar uchun
    raw_id_fields = ['yaratuvchi']
    
    def rasm_preview(self, obj):
        """
        Rasmni kichik ko'rinishda ko'rsatish
        """
        if obj.rasm:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.rasm.url)
        return "Rasm yo'q"
    rasm_preview.short_description = 'Rasm'
    
    def joriy_narx_display(self, obj):
        """
        Joriy narxni formatlangan holda ko'rsatish
        """
        narx = obj.joriy_narx()
        return format_html('<strong>{:,.2f} so\'m</strong>', narx)
    joriy_narx_display.short_description = 'Joriy narx'
    
    def chegirma_display(self, obj):
        """
        Chegirma foizini ko'rsatish
        """
        foiz = obj.chegirma_foizi()
        if foiz > 0:
            return format_html('<span style="color: green; font-weight: bold;">-{}%</span>', foiz)
        return '-'
    chegirma_display.short_description = 'Chegirma'
    
    def chegirma_foizi_display(self, obj):
        """
        Chegirma foizini batafsil ko'rsatish
        """
        foiz = obj.chegirma_foizi()
        if foiz > 0:
            return f'{foiz}%'
        return 'Chegirma yo\'q'
    chegirma_foizi_display.short_description = 'Chegirma foizi'
    
    def save_model(self, request, obj, form, change):
        """
        Mahsulotni saqlashda yaratuvchini avtomatik qo'shish
        """
        if not change:  # Yangi obyekt yaratilayotgan bo'lsa
            obj.yaratuvchi = request.user
        super().save_model(request, obj, form, change)


# ============================================================================
# SHARH ADMIN
# ============================================================================

@admin.register(Sharh)
class SharhAdmin(admin.ModelAdmin):
    """
    Sharh modelini admin panelda boshqarish
    """
    
    # Ro'yxatda ko'rsatiladigan ustunlar
    list_display = ['foydalanuvchi', 'mahsulot', 'baho', 'qisqa_matn', 'tasdiqlangan', 'yaratilgan_sana']
    
    # Filtr qilish uchun maydonlar
    list_filter = ['tasdiqlangan', 'baho', 'yaratilgan_sana']
    
    # Qidiruv uchun maydonlar
    search_fields = ['foydalanuvchi__username', 'mahsulot__nomi', 'matn']
    
    # Ro'yxatda tahrirlash mumkin bo'lgan maydonlar
    list_editable = ['tasdiqlangan']
    
    # Har bir sahifada nechta obyekt ko'rsatish
    list_per_page = 30
    
    # Tartiblash
    ordering = ['-yaratilgan_sana']
    
    # Sanalar bo'yicha navigatsiya
    date_hierarchy = 'yaratilgan_sana'
    
    # O'qish uchun maydonlar
    readonly_fields = ['yaratilgan_sana']
    
    # Batafsil ko'rinishda maydonlarni guruhlash
    fieldsets = (
        ('Sharh ma\'lumotlari', {
            'fields': ('foydalanuvchi', 'mahsulot', 'baho', 'matn')
        }),
        ('Moderatsiya', {
            'fields': ('tasdiqlangan',)
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('yaratilgan_sana',),
            'classes': ('collapse',)
        }),
    )
    
    # Tashqi kalitlar uchun
    raw_id_fields = ['foydalanuvchi', 'mahsulot']
    
    def qisqa_matn(self, obj):
        """
        Sharh matnini qisqartirib ko'rsatish
        """
        if len(obj.matn) > 50:
            return obj.matn[:50] + '...'
        return obj.matn
    qisqa_matn.short_description = 'Sharh matni'
    
    # Actions - bir nechta obyektga bir vaqtda amal qilish
    actions = ['tasdiqlash', 'bekor_qilish']
    
    def tasdiqlash(self, request, queryset):
        """
        Tanlangan sharhlarni tasdiqlash
        """
        updated = queryset.update(tasdiqlangan=True)
        self.message_user(request, f'{updated} ta sharh tasdiqlandi.')
    tasdiqlash.short_description = 'Tanlangan sharhlarni tasdiqlash'
    
    def bekor_qilish(self, request, queryset):
        """
        Tanlangan sharhlarni bekor qilish
        """
        updated = queryset.update(tasdiqlangan=False)
        self.message_user(request, f'{updated} ta sharh bekor qilindi.')
    bekor_qilish.short_description = 'Tanlangan sharhlarni bekor qilish'


# ============================================================================
# PROFIL ADMIN
# ============================================================================

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    """
    Profil modelini admin panelda boshqarish
    """
    
    # Ro'yxatda ko'rsatiladigan ustunlar
    list_display = ['foydalanuvchi', 'toliq_ism_display', 'telefon', 'shahar', 
                    'email_xabarnoma', 'rasm_preview']
    
    # Filtr qilish uchun maydonlar
    list_filter = ['jins', 'shahar', 'mamlakat', 'email_xabarnoma']
    
    # Qidiruv uchun maydonlar
    search_fields = ['foydalanuvchi__username', 'foydalanuvchi__first_name', 
                     'foydalanuvchi__last_name', 'telefon', 'shahar']
    
    # Har bir sahifada nechta obyekt ko'rsatish
    list_per_page = 25
    
    # Tartiblash
    ordering = ['foydalanuvchi__username']
    
    # O'qish uchun maydonlar
    readonly_fields = ['yaratilgan_sana', 'yangilangan_sana', 'rasm_preview', 'yosh_display']
    
    # Batafsil ko'rinishda maydonlarni guruhlash
    fieldsets = (
        ('Foydalanuvchi', {
            'fields': ('foydalanuvchi',)
        }),
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('rasm', 'rasm_preview', 'bio', 'tugilgan_sana', 'yosh_display', 'jins')
        }),
        ('Aloqa ma\'lumotlari', {
            'fields': ('telefon', 'manzil', 'shahar', 'mamlakat', 'vebsayt')
        }),
        ('Sozlamalar', {
            'fields': ('email_xabarnoma',)
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('yaratilgan_sana', 'yangilangan_sana'),
            'classes': ('collapse',)
        }),
    )
    
    # Tashqi kalitlar uchun
    raw_id_fields = ['foydalanuvchi']
    
    def rasm_preview(self, obj):
        """
        Profil rasmini kichik ko'rinishda ko'rsatish
        """
        if obj.rasm:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 50%;" />', obj.rasm.url)
        return "Rasm yo'q"
    rasm_preview.short_description = 'Profil rasmi'
    
    def toliq_ism_display(self, obj):
        """
        To'liq ismni ko'rsatish
        """
        return obj.toliq_ism()
    toliq_ism_display.short_description = 'To\'liq ism'
    
    def yosh_display(self, obj):
        """
        Yoshni ko'rsatish
        """
        yosh = obj.yosh()
        if yosh:
            return f'{yosh} yosh'
        return 'Kiritilmagan'
    yosh_display.short_description = 'Yosh'


# ============================================================================
# ADMIN PANEL SOZLAMALARI
# ============================================================================

# Admin panel sarlavhalarini sozlash (config/urls.py da ham sozlangan)
admin.site.site_header = "Django Shablon - Admin Panel"
admin.site.site_title = "Django Shablon"
admin.site.index_title = "Boshqaruv Paneli"
