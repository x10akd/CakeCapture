from django.urls import path
from .views import *

app_name = "chats"

urlpatterns = [
    path("", chat_view, name="home"),
    path("callback", callback, name="callback"),
]
