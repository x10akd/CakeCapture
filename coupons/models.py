from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from orders.models import *


class Coupon(models.Model):
    users = models.ManyToManyField(User, through="UserCoupon", related_name="coupons")
    code = models.CharField(max_length=25)
    discount = models.IntegerField(blank=False)
    min_order = models.IntegerField(blank=True, null=True)
    usage_limit = models.IntegerField(blank=False)

    def __str__(self):
        return self.code


class UserCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    used_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True)
    usage_count = models.IntegerField(default=0, blank=False)

    def clean(self):
        if self.usage_count > self.coupon.usage_limit:
            raise ValidationError("此優惠券使用次數已達上限")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.coupon.code}"
