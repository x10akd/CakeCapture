from django.db import models

import datetime


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=1, max_digits=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1, related_name="items"
    )
    quantity = models.IntegerField(default=0)
    description = models.CharField(max_length=100, default="", blank=True, null=True)
    image = models.ImageField(upload_to="uploads/product/")

    def __str__(self):
        return self.name
