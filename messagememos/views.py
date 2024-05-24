from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import MessageModel

# Create your views here.

def create(request):
      if request.method == 'POST':
        message = request.POST.get('mytext')
        if message:
            new_message = MessageModel(
                message=message,
                user=request.user
            )
            new_message.save()
      return redirect('accounts:user')


def message(request):
    comments = MessageModel.objects.all()  # 獲取所有留言
    return render(request, 'user.html', {'comments': comments})
    








