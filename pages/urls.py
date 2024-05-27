from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("my_favorite/", views.my_favorite, name="my_favorite"),
    path("common/",views.common,name="common"),
]
