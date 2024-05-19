from django.urls import path
from . import views

urlpatterns = [
    path("order", views.order_checkout(), name="order"),

]
