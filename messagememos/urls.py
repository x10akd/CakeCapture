from django.urls import path
from . import views


app_name = "messagememos"

urlpatterns = [
    path("", views.create, name="create"),
    path("message", views.message, name="message"),
]
