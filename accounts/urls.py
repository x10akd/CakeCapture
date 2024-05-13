from django.urls import path
from . import views

urlpatterns = [
    
    path('register',views.register,name="register"),
    path('login', views.sign_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('user', views.user, name='user'),
    path('user/edit', views.edit_user_info, name='edit'),

]