from django.urls import path
from . import views
from .views import NewLoginView

urlpatterns = [
    
    path('register',views.register,name="register"),
    path('login', NewLoginView.as_view(
        template_name='accounts/login.html'), name='login'),
    path('logout', views.log_out, name='logout'),
    path('user', views.profile, name='user'),
    path('user/edit', views.profile, name='edit'),

]