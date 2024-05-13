from django.shortcuts import render, redirect
from .models import Product, Category
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse


def products_list(request):
    # products = Product.objects.all()

    # setup paginator
    p = Paginator(Product.objects.all(), 9)
    page = request.GET.get("page")
    products = p.get_page(page)

    return render(request, "products/products_list.html", {"products": products})


def category(request, foo):
    # foo = foo.replace("-", " ")
    try:
        category = Category.objects.get(name=foo)
        p = Paginator(Product.objects.filter(category=category), 9)
        page = request.GET.get("page")
        products = p.get_page(page)
        return render(
            request,
            "products/category.html",
            {"products": products, "category": category},
        )
    except Category.DoesNotExist:
        messages.error(request, ("That Category Doesn't Exist!"))
        return redirect("home")


def search(request):
    query = request.GET.get("search")
    if query:
        p = Paginator(Product.objects.filter(name__icontains=query), 9)
        page = request.GET.get("page")
        products = p.get_page(page)
        return render(
            request,
            "products/search.html",
            {"products": products, "query": query},
        )


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "products/product_detail.html", {"product": product})
