from django import forms
from .models import Order, OrderMethod
from accounts.models import UserCoupon


class OrderForm(forms.ModelForm):

    used_coupon = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        user = kwargs["initial"]["user"]

        super(OrderForm, self).__init__(*args, **kwargs)

        if user:
            user_coupons = UserCoupon.objects.filter(profile_id=user.id)
            COUPON_CHOICES = [
                (
                    user_coupon.id,
                    f"{user_coupon.coupon.code} - 折價 {user_coupon.coupon.discount} 元",
                )
                for user_coupon in user_coupons
            ]
        else:
            COUPON_CHOICES = []
        self.fields["used_coupon"].choices = COUPON_CHOICES

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

    # coupon_code = forms.CharField(max_length=20, required=False, label="優惠券代碼")

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
