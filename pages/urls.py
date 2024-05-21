from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("about/", views.about, name="about"),
    path("my_favorite/", views.my_favorite, name="my_favorite"),
    path("cart/detail", views.cart_detail, name="cart_detail"),
    path("cart/confirm", views.cart_confirm, name="cart_confirm"),
    path("cart/payment", views.cart_payment, name="cart_payment"),
    path("cart/checkout", views.cart_checkout, name="cart_checkout"),
]


# path('accounts/', include('allauth.urls')),
