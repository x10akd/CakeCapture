from django.shortcuts import render, redirect
from .models import Product, Category
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import ProductReview
from django.db.models import Avg
from .form import ProductReviewForm


def products_list(request):
    # 傳遞selected_option預設值給模板排序區域標題
    selected_option = "預設排序"
    # 透過url獲取sort_by的值，若sort_by不存在，返回"default"值
    sort_by = request.GET.get("sort_by", "default")
    # setup paginator & sort_by logic
    if sort_by == "default":
        # 從Product model根據每9個一組取出數據
        p = Paginator(Product.objects.all(), 9)
        # 傳遞值給模板排序區域標題
        selected_option = "預設排序"
    elif sort_by == "pl2h":  # pl2h = price low to high
        # 將數據根據price由低到高排序並取出再用分頁器分組
        p = Paginator(Product.objects.all().order_by("price"), 9)
        selected_option = "價格由低到高"
    elif sort_by == "ph2l":  # ph2l = price high to low
        p = Paginator(Product.objects.all().order_by("-price"), 9)
        selected_option = "價格由高到低"
    # 透過url獲取page的值 (網址後page="")
    page = request.GET.get("page")
    # 依據上面取得的分頁p物件及page的值決定要傳給模板的東西
    products = p.get_page(page)

    return render(
        request,
        "products/products_list.html",
        {"products": products, "selected_option": selected_option},
    )


# 因需要category值，用cat變數來接
def category(request, cat):
    selected_option = "預設排序"
    sort_by = request.GET.get("sort_by", "default")
    try:
        # 獲取Category models中符合cat輸入值的對象
        category = Category.objects.get(name=cat)
        if sort_by == "default":
            # 篩選出類別值符合category值的 products，並用分頁器分組
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
    # 若 Category 類別找不到輸入值，導回首頁
    except Category.DoesNotExist:
        messages.error(request, ("That Category Doesn't Exist!"))
        return redirect("home")


def search(request):
    selected_option = "預設排序"
    # 透過url獲取search的值(網址後?search="")
    query = request.GET.get("search")
    sort_by = request.GET.get("sort_by", "default")
    if query:
        if sort_by == "default":
            # 篩選出 products中 name值有包含 query的 products(模糊搜尋)，並用分頁器分組
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
    # 相關商品 (related_products)
    related_ps = (
        Product.objects.filter(category=product.category)
        .exclude(id=pk)
        .order_by("?")[0:4]
    )

    review_form = ProductReviewForm()

    # Getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    star_range = range(1, 6)

    average_rating = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product
        ).count()

        if user_review_count > 0:
            make_review = False

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "review_form": review_form,
            "related_ps": related_ps,
            "star_range": star_range,
            "average_rating": average_rating,
            "make_review": make_review,
        },
    )


def ajax_add_review(request, pk):
    product = Product.objects.get(id=pk)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST["review"],
        rating=request.POST["rating"],
    )

    reviews_count = product.reviews.count()
    average_rating = product.reviews.aggregate(Avg("rating"))["rating__avg"]

    context = {
        "user": user.username.capitalize(),
        "review": request.POST["review"],
        "rating": request.POST["rating"],
        "reviews_count": reviews_count,
        "average_rating": average_rating,
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    return JsonResponse(
        {
            "bool": True,
            "context": context,
            "average_reviews": average_reviews,
        }
    )
