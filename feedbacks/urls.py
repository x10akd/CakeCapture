from django.urls import path
from . import views


app_name = "feedbacks"

urlpatterns = [
    path("", views.create, name="create"),
    path("message", views.message, name="message"),
]
