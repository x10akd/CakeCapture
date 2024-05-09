from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("products/", include("store.urls")),
    path("about/", views.about, name="about"),
    path("my_favorite/", views.my_favorite, name="my_favorite"),
    path("item_detail", views.detail, name="detail"),
    path("about/",views.about,name="about"),
    path("cart/list", views.cart_list, name="cart_list"),
    path("cart/confirm", views.cart_confirm, name="cart_confirm"),
]

# path('accounts/', include('allauth.urls')),

