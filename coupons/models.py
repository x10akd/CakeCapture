from django.db import models
from django.contrib.auth.models import User
from orders.models import *


class Coupon(models.Model):
    users = models.ManyToManyField(User, through="UserCoupon", related_name="coupons")
    code = models.CharField(max_length=25)
    discount = models.IntegerField(blank=False)
    min_order = models.IntegerField(blank=True, null=True)
    usage_limit = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.code


class UserCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="usercoupons_coupons"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="usercoupons_coupons",
    )
    used_at = models.DateTimeField(auto_now=True)
    usage_count = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return f"{self.user.username} - {self.coupon.code}"
