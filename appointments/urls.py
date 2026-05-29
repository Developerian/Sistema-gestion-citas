# appointments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.clientes_view, name='clientes'),
]