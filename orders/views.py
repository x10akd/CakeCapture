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
from .line_pay import *
import environ
import importlib.util

spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk", "orders/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

env = environ.Env()
environ.Env.read_env()


def order_form(request):
    if request.user.is_authenticated and hasattr(request.user, "profile"):
        initial_data = {
            "order_name": request.user.profile.full_name,
            "order_cell_phone": request.user.profile.phone,
            "order_address": request.user.profile.address,
            "order_email": request.user.email,
        }
    else:
        initial_data = {}

    form = OrderForm(initial=initial_data)
    return render(request, "orders/order_form.html", {"form": form})


def order_confirm(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = Cart(request)
            product_stock_sufficient = True

            for product_id, quantity in cart.get_quants().items():
                product = Product.objects.get(id=product_id)
                if product.quantity < quantity:
                    messages.error(request, f"{product.name} 庫存不足。")
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
            # 處理購物車
            cart = Cart(request)
            totals = cart.cart_total()
            shipping_fee = 70
            totals_with_shipping = totals + shipping_fee
            order.total = totals_with_shipping
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
                coupon_used="coupon" in request.POST,
                store_name=request.POST.get("store_name", ""),
                store_address=request.POST.get("store_address", ""),
                order_name=request.POST.get("order_name"),
                order_cell_phone=request.POST.get("order_cell_phone"),
                order_address=request.POST.get("order_address", ""),
                order_email=request.POST.get("order_email"),
                recipient_name=request.POST.get("recipient_name"),
                recipient_cell_phone=request.POST.get("recipient_cell_phone"),
                recipient_address=request.POST.get("recipient_address", ""),
                recipient_email=request.POST.get("recipient_email"),
                invoice_option=request.POST.get("invoice_option"),
                invoice_number=request.POST.get("invoice_number", ""),
                return_agreement="return_agreement" in request.POST,
            )

            # 清空購物車 需再確認
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            return render(
                request,
                "orders/order_confirm.html",
                {
                    "order": order,
                    "order_method": order_method,
                    "cart_products": cart.get_prods(),
                    "quantities": cart.get_quants(),
                    "totals": totals,
                },
            )
        else:
            messages.error(request, "請檢查輸入的資料。")
            return render(request, "orders/order_form.html", {"form": form})
    else:
        form = OrderForm()
        return render(request, "home.html")


class ECPayView(TemplateView):
    template_name = "orders/ecpay.html"

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id")
        order = Order.objects.get(order_id=order_id)
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
        if check_mac_value == back_check_mac_value and rtnmsg == 'Succeeded' and rtncode == '1':
            order = Order.objects.get(order_id=order_id)
            order.status = "waiting_for_shipment"
            order.save()
            return render(request, 'orders/order_success.html',{"order":order})
        return render(request, 'orders/order_fail.html', {"rtncode": rtncode, "order_id": order_id})
    else:
        return HttpResponse("Invalid request method", status=405)


def create_line_pay_payment(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        order_id = request.POST["order_id"]
        payment_response = request_line_pay(amount, order_id)
        if payment_response["returnCode"] == "0000":
            return redirect(payment_response["info"]["paymentUrl"]["web"])
        else:
            print(payment_response)
            return HttpResponse("Payment request failed", status=400)
    return render(request, "create_payment.html")


def confirm_line_pay_payment(request):
    transaction_id = request.GET.get("transactionId")
    order_id = request.GET.get("orderId")

    if transaction_id and order_id:
        # 在這裡你可以處理支付成功的邏輯，例如更新訂單狀態
        try:
            order = Order.objects.get(id=order_id)
            order.status = "Paid"
            order.transaction_id = transaction_id
            order.save()
            return render(request, "payment_success.html", {"order": order})
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)
    else:
        return HttpResponse("Invalid parameters", status=400)


def cancel_line_pay_payment(request):
    order_id = request.GET.get("orderId")

    if order_id:
        # 在這裡你可以處理支付取消的邏輯，例如更新訂單狀態
        try:
            order = Order.objects.get(id=order_id)
            order.status = "Cancelled"
            order.save()
            return render(request, "payment_cancelled.html", {"order": order})
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)
    else:
        return HttpResponse("Invalid parameters", status=400)
