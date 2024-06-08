
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('16th-CakeCapture')

# 使用 Django 的設定文件來配置 Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自動發現 Django 項目中的任務模組
app.autodiscover_tasks()




