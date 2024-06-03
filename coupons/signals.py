from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone
from datetime import timedelta


@receiver(post_save, sender=User)
def create_coupon_for_new_user(sender, instance, created, **kwargs):

    if created:
        coupon = Coupon.objects.create(
            code="5XCAMP",
            discount=50,
            min_order=0,
            usage_limit=1,
            expired_at=timezone.now() + timedelta(days=30),
        )

        UserCoupon.objects.create(
            user=instance,
            coupon=coupon,
            order=None,
            usage_count=0,
        )
