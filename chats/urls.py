from django.urls import path
from .views import *

app_name = "chats"

urlpatterns = [
    path("", chat_view, name="home"),
    path("line_callback", line_callback, name="line_callback"),
]
