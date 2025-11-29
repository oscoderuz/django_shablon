# Django Shablon - To'liq Qo'llanma

Bu qo'llanma Django Shablon loyihasi bilan ishlash bo'yicha batafsil ko'rsatmalar beradi.

## Mundarija

1. [Loyiha haqida](#loyiha-haqida)
2. [O'rnatish va sozlash](#ornatish-va-sozlash)
3. [Loyiha strukturasi](#loyiha-strukturasi)
4. [Models (Modellar)](#models-modellar)
5. [Views (Ko'rinishlar)](#views-korinishlar)
6. [Forms (Formalar)](#forms-formalar)
7. [Templates (Shablonlar)](#templates-shablonlar)
8. [Signals (Signallar)](#signals-signallar)
9. [Admin panel](#admin-panel)
10. [URL marshrutlari](#url-marshrutlari)
11. [Statik va media fayllar](#statik-va-media-fayllar)
12. [Ma'lumotlar bazasi](#malumotlar-bazasi)
13. [Autentifikatsiya](#autentifikatsiya)
14. [Kengaytirish](#kengaytirish)

---

## Loyiha haqida

Django Shablon - bu to'liq funksional Django loyihasi shabloni bo'lib, quyidagi xususiyatlarga ega:

- ✅ To'liq o'zbekcha izohlar
- ✅ Tailwind CSS bilan zamonaviy dizayn
- ✅ Barcha asosiy Django imkoniyatlari
- ✅ Tayyor autentifikatsiya tizimi
- ✅ Admin panel sozlamalari
- ✅ Signals tizimi
- ✅ Ko'p ma'lumotlar bazasiga moslik

---

## O'rnatish va sozlash

### 1. Talablar

- Python 3.11 yoki yuqori
- pip (Python paket menejeri)
- Virtual environment (tavsiya etiladi)

### 2. Loyihani yuklab olish

```bash
# Git orqali
git clone https://github.com/sizning-username/django-shablon.git
cd django-shablon

# Yoki ZIP faylni yuklab olib, ochish
```

### 3. Virtual muhit yaratish

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 5. Ma'lumotlar bazasini sozlash

Standart holatda SQLite ishlatiladi. Boshqa ma'lumotlar bazasi uchun `config/settings.py` faylini tahrirlang.

### 6. Migratsiyalarni qo'llash

```bash
python manage.py migrate
```

### 7. Superuser yaratish

```bash
python manage.py createsuperuser
```

### 8. Serverni ishga tushirish

```bash
python manage.py runserver
```

Brauzerda ochish: http://localhost:8000

---

## Loyiha strukturasi

```
django_shablon/
├── config/                 # Asosiy sozlamalar
│   ├── settings.py        # Django sozlamalari
│   ├── urls.py            # Asosiy URL lar
│   ├── wsgi.py            # WSGI konfiguratsiyasi
│   └── asgi.py            # ASGI konfiguratsiyasi
├── asosiy_app/            # Asosiy ilova
│   ├── models.py          # Ma'lumotlar bazasi modellari
│   ├── views.py           # View funksiyalari
│   ├── forms.py           # Django formalar
│   ├── admin.py           # Admin panel
│   ├── signals.py         # Signallar
│   ├── urls.py            # URL marshrutlari
│   └── templates/         # HTML shablonlar
├── templates/             # Umumiy shablonlar
├── static/               # Statik fayllar
├── media/                # Yuklangan fayllar
└── manage.py             # Django boshqaruv fayli
```

---

## Models (Modellar)

### Kategoriya modeli

```python
class Kategoriya(models.Model):
    nomi = models.CharField(max_length=100, unique=True)
    tavsif = models.TextField(blank=True, null=True)
    rasm = models.ImageField(upload_to='kategoriyalar/', blank=True)
    faol = models.BooleanField(default=True)
    yaratilgan_sana = models.DateTimeField(auto_now_add=True)
```

**Ishlatish:**

```python
# Yangi kategoriya yaratish
kategoriya = Kategoriya.objects.create(
    nomi="Elektronika",
    tavsif="Elektronika mahsulotlari",
    faol=True
)

# Kategoriyani olish
kategoriya = Kategoriya.objects.get(id=1)

# Barcha kategoriyalarni olish
kategoriyalar = Kategoriya.objects.all()

# Faol kategoriyalarni olish
faol_kategoriyalar = Kategoriya.objects.filter(faol=True)
```

### Mahsulot modeli

```python
class Mahsulot(models.Model):
    nomi = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE)
    narx = models.DecimalField(max_digits=10, decimal_places=2)
    chegirma_narxi = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rasm = models.ImageField(upload_to='mahsulotlar/%Y/%m/%d/')
    # ... va boshqa maydonlar
```

**Ishlatish:**

```python
# Yangi mahsulot yaratish
mahsulot = Mahsulot.objects.create(
    nomi="iPhone 15",
    slug="iphone-15",
    kategoriya=kategoriya,
    narx=15000000,
    chegirma_narxi=14000000,
    toliq_tavsif="Yangi iPhone 15",
    miqdor=10,
    holat='mavjud'
)

# Mahsulotni slug bo'yicha olish
mahsulot = Mahsulot.objects.get(slug='iphone-15')

# Kategoriya bo'yicha mahsulotlarni olish
mahsulotlar = Mahsulot.objects.filter(kategoriya=kategoriya)

# Mavjud mahsulotlarni olish
mavjud_mahsulotlar = Mahsulot.objects.filter(holat='mavjud')

# Qidirish
mahsulotlar = Mahsulot.objects.filter(nomi__icontains='iPhone')
```

### Sharh modeli

```python
class Sharh(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)
    matn = models.TextField()
    baho = models.PositiveSmallIntegerField()
    tasdiqlangan = models.BooleanField(default=False)
```

**Ishlatish:**

```python
# Sharh qo'shish
sharh = Sharh.objects.create(
    mahsulot=mahsulot,
    foydalanuvchi=request.user,
    matn="Ajoyib mahsulot!",
    baho=5,
    tasdiqlangan=False
)

# Mahsulotning sharhlarini olish
sharhlar = mahsulot.sharhlar.filter(tasdiqlangan=True)

# O'rtacha reytingni hisoblash
from django.db.models import Avg
ortacha = mahsulot.sharhlar.aggregate(Avg('baho'))
```

---

## Views (Ko'rinishlar)

### Function-based views (FBV)

```python
def bosh_sahifa(request):
    """Asosiy sahifa"""
    mashhur_mahsulotlar = Mahsulot.objects.filter(mashhur=True)[:8]
    yangi_mahsulotlar = Mahsulot.objects.filter(yangi=True)[:8]
    
    context = {
        'mashhur_mahsulotlar': mashhur_mahsulotlar,
        'yangi_mahsulotlar': yangi_mahsulotlar,
    }
    
    return render(request, 'asosiy_app/bosh_sahifa.html', context)
```

### Class-based views (CBV)

```python
class MahsulotlarListView(ListView):
    """Mahsulotlar ro'yxati"""
    model = Mahsulot
    template_name = 'asosiy_app/mahsulotlar.html'
    context_object_name = 'mahsulotlar'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Mahsulot.objects.filter(holat='mavjud')
        # Qidiruv va filtrlash
        return queryset
```

### Login required decorator

```python
from django.contrib.auth.decorators import login_required

@login_required
def profil(request):
    """Foydalanuvchi profili"""
    profil = request.user.profil
    return render(request, 'asosiy_app/profil.html', {'profil': profil})
```

---

## Forms (Formalar)

### ModelForm

```python
class MahsulotForm(forms.ModelForm):
    """Mahsulot formasi"""
    
    class Meta:
        model = Mahsulot
        fields = ['nomi', 'slug', 'kategoriya', 'narx', ...]
        widgets = {
            'nomi': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Mahsulot nomi'
            }),
            # ... boshqa maydonlar
        }
    
    def clean_chegirma_narxi(self):
        """Chegirma narxi validatsiyasi"""
        narx = self.cleaned_data.get('narx')
        chegirma_narxi = self.cleaned_data.get('chegirma_narxi')
        
        if chegirma_narxi and chegirma_narxi >= narx:
            raise forms.ValidationError('Chegirma narxi asosiy narxdan kichik bo\'lishi kerak.')
        
        return chegirma_narxi
```

### Formadan foydalanish

```python
def mahsulot_qoshish(request):
    if request.method == 'POST':
        form = MahsulotForm(request.POST, request.FILES)
        if form.is_valid():
            mahsulot = form.save(commit=False)
            mahsulot.yaratuvchi = request.user
            mahsulot.save()
            messages.success(request, 'Mahsulot qo\'shildi!')
            return redirect('mahsulotlar')
    else:
        form = MahsulotForm()
    
    return render(request, 'asosiy_app/mahsulot_qoshish.html', {'form': form})
```

---

## Templates (Shablonlar)

### Base template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Django Shablon{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <!-- Header -->
    <header>...</header>
    
    <!-- Messages -->
    {% if messages %}
        {% for message in messages %}
        <div class="alert">{{ message }}</div>
        {% endfor %}
    {% endif %}
    
    <!-- Main content -->
    <main>
        {% block content %}
        {% endblock %}
    </main>
    
    <!-- Footer -->
    <footer>...</footer>
</body>
</html>
```

### Child template

```html
<!-- asosiy_app/templates/asosiy_app/mahsulotlar.html -->
{% extends 'base.html' %}

{% block title %}Mahsulotlar - Django Shablon{% endblock %}

{% block content %}
<div class="container">
    <h1>Mahsulotlar</h1>
    
    {% for mahsulot in mahsulotlar %}
    <div class="card">
        <h3>{{ mahsulot.nomi }}</h3>
        <p>{{ mahsulot.narx }} so'm</p>
    </div>
    {% empty %}
    <p>Mahsulotlar topilmadi</p>
    {% endfor %}
</div>
{% endblock %}
```

---

## Signals (Signallar)

### Profil yaratish signali

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def profil_yaratish(sender, instance, created, **kwargs):
    """Yangi foydalanuvchi uchun profil yaratish"""
    if created:
        Profil.objects.create(foydalanuvchi=instance)
```

### Reyting yangilash signali

```python
@receiver(post_save, sender=Sharh)
def mahsulot_reyting_yangilash(sender, instance, **kwargs):
    """Sharh qo'shilganda reytingni yangilash"""
    mahsulot = instance.mahsulot
    sharhlar = mahsulot.sharhlar.filter(tasdiqlangan=True)
    
    if sharhlar.exists():
        ortacha = sum([s.baho for s in sharhlar]) / sharhlar.count()
        mahsulot.reyting = round(ortacha, 2)
        mahsulot.save()
```

---

## Admin panel

### Oddiy admin

```python
from django.contrib import admin
from .models import Kategoriya

admin.site.register(Kategoriya)
```

### Kengaytirilgan admin

```python
@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'kategoriya', 'narx', 'holat', 'rasm_preview']
    list_filter = ['kategoriya', 'holat', 'yaratilgan_sana']
    search_fields = ['nomi', 'tavsif']
    list_editable = ['holat']
    prepopulated_fields = {'slug': ('nomi',)}
    
    def rasm_preview(self, obj):
        if obj.rasm:
            return format_html('<img src="{}" width="50" />', obj.rasm.url)
        return "Rasm yo'q"
```

---

## URL marshrutlari

### Asosiy URLs

```python
# config/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('asosiy_app.urls')),
]
```

### Ilova URLs

```python
# asosiy_app/urls.py
urlpatterns = [
    path('', views.bosh_sahifa, name='bosh_sahifa'),
    path('mahsulotlar/', views.MahsulotlarListView.as_view(), name='mahsulotlar'),
    path('mahsulot/<slug:slug>/', views.MahsulotDetailView.as_view(), name='mahsulot_batafsil'),
    path('kirish/', views.kirish, name='kirish'),
    path('chiqish/', views.chiqish, name='chiqish'),
]
```

---

## Statik va media fayllar

### Sozlamalar

```python
# config/settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Templateda ishlatish

```html
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{{ mahsulot.rasm.url }}" alt="{{ mahsulot.nomi }}">
```

---

## Ma'lumotlar bazasi

### SQLite (standart)

Hech narsa o'zgartirish shart emas.

### PostgreSQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'loyiha_nomi',
        'USER': 'postgres',
        'PASSWORD': 'parol',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### MySQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'loyiha_nomi',
        'USER': 'root',
        'PASSWORD': 'parol',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

---

## Autentifikatsiya

### Ro'yxatdan o'tish

```python
def royxatdan_otish(request):
    if request.method == 'POST':
        form = RoyxatdanOtishForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('bosh_sahifa')
    else:
        form = RoyxatdanOtishForm()
    return render(request, 'asosiy_app/royxatdan_otish.html', {'form': form})
```

### Kirish

```python
def kirish(request):
    if request.method == 'POST':
        form = KirishForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('bosh_sahifa')
    else:
        form = KirishForm()
    return render(request, 'asosiy_app/kirish.html', {'form': form})
```

---

## Kengaytirish

### Yangi model qo'shish

1. `models.py` da yangi model yarating
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `admin.py` da ro'yxatdan o'tkazing

### Yangi sahifa qo'shish

1. `views.py` da view yarating
2. `urls.py` da URL qo'shing
3. `templates/` da HTML shablon yarating

### Yangi forma qo'shish

1. `forms.py` da forma yarating
2. View da formani ishlatish
3. Templateda formani ko'rsatish

---

## Xulosa

Bu qo'llanma Django Shablon loyihasi bilan ishlash bo'yicha asosiy ma'lumotlarni beradi. Batafsil ma'lumot uchun:

- Django rasmiy dokumentatsiyasi: https://docs.djangoproject.com/
- Tailwind CSS: https://tailwindcss.com/docs
- Python dokumentatsiyasi: https://docs.python.org/

**Omad tilaymiz!** 🚀
