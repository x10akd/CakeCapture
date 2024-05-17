from django import forms
from store.models import ProductReview, RATING


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "留下您的評論",
                "class": "focus:outline-none border-2 border-gray-300 rounded-xl p-5",
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
