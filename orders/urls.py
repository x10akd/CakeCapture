from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("order_form", views.order_form, name="order_form"),
    path("order_confirm", views.order_confirm, name="order_confirm"),
    path("ecpay", views.ECPayView.as_view(), name="ecpay"),
    path("return", views.ReturnView.as_view(), name="return"),
    path("result", views.order_result, name="result"),
    path("create-payment/", views.create_line_pay_payment, name="create_payment"),
    path("confirm/", views.confirm_line_pay_payment, name="confirm_payment"),
    path("cancel/", views.cancel_line_pay_payment, name="cancel_payment"),
]
