from django.shortcuts import render
from django.views.generic import FormView,TemplateView
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


class ECPayView(TemplateView):
    template_name = "orders/ecpay.html"

    def post(self, request, *args, **kwargs):
        scheme = request.is_secure() and "https" or "http"
        domain = request.META['HTTP_HOST']

        order_id = request.POST.get("order_id")
        order = Order.objects.get(order_id=order_id)
        product_list = "#".join(
            [product.name for product in order.product.all()])
        order_params = {
            'MerchantTradeNo': order.order_id,
            'StoreID': '',
            'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            'PaymentType': 'aio',
            'TotalAmount': order.total,
            'TradeDesc': order.order_id,
            'ItemName': product_list,
            # ReturnURL為付款結果通知回傳網址，為特店server或主機的URL，用來接收綠界後端回傳的付款結果通知。
            'ReturnURL': f'{scheme}://{domain}/orders/return/',
            'ChoosePayment': 'ALL',
            # 消費者點選此按鈕後，會將頁面導回到此設定的網址(返回商店按鈕)
            'ClientBackURL': f'{scheme}://{domain}/products/list/',
            'ItemURL': f'{scheme}://{domain}/products/list/',  # 商品銷售網址
            'Remark': '交易備註',
            'ChooseSubPayment': '',
            # 消費者付款完成後，綠界會將付款結果參數以POST方式回傳到到該網址
            'OrderResultURL': f'{scheme}://{domain}/orders/orderresult/',
            'NeedExtraPaidInfo': 'Y',
            'DeviceSource': '',
            'IgnorePayment': '',
            'PlatformID': '',
            'InvoiceMark': 'N',
            'CustomField1': '',
            'CustomField2': '',
            'CustomField3': '',
            'CustomField4': '',
            'EncryptType': 1,
        }
        # 建立實體
        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID='3002607',
            HashKey='pwFHCqoQZGmho4w6',
            HashIV='EkRm7iFT261dpevs'
        )
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        ecpay_form = ecpay_payment_sdk.gen_html_post_form(
            action_url, final_order_params)
        context = self.get_context_data(**kwargs)
        context['ecpay_form'] = ecpay_form
        return self.render_to_response(context)
