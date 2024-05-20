from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("checkout", views.order_checkout(), name="checkout"),
    path('ecpay', views.ECPayView.as_view(), name='ecpay'),
    path('return', views.ReturnView.as_view(), name='return'),
    path('order_result', views.OrderResultView.as_view(), name='order_result'),
    path('order_success', views.OrderSuccessView.as_view(), name='order_success'),
    path('order_fail', views.OrderFailView.as_view(), name='order_fail'),

]
