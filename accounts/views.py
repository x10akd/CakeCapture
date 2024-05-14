from .forms import LoginForm
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, UpdateProfileFrom, UpdateUserForm

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
class NewLoginView(LoginView):
    form_class = LoginForm
    def form_valid(self, form):
        response = super(NewLoginView, self).form_valid(form)
        messages.success(self.request, '登入成功！')
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return response

    def form_invalid(self, form):
        messages.error(self.request, '登入失敗, 請確認輸入的訊息!')
        return super(NewLoginView, self).form_invalid(form)

# 登出
def log_out(request):
    messages.success(request, "登出成功!")
    logout(request)
    return redirect("login")  # 重新導向到登入畫面


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileFrom(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '個人資料更新成功')
            return redirect('user')
        else:
            messages.error(request, '更新失敗，請檢查輸入的資料。')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileFrom(instance=request.user.profile)
    
    return render(request, 'accounts/user.html', {'user_form': user_form, 'profile_form':profile_form})








