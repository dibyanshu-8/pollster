# accounts/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    
    path('register/', views.register_user, name='register'),
    
    path('login/', views.jwt_login_page, name='login'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('login/', views.login_page, name='login'),
]