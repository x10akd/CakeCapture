from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from products.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from orders.models import Order

def summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    user = request.user
    return render(request, 'carts/cart_summary.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'user': user})

def add(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "not_authenticated"})
    # get the cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #lookup product into db
        product = get_object_or_404(Product,id=product_id)
        #save to session
        if product.quantity < product_qty:
            return JsonResponse({"error": "沒有庫存了，無法放到購物車內"}, status=400)
        cart.add(product=product,quantity=product_qty)
            #get cart quantity
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
        total_price = cart.cart_total()
        cart_quantity = cart.__len__()
        response = JsonResponse({"product": product_id,"total_price": total_price,"cart_quantity": cart_quantity})
        return response


def update(request):
    # get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get("action") == "post":
        # get stuff
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        total_price = cart.cart_total()

        cart.update(product = product_id,quantity = product_qty)
        response = JsonResponse({'qty':product_qty,'total_price': total_price})
        return response

@require_POST
def delete_all(request):
    if request.POST.get("action") == "delete-all":
        # 從 POST 請求中獲取要刪除的商品 ID 列表
        product_ids = request.POST.getlist("product_ids[]")
        # 在這裡執行刪除商品的邏輯，例如從購物車中刪除指定的商品
        cart = Cart(request)

        for product_id in product_ids:
            cart.delete(product=product_id)

        # 在成功刪除商品後，返回 JSON 響應
        return JsonResponse({"message": "Products deleted successfully."})


def rebuyonfail(request, order_id):
    cart = Cart(request)
    order = Order.objects.get(order_id=order_id)
    
    for item in order.orderitem_set.all():
        cart.add(item.product, item.quantity,)

    return redirect('carts:summary')  

