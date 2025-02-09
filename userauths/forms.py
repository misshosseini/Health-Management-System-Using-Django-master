from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


USER_TYPE = [
    ("Doctor", "پزشک"),
    ("Patient", "بیمار"),
]

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کامل'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'}))
    user_type = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={"class": "form-select"}))

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2', 'user_type']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))

    class Meta:
        model = User
        fields = ['email', 'password']