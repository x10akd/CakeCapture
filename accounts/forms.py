from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            }
        ),
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control  mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            }
        ),
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control  mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            }
        ),
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control  mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        label="帳號",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label="密碼",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            }
        ),
    )
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ["username", "password", "remember_me"]


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        label="帳號",
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label="電子郵件",
        widget=forms.EmailInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email"]

class UpdateProfileFrom(forms.ModelForm):
    full_name = forms.CharField(
        max_length=10,
        label="名字",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "block w-full rounded-md border-0 py-1.5 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"})
    )
    phone = forms.CharField(
        max_length=15,
        label="手機號碼",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            }
        ),
    )
    birthday = forms.DateField(
        label="出生日期",
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",  # 設置為 date 類型
                "class": "block w-full rounded-md border-0 py-1.5 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
            },
            format="%Y-%m-%d",
        ),  # 確保後端接收的格式是 YYYY-MM-DD
    )
    
    address = forms.CharField(
        max_length=100,
        label="詳細地址",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["full_name","phone", "birthday", "address"]
