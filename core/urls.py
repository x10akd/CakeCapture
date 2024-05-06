from django.contrib import admin
from django.urls import path, include
from pages import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("item_detail/", views.detail, name="detail"),
]
