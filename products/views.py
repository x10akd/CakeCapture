from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, ProductReview, Favorite
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from .forms import ProductReviewForm
from django.db.models import Avg, Case, When, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def all(request):
    selected_option = "預設排序"
    sort_by = request.GET.get("sort_by", "default")

    products = Product.objects.all()

    if sort_by == "price_asc":
        products = products.order_by("price")
        selected_option = "價格由低到高"
    elif sort_by == "price_desc":
        products = products.order_by("-price")
        selected_option = "價格由高到低"
    elif sort_by == "rating_asc":
        products = products.annotate(
            avg_rating=Avg("reviews__rating"),
            sorted_rating=Case(
                When(avg_rating=None, then=Value(6.0)),
                default="avg_rating",
            ),
        ).order_by("sorted_rating")
        selected_option = "評價由低到高"
    elif sort_by == "rating_desc":
        products = products.annotate(
            avg_rating=Avg("reviews__rating"),
            sorted_rating=Case(
                When(avg_rating=None, then=Value(-1.0)),
                default="avg_rating",
            ),
        ).order_by("-sorted_rating")
        selected_option = "評價由高到低"
    else:
        products = products
        selected_option = "預設排序"

    products = Paginator(products, 9)
    page = request.GET.get("page")
    products = products.get_page(page)

    return render(
        request,
        "products/all.html",
        {"products": products, "selected_option": selected_option, "sort_by": sort_by},
    )


def category(request, category):
    selected_option = "預設排序"
    sort_by = request.GET.get("sort_by", "default")
    try:
        category = Category.objects.get(name=category)
        products = Product.objects.filter(category=category)

        if sort_by == "price_asc":
            products = products.order_by("price")
            selected_option = "價格由低到高"
        elif sort_by == "price_desc":
            products = products.order_by("-price")
            selected_option = "價格由高到低"
        elif sort_by == "rating_asc":
            products = products.annotate(
                avg_rating=Avg("reviews__rating"),
                sorted_rating=Case(
                    When(avg_rating=None, then=Value(6.0)),
                    default="avg_rating",
                ),
            ).order_by("sorted_rating")
            selected_option = "評價由低到高"
        elif sort_by == "rating_desc":
            products = products.annotate(
                avg_rating=Avg("reviews__rating"),
                sorted_rating=Case(
                    When(avg_rating=None, then=Value(-1.0)),
                    default="avg_rating",
                ),
            ).order_by("-sorted_rating")
            selected_option = "評價由高到低"
        else:
            products = products
            selected_option = "預設排序"

        products = Paginator(products, 9)
        page = request.GET.get("page")
        products = products.get_page(page)
        return render(
            request,
            "products/category.html",
            {
                "products": products,
                "category": category,
                "selected_option": selected_option,
                "sort_by": sort_by,
            },
        )
    except Category.DoesNotExist:
        messages.error(request, ("That Category Doesn't Exist!"))
        return redirect("home")


def search(request):
    selected_option = "預設排序"
    query = request.GET.get("search")
    sort_by = request.GET.get("sort_by", "default")
    if query:
        products = Product.objects.filter(name__icontains=query)

        if sort_by == "price_asc":
            products = products.order_by("price")
            selected_option = "價格由低到高"
        elif sort_by == "price_desc":
            products = products.order_by("-price")
            selected_option = "價格由高到低"
        elif sort_by == "rating_asc":
            products = products.annotate(
                avg_rating=Avg("reviews__rating"),
                sorted_rating=Case(
                    When(avg_rating=None, then=Value(6.0)),
                    default="avg_rating",
                ),
            ).order_by("sorted_rating")
            selected_option = "評價由低到高"
        elif sort_by == "rating_desc":
            products = products.annotate(
                avg_rating=Avg("reviews__rating"),
                sorted_rating=Case(
                    When(avg_rating=None, then=Value(-1.0)),
                    default="avg_rating",
                ),
            ).order_by("-sorted_rating")
            selected_option = "評價由高到低"
        else:
            products = products
            selected_option = "預設排序"

        products = Paginator(products, 9)
        page = request.GET.get("page")
        products = products.get_page(page)
        return render(
            request,
            "products/search.html",
            {
                "products": products,
                "query": query,
                "selected_option": selected_option,
                "sort_by": sort_by,
            },
        )


def detail(request, pk):
    product = Product.objects.get(id=pk)
    related_products = (
        Product.objects.filter(category=product.category)
        .exclude(id=pk)
        .order_by("?")[0:4]  # 想讓顯示商品隨機
    )

    review_form = ProductReviewForm()

    # Getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    p = Paginator(reviews, 10)
    page_obj = p.get_page(1)

    # render星星變數
    star_range = range(1, 6)

    # 所有評價平均分數
    average_rating = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    # 辨別是否顯示新增評論區變數
    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product
        ).count()

        if user_review_count > 0:
            make_review = False

    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "related_products": related_products,
            "reviews": page_obj,
            "has_next": page_obj.has_next(),  # 是否有下一頁
            "review_form": review_form,
            "star_range": star_range,
            "average_rating": average_rating,
            "make_review": make_review,
        },
    )


def add_review(request, pk):
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

    return JsonResponse(
        {
            "bool": True,
            "context": context,
        }
    )


def edit_review(request, review_id):
    if request.method == "POST":
        review = get_object_or_404(ProductReview, id=review_id, user=request.user)
        review_text = request.POST.get("review")
        review_rating = request.POST.get("rating")

        if review_text and review_rating:
            review.review = review_text
            review.rating = review_rating
            review.save()

            product = review.product
            reviews_count = product.reviews.count()
            average_rating = product.reviews.aggregate(Avg("rating"))["rating__avg"]

            context = {
                "user": request.user.username.capitalize(),
                "review": review_text,
                "rating": int(review_rating),
                "reviews_count": reviews_count,
                "average_rating": average_rating,
            }

            return JsonResponse(
                {
                    "bool": True,
                    "context": context,
                }
            )
        else:
            return JsonResponse({"bool": False})
    else:
        return JsonResponse({"bool": False})


def load_more_reviews(request, product_id):
    page = request.GET.get("page", 1)
    reviews = ProductReview.objects.filter(product_id=product_id).order_by("-date")
    reviews = Paginator(reviews, 10)

    try:
        reviews = reviews.page(page)
    except PageNotAnInteger:
        reviews = reviews.page(1)
    except EmptyPage:
        return JsonResponse({"reviews": [], "has_next": False})

    reviews_data = []
    for review in reviews:
        reviews_data.append(
            {
                "user": review.user.username,
                "date": review.date.strftime("%d %b, %Y"),
                "rating": review.rating,
                "review": review.review,
                "id": review.id,
                "is_user_review": review.user == request.user,
            }
        )

    return JsonResponse({"reviews": reviews_data, "has_next": reviews.has_next()})


@login_required
def add_to_favorites(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user, product=product
        )
        if created:
            return JsonResponse({"status": "added"})
        else:
            return JsonResponse({"status": "exists"})
