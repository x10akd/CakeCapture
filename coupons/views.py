from django.shortcuts import render
from django.http import JsonResponse
from .models import Coupon


def input(request):
    return render(request, "coupons/input.html")


def coupon_apply(request):
    if request.method == "GET":
        code = request.GET.get("code", "")
        try:
            coupon = Coupon.objects.get(code=code)
            return JsonResponse({"discount": coupon.discount})
        except Coupon.DoesNotExist:
            return JsonResponse({"error": "找不到該折扣代碼"})
    return JsonResponse({"error": "無效的請求"})
