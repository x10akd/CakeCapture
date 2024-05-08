from django.shortcuts import render


def home(req):
    return render(req, "pages/home.html")

def detail(req):
    return render(req, "item_detail/item_detail.html")

def about(req):
    return render(req, "pages/about.html")
