from django.contrib import admin
from .models import Cliente, Cita, Empleado, Propietario, Servicio


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
        'nombre_empleado',
        'apellido_empleado',
        'negocio',
        'rol',
        'celular',
        'estado',
    )
    
    @admin.display(description='Nombre', ordering='usuario__first_name')
    def nombre_empleado(self, obj):
        return obj.usuario.first_name

    @admin.display(description='Apellido', ordering='usuario__last_name')
    def apellido_empleado(self, obj):
        return obj.usuario.last_name
    
    list_select_related = ('usuario', 'negocio')
    
    @admin.register(Propietario)
    class PropietarioAdmin(admin.ModelAdmin):
        list_display = (
            'usuario',
            'get_nombre',
            'get_apellido',
            'negocio',
        )
        
        list_select_related = ('usuario', 'negocio')

        @admin.display(description='Nombre', ordering='usuario__first_name')
        def get_nombre(self, obj):
            return obj.usuario.first_name

        @admin.display(description='Apellido', ordering='usuario__last_name')
        def get_apellido(self, obj):
            return obj.usuario.last_name