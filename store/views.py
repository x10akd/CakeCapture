from django.shortcuts import render, redirect
from .models import Product, Category
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse


def products_list(request):
    # products = Product.objects.all()
    selected_option = "預設排序"
    sort_by = request.GET.get("sort", "default")
    # setup paginator
    if sort_by == "default":
        p = Paginator(Product.objects.all(), 9)
        selected_option = "預設排序"
    elif sort_by == "pl2h":
        p = Paginator(Product.objects.all().order_by("price"), 9)
        selected_option = "價格由低到高"
    elif sort_by == "ph2l":
        p = Paginator(Product.objects.all().order_by("-price"), 9)
        selected_option = "價格由高到低"
    page = request.GET.get("page")
    products = p.get_page(page)

    return render(
        request,
        "products/products_list.html",
        {"products": products, "selected_option": selected_option},
    )


def category(request, foo):
    # foo = foo.replace("-", " ")
    selected_option = "預設排序"
    sort_by = request.GET.get("sort", "default")
    try:
        category = Category.objects.get(name=foo)
        if sort_by == "default":
            p = Paginator(Product.objects.filter(category=category), 9)
            selected_option = "預設排序"
        elif sort_by == "pl2h":
            p = Paginator(
                Product.objects.filter(category=category).order_by("price"), 9
            )
            selected_option = "價格由低到高"
        elif sort_by == "ph2l":
            p = Paginator(
                Product.objects.filter(category=category).order_by("-price"), 9
            )
            selected_option = "價格由高到低"
        page = request.GET.get("page")
        products = p.get_page(page)
        return render(
            request,
            "products/category.html",
            {
                "products": products,
                "category": category,
                "selected_option": selected_option,
            },
        )
    except Category.DoesNotExist:
        messages.error(request, ("That Category Doesn't Exist!"))
        return redirect("home")


def search(request):
    selected_option = "預設排序"
    query = request.GET.get("search")
    sort_by = request.GET.get("sort", "default")
    if query:
        if sort_by == "default":
            p = Paginator(Product.objects.filter(name__icontains=query), 9)
            selected_option = "預設排序"
        elif sort_by == "pl2h":
            p = Paginator(
                Product.objects.filter(name__icontains=query).order_by("price"), 9
            )
            selected_option = "價格由低到高"
        elif sort_by == "ph2l":
            p = Paginator(
                Product.objects.filter(name__icontains=query).order_by("-price"), 9
            )
            selected_option = "價格由高到低"

        page = request.GET.get("page")
        products = p.get_page(page)
        return render(
            request,
            "products/search.html",
            {"products": products, "query": query, "selected_option": selected_option},
        )


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "products/product_detail.html", {"product": product})
