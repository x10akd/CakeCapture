from django import forms
from .models import Order, OrderMethod


class OrderForm(forms.ModelForm):
    order_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "border-2 border-gray-300 rounded-md p-2"}
        )
    )
    order_cell_phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "border-2 border-gray-300 rounded-md p-2"}
        )
    )
    order_address = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "border-2 border-gray-300 rounded-md p-2"}
        )
    )
    order_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "border-2 border-gray-300 rounded-md p-2"}
        )
    )
    recipient_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "border-2 border-gray-300 rounded-md p-2"}
        )
    )
    recipient_cell_phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "border-2 border-gray-300 rounded-md p-2"}
        )
    )
    recipient_address = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "border-2 border-gray-300 rounded-md p-2"}
        )
    )
    recipient_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "border-2 border-gray-300 rounded-md p-2",
                "required": "required",
            }
        )
    )

    coupon_code = forms.CharField(max_length=20, required=False, label="優惠券代碼")

    class Meta:
        model = OrderMethod
        fields = [
            "delivery_method",
            "payment_method",
            "store_name",
            "store_address",
            "order_name",
            "order_cell_phone",
            "order_address",
            "order_email",
            "recipient_name",
            "recipient_cell_phone",
            "recipient_address",
            "recipient_email",
            "return_agreement",
        ]
        widgets = {
            "delivery_method": forms.RadioSelect,
            "payment_method": forms.RadioSelect,
            "return_agreement": forms.CheckboxInput,
        }
