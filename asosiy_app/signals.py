"""
Signals - Signallar

Bu faylda Django signallari aniqlanadi.
Signallar - ma'lum hodisalar sodir bo'lganda avtomatik ishga tushadigan funksiyalar.

Masalan:
- Foydalanuvchi yaratilganda avtomatik profil yaratish
- Mahsulot saqlanganida reyting hisoblash
- Email yuborish va h.k.
"""

from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profil, Mahsulot, Sharh

# ============================================================================
# PROFIL YARATISH SIGNALI
# ============================================================================

@receiver(post_save, sender=User)
def profil_yaratish(sender, instance, created, **kwargs):
    """
    Yangi foydalanuvchi yaratilganda avtomatik profil yaratish
    
    Bu signal User modeli saqlanganidan keyin (post_save) ishga tushadi.
    Agar yangi foydalanuvchi yaratilgan bo'lsa (created=True),
    unga avtomatik profil yaratiladi.
    
    Args:
        sender: Signal yuboruvchi model (User)
        instance: Yaratilgan yoki yangilangan User obyekti
        created: Yangi obyekt yaratildimi? (True/False)
        **kwargs: Qo'shimcha argumentlar
    """
    if created:
        # Yangi foydalanuvchi uchun profil yaratish
        Profil.objects.create(foydalanuvchi=instance)
        print(f"✓ {instance.username} uchun profil yaratildi")


@receiver(post_save, sender=User)
def profil_saqlash(sender, instance, **kwargs):
    """
    Foydalanuvchi saqlanganida profilni ham saqlash
    
    Bu signal User modeli har safar saqlanganida ishga tushadi
    va unga tegishli profilni ham saqlaydi.
    
    Args:
        sender: Signal yuboruvchi model (User)
        instance: Saqlangan User obyekti
        **kwargs: Qo'shimcha argumentlar
    """
    # Agar profil mavjud bo'lsa, uni saqlash
    if hasattr(instance, 'profil'):
        instance.profil.save()


# ============================================================================
# MAHSULOT REYTING YANGILASH SIGNALI
# ============================================================================

@receiver(post_save, sender=Sharh)
def mahsulot_reyting_yangilash(sender, instance, **kwargs):
    """
    Yangi sharh qo'shilganda mahsulot reytingini avtomatik yangilash
    
    Bu signal Sharh modeli saqlanganidan keyin ishga tushadi
    va tegishli mahsulotning reytingini qayta hisoblaydi.
    
    Args:
        sender: Signal yuboruvchi model (Sharh)
        instance: Saqlangan Sharh obyekti
        **kwargs: Qo'shimcha argumentlar
    """
    # Mahsulotni olish
    mahsulot = instance.mahsulot
    
    # Mahsulotning barcha tasdiqlangan sharhlarini olish
    sharhlar = mahsulot.sharhlar.filter(tasdiqlangan=True)
    
    # Agar sharhlar bo'lsa, o'rtacha reytingni hisoblash
    if sharhlar.exists():
        # Barcha baholarning o'rtacha qiymatini hisoblash
        jami_baho = sum([sharh.baho for sharh in sharhlar])
        sharhlar_soni = sharhlar.count()
        ortacha_reyting = jami_baho / sharhlar_soni
        
        # Mahsulot reytingini yangilash
        mahsulot.reyting = round(ortacha_reyting, 2)
        mahsulot.save()
        
        print(f"✓ {mahsulot.nomi} reytingi yangilandi: {mahsulot.reyting}")


# ============================================================================
# MAHSULOT SLUG YARATISH SIGNALI
# ============================================================================

@receiver(pre_save, sender=Mahsulot)
def mahsulot_slug_yaratish(sender, instance, **kwargs):
    """
    Mahsulot saqlanishidan oldin slug yaratish (agar bo'sh bo'lsa)
    
    Bu signal Mahsulot modeli saqlanishidan oldin (pre_save) ishga tushadi.
    Agar slug maydoni bo'sh bo'lsa, mahsulot nomidan avtomatik slug yaratadi.
    
    Args:
        sender: Signal yuboruvchi model (Mahsulot)
        instance: Saqlanayotgan Mahsulot obyekti
        **kwargs: Qo'shimcha argumentlar
    """
    from django.utils.text import slugify
    import uuid
    
    # Agar slug bo'sh bo'lsa
    if not instance.slug:
        # Mahsulot nomidan slug yaratish
        base_slug = slugify(instance.nomi, allow_unicode=True)
        
        # Agar slug allaqachon mavjud bo'lsa, unga random qo'shimcha qo'shish
        slug = base_slug
        counter = 1
        
        while Mahsulot.objects.filter(slug=slug).exists():
            # Agar bu yangi obyekt emas (tahrirlanyapti) va slug o'zgartirilmagan bo'lsa
            if instance.pk and Mahsulot.objects.filter(pk=instance.pk, slug=slug).exists():
                break
            # Yangi slug yaratish
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        instance.slug = slug
        print(f"✓ Mahsulot uchun slug yaratildi: {slug}")


# ============================================================================
# MAHSULOT HOLAT TEKSHIRISH SIGNALI
# ============================================================================

@receiver(pre_save, sender=Mahsulot)
def mahsulot_holat_tekshirish(sender, instance, **kwargs):
    """
    Mahsulot saqlanishidan oldin holat tekshirish
    
    Bu signal mahsulot miqdorini tekshiradi va agar 0 bo'lsa,
    holatni avtomatik "tugagan" ga o'zgartiradi.
    
    Args:
        sender: Signal yuboruvchi model (Mahsulot)
        instance: Saqlanayotgan Mahsulot obyekti
        **kwargs: Qo'shimcha argumentlar
    """
    # Agar miqdor 0 bo'lsa, holatni "tugagan" ga o'zgartirish
    if instance.miqdor == 0 and instance.holat == 'mavjud':
        instance.holat = 'tugagan'
        print(f"⚠ {instance.nomi} holati 'tugagan' ga o'zgartirildi (miqdor 0)")
    
    # Agar miqdor 0 dan katta bo'lsa va holat "tugagan" bo'lsa, "mavjud" ga o'zgartirish
    elif instance.miqdor > 0 and instance.holat == 'tugagan':
        instance.holat = 'mavjud'
        print(f"✓ {instance.nomi} holati 'mavjud' ga o'zgartirildi (miqdor: {instance.miqdor})")


# ============================================================================
# SHARH O'CHIRILGANDA REYTING YANGILASH
# ============================================================================

from django.db.models.signals import post_delete

@receiver(post_delete, sender=Sharh)
def sharh_ochirilganda_reyting_yangilash(sender, instance, **kwargs):
    """
    Sharh o'chirilganda mahsulot reytingini qayta hisoblash
    
    Args:
        sender: Signal yuboruvchi model (Sharh)
        instance: O'chirilgan Sharh obyekti
        **kwargs: Qo'shimcha argumentlar
    """
    # Mahsulotni olish
    mahsulot = instance.mahsulot
    
    # Mahsulotning qolgan tasdiqlangan sharhlarini olish
    sharhlar = mahsulot.sharhlar.filter(tasdiqlangan=True)
    
    # Agar sharhlar bo'lsa, o'rtacha reytingni hisoblash
    if sharhlar.exists():
        jami_baho = sum([sharh.baho for sharh in sharhlar])
        sharhlar_soni = sharhlar.count()
        ortacha_reyting = jami_baho / sharhlar_soni
        mahsulot.reyting = round(ortacha_reyting, 2)
    else:
        # Agar sharh qolmagan bo'lsa, reytingni 0 ga o'rnatish
        mahsulot.reyting = 0
    
    mahsulot.save()
    print(f"✓ {mahsulot.nomi} reytingi yangilandi (sharh o'chirildi): {mahsulot.reyting}")


# ============================================================================
# SIGNAL SOZLAMALARI
# ============================================================================

"""
Signallarni faollashtirish uchun apps.py faylida quyidagi kodni qo'shish kerak:

class AsosiyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'asosiy_app'
    
    def ready(self):
        import asosiy_app.signals

Bu kod ilovamiz ishga tushganda signallarni avtomatik yuklaydi.
"""
