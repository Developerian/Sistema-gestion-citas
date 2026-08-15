# appointments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    #Dashboard
    path("", views.dashboard, name="dashboard"),

    #Rutas citas
    path('citas/nueva/', views.crear_cita, name='crear_cita'),
    path('citas/',views.lista_citas, name = "lista_citas"),
    path("citas/<int:id_cita>/eliminar/", views.eliminar_cita, name="eliminar_cita"),
    path("citas/<int:id_cita>/editar/", views.editar_cita, name = "editar_cita"),

    #Url clientes
    path("clientes/", views.lista_clientes, name="clientes"),
    path("clientes/nuevo/", views.crear_cliente, name="crear_cliente"),
    path("clientes/<int:id_cliente>/editar/", views.editar_cliente,name="editar_cliente"),
    path("clientes/<int:id_cliente>/eliminar/", views.eliminar_cliente, name="eliminar_cliente"),

    #Urls servicios
    path("servicios/",views.lista_servicios, name="servicios"),
    path("servicios/crear/", views.crear_servicio, name="crear_servicio"),
    path("servicios/<int:id_servicio>/editar/", views.editar_servicio, name="editar_servicio"),
    path("servicios/<int:id_servicio>/eliminar/", views.eliminar_servicio,  name="eliminar_servicio"),

    # URLS empleados
    path("empleados/", views.lista_empleados, name="empleados"),
    path("empleados/nuevo/", views.crear_empleado, name="crear_empleado"),
    path("empleados/<int:id_empleado>/editar/", views.editar_empleado, name="editar_empleado"),
    path("empleados/<int:id_empleado>/eliminar/", views.eliminar_empleado, name="eliminar_empleado"),
]