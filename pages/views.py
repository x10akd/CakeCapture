from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def detail(request):
    return render(request, "products/product_detail.html")


def about(request):
    return render(request, "pages/about.html")


def cart_detail(request):
    return render(request, "cart/cart_detail.html")


def products_list(request):
    return render(request, "products/products_list.html")


def my_favorite(request):
    return render(request, "my_favorite/my_favorite.html")


def cart_list(request):
    return render(request, "pages/cart_list.html")


def cart_confirm(request):
    return render(request, "pages/cart_confirm")
