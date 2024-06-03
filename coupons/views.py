from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Coupon
import json


@csrf_exempt
def check(request):
    if request.method == "POST":
        data = json.loads(request.body)
        coupon_code = data.get("coupon_code")
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            response = {
                "valid": True,
                "discount_amount": coupon.discount,
            }
        except Coupon.DoesNotExist:
            response = {
                "valid": False,
            }
        return JsonResponse(response)
