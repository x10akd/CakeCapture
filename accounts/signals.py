from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_coupon_for_new_user(sender, instance, created, **kwargs):
    if created:
        coupon, created = Coupon.objects.get_or_create(
            code="5XCAMP",
            defaults={
                "discount": 50,
                "min_order": 0,
                "usage_limit": 1,
                "expired_at" : timezone.now() + timedelta(days=30),
            },
        )
        expired_at = timezone.now() + timedelta(days=30)

        profile = Profile.objects.get(user=instance)
        UserCoupon.objects.create(
            profile=profile,
            coupon=coupon,
            order=None,
            usage_count=0,
            expired_at=expired_at,
        )
