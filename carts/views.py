from django.shortcuts import render, get_object_or_404
from .cart import Cart
from products.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def confirm(request):
    return render(request, "cart/cart_confirm.html")


def payment(request):
    return render(request, "cart/cart_payment.html")


def summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(
        request,
        "cart/cart_list.html",
        {"cart_products": cart_products, "quantities": quantities, "totals": totals},
    )


def add(request):
    # get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get("action") == "post":
        # get stuff
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        # lookup product into db
        product = get_object_or_404(Product, id=product_id)
        # save to session
        cart.add(product=product, quantity=product_qty)
        # get cart quantity
        cart_quantity = cart.__len__()
        # return response
        response = JsonResponse({"qty": cart_quantity})
        return response


def delete(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        # get stuff
        product_id = int(request.POST.get("product_id"))
        # call delete fn
        cart.delete(product=product_id)

        response = JsonResponse({"product": product_id})
        return response


def update(request):
    # get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get("action") == "post":
        # get stuff
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))

        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({"qty": product_qty})
        return response


@require_POST
def delete_all(request):
    if request.POST.get("action") == "delete-all":
        # 從 POST 請求中獲取要刪除的商品 ID 列表
        product_ids = request.POST.getlist("product_ids[]")
        # 在這裡執行刪除商品的邏輯，例如從購物車中刪除指定的商品
        cart = Cart(request)
        for product_id in product_ids:
            print(product_id)
            cart.delete(product=product_id)

        # 在成功刪除商品後，返回 JSON 響應
        return JsonResponse({"message": "Products deleted successfully."})
