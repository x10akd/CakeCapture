from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chats/", include("chats.urls")),
    path("", include("pages.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("products/", include("store.urls")),
    path("cart/", include("cart.urls")),
    path("order/", include("order.urls")),
]
