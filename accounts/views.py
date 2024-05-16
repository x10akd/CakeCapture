from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, UpdateProfileFrom, UpdateUserForm




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

# get先給予DB內個人資料, POST為修改個人資訊
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


#忘記密碼
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_message  = "我們已經寄出密碼重置信, "\
                        "你會在最初所填入註冊的信箱收到;"\
                        "如果沒有收到該信件, "\
                        "請確認是否為當初註冊信箱, 並檢查垃圾信箱"
    success_url = reverse_lazy('login')


# class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
#     template_name = 'accounts/password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         return redirect(self.success_url)

#     def form_invalid(self, form):
#         print(form.errors)  # 添加這行來打印表單錯誤信息
#         return super().form_invalid(form)
