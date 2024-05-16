from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")



def about(request):
    return render(request, "pages/about.html")


def my_favorite(request):
    return render(request, "my_favorite/my_favorite.html")



