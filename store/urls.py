from django.urls import path
from . import views

urlpatterns = [
    path('<pk>',views.product_detail,name="product_detail"),
]