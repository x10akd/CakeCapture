from django.urls import path
from . import views
from .views import NewLoginView, PasswordResetView

urlpatterns = [
    
    path('register',views.register,name="register"),
    path('login', NewLoginView.as_view(
        template_name='accounts/login.html'), name='login'),
    path('logout', views.log_out, name='logout'),
    path('password_reset', PasswordResetView.as_view(), name='password_reset'),
    path('user', views.profile, name='user'),
    path('user/edit', views.profile, name='edit'),
    path('user/update', views.profile, name='profile_update'),
]