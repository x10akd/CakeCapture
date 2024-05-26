from django.shortcuts import render, redirect
from .models import MessageModel


def create(request):
    if request.method == "POST":
        message = request.POST.get("mytext")
        if message:
            new_message = MessageModel(message=message, user=request.user)
            new_message.save()
    return redirect("accounts:user")


def message(request):
    comments = MessageModel.objects.all()
    return render(request, "user.html", {"comments": comments})
