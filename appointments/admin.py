from django.contrib import admin
from .models import Cliente, Cita, Empleado, Servicio


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'id_cliente',
        'primer_nombre',
        'primer_apellido',
        'celular',
        'email'
    )
    search_fields = (
        'primer_nombre',
        'primer_apellido',
        'cedula',
        'celular'
    )


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        'id_servicio',
        'nombre_servicio',
        'precio',
        'duracion_minutos'
    )
    search_fields = ('nombre_servicio',)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = (
        'id_cita',
        'id_cliente',
        'id_usuario',
        'id_servicio',
        'fecha_cita',
        'hora_cita',
        'estado'
    )
    list_filter = (
        'estado',
        'fecha_cita'
    )

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'negocio',
        'rol',
        'celular',
        'estado',
    )