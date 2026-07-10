# appointments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('citas/nueva/', views.crear_cita, name='crear_cita'),
    path('clientes/', views.clientes_view, name='clientes'),
]