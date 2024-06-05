from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from products.models import Favorite, RelationalProduct
from orders.models import Order
from feedbacks.models import *
from carts.cart import *
from .models import Profile
from .forms import *
import json


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "註冊成功！")
            return redirect("accounts:login")
        else:
            messages.error(request, "註冊失敗，請確認輸入的訊息！")
    context = {"form": form}
    return render(request, "accounts/register.html", context)


class NewLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        response = super(NewLoginView, self).form_valid(form)
        current_user = Profile.objects.get(user__id=self.request.user.id)
        saved_cart = current_user.old_cart
        if saved_cart:
            converted_cart = json.loads(saved_cart)
            cart = Cart(self.request)
            for key, value in converted_cart.items():
                cart.db_add(product=key, quantity=value)
        messages.success(self.request, "登入成功！")
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return response

    def form_invalid(self, form):
        messages.error(self.request, "登入失敗, 請確認輸入的訊息!")
        return super(NewLoginView, self).form_invalid(form)


def logout(request):
    messages.success(request, "登出成功!")
    auth_logout(request)
    return redirect("accounts:login")


@login_required
def profile(request):

    favorites = Favorite.objects.filter(user=request.user)
    orders = Order.objects.filter(buyer=request.user)
    relational_product = RelationalProduct.objects.filter(order__in=orders)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "個人資料更新成功")
            return redirect("accounts:user")
        else:
            messages.error(request, "更新失敗，請檢查輸入的資料。")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(
        request,
        "accounts/user.html",
        {"user_form": user_form, "profile_form": profile_form,
            "favorites": favorites, "orders": orders},
    )


# 忘記密碼
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_message = (
        "我們已經寄出密碼重置信"
        "您將會在當初填入註冊的信箱收到"
        "如果您沒有收到該信件"
        "請先檢查垃圾信箱並確認該信箱是否為當初註冊信箱"
    )
    success_url = reverse_lazy("accounts:login")


class NewPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class NewPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"


def user(request):
    user = User.objects.get(username=request.user.username)
    feedbacks = Feedback.objects.filter(user_id=user.id)
    return render(request, "accounts/user.html", {"feedbacks": feedbacks})


def favorite_delete(request):

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        favorite = get_object_or_404(
            Favorite, product_id=product_id, user_id=request.user.id
        )
        favorite.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)
