from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chats/", include("chats.urls")),
    path("", include("pages.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("products/", include("store.urls")),
    path("carts/", include("carts.urls")),
    path("order/", include("order.urls")),
    path("messagememos/", include("messagememos.urls")),
]
