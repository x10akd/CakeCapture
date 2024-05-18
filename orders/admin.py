from django.contrib import admin
from orders.models import Order
from store.models import RelationalProduct
# Register your models here.

# admin.TabularInline 用來表示一個模型與另一個模型之間的關聯，這種關聯在管理界面中以表格形式（tabular）呈現
class RelationalProductInline(admin.TabularInline):
    model = RelationalProduct
    model = Order.product.through  # 指向多對多關係的中間模型
    verbose_name = '商品名稱'
    extra = 2  # 控制在界面底部額外顯示的空白表格的數量，用於新增紀錄。
    fields = ('name', 'price', 'number')
    readonly_fields = ('name', 'price', 'number')  # 唯讀，不能修改

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['order_id', 'name']
    fields = ('order_id', 'name', 'email', 'phone', 'district', 'zipcode', 'address', 'total', 'status', 'created', 'modified')
    list_display = ('order_id', 'name', 'email', 'total')
    list_filter = ('status',)
    readonly_fields = ('order_id', 'name', 'email', 'phone', 'district', 'zipcode', 'address', 'total', 'created', 'modified')
    inlines = [RelationalProductInline,]


admin.site.register(Order, OrderAdmin)
