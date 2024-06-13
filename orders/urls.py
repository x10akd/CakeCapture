from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("order_form", views.order_form, name="order_form"),
    path("order_confirm", views.order_confirm, name="order_confirm"),
    path("ecpay", views.ECPayView.as_view(), name="ecpay"),
    path("return", views.ReturnView.as_view(), name="return"),
    path("result", views.order_result, name="result"),
    path("line_pay_request/", views.line_pay_request, name="line_pay_request"),
    path("line_pay_confirm/", views.line_pay_confirm, name="line_pay_confirm"),
    path("line_pay_cancel/", views.line_pay_cancel, name="line_pay_cancel"),
    path(
        "line_pay_success/<str:order_id>",
        views.line_pay_success,
        name="line_pay_success",
    ),
]
