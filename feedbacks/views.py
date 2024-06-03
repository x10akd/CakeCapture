from django.shortcuts import render, redirect
from .models import *


def create(request):
    if request.method == "POST":
        message = request.POST.get("user-feedback")
        if message:
            new_message = Feedback(message=message, user=request.user)
            new_message.save()
    return redirect("feedbacks:list")


def list(request):
    feedbacks = Feedback.objects.all()
    return render(request, "accounts/user.html", {"feedbacks": feedbacks})
