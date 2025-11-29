"""
Views - Ko'rinishlar (View funksiyalari va classlari)

Bu faylda URL ga kelgan so'rovlarni qayta ishlovchi funksiyalar va classlar aniqlanadi.
View - foydalanuvchi so'rovini qabul qilib, javob qaytaradi (HTML sahifa, JSON, redirect va h.k.)

Django Views:
- Function-based views (FBV) - oddiy funksiyalar
- Class-based views (CBV) - classlar (ListView, DetailView va h.k.)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Mahsulot, Kategoriya, Sharh, Profil
from .forms import (RoyxatdanOtishForm, KirishForm, ProfilTahrirlashForm, 
                    FoydalanuvchiTahrirlashForm, MahsulotForm, SharhForm, QidiruvForm)

# ============================================================================
# ASOSIY SAHIFA
# ============================================================================

def bosh_sahifa(request):
    """
    Asosiy sahifa view
    
    Bu funksiya asosiy sahifani ko'rsatadi.
    Mashhur mahsulotlar, yangi mahsulotlar va kategoriyalarni ko'rsatadi.
    
    Args:
        request: HTTP so'rov obyekti
        
    Returns:
        HttpResponse: Render qilingan HTML sahifa
    """
    # Mashhur mahsulotlarni olish (birinchi 8 ta)
    mashhur_mahsulotlar = Mahsulot.objects.filter(mashhur=True, holat='mavjud')[:8]
    
    # Yangi mahsulotlarni olish (birinchi 8 ta)
    yangi_mahsulotlar = Mahsulot.objects.filter(yangi=True, holat='mavjud').order_by('-yaratilgan_sana')[:8]
    
    # Barcha faol kategoriyalarni olish
    kategoriyalar = Kategoriya.objects.filter(faol=True)
    
    # Context - shablonga uzatiladigan ma'lumotlar
    context = {
        'mashhur_mahsulotlar': mashhur_mahsulotlar,
        'yangi_mahsulotlar': yangi_mahsulotlar,
        'kategoriyalar': kategoriyalar,
    }
    
    return render(request, 'asosiy_app/bosh_sahifa.html', context)


# ============================================================================
# MAHSULOTLAR RO'YXATI
# ============================================================================

class MahsulotlarListView(ListView):
    """
    Mahsulotlar ro'yxati view (Class-based view)
    
    ListView - Django'ning standart view classi
    Ro'yxatni ko'rsatish uchun ishlatiladi
    """
    model = Mahsulot
    template_name = 'asosiy_app/mahsulotlar.html'
    context_object_name = 'mahsulotlar'
    paginate_by = 12  # Har bir sahifada 12 ta mahsulot
    
    def get_queryset(self):
        """
        Mahsulotlar ro'yxatini olish va filtrlash
        
        Returns:
            QuerySet: Filtrlangan mahsulotlar ro'yxati
        """
        queryset = Mahsulot.objects.filter(holat='mavjud')
        
        # Qidiruv
        qidiruv = self.request.GET.get('qidiruv', '')
        if qidiruv:
            queryset = queryset.filter(
                Q(nomi__icontains=qidiruv) | 
                Q(qisqacha_tavsif__icontains=qidiruv) |
                Q(toliq_tavsif__icontains=qidiruv)
            )
        
        # Kategoriya bo'yicha filtrlash
        kategoriya_id = self.request.GET.get('kategoriya', '')
        if kategoriya_id:
            queryset = queryset.filter(kategoriya_id=kategoriya_id)
        
        # Narx oralig'i bo'yicha filtrlash
        min_narx = self.request.GET.get('min_narx', '')
        max_narx = self.request.GET.get('max_narx', '')
        
        if min_narx:
            queryset = queryset.filter(narx__gte=min_narx)
        if max_narx:
            queryset = queryset.filter(narx__lte=max_narx)
        
        # Tartiblash
        tartiblash = self.request.GET.get('tartiblash', '-yaratilgan_sana')
        if tartiblash:
            queryset = queryset.order_by(tartiblash)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Qo'shimcha context ma'lumotlarini qo'shish
        """
        context = super().get_context_data(**kwargs)
        context['kategoriyalar'] = Kategoriya.objects.filter(faol=True)
        context['qidiruv_form'] = QidiruvForm(self.request.GET)
        return context


# ============================================================================
# MAHSULOT BATAFSIL
# ============================================================================

class MahsulotDetailView(DetailView):
    """
    Mahsulot batafsil view
    
    DetailView - bitta obyektni batafsil ko'rsatish uchun
    """
    model = Mahsulot
    template_name = 'asosiy_app/mahsulot_batafsil.html'
    context_object_name = 'mahsulot'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_object(self, queryset=None):
        """
        Mahsulotni olish va ko'rilganlar sonini oshirish
        """
        obj = super().get_object(queryset)
        # Ko'rilganlar sonini oshirish
        obj.korilganlar_soni += 1
        obj.save(update_fields=['korilganlar_soni'])
        return obj
    
    def get_context_data(self, **kwargs):
        """
        Qo'shimcha context ma'lumotlarini qo'shish
        """
        context = super().get_context_data(**kwargs)
        
        # Mahsulotga tegishli tasdiqlangan sharhlarni olish
        context['sharhlar'] = self.object.sharhlar.filter(tasdiqlangan=True).order_by('-yaratilgan_sana')
        
        # Sharh formasi
        context['sharh_form'] = SharhForm()
        
        # O'xshash mahsulotlar (bir xil kategoriyadan)
        context['oxshash_mahsulotlar'] = Mahsulot.objects.filter(
            kategoriya=self.object.kategoriya,
            holat='mavjud'
        ).exclude(id=self.object.id)[:4]
        
        return context


# ============================================================================
# SHARH QO'SHISH
# ============================================================================

@login_required
def sharh_qoshish(request, mahsulot_slug):
    """
    Mahsulotga sharh qo'shish
    
    Args:
        request: HTTP so'rov obyekti
        mahsulot_slug: Mahsulot slug
        
    Returns:
        HttpResponse: Redirect yoki JSON javob
    """
    mahsulot = get_object_or_404(Mahsulot, slug=mahsulot_slug)
    
    if request.method == 'POST':
        form = SharhForm(request.POST)
        if form.is_valid():
            # Formani saqlash, lekin hali ma'lumotlar bazasiga yozmaslik
            sharh = form.save(commit=False)
            sharh.mahsulot = mahsulot
            sharh.foydalanuvchi = request.user
            
            # Foydalanuvchi avval sharh yozganmi tekshirish
            if Sharh.objects.filter(mahsulot=mahsulot, foydalanuvchi=request.user).exists():
                messages.error(request, 'Siz bu mahsulotga allaqachon sharh yozgansiz.')
            else:
                sharh.save()
                messages.success(request, 'Sharhingiz muvaffaqiyatli qo\'shildi! Moderatsiyadan o\'tgandan keyin ko\'rsatiladi.')
            
            return redirect('mahsulot_batafsil', slug=mahsulot_slug)
    
    return redirect('mahsulot_batafsil', slug=mahsulot_slug)


# ============================================================================
# RO'YXATDAN O'TISH
# ============================================================================

def royxatdan_otish(request):
    """
    Foydalanuvchi ro'yxatdan o'tish view
    
    Args:
        request: HTTP so'rov obyekti
        
    Returns:
        HttpResponse: Render qilingan sahifa yoki redirect
    """
    # Agar foydalanuvchi allaqachon tizimga kirgan bo'lsa
    if request.user.is_authenticated:
        return redirect('bosh_sahifa')
    
    if request.method == 'POST':
        form = RoyxatdanOtishForm(request.POST)
        if form.is_valid():
            # Foydalanuvchini yaratish
            user = form.save()
            # Avtomatik tizimga kirish
            login(request, user)
            messages.success(request, f'Xush kelibsiz, {user.username}! Ro\'yxatdan o\'tish muvaffaqiyatli yakunlandi.')
            return redirect('bosh_sahifa')
    else:
        form = RoyxatdanOtishForm()
    
    return render(request, 'asosiy_app/royxatdan_otish.html', {'form': form})


# ============================================================================
# TIZIMGA KIRISH
# ============================================================================

def kirish(request):
    """
    Foydalanuvchi tizimga kirish view
    
    Args:
        request: HTTP so'rov obyekti
        
    Returns:
        HttpResponse: Render qilingan sahifa yoki redirect
    """
    # Agar foydalanuvchi allaqachon tizimga kirgan bo'lsa
    if request.user.is_authenticated:
        return redirect('bosh_sahifa')
    
    if request.method == 'POST':
        form = KirishForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Xush kelibsiz, {username}!')
                # Agar next parametri bo'lsa, u yerga yo'naltirish
                next_url = request.GET.get('next', 'bosh_sahifa')
                return redirect(next_url)
    else:
        form = KirishForm()
    
    return render(request, 'asosiy_app/kirish.html', {'form': form})


# ============================================================================
# TIZIMDAN CHIQISH
# ============================================================================

@login_required
def chiqish(request):
    """
    Foydalanuvchi tizimdan chiqish view
    
    Args:
        request: HTTP so'rov obyekti
        
    Returns:
        HttpResponse: Redirect
    """
    logout(request)
    messages.info(request, 'Tizimdan muvaffaqiyatli chiqdingiz.')
    return redirect('bosh_sahifa')


# ============================================================================
# PROFIL
# ============================================================================

@login_required
def profil(request):
    """
    Foydalanuvchi profili view
    
    Args:
        request: HTTP so'rov obyekti
        
    Returns:
        HttpResponse: Render qilingan sahifa
    """
    # Foydalanuvchi profilini olish
    profil = request.user.profil
    
    # Foydalanuvchining sharhlarini olish
    sharhlar = request.user.sharhlar.all().order_by('-yaratilgan_sana')
    
    context = {
        'profil': profil,
        'sharhlar': sharhlar,
    }
    
    return render(request, 'asosiy_app/profil.html', context)


# ============================================================================
# PROFIL TAHRIRLASH
# ============================================================================

@login_required
def profil_tahrirlash(request):
    """
    Foydalanuvchi profilini tahrirlash view
    
    Args:
        request: HTTP so'rov obyekti
        
    Returns:
        HttpResponse: Render qilingan sahifa yoki redirect
    """
    profil = request.user.profil
    
    if request.method == 'POST':
        user_form = FoydalanuvchiTahrirlashForm(request.POST, instance=request.user)
        profil_form = ProfilTahrirlashForm(request.POST, request.FILES, instance=profil)
        
        if user_form.is_valid() and profil_form.is_valid():
            user_form.save()
            profil_form.save()
            messages.success(request, 'Profilingiz muvaffaqiyatli yangilandi!')
            return redirect('profil')
    else:
        user_form = FoydalanuvchiTahrirlashForm(instance=request.user)
        profil_form = ProfilTahrirlashForm(instance=profil)
    
    context = {
        'user_form': user_form,
        'profil_form': profil_form,
    }
    
    return render(request, 'asosiy_app/profil_tahrirlash.html', context)


# ============================================================================
# KATEGORIYA BO'YICHA MAHSULOTLAR
# ============================================================================

def kategoriya_mahsulotlar(request, kategoriya_id):
    """
    Ma'lum kategoriyaga tegishli mahsulotlarni ko'rsatish
    
    Args:
        request: HTTP so'rov obyekti
        kategoriya_id: Kategoriya ID
        
    Returns:
        HttpResponse: Render qilingan sahifa
    """
    kategoriya = get_object_or_404(Kategoriya, id=kategoriya_id, faol=True)
    mahsulotlar = Mahsulot.objects.filter(kategoriya=kategoriya, holat='mavjud')
    
    # Pagination
    paginator = Paginator(mahsulotlar, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'kategoriya': kategoriya,
        'mahsulotlar': page_obj,
    }
    
    return render(request, 'asosiy_app/kategoriya_mahsulotlar.html', context)


# ============================================================================
# QIDIRUV
# ============================================================================

def qidiruv(request):
    """
    Mahsulotlarni qidirish view
    
    Args:
        request: HTTP so'rov obyekti
        
    Returns:
        HttpResponse: Render qilingan sahifa
    """
    form = QidiruvForm(request.GET)
    mahsulotlar = Mahsulot.objects.filter(holat='mavjud')
    
    if form.is_valid():
        # Qidiruv
        qidiruv_text = form.cleaned_data.get('qidiruv')
        if qidiruv_text:
            mahsulotlar = mahsulotlar.filter(
                Q(nomi__icontains=qidiruv_text) | 
                Q(qisqacha_tavsif__icontains=qidiruv_text) |
                Q(toliq_tavsif__icontains=qidiruv_text)
            )
        
        # Kategoriya
        kategoriya = form.cleaned_data.get('kategoriya')
        if kategoriya:
            mahsulotlar = mahsulotlar.filter(kategoriya=kategoriya)
        
        # Narx oralig'i
        min_narx = form.cleaned_data.get('min_narx')
        max_narx = form.cleaned_data.get('max_narx')
        
        if min_narx:
            mahsulotlar = mahsulotlar.filter(narx__gte=min_narx)
        if max_narx:
            mahsulotlar = mahsulotlar.filter(narx__lte=max_narx)
        
        # Tartiblash
        tartiblash = form.cleaned_data.get('tartiblash')
        if tartiblash:
            mahsulotlar = mahsulotlar.order_by(tartiblash)
    
    # Pagination
    paginator = Paginator(mahsulotlar, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'mahsulotlar': page_obj,
        'natijalar_soni': mahsulotlar.count(),
    }
    
    return render(request, 'asosiy_app/qidiruv.html', context)


# ============================================================================
# HAQIDA
# ============================================================================

def haqida(request):
    """
    Loyiha haqida sahifa
    
    Args:
        request: HTTP so'rov obyekti
        
    Returns:
        HttpResponse: Render qilingan sahifa
    """
    return render(request, 'asosiy_app/haqida.html')


# ============================================================================
# ALOQA
# ============================================================================

def aloqa(request):
    """
    Aloqa sahifasi
    
    Args:
        request: HTTP so'rov obyekti
        
    Returns:
        HttpResponse: Render qilingan sahifa
    """
    if request.method == 'POST':
        # Bu yerda aloqa formasi ishlov beriladigan bo'lishi mumkin
        messages.success(request, 'Xabaringiz yuborildi! Tez orada siz bilan bog\'lanamiz.')
        return redirect('aloqa')
    
    return render(request, 'asosiy_app/aloqa.html')
