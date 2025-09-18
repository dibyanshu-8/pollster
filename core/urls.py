# core/urls.py

from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    # This gives the URL the name 'home' that Django is looking for
    path('', views.home, name='home'),
]