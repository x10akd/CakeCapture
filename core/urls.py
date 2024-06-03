from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("products/", include("products.urls")),
    path("carts/", include("carts.urls")),
    path("chats/", include("chats.urls")),
    path("orders/", include("orders.urls")),
    path("feedbacks/", include("feedbacks.urls")),
    path("managements/", include("managements.urls")),
    path("coupons/", include("coupons.urls")),
]
