import plotly.graph_objs as create_plot
import plotly.offline as html_plot
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, Category
from products.forms import CategoryForm, ProductForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from coupons.models import *
from coupons.forms import *


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
    categories = Category.objects.all()
    category_graphs = {}

    for category in categories:
        products_in_category = Product.objects.filter(category=category)
        product_names = [product.name for product in products_in_category]
        product_quantities = [product.quantity for product in products_in_category]

        # 根據商品數量動態調整圖表高度
        height = max(400, 70 * len(product_names))

        # 創建水平長條圖
        bar = create_plot.Bar(
            x=product_quantities,
            y=product_names,
            name=category.name,
            orientation="h",  # 設置為水平長條圖
        )
        layout = create_plot.Layout(
            title={"text": f"{category.name} 庫存數量", "font": {"size": 24}},
            xaxis=dict(title="數量"),
            yaxis=dict(title="商品名稱", tickfont=dict(size=20)),
            height=height,
        )
        fig = create_plot.Figure(data=[bar], layout=layout)

        # 將圖表轉換為HTML
        div = html_plot.plot(fig, auto_open=False, output_type="div")
        category_graphs[category.name] = div

    return render(
        request,
        "managements/quantity_charts.html",
        {"category_graphs": category_graphs, "categories": categories},
    )


@user_passes_test(superuser_required)
def quantity_alter(request, category):
    category = get_object_or_404(Category, name=category)
    products = Product.objects.filter(category=category).order_by("id")

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
