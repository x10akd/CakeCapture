from django.urls import path
from .views import CheckoutView, ConfirmView
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout", CheckoutView.as_view(), name="checkout"),
    path("confirm/", ConfirmView.as_view(), name="confirm"),
    path('ecpay', views.ECPayView.as_view(), name='ecpay'),
    path('return', views.ReturnView.as_view(), name='return'),
    path('orderresult', views.OrderResultView.as_view(), name='orderresult'),
    path('order_success', views.OrderSuccessView.as_view(), name='order_success'),
    path('order_fail', views.OrderFailView.as_view(), name='order_fail'),

]
