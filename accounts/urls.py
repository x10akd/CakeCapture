from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import NewLoginView, ResetPasswordView

app_name = "accounts"

urlpatterns = [
    path("register", views.register, name="register"),
    path(
        "login/",
        NewLoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout", views.log_out, name="logout"),
    path("password_reset", ResetPasswordView.as_view(), name="password_reset"),
    path("user", views.profile, name="user"),
    path("user/edit", views.profile, name="edit"),
    path("user/update", views.profile, name="profile_update"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("user/favorite_delete", views.favorite_delete, name="favorite_delete"),
]
