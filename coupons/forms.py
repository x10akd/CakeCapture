from django import forms
from .models import *


class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ["code", "discount", "min_order", "usage_limit"]
        widgets = {
            "code": forms.TextInput(
                attrs={
                    "class": "focus:outline-none border-2 border-gray-300 rounded-xl p-2",
                    "required": "True",
                }
            ),
            "discount": forms.NumberInput(
                attrs={
                    "class": "focus:outline-none border-2 border-gray-300 rounded-xl p-2",
                    "required": "True",
                    "min": "0",
                }
            ),
            "usage_limit": forms.NumberInput(
                attrs={
                    "class": "focus:outline-none border-2 border-gray-300 rounded-xl p-2",
                    "required": "True",
                    "min": "0",
                }
            ),
        }
