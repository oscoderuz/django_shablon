"""
Forms - Formalar

Bu faylda HTML formalar uchun Django form classlari aniqlanadi.
Formalar foydalanuvchidan ma'lumot olish va validatsiya qilish uchun ishlatiladi.

Django Forms:
- Ma'lumotlarni validatsiya qiladi
- HTML formalarni avtomatik yaratadi
- XSS va CSRF hujumlaridan himoya qiladi
- Xatolarni avtomatik boshqaradi
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Mahsulot, Kategoriya, Sharh, Profil

# ============================================================================
# RO'YXATDAN O'TISH FORMASI
# ============================================================================

class RoyxatdanOtishForm(UserCreationForm):
    """
    Foydalanuvchi ro'yxatdan o'tish formasi
    
    UserCreationForm - Django'ning standart ro'yxatdan o'tish formasi
    Biz uni kengaytirib, qo'shimcha maydonlar qo'shamiz
    """
    
    # Email maydoni - majburiy
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Email manzilingiz'
        }),
        label='Email'
    )
    
    # Ism - ixtiyoriy
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Ismingiz'
        }),
        label='Ism'
    )
    
    # Familiya - ixtiyoriy
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Familiyangiz'
        }),
        label='Familiya'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        """
        Formani sozlash - barcha maydonlarga Tailwind CSS classlari qo'shish
        """
        super().__init__(*args, **kwargs)
        
        # Username maydonini sozlash
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Foydalanuvchi nomi'
        })
        self.fields['username'].label = 'Foydalanuvchi nomi'
        self.fields['username'].help_text = 'Faqat harflar, raqamlar va @/./+/-/_ belgilari'
        
        # Parol maydonlarini sozlash
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Parol'
        })
        self.fields['password1'].label = 'Parol'
        self.fields['password1'].help_text = 'Kamida 8 ta belgi, faqat raqamlardan iborat bo\'lmasligi kerak'
        
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Parolni tasdiqlang'
        })
        self.fields['password2'].label = 'Parolni tasdiqlang'
        self.fields['password2'].help_text = 'Tasdiqlash uchun bir xil parolni kiriting'
    
    def clean_email(self):
        """
        Email validatsiyasi - email noyob bo'lishi kerak
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email manzil allaqachon ro\'yxatdan o\'tgan.')
        return email
    
    def save(self, commit=True):
        """
        Foydalanuvchini saqlash
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


# ============================================================================
# KIRISH FORMASI
# ============================================================================

class KirishForm(AuthenticationForm):
    """
    Foydalanuvchi tizimga kirish formasi
    
    AuthenticationForm - Django'ning standart kirish formasi
    """
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Foydalanuvchi nomi'
        }),
        label='Foydalanuvchi nomi'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Parol'
        }),
        label='Parol'
    )


# ============================================================================
# PROFIL TAHRIRLASH FORMASI
# ============================================================================

class ProfilTahrirlashForm(forms.ModelForm):
    """
    Foydalanuvchi profilini tahrirlash formasi
    """
    
    class Meta:
        model = Profil
        fields = ['rasm', 'bio', 'tugilgan_sana', 'jins', 'telefon', 'manzil', 'shahar', 'mamlakat', 'vebsayt', 'email_xabarnoma']
        widgets = {
            'rasm': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'O\'zingiz haqingizda qisqacha yozing...'
            }),
            'tugilgan_sana': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date'
            }),
            'jins': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'telefon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '+998 90 123 45 67'
            }),
            'manzil': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'To\'liq manzilingiz'
            }),
            'shahar': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Toshkent'
            }),
            'mamlakat': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'O\'zbekiston'
            }),
            'vebsayt': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'https://example.com'
            }),
            'email_xabarnoma': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
        }


class FoydalanuvchiTahrirlashForm(forms.ModelForm):
    """
    Foydalanuvchi asosiy ma'lumotlarini tahrirlash formasi
    """
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ismingiz'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Familiyangiz'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'email@example.com'
            }),
        }
    
    def clean_email(self):
        """
        Email validatsiyasi - boshqa foydalanuvchida bo'lmasligi kerak
        """
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError('Bu email manzil allaqachon ishlatilmoqda.')
        return email


# ============================================================================
# MAHSULOT FORMASI
# ============================================================================

class MahsulotForm(forms.ModelForm):
    """
    Mahsulot qo'shish va tahrirlash formasi
    """
    
    class Meta:
        model = Mahsulot
        fields = ['nomi', 'slug', 'kategoriya', 'qisqacha_tavsif', 'toliq_tavsif', 
                  'narx', 'chegirma_narxi', 'rasm', 'miqdor', 'holat', 'mashhur', 'yangi']
        widgets = {
            'nomi': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Mahsulot nomi'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'mahsulot-nomi'
            }),
            'kategoriya': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'qisqacha_tavsif': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Qisqacha tavsif'
            }),
            'toliq_tavsif': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 6,
                'placeholder': 'Mahsulot haqida batafsil ma\'lumot...'
            }),
            'narx': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '0.00'
            }),
            'chegirma_narxi': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '0.00'
            }),
            'rasm': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'miqdor': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '0'
            }),
            'holat': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'mashhur': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
            'yangi': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
        }
    
    def clean_chegirma_narxi(self):
        """
        Chegirma narxi validatsiyasi - asosiy narxdan kichik bo'lishi kerak
        """
        narx = self.cleaned_data.get('narx')
        chegirma_narxi = self.cleaned_data.get('chegirma_narxi')
        
        if chegirma_narxi and narx:
            if chegirma_narxi >= narx:
                raise forms.ValidationError('Chegirma narxi asosiy narxdan kichik bo\'lishi kerak.')
        
        return chegirma_narxi


# ============================================================================
# SHARH FORMASI
# ============================================================================

class SharhForm(forms.ModelForm):
    """
    Mahsulotga sharh qoldirish formasi
    """
    
    class Meta:
        model = Sharh
        fields = ['matn', 'baho']
        widgets = {
            'matn': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Mahsulot haqida fikringizni yozing...'
            }),
            'baho': forms.Select(
                choices=[(i, f'{i} yulduz') for i in range(1, 6)],
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                }
            ),
        }


# ============================================================================
# QIDIRUV FORMASI
# ============================================================================

class QidiruvForm(forms.Form):
    """
    Mahsulotlarni qidirish formasi
    """
    
    qidiruv = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Mahsulot qidirish...'
        }),
        label='Qidiruv'
    )
    
    kategoriya = forms.ModelChoiceField(
        queryset=Kategoriya.objects.filter(faol=True),
        required=False,
        empty_label='Barcha kategoriyalar',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        }),
        label='Kategoriya'
    )
    
    min_narx = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Min narx'
        }),
        label='Minimal narx'
    )
    
    max_narx = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Max narx'
        }),
        label='Maksimal narx'
    )
    
    TARTIBLASH_TANLOVI = [
        ('', 'Standart'),
        ('narx', 'Narx: Arzon'),
        ('-narx', 'Narx: Qimmat'),
        ('-yaratilgan_sana', 'Yangi'),
        ('-reyting', 'Reyting'),
    ]
    
    tartiblash = forms.ChoiceField(
        choices=TARTIBLASH_TANLOVI,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        }),
        label='Tartiblash'
    )
