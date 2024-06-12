from django.urls import path
from . import views
from .views import *

app_name = "accounts"

urlpatterns = [
    path("register", views.register, name="register"),
    path(
        "login/",
        NewLoginView.as_view(),
        name="login",
    ),
    path("logout", views.logout, name="logout"),
    path("user", views.profile, name="user"),
    path("user/edit", views.profile, name="edit"),
    path("user/update", views.profile, name="profile_update"),
    path("user/favorite-list", views.favorite_list, name="favorite-list"),
    path("user/favorite-delete", views.favorite_delete, name="favorite-delete"),
    path("password-reset", ResetPasswordView.as_view(), name="password-reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        NewPasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete/",
        NewPasswordResetCompleteView.as_view(),
        name="password-reset-complete",
    ),
]
