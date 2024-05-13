from django.contrib import admin
from django.urls import path, include
from pages import views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("products/", include("store.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
