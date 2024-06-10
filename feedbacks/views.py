from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


@login_required
def create(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect("feedbacks:list")
    else:
        form = FeedbackForm()
    return render(request, "feedbacks/create.html", {"form": form})


@login_required
def list(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by("-id")
    return render(request, "feedbacks/list.html", {"feedbacks": feedbacks})


@login_required
def reply(request, pk):
    feedback = get_object_or_404(Feedback, id=pk)
    return render(request, "feedbacks/reply.html", {"feedback": feedback})
