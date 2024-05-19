from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="avatars", null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=10, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    old_cart = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return self.user.username

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static("images/avatar.svg")
        return avatar
