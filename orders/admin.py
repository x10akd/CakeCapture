from django.contrib import admin
from orders.models import Order, OrderMethod, OrderItem
from products.models import RelationalProduct

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class RelationalProductInline(admin.TabularInline):
    model = Order.product.through 
    verbose_name = '商品名稱'
    extra = 2  # 控制在界面底部額外顯示的空白表格的數量，用於新增紀錄。
    fields = ('product', 'order',) 
    readonly_fields = ('product', 'order') 

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['order_id', 'name']
    fields = ('order_id', 'name', 'email', 'phone', 'address', 'total', 'status', 'created', 'modified')
    list_display = ('order_id', 'name', 'email', 'total')
    list_filter = ('status',)
    readonly_fields = ('order_id', 'name', 'email', 'phone', 'address', 'total', 'created', 'modified')
    inlines = [OrderItemInline, RelationalProductInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderMethod)
