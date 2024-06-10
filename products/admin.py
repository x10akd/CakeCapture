from django.contrib import admin
from .models import Category, Product, ProductReview, Favorite
from .admin_forms import ProductAdminForm

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

admin.site.register(Product, ProductAdmin)

admin.site.register(Category)
admin.site.register(ProductReview)
admin.site.register(Favorite)
