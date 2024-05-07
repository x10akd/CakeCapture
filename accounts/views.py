from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from . import models
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, LoginForm

# Create your views here.
# 註冊
# 註冊
def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)



#登入
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  #重新導向到首頁
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
 
# 登出
def log_out(request):
    logout(request)
    return redirect('login') #重新導向到登入畫面