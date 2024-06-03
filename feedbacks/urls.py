from django.urls import path
from . import views


app_name = "feedbacks"

urlpatterns = [
    path("create/", views.create, name="create"),
    path("list/", views.list, name="list"),
]
