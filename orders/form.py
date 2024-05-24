from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ( 
            'email',
            'name',
            'phone',
            'address',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ml-7 w-1/2 rounded-xl border border-red-300 p-2', 'id': 'recipient_name', 'maxlength': '50', 'placeholder': '請輸入收件者的姓名'}),
            'address': forms.TextInput(attrs={'class': 'form-control ml-7 w-1/2 rounded-xl border border-red-300 p-2', 'id': 'recipient_address', 'maxlength': '50', 'placeholder': '請輸入收件地址'}),
            'email': forms.TextInput(attrs={'class': 'form-control ml-7 w-1/2 rounded-xl border border-red-300 p-2', 'id': 'recipient_email', 'maxlength': '50', 'placeholder': '請輸入收件者的email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control ml-7 w-1/2 rounded-xl border border-red-300 p-2', 'id': 'recipient_phone', 'maxlength': '10', 'placeholder': '請輸入收件者的聯絡電話'}),
        }