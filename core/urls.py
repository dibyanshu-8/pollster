from django.urls import path
from .views import home, DashboardView

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
