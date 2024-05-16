from django.contrib import admin
from .models import OrderMethod,Order,OrderItem

admin.site.register(OrderMethod)
admin.site.register(Order)
admin.site.register(OrderItem)
