from django import forms
from products.models import ProductReview, Category, Product, RATING


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "留下您的評論",
                "class":"resize-none h-20 sm:h-40 w-full px-3 py-2 border rounded-md",
                "cols": 80,
                "rows": 5,
            }
        )
    )
    rating = forms.ChoiceField(
        choices=RATING,
        widget=forms.Select(
            attrs={
                "class": "border-2 border-gray-300 rounded-xl p-2 focus:outline-none"
            }
        ),
    )

    class Meta:
        model = ProductReview
        fields = ["review", "rating"]

    def __init__(self, *args, **kwargs):
        super(ProductReviewForm, self).__init__(*args, **kwargs)
        # 將初始的rating值設置為5
        self.initial["rating"] = 5

    def clean_review(self):
        review = self.cleaned_data["review"]
        if review.strip() == "":
            raise forms.ValidationError("評論內容不能為空白")
        return review


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class ProductForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "focus:outline-none border-2 border-gray-300 rounded-xl p-5",
                "cols": 50,
                "rows": 5,
            }
        )
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "category",
            "quantity",
            "description",
            "image",
            "status",
        ]
