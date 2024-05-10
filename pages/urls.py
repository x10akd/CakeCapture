from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("product_detail", views.detail, name="detail"),
    path("about/", views.about, name="about"),
    path("my_favourite/",views.my_favourite,name="my_favourite"),
    path("cart/detail", views.cart_detail, name="cart_detail"),
]


# path('accounts/', include('allauth.urls')),
