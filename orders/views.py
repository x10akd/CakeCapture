from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order, OrderMethod, OrderItem
from products.models import Product, RelationalProduct
from .forms import OrderForm
from carts.cart import Cart
from orders import ecpay_payment_sdk
import environ
import importlib.util
from accounts.models import *
import secrets
import json
import hmac
import hashlib
import base64
import requests

spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk", "orders/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

env = environ.Env()
environ.Env.read_env()


def order_form(request):
    cart = Cart(request)
    product_stock_sufficient = True

    for product_id, quantity in cart.get_quants().items():
        product = Product.objects.get(id=product_id)
        if product.quantity < quantity or quantity == 0:
            messages.error(request, f"{product.name} 的庫存不足。")
            product_stock_sufficient = False

    if not product_stock_sufficient:
        return redirect("carts:summary")

    if request.user.is_authenticated and hasattr(request.user, "profile"):
        initial_data = {
            "order_name": request.user.profile.full_name,
            "order_cell_phone": request.user.profile.phone,
            "order_address": request.user.profile.address,
            "order_email": request.user.email,
            "user": request.user,
        }
    else:
        initial_data = {}

    if request.method == "POST":
        form = OrderForm(request.POST, initial=initial_data)
        if form.is_valid():
            order = form.save(commit=False)
            coupon_code = form.cleaned_data.get("coupon_code")
            if coupon_code:
                try:
                    user_coupon = UserCoupon.objects.get(
                        coupon__code=coupon_code, profile__user=request.user
                    )
                    order.coupon = user_coupon.coupon
                    order.discount_amount = user_coupon.coupon.discount
                except UserCoupon.DoesNotExist:
                    form.add_error("coupon_code", "Invalid coupon code")

            order.buyer = request.user
            order.save()
            return redirect("orders:order_confirm", order_id=order.id)
    else:
        form = OrderForm(initial=initial_data)

    user_coupons = UserCoupon.objects.filter(profile__user=request.user)
    return render(
        request, "orders/order_form.html", {"form": form, "user_coupons": user_coupons}
    )


def order_confirm(request):
    if request.method == "POST":
        initial_data = {"user": request.user}
        form = OrderForm(request.POST, initial=initial_data)

        if form.is_valid():
            cart = Cart(request)
            # 此處怕邏輯漏洞, 再次檢查庫存以防萬一
            product_stock_sufficient = True
            for product_id, quantity in cart.get_quants().items():
                product = Product.objects.get(id=product_id)
                if product.quantity < quantity or quantity == 0:
                    messages.error(request, "這段期間內已售出,故庫存不足。")
                    product_stock_sufficient = False
            if not product_stock_sufficient:
                return redirect("orders:order_form")

            order = Order()
            order.buyer = request.user if request.user.is_authenticated else None

            order.save()
            order.refresh_from_db()

            order.name = form.cleaned_data["recipient_name"]
            order.phone = form.cleaned_data["recipient_cell_phone"]
            order.email = form.cleaned_data["recipient_email"]
            order.address = form.cleaned_data["recipient_address"]

            used_coupon_id = form.cleaned_data["used_coupon"]
            if used_coupon_id:
                try:
                    order.used_coupon = UserCoupon.objects.get(pk=used_coupon_id)
                except UserCoupon.DoesNotExist:
                    messages.error(request, "選擇的優惠券無效。")
                    return redirect("orders:order_form")

            # 處理購物車
            totals = cart.cart_total()

            delivery_method = request.POST.get("delivery_method")
            if delivery_method == "pick_up":
                shipping_fee = 0
            else:
                shipping_fee = 70

            if (
                Coupon.objects.get(code=order.used_coupon).discount
                > totals + shipping_fee
            ):
                coupon_discount = totals + shipping_fee
            else:
                coupon_discount = Coupon.objects.get(code=order.used_coupon).discount

            totals_with_everything = totals + shipping_fee - coupon_discount
            order.total = totals_with_everything
            order.save()  # 更新金額

            for product_id, quantity in cart.get_quants().items():
                try:
                    product = Product.objects.get(id=product_id)
                    RelationalProduct.objects.create(
                        order=order, product=product, number=quantity
                    )
                    price = product.price
                    item_total = price * quantity
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        user=request.user,
                        quantity=quantity,
                        price=price,
                        item_total=item_total,
                    )
                except Product.DoesNotExist:
                    continue
            order_method = OrderMethod.objects.create(
                order=order,
                user=request.user if request.user.is_authenticated else None,
                delivery_method=request.POST.get("delivery_method"),
                payment_method=request.POST.get("payment_method"),
                store_name=request.POST.get("store_name", ""),
                store_address=request.POST.get(
                    "store_address", "10046 台北市中正區衡陽路 7 號 5 樓"
                ),
                order_name=request.POST.get("order_name"),
                order_cell_phone=request.POST.get("order_cell_phone"),
                order_address=request.POST.get("order_address", ""),
                order_email=request.POST.get("order_email"),
                recipient_name=request.POST.get("recipient_name"),
                recipient_cell_phone=request.POST.get("recipient_cell_phone"),
                recipient_address=request.POST.get("recipient_address", ""),
                recipient_email=request.POST.get("recipient_email"),
                return_agreement="return_agreement" in request.POST,
            )

            return render(
                request,
                "orders/order_confirm.html",
                {
                    "order": order,
                    "order_method": order_method,
                    "cart_products": cart.get_prods(),
                    "quantities": cart.get_quants(),
                    "totals": totals,
                    "shipping_fee": shipping_fee,
                    "totals_with_everything": totals_with_everything,
                    "coupon_discount": coupon_discount,
                },
            )
        else:
            messages.error(request, "請檢查輸入的資料。")
            return render(request, "orders/order_form.html", {"form": form})
    else:
        form = OrderForm()
        return render(request, "pages/home.html")


class ECPayView(TemplateView):
    template_name = "orders/ecpay.html"

    def post(self, request, *args, **kwargs):

        order_id = request.POST.get("order_id")
        order = Order.objects.get(order_id=order_id)

        used_coupon_id = order.used_coupon.id
        user_coupon = UserCoupon.objects.get(pk=used_coupon_id)

        user_coupon.order = order
        user_coupon.used_at = datetime.now()
        user_coupon.usage_count = user_coupon.usage_count + 1
        user_coupon.save()

        order.confirm()

        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]

        from .tasks import check_order_payment_status  # 延遲導入以避免循環導入問題

        check_order_payment_status.apply_async((order.id,), countdown=1200)

        product_list = "#".join([product.name for product in order.product.all()])
        order_params = {
            "MerchantTradeNo": order.order_id,
            "StoreID": "",
            "MerchantTradeDate": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "PaymentType": "aio",
            "TotalAmount": order.total,
            "TradeDesc": order.order_id,
            "ItemName": product_list,
            # ReturnURL為付款結果通知回傳網址，為特店server或主機的URL，用來接收綠界後端回傳的付款結果通知。
            "ReturnURL": env("DOMAIN_ORDERS_RETURN"),
            "ChoosePayment": "ALL",
            # 消費者點選此按鈕後，會將頁面導回到此設定的網址(返回商店按鈕)
            "ClientBackURL": env("DOMAIN"),
            "ItemURL": env("DOMAIN_PRODUCTS"),  # 商品銷售網址
            "Remark": "交易備註",
            "ChooseSubPayment": "",
            # 消費者付款完成後，綠界會將付款結果參數以POST方式回傳到到該網址
            "OrderResultURL": env("DOMAIN_ORDERS_RESULT"),
            "NeedExtraPaidInfo": "Y",
            "DeviceSource": "",
            "IgnorePayment": "",
            "PlatformID": "",
            "InvoiceMark": "N",
            "CustomField1": "",
            "CustomField2": "",
            "CustomField3": "",
            "CustomField4": "",
            "EncryptType": 1,
        }
        # 建立實體
        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID=env("ECPAY_MERCHANT_ID"),
            HashKey=env("ECPAY_HASH_KEY"),
            HashIV=env("ECPAY_HASH_IV"),
        )
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = (
            "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"  # 測試環境
        )
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        ecpay_form = ecpay_payment_sdk.gen_html_post_form(
            action_url, final_order_params
        )
        context = self.get_context_data(**kwargs)
        context["ecpay_form"] = ecpay_form
        return self.render_to_response(context)


class ReturnView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ReturnView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID=env("ECPAY_MERCHANT_ID"),
            HashKey=env("ECPAY_HASH_KEY"),
            HashIV=env("ECPAY_HASH_IV"),
        )
        res = request.POST.dict()
        back_check_mac_value = request.POST.get("CheckMacValue")
        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        if check_mac_value == back_check_mac_value:
            return HttpResponse("1|OK")
        return HttpResponse("0|Fail")


@csrf_exempt
def order_result(request):
    if request.method == "POST":
        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID=env("ECPAY_MERCHANT_ID"),
            HashKey=env("ECPAY_HASH_KEY"),
            HashIV=env("ECPAY_HASH_IV"),
        )
        res = request.POST.dict()
        back_check_mac_value = request.POST.get("CheckMacValue")
        order_id = request.POST.get("MerchantTradeNo")
        rtnmsg = request.POST.get("RtnMsg")
        rtncode = request.POST.get("RtnCode")
        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        order = Order.objects.get(order_id=order_id)

        if (
            check_mac_value == back_check_mac_value
            and rtnmsg == "Succeeded"
            and rtncode == "1"
        ):
            order.pay()
            return render(request, "orders/order_success.html")

        order.fail()
        return render(request, "orders/order_fail.html")
    else:
        return HttpResponse("Invalid request method", status=405)


def line_pay_request(request):

    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(order_id=order_id)

        used_coupon_id = order.used_coupon.id
        user_coupon = UserCoupon.objects.get(pk=used_coupon_id)

        user_coupon.order = order
        user_coupon.used_at = datetime.now()
        user_coupon.usage_count = user_coupon.usage_count + 1
        user_coupon.save()
        order.confirm()

        package_id = order.pk
        url = f"{env('LINE_SANDBOX_URL')}{env('LINE_REQUEST_URL')}"

        products = [
            {
                "id": "1",
                "name": "甜點",
                "quantity": 1,
                "price": order.total,
            }
        ]
        amount = sum([product["quantity"] * product["price"] for product in products])

        payload = {
            "amount": amount,
            "currency": "TWD",
            "orderId": order_id,
            "packages": [
                {
                    "id": package_id,
                    "amount": amount,
                    "products": products,
                }
            ],
            "redirectUrls": {
                "confirmUrl": f"{env("DOMAIN")}/orders/line_pay_confirm",
                "cancelUrl": f"{env("DOMAIN")}/orders/line_pay_cancel",
            },
        }

        LINE_PAY_URI = env("LINE_SIGNATURE_REQUEST_URI")
        headers = create_line_pay_headers(payload, LINE_PAY_URI)
        body = json.dumps(payload)
        response = requests.post(url, headers=headers, data=body)

        if response.status_code == 200:
            data = response.json()
            if data["returnCode"] == "0000":
                return redirect(data["info"]["paymentUrl"]["web"])
            else:
                print(data["returnMessage"])
                return render(request, "orders/line_pay_checkout.html")
        else:
            print(f"Error: {response.status_code}")
            return render(request, "orders/line_pay_checkout.html")

    else:
        return render(request, "orders/line_pay_checkout.html")


def create_line_pay_headers(body, uri):

    nonce = secrets.token_hex(16)
    LINE_PAY_CHANNEL_SECRET = env("LINE_PAY_CHANNEL_SECRET")
    body_to_json = json.dumps(body)
    message = LINE_PAY_CHANNEL_SECRET + uri + body_to_json + nonce

    binary_message = message.encode()
    binary_LINE_PAY_CHANNEL_SECRET = LINE_PAY_CHANNEL_SECRET.encode()

    hash = hmac.new(binary_LINE_PAY_CHANNEL_SECRET, binary_message, hashlib.sha256)
    signature = base64.b64encode(hash.digest()).decode()

    headers = {
        "Content-Type": "application/json",
        "X-LINE-ChannelId": env("LINE_PAY_CHANNEL_ID"),
        "X-LINE-Authorization-Nonce": nonce,
        "X-LINE-Authorization": signature,
    }

    return headers


def line_pay_confirm(request):
    transaction_id = request.GET.get("transactionId")
    order_id = request.GET.get("orderId")
    order = Order.objects.get(order_id=order_id)
    uri = f"{env('LINE_SANDBOX_URL')}/v3/payments/{transaction_id}/confirm"

    products = [
        {
            "id": "1",
            "name": "甜點",
            "quantity": 1,
            "price": order.total,
        }
    ]
    amount = sum([product["quantity"] * product["price"] for product in products])

    payload = {
        "amount": amount,
        "currency": "TWD",
    }

    signature_uri = f"/v3/payments/{transaction_id}/confirm"
    headers = create_line_pay_headers(payload, signature_uri)
    body = json.dumps(payload)
    response = requests.post(uri, headers=headers, data=body)

    data = response.json()
    if data["returnCode"] == "0000":
        return redirect("orders:line_pay_success", order_id=order_id)
    else:
        print(data["returnMessage"])
        return render(request, "orders/line_pay_fail.html")


def line_pay_cancel(request):
    return render(request, "orders/line_pay_cancel.html")


def line_pay_success(request, order_id):
    order = Order.objects.get(order_id=order_id)

    context = {
        "order": order,
    }

    return render(request, "orders/line_pay_success.html", context=context)
