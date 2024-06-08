from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from coupons.models import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="avatars", null=True, blank=True)
    full_name = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    coupon = models.ManyToManyField(Coupon, through="UserCoupon", related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    old_cart = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return self.user.username

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static("images/avatar.svg")
        return avatar


class UserCoupon(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    used_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True, null=True)
    usage_count = models.IntegerField(default=0, blank=False)

    def clean(self):
        if self.usage_count > self.coupon.usage_limit:
            raise ValidationError("此優惠券使用次數已達上限")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.coupon.code}"
