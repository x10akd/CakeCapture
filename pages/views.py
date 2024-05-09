from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")

def detail(request):
    return render(request, "item_detail/item_detail.html")

def about(request):
    return render(request, "pages/about.html")

def cart_detail(request):
    return render(request, "pages/cart_detail.html")
