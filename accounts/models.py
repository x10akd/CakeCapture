from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

AREA_OPTIONS = [
    ("KLU", "基隆市"),
    ("TPH", "新北市"),
    ("TPE", "臺北市"),
    ("TYC", "桃園市"),
    ("HSH", "新竹縣"),
    ("HSC", "新竹市"),
    ("MAL", "苗栗縣"),
    ("TXG", "臺中市"),
    ("CWH", "彰化縣"),
    ("NTO", "南投縣"),
    ("YLH", "雲林縣"),
    ("CHY", "嘉義縣"),
    ("CYI", "嘉義市"),
    ("TNN", "臺南市"),
    ("KHH", "高雄市"),
    ("IUH", "屏東縣"),
    ("ILN", "宜蘭縣"),
    ("HWA", "花蓮縣"),
    ("TTT", "臺東縣"),
    ("PEH", "澎湖縣"),
    ("KMN", "金門縣"),
    ("LNN", "連江縣"),
]

class NewUser(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, choices=AREA_OPTIONS, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

