import plotly.graph_objs as create_plot
import plotly.offline as html_plot
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, Category, Favorite
from products.forms import CategoryForm, ProductForm
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from coupons.models import *
from coupons.forms import *
from accounts.forms import *
from django.db.models import Count, Sum, F, Prefetch, Case, When, Value, IntegerField
from feedbacks.models import Feedback, FeedbackReply
from feedbacks.forms import FeedbackReplyForm
from orders.models import Order
from django.core.paginator import Paginator
import calendar
from concurrent.futures import ThreadPoolExecutor
from django.utils import timezone
from datetime import datetime


# 定義superuser decorator
class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def superuser_required(user):
    return user.is_superuser


@user_passes_test(superuser_required)
def product_list(request):
    query = request.GET.get("search", "")
    if query:
        products = Product.objects.filter(name__icontains=query).order_by("-id")
    else:
        products = Product.objects.all().order_by("-id")

    return render(
        request,
        "managements/product_list.html",
        {"products": products, "query": query},
    )


@user_passes_test(superuser_required)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("managements:product_list")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "managements/edit_product.html",
        {"product": product, "form": form},
    )


@user_passes_test(superuser_required)
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    return redirect(reverse("managements:product_list"))


class ProductCreateView(SuperuserRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "managements/add_product.html"
    success_url = reverse_lazy("managements:product_list")


@user_passes_test(superuser_required)
def category_list(request):
    categories = Category.objects.all()
    return render(
        request,
        "managements/category_list.html",
        {"categories": categories},
    )


class CategoryCreateView(SuperuserRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "managements/add_category.html"
    success_url = reverse_lazy("managements:category_list")


@user_passes_test(superuser_required)
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    return redirect(reverse("managements:category_list"))


@user_passes_test(superuser_required)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("managements:category_list")
    else:
        form = ProductForm(instance=category)
    return render(
        request,
        "managements/edit_category.html",
        {"category": category, "form": form},
    )


def quantity_index(request):
    return render(
        request,
        "managements/quantity_index.html",
    )


@user_passes_test(superuser_required)
def quantity_charts(request):
    categories = Category.objects.prefetch_related(
        Prefetch("items", queryset=Product.objects.only("name", "quantity"))
    )
    category_graphs = {}

    def generate_chart(category):
        products = category.items.all()
        product_names = [product.name for product in products]
        product_quantities = [product.quantity for product in products]

        height = max(400, 70 * len(product_names))

        bar = create_plot.Bar(
            x=product_quantities,
            y=product_names,
            name=category.name,
            orientation="h",
        )
        layout = create_plot.Layout(
            title={"text": f"{category.name} 庫存數量", "font": {"size": 24}},
            xaxis=dict(title="數量"),
            yaxis=dict(title="商品名稱", tickfont=dict(size=20)),
            height=height,
        )
        fig = create_plot.Figure(data=[bar], layout=layout)

        div = html_plot.plot(fig, auto_open=False, output_type="div")
        return (category.name, div)

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(generate_chart, categories))

    category_graphs = dict(results)

    return render(
        request,
        "managements/quantity_charts.html",
        {"category_graphs": category_graphs},
    )


@user_passes_test(superuser_required)
def quantity_alter(request, category):
    category = get_object_or_404(Category, name=category)
    products = category.items.all()

    if request.method == "POST":
        for product in products:
            new_quantity = request.POST.get(f"quantity_{product.id}")
            if new_quantity:
                product.quantity = int(new_quantity)
                product.save()
        return HttpResponseRedirect(request.path_info)  # Refresh the page

    return render(
        request,
        "managements/quantity_alter.html",
        {"category": category, "products": products},
    )


def order_list(request):
    query = request.GET.get("search", "")
    if query:
        orders = Order.objects.filter(order_id__icontains=query)
    else:
        orders = Order.objects.all()

    orders = orders.annotate(
        priority=Case(
            When(status="waiting_for_shipment", then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).order_by("priority", "-id")

    orders = Paginator(orders, 20)
    page = request.GET.get("page")
    orders = orders.get_page(page)

    return render(
        request,
        "managements/order_list.html",
        {"orders": orders, "query": query},
    )


@user_passes_test(superuser_required)
def coupon_list(request):
    query = request.GET.get("search", "")
    if query:
        coupons = Coupon.objects.filter(name__icontains=query).order_by("-id")
    else:
        coupons = Coupon.objects.all().order_by("-id")

    return render(
        request,
        "managements/coupon_list.html",
        {"coupons": coupons, "query": query},
    )


@user_passes_test(superuser_required)
def edit_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == "POST":
        form = CouponForm(request.POST, request.FILES, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect("managements:coupon_list")
    else:
        form = CouponForm(instance=coupon)
    return render(
        request,
        "managements/edit_coupon.html",
        {"coupon": coupon, "form": form},
    )


class CouponCreateView(SuperuserRequiredMixin, CreateView):
    model = Coupon
    form_class = CouponForm
    template_name = "managements/add_coupon.html"
    success_url = reverse_lazy("managements:coupon_list")


class CouponDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Coupon
    success_url = reverse_lazy("managements:coupon_list")


@user_passes_test(superuser_required)
def activate_coupon(request, pk):
    try:
        coupon = Coupon.objects.get(id=pk)
        profiles = Profile.objects.all().order_by("id")
        for profile in profiles:
            UserCoupon.objects.create(profile=profile, coupon=coupon)
        messages.success(request, f"優惠券 {coupon.code} 已成功發放")
    except Coupon.DoesNotExist:
        messages.error(request, "優惠券不存在")
    return redirect("managements:coupon_list")


def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by("-id")

    return render(
        request,
        "managements/feedback_list.html",
        {"feedbacks": feedbacks},
    )


@user_passes_test(superuser_required)
def feedback_reply(request, pk):
    feedback = get_object_or_404(Feedback, id=pk)
    try:
        reply = feedback.reply
        form = FeedbackReplyForm(instance=reply)
    except FeedbackReply.DoesNotExist:
        reply = None
        form = FeedbackReplyForm()

    if request.method == "POST":
        if reply:
            form = FeedbackReplyForm(request.POST, instance=reply)
        else:
            form = FeedbackReplyForm(request.POST)

        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.feedback = feedback
            new_reply.reply_time = timezone.now()
            new_reply.save()
            return redirect("managements:feedback_list")

    return render(
        request, "managements/feedback_reply.html", {"form": form, "feedback": feedback}
    )


@user_passes_test(superuser_required)
def favorite_charts(request):

    favorite_counts = (
        Favorite.objects.values("product__name")
        .annotate(count=Count("product"))
        .order_by("count")
    )

    product_names = [item["product__name"] for item in favorite_counts]
    counts = [item["count"] for item in favorite_counts]

    height = max(500, 70 * len(product_names))

    bar = create_plot.Bar(
        x=counts,
        y=product_names,
        orientation="h",
    )

    layout = create_plot.Layout(
        title={"text": "收藏商品排行", "font": {"size": 24}},
        xaxis=dict(title="被收藏數量"),
        yaxis=dict(title="商品名稱", tickfont=dict(size=20)),
        height=height,
    )

    fig = create_plot.Figure(data=[bar], layout=layout)

    graph_html = html_plot.plot(fig, output_type="div")

    return render(
        request, "managements/favorite_charts.html", {"graph_html": graph_html}
    )


# 定義月份計算區間
now = datetime.now()
first_day_of_month = now.replace(day=1)
last_day_of_month = now.replace(day=calendar.monthrange(now.year, now.month)[1])


@user_passes_test(superuser_required)
def month_sell_quantity_charts(request):

    completed_orders = (
        Order.objects.filter(
            status="completed", created__range=(first_day_of_month, last_day_of_month)
        )
        .values("product__name")
        .annotate(total_quantity=Sum("relationalproduct__number"))
        .order_by("total_quantity")
    )

    product_names = [entry["product__name"] for entry in completed_orders]
    product_quantities = [entry["total_quantity"] for entry in completed_orders]

    height = max(500, 70 * len(product_names))

    bar = create_plot.Bar(
        x=product_quantities,
        y=product_names,
        orientation="h",
    )

    layout = create_plot.Layout(
        title={"text": "本月商品銷售數量排行", "font": {"size": 24}},
        xaxis=dict(title="銷售數量"),
        yaxis=dict(title="商品名稱", tickfont=dict(size=20)),
        height=height,
    )

    fig = create_plot.Figure(data=[bar], layout=layout)

    graph_html = html_plot.plot(fig, output_type="div")

    return render(
        request,
        "managements/month_sell_quantity_charts.html",
        {"graph_html": graph_html},
    )


@user_passes_test(superuser_required)
def month_sell_amount_charts(request):
    completed_orders = (
        Order.objects.filter(
            status="completed", created__range=(first_day_of_month, last_day_of_month)
        )
        .values("product__name", "product__price")
        .annotate(
            total_quantity=Sum("relationalproduct__number"),
            total_amount=Sum(F("relationalproduct__number") * F("product__price")),
        )
        .order_by("total_amount")
    )

    product_names = [entry["product__name"] for entry in completed_orders]
    product_amounts = [entry["total_amount"] for entry in completed_orders]

    height = max(500, 70 * len(product_names))

    bar = create_plot.Bar(
        x=product_amounts,
        y=product_names,
        orientation="h",
    )

    layout = create_plot.Layout(
        title={"text": "本月商品銷售額排行", "font": {"size": 24}},
        xaxis=dict(title="銷售金額"),
        yaxis=dict(title="商品名稱", tickfont=dict(size=20)),
        height=height,
    )

    fig = create_plot.Figure(data=[bar], layout=layout)

    graph_html = html_plot.plot(fig, output_type="div")

    return render(
        request,
        "managements/month_sell_amount_charts.html",
        {"graph_html": graph_html},
    )
