from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import SubUser
from .forms import RegisterForm, LoginForm

# Create your views here.
# 註冊
def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "註冊成功!")
            return redirect("login")
        else:
            messages.error(request, "註冊失敗, 請確認輸入的訊息!")
            print(form.errors)  # 重新導向到登入畫面
    context = {"form": form}
    return render(request, "accounts/register.html", context)


# 登入
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '登入成功！')
            return render(request, 'pages/home.html', {'show_popup': True}) #重新導向到首頁
        else:
            messages.error(request, "登入失敗, 請確認輸入的訊息!")
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/login.html', context)

# 登出
def log_out(request):
    messages.success(request, "登出成功!")
    logout(request)
    return redirect("login")  # 重新導向到登入畫面



def user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # 判斷有無登入無登入導向登入頁
    user_id = request.user.id
    user = SubUser.objects.get(pk=user_id)
    return render(request, 'accounts/user.html', {'user': user})


@login_required
def edit_user_info(request):
    user_id = request.user.id
    user = SubUser.objects.get(pk=user_id)
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.phone = request.POST['phone']
        user.birthday = request.POST['birthday']
        user.email = request.POST['email']
        user.country = request.POST['country']
        user.street_address = request.POST['street_address']
        user.save()
        return redirect('user')
    else:
        return render(request, 'accounts/user.html', {'user': user})



