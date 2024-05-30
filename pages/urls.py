from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("my_favorite/", views.my_favorite, name="my_favorite"),
    path("common_problem/",views.common_problem,name="common_problem"),
]
