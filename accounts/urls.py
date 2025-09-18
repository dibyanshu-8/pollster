# accounts/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Make sure this line is uncommented
    path('register/', views.register_user, name='register'),
    
    path('login/', views.login_user, name='login'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
]