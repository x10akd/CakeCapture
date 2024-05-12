from django.shortcuts import render
from .models import Product
# Create your views here.
def product_detail(request,pk):
  product = Product.objects.get(id = pk)
  return render (request,'products/item_detail.html',{'product':product})