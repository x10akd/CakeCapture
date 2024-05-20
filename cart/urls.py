from django.urls import path
from . import views



urlpatterns = [
    path("", views.cart_summary, name="cart_summary"),
    path("add/",views.cart_add,name='cart_add'),
    path("delete/",views.cart_delete,name='cart_delete'),
    path("deleteAll/",views.cart_delete_all,name='cart_delete_all'),
    path("update/",views.cart_update,name='cart_update'),
    path("confirm", views.cart_confirm, name="cart_confirm"),
    path("payment", views.cart_payment, name="cart_payment"),
]
