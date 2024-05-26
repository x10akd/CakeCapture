from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    return render(request, "pages/home.html")



def about(request):
    return render(request, "pages/about.html")


def my_favorite(request):
    return render(request, "my_favorite/my_favorite.html")



