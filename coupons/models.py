from django.db import models
from orders.models import *
from django.core.validators import MinValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=25)
    discount = models.IntegerField(blank=False, validators=[MinValueValidator(0)])
    min_order = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    usage_limit = models.IntegerField(blank=False, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.code
