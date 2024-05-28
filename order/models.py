from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class OrderMethod(models.Model):
    DELIVERY_CHOICES = [
        ("超商取貨", "超商取貨"),
        ("宅配到府", "宅配到府"),
    ]

    PAYMENT_CHOICES = [
        ("超商取貨付款", "超商取貨付款"),
        ("信用卡", "信用卡"),
        ("第三方支付", "第三方支付"),
        ("ATM 轉帳付款", "ATM 轉帳付款"),
    ]

    INVOICE_CHOICES = [
        ("捐贈發票", "捐贈發票"),
        ("二聯式電子發票", "二聯式電子發票"),
        ("三聯式電子發票", "三聯式電子發票"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    coupon_used = models.BooleanField(default=False)
    store_name = models.CharField(max_length=100, blank=True)
    store_address = models.CharField(max_length=200, blank=True)
    order_name = models.CharField(max_length=50)
    order_cell_phone = models.CharField(max_length=10)
    order_phone = models.CharField(max_length=10, blank=True)
    order_email = models.EmailField(max_length=50)
    recipient_name = models.CharField(max_length=50)
    recipient_cell_phone = models.CharField(max_length=10)
    recipient_email = models.EmailField(max_length=50)
    invoice_option = models.CharField(max_length=100, choices=INVOICE_CHOICES)
    invoice_number = models.CharField(max_length=8, null=True, blank=True)
    return_agreement = models.BooleanField(default=False)

    def __str__(self):
        return self.order_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    shipping_address = models.CharField(max_length=200)
    amount_paid = models.IntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"Order - {str(self.id)}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"OrderItem - {str(self.id)}"
