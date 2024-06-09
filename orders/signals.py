from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product
from .models import *


@receiver(post_save, sender=OrderMethod)
def update_stock(sender, instance, created, **kwargs):
    if created:
        order = instance.order
        for item in order.relationalproduct_set.all():
            product = item.product
            product.quantity -= item.number
            product.save()


@receiver(post_save, sender=Order)
def restore_stock_if_payment_failed(sender, instance, created, **kwargs):
    if not created and instance.status == 'payment_fail':
        for item in instance.relationalproduct_set.all():
            product = item.product
            product.quantity += item.number
            product.save()


@receiver(post_save, sender=Order)
def schedule_order_payment_check(sender, instance, created, **kwargs):
    """創訂單五分鐘後若不確認自動將訂單轉為fail"""
    if created and instance.status == 'waiting_for_check':
        from .tasks import check_order_payment_status
        check_order_payment_status.apply_async((instance.id,), countdown=30) #300秒五分鐘


@receiver(post_save, sender=Order)
def schedule_check(sender, instance, created, **kwargs):
    if created or instance.status == 'unpaid':
        from .tasks import check_order_unpaid_to_fail
        check_order_unpaid_to_fail.apply_async((instance.id,), countdown=1200) #1200秒 20分鐘
