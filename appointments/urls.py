# appointments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('citas/nueva/', views.crear_cita, name='crear_cita'),
    path('clientes/', views.clientes_view, name='clientes'),
    path('citas/',views.lista_citas, name = "lista_citas"),
    path("", views.dashboard, name="dashboard"),
    path("citas/<int:id_cita>/eliminar/", views.eliminar_cita, name="eliminar_cita"),
]