# appointments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.clientes_view, name='clientes'),
    path('clientes/nuevo/', views.registrar_cliente, name='registrar_cliente'),
    
]