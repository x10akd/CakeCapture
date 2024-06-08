from .models import Category


def categories(request):
    categories = Category.objects.exclude(name="其他")
    return {"categories": categories}
