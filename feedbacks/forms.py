from django import forms
from .models import Feedback, FeedbackReply


class FeedbackForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "標題文字",
                "class": "focus:outline-none border-2 border-gray-300 rounded-xl p-2",
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "留言內容",
                "class": "focus:outline-none border-2 border-gray-300 rounded-xl px-2 py-5",
                "cols": 50,
                "rows": 5,
            }
        )
    )

    class Meta:
        model = Feedback
        fields = ["title", "message"]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title", "").strip()
        message = cleaned_data.get("message", "").strip()

        if not title:
            self.add_error("title", "標題不能為空白")
        if not message:
            self.add_error("message", "留言不能為空白")


class FeedbackReplyForm(forms.ModelForm):
    reply_message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "回覆訊息",
                "class": "focus:outline-none border-2 border-gray-300 rounded-xl p-5",
                "cols": 50,
                "rows": 5,
            }
        )
    )

    class Meta:
        model = FeedbackReply
        fields = ["reply_message"]
