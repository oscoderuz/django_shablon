"""
Apps - Ilova konfiguratsiyasi

Bu faylda ilovaning asosiy sozlamalari va konfiguratsiyasi aniqlanadi.
"""

from django.apps import AppConfig


class AsosiyAppConfig(AppConfig):
    """
    Asosiy ilova konfiguratsiyasi
    
    Bu class ilovaning asosiy sozlamalarini o'z ichiga oladi.
    """
    
    # Primary key turi - avtomatik ID maydonlari uchun
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Ilova nomi - INSTALLED_APPS da ishlatiladi
    name = 'asosiy_app'
    
    # Ilova uchun o'qiladigan nom (admin panelda ko'rsatiladi)
    verbose_name = 'Asosiy Ilova'
    
    def ready(self):
        """
        Ilova tayyor bo'lganda ishga tushadigan metod
        
        Bu metod ilova to'liq yuklangandan keyin bir marta ishga tushadi.
        Signallarni yuklash uchun ishlatiladi.
        """
        # Signallarni import qilish - bu signallarni faollashtiradi
        import asosiy_app.signals
        
        print("✓ Asosiy ilova signallari yuklandi")
