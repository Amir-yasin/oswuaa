from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser, SP_Profile, ST_Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'gender', 'user_type', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')

CATEGORY_CHOICES = (
    ("Computer maintenance", "Computer maintenance"),
    ("Camera Installation", "Camera Installation"),
    ("Dish Installation", "Dish Installation"),
    ("Office Machine", "Office Machine"),
    ("Kitchen Machine", "Kitchen Machine"),
    ("Electrician", "Electrician"),
)

EXPERIENCE_CHOICES = (
    ("0 to 1 Year", "0 to 1 Year"),
    ("2 Years", "2 Years"),
    ("3 Years", "3 Years"),
    ("4 Years", "4 Years"),
    (">5 Years", ">5 Years"),
)

ADDRESS_CHOICES = (
    ("Addis Ababa", "Addis Ababa"),
    ("Oromia", "Oromia"),
    ("Amhara", "Amhara"),
    ("Tigray", "Tigray"),
    ("Gambella", "Gambella"),
    ("Afar", "Afar"),
    ("Somali", "Somali"),
    ("Harar", "Harar"),
    ("SNNP", "SNNP"),
    ("Benishangul Gumuz", "Benishangul Gumuz"),
)

class SP_ProfileForm(forms.ModelForm):
    experience = forms.ChoiceField(choices=EXPERIENCE_CHOICES)
    address = forms.ChoiceField(choices=ADDRESS_CHOICES)

    class Meta:
        model = SP_Profile
        fields = ['phone_number', 'category', 'experience', 'address', 'image']

class ST_ProfileForm(forms.ModelForm):
    address = forms.ChoiceField(choices=ADDRESS_CHOICES)

    class Meta:
        model = ST_Profile
        fields = ['phone_number', 'address', 'image']
