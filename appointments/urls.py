# appointments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.clientes_view, name='clientes'),
    path('clientes/nuevo/', views.registrar_cliente, name='registrar_cliente'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
]