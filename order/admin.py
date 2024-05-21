from django.contrib import admin
from .models import OrderMethod,Order,OrderItem
from django.contrib.auth.models import User

admin.site.register(OrderMethod)
admin.site.register(Order)
admin.site.register(OrderItem)


# 在 Django 中，Inline 是用來在管理界面中顯示和管理相關對象的工具。當兩個模型之間存在一對多或多對多的關係時，可以使用 Inline 來在父模型的管理頁面中嵌入子模型的表單，這樣可以在同一個頁面上同時查看和編輯相關的數據。


#creat orderitem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    inlines =[OrderItemInline]

admin.site.unregister(Order)

admin.site.register(Order,OrderAdmin)