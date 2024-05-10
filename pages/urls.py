from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("item_detail", views.detail, name="detail"),
    path("products_list", views.products_list, name="products_list"),
    path("about/", views.about, name="about"),
    path("cart/detail", views.cart_detail, name="cart_detail"),
]


# path('accounts/', include('allauth.urls')),
