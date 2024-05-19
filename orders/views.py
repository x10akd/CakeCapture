from django.shortcuts import render
from django.views.generic import FormView
from .form import OrderForm
from .models import Product, RelationalProduct
from cart.cart import Cart  


class CheckoutView(FormView):
    template_name = "orders/checkout.html" #需要修改
    form_class = OrderForm
    success_url = 'orders/confirmation.html' #需要修改

    def get(self, request, *args, **kwargs):
        cart = Cart(request)  # 導入購物車
        products = cart.get_prods()  # 抓取購物車的產品
        quantities = cart.get_quants()  # 抓取購物車的數量(dict)
        total = cart.cart_total()  # 計算總價
        # 創立字典, 用id 當作鍵, 值是產品跟數量的字典
        product_dict = {}
        for product in products:
            product_id = str(product.id)
            product_dict[product_id] = {
                "product": product,
                "count": quantities.get(product_id, 0)
            }

        context = self.get_context_data(**kwargs)
        context["product_dict"] = product_dict
        context["total"] = total
        return self.render_to_response(context)

    def form_valid(self, form):
        cart = Cart(self.request)
        self.object = form.save(commit=False)
        self.object.save()  # 先保存订单以生成 ID

        total = 0
        for product in cart.get_prods():
            quantity = cart.cart.get(str(product.id), 0)
            RelationalProduct.objects.create(
                order=self.object, product=product, number=quantity)
            total += product.price * quantity

        self.object.total = total
        self.object.save()

        context = self.get_context_data(form=form)
        context['order_id'] = self.object.order_id
        return render(self.request, self.success_url, context=context)
