from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.products_list, name="products_list"),
    path("category/<str:foo>", views.category, name="category"),
    path("search/", views.search, name="search"),
]
