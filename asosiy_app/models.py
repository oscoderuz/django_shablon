"""
Models - Ma'lumotlar bazasi modellari

Bu faylda ma'lumotlar bazasi jadvallari (models) aniqlanadi.
Har bir model ma'lumotlar bazasida alohida jadval yaratadi.

Model - bu ma'lumotlarning strukturasini belgilovchi Python classi.
Django ORM (Object-Relational Mapping) orqali SQL yozmasdan
ma'lumotlar bazasi bilan ishlash mumkin.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# ============================================================================
# KATEGORIYA MODELI
# ============================================================================

class Kategoriya(models.Model):
    """
    Kategoriya modeli - mahsulotlar yoki maqolalar uchun kategoriyalar
    
    Bu model mahsulotlarni yoki maqolalarni guruhlash uchun ishlatiladi.
    Masalan: Elektronika, Kiyim, Oziq-ovqat va h.k.
    """
    
    # Kategoriya nomi - maksimal 100 ta belgi
    # unique=True - har bir kategoriya nomi yagona bo'lishi kerak
    nomi = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Kategoriya nomi",
        help_text="Kategoriyaning nomi (masalan: Elektronika)"
    )
    
    # Kategoriya tavsifi - ixtiyoriy maydon
    # blank=True - admin panelda bo'sh qoldirish mumkin
    # null=True - ma'lumotlar bazasida NULL qiymat saqlash mumkin
    tavsif = models.TextField(
        blank=True,
        null=True,
        verbose_name="Tavsif",
        help_text="Kategoriya haqida qisqacha ma'lumot"
    )
    
    # Kategoriya rasmi - ixtiyoriy
    # upload_to - fayllar qayerga yuklanishi kerakligini belgilaydi
    rasm = models.ImageField(
        upload_to='kategoriyalar/',
        blank=True,
        null=True,
        verbose_name="Rasm",
        help_text="Kategoriya uchun rasm yuklang"
    )
    
    # Faolmi - kategoriya ko'rinishini boshqarish uchun
    # default=True - standart qiymat True (faol)
    faol = models.BooleanField(
        default=True,
        verbose_name="Faol",
        help_text="Kategoriya faolmi?"
    )
    
    # Yaratilgan sana - avtomatik qo'shiladi
    # auto_now_add=True - obyekt yaratilganda avtomatik joriy vaqt qo'yiladi
    yaratilgan_sana = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    
    # Yangilangan sana - har safar o'zgartirilganda yangilanadi
    # auto_now=True - obyekt har safar saqlanganida avtomatik yangilanadi
    yangilangan_sana = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )
    
    class Meta:
        """
        Meta class - modelning qo'shimcha sozlamalari
        """
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['nomi']  # Kategoriyalarni nom bo'yicha tartiblash
        
    def __str__(self):
        """
        Obyektning string ko'rinishi
        Admin panelda va boshqa joylarda ko'rsatiladi
        """
        return self.nomi
    
    def mahsulotlar_soni(self):
        """
        Bu kategoriyaga tegishli mahsulotlar sonini qaytaradi
        Custom method - admin panelda ko'rsatish mumkin
        """
        return self.mahsulotlar.count()
    mahsulotlar_soni.short_description = "Mahsulotlar soni"


# ============================================================================
# MAHSULOT MODELI
# ============================================================================

class Mahsulot(models.Model):
    """
    Mahsulot modeli - asosiy mahsulot ma'lumotlari
    
    Bu model mahsulot haqidagi barcha ma'lumotlarni saqlaydi:
    nomi, narxi, tavsifi, rasmi va h.k.
    """
    
    # STATUS tanlovlari - mahsulot holati uchun
    # Tuple formatida: (ma'lumotlar bazasida saqlanadigan qiymat, Ko'rsatiladigan nom)
    STATUS_TANLOVI = [
        ('mavjud', 'Mavjud'),
        ('tugagan', 'Tugagan'),
        ('buyurtma', 'Buyurtma asosida'),
    ]
    
    # Mahsulot nomi
    nomi = models.CharField(
        max_length=200,
        verbose_name="Mahsulot nomi",
        help_text="Mahsulotning to'liq nomi"
    )
    
    # Mahsulot slug - URL uchun ishlatiladi
    # slug - URL da foydalanish uchun maxsus format (masalan: yangi-mahsulot)
    # unique=True - har bir slug yagona bo'lishi kerak
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug",
        help_text="URL uchun (masalan: yangi-mahsulot)"
    )
    
    # Kategoriya bilan bog'lanish - ForeignKey (Ko'pga-birlik aloqasi)
    # on_delete=models.CASCADE - kategoriya o'chirilsa, unga tegishli mahsulotlar ham o'chiriladi
    # related_name - teskari bog'lanish nomi (kategoriya.mahsulotlar)
    kategoriya = models.ForeignKey(
        Kategoriya,
        on_delete=models.CASCADE,
        related_name='mahsulotlar',
        verbose_name="Kategoriya",
        help_text="Mahsulot qaysi kategoriyaga tegishli"
    )
    
    # Qisqacha tavsif
    qisqacha_tavsif = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Qisqacha tavsif",
        help_text="Mahsulot haqida qisqacha ma'lumot"
    )
    
    # To'liq tavsif
    toliq_tavsif = models.TextField(
        verbose_name="To'liq tavsif",
        help_text="Mahsulot haqida batafsil ma'lumot"
    )
    
    # Narx - DecimalField (aniq raqamlar uchun)
    # max_digits=10 - maksimal 10 ta raqam
    # decimal_places=2 - verguldan keyin 2 ta raqam (masalan: 99999999.99)
    narx = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],  # Narx 0 dan kichik bo'lmasligi kerak
        verbose_name="Narx",
        help_text="Mahsulot narxi (so'mda)"
    )
    
    # Chegirma narxi - ixtiyoriy
    chegirma_narxi = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name="Chegirma narxi",
        help_text="Chegirma qo'llanilgan narx"
    )
    
    # Mahsulot rasmi
    rasm = models.ImageField(
        upload_to='mahsulotlar/%Y/%m/%d/',  # Yil/Oy/Kun bo'yicha papkalarga saqlash
        verbose_name="Rasm",
        help_text="Mahsulot rasmi"
    )
    
    # Qo'shimcha rasmlar uchun alohida model yaratish mumkin (MahsulotRasm)
    
    # Mahsulot miqdori - omborda qancha bor
    miqdor = models.PositiveIntegerField(
        default=0,
        verbose_name="Miqdor",
        help_text="Omborda mavjud miqdor"
    )
    
    # Mahsulot holati
    holat = models.CharField(
        max_length=20,
        choices=STATUS_TANLOVI,
        default='mavjud',
        verbose_name="Holat",
        help_text="Mahsulot holati"
    )
    
    # Mashhurmi - asosiy sahifada ko'rsatish uchun
    mashhur = models.BooleanField(
        default=False,
        verbose_name="Mashhur",
        help_text="Asosiy sahifada ko'rsatilsinmi?"
    )
    
    # Yangilikmi
    yangi = models.BooleanField(
        default=True,
        verbose_name="Yangi",
        help_text="Yangi mahsulotmi?"
    )
    
    # Ko'rilganlar soni - statistika uchun
    korilganlar_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Ko'rilganlar soni",
        help_text="Mahsulot necha marta ko'rilgan"
    )
    
    # Reyting - 1 dan 5 gacha
    reyting = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Reyting",
        help_text="Mahsulot reytingi (0-5)"
    )
    
    # Yaratuvchi - kim qo'shgan
    # on_delete=models.SET_NULL - foydalanuvchi o'chirilsa, NULL qo'yiladi
    yaratuvchi = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='yaratgan_mahsulotlar',
        verbose_name="Yaratuvchi",
        help_text="Mahsulotni kim qo'shgan"
    )
    
    # Yaratilgan va yangilangan sanalar
    yaratilgan_sana = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    
    yangilangan_sana = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )
    
    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-yaratilgan_sana']  # Yangi mahsulotlar birinchi
        indexes = [
            models.Index(fields=['slug']),  # Slug bo'yicha tezkor qidiruv uchun
            models.Index(fields=['-yaratilgan_sana']),  # Sana bo'yicha
        ]
    
    def __str__(self):
        return self.nomi
    
    def chegirma_foizi(self):
        """
        Chegirma foizini hisoblash
        """
        if self.chegirma_narxi and self.narx > 0:
            foiz = ((self.narx - self.chegirma_narxi) / self.narx) * 100
            return round(foiz, 2)
        return 0
    
    def joriy_narx(self):
        """
        Joriy narxni qaytarish (chegirma bor bo'lsa, chegirma narxini)
        """
        return self.chegirma_narxi if self.chegirma_narxi else self.narx
    
    def mavjudmi(self):
        """
        Mahsulot mavjudligini tekshirish
        """
        return self.miqdor > 0 and self.holat == 'mavjud'


# ============================================================================
# SHARH MODELI
# ============================================================================

class Sharh(models.Model):
    """
    Sharh modeli - foydalanuvchilar mahsulotlarga sharh qoldirishi uchun
    """
    
    # Mahsulot bilan bog'lanish
    mahsulot = models.ForeignKey(
        Mahsulot,
        on_delete=models.CASCADE,
        related_name='sharhlar',
        verbose_name="Mahsulot"
    )
    
    # Foydalanuvchi
    foydalanuvchi = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sharhlar',
        verbose_name="Foydalanuvchi"
    )
    
    # Sharh matni
    matn = models.TextField(
        verbose_name="Sharh",
        help_text="Mahsulot haqida fikringiz"
    )
    
    # Baho - 1 dan 5 gacha
    baho = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Baho",
        help_text="1 dan 5 gacha baho bering"
    )
    
    # Tasdiqlanganmi - moderatsiya uchun
    tasdiqlangan = models.BooleanField(
        default=False,
        verbose_name="Tasdiqlanganmi",
        help_text="Sharh tasdiqlanganmi?"
    )
    
    # Yaratilgan sana
    yaratilgan_sana = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    
    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ['-yaratilgan_sana']
        # Bir foydalanuvchi bir mahsulotga faqat bir marta sharh yozishi mumkin
        unique_together = ['mahsulot', 'foydalanuvchi']
    
    def __str__(self):
        return f"{self.foydalanuvchi.username} - {self.mahsulot.nomi}"


# ============================================================================
# PROFIL MODELI
# ============================================================================

class Profil(models.Model):
    """
    Foydalanuvchi profili - User modeliga qo'shimcha ma'lumotlar
    
    Django'ning standart User modeli cheklangan ma'lumotlarga ega.
    Bu model orqali qo'shimcha ma'lumotlar qo'shish mumkin.
    """
    
    JINS_TANLOVI = [
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol'),
    ]
    
    # User bilan birga-birlik aloqasi (OneToOneField)
    # Har bir User uchun faqat bitta Profil bo'ladi
    foydalanuvchi = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil',
        verbose_name="Foydalanuvchi"
    )
    
    # Profil rasmi
    rasm = models.ImageField(
        upload_to='profillar/',
        blank=True,
        null=True,
        verbose_name="Profil rasmi"
    )
    
    # Bio - o'zi haqida
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Bio",
        help_text="O'zingiz haqingizda qisqacha"
    )
    
    # Tug'ilgan sana
    tugilgan_sana = models.DateField(
        blank=True,
        null=True,
        verbose_name="Tug'ilgan sana"
    )
    
    # Jins
    jins = models.CharField(
        max_length=10,
        choices=JINS_TANLOVI,
        blank=True,
        verbose_name="Jins"
    )
    
    # Telefon raqami
    telefon = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefon raqami",
        help_text="+998 90 123 45 67"
    )
    
    # Manzil
    manzil = models.TextField(
        blank=True,
        verbose_name="Manzil"
    )
    
    # Shahar
    shahar = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Shahar"
    )
    
    # Mamlakat
    mamlakat = models.CharField(
        max_length=100,
        default="O'zbekiston",
        verbose_name="Mamlakat"
    )
    
    # Veb-sayt
    vebsayt = models.URLField(
        blank=True,
        verbose_name="Veb-sayt",
        help_text="https://example.com"
    )
    
    # Email xabarnomalarini qabul qilish
    email_xabarnoma = models.BooleanField(
        default=True,
        verbose_name="Email xabarnomalar",
        help_text="Email orqali xabarnomalar olishni xohlaysizmi?"
    )
    
    # Yaratilgan va yangilangan sanalar
    yaratilgan_sana = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    
    yangilangan_sana = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"
    
    def __str__(self):
        return f"{self.foydalanuvchi.username} profili"
    
    def toliq_ism(self):
        """
        Foydalanuvchining to'liq ismini qaytarish
        """
        if self.foydalanuvchi.first_name and self.foydalanuvchi.last_name:
            return f"{self.foydalanuvchi.first_name} {self.foydalanuvchi.last_name}"
        return self.foydalanuvchi.username
    
    def yosh(self):
        """
        Foydalanuvchi yoshini hisoblash
        """
        if self.tugilgan_sana:
            bugun = timezone.now().date()
            yosh = bugun.year - self.tugilgan_sana.year
            # Tug'ilgan kun o'tmagan bo'lsa, 1 yil ayirish
            if bugun.month < self.tugilgan_sana.month or \
               (bugun.month == self.tugilgan_sana.month and bugun.day < self.tugilgan_sana.day):
                yosh -= 1
            return yosh
        return None
