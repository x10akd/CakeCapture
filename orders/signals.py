from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product
from .models import OrderMethod


@receiver(post_save, sender=OrderMethod)
def update_stock(sender, instance, created, **kwargs):
    if created:
        order = instance.order
        for item in order.relationalproduct_set.all():
            product = item.product
            product.quantity -= item.number
            product.save()
