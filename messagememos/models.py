from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class MessageModel(models.Model):
    message = models.TextField(max_length=500)
    add_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message", default=None)

    def __repr__(self):
        return 'MessageModel<message = %s,addtime = %s>' %(self.message,self.add_time)
