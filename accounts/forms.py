from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control  mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control  mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control  mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
        required=True,
        username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
    
    )
        password = forms.CharField(
        required=True,
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
    )
        remember_me = forms.BooleanField(required=False)

        class Meta:
            model = User
            fields = ["username", "password", "remember_me"]

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        label="帳號",
        widget=forms.TextInput(attrs={
                                'class': 'form-control mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
    )
    email = forms.EmailField(
        required=True,
        label="電子郵件",
        widget=forms.EmailInput(attrs={
                                'class': 'form-control  mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
    )
    class Meta:
        model = User
        fields = ["username", "email"]

class UpdateProfileFrom(forms.ModelForm):
    phone = forms.CharField(max_length=15)
    birthday = forms.DateField()
    country = forms.CharField(max_length=100)
    street_address = forms.CharField(max_length=100)


    class Meta:
        model = Profile
        fields = ["phone", "birthday", "country", "street_address"]
