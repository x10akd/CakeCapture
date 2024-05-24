from django.db import models
from accounts.models import Profile
from store.models import Product,RelationalProduct

class Order(models.Model):
    order_id = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    total = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    product = models.ManyToManyField('store.Product', related_name='order_set', through='store.RelationalProduct')
    # 可由產品查詢到所有order, 如 :
    # product = Product.objects.get(id=特定的產品ID)
    # orders_with_product = product.orders.all()
    status = models.CharField(max_length=100, choices=(("unpaid", "Unpaid"), ("payment_fail", "Payment Fail"), ("waiting_for_shipment", "Waiting for shipment"), ("transporting", "Transporting"), ("completed", "Completed"), ("cancelled", "Cancelled")), default="unpaid"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 先確認有無該訂單 id
        if not self.order_id:
            #將 id 設置為八位數(不足由 0 補上)
            self.order_id = f'ORDER{self.id:08}'
            super().save(*args, **kwargs)
            # 先創立物件後在創立特定 訂單id 後再存入

    class Meta:
        verbose_name = '訂單'
        verbose_name_plural = '訂單' 
        # 單筆或多筆接載管理介面中稱之訂單

    def __str__(self):
        return self.order_id


