from django.shortcuts import render
from products.models import Category


def home(request):
    categories = Category.objects.all()
    return render(request, "pages/home.html", {"categories": categories})


def about(request):
    categories = Category.objects.all()
    return render(request, "pages/about.html", {"categories": categories})


def questions(request):
    return render(request, "pages/questions.html")
