from django.urls import path
from . import views


urlpatterns = [
    path("order_form",views.order_form,name="order_form"),
    path("order_success",views.order_success,name="order_success"),
    path("order_confirm",views.order_confirm,name="order_confirm"),
    path("order_process",views.order_process,name="order_process"),
    
]