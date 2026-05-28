# authentication/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Rol, Negocio, Usuario

# Registramos los modelos simples
admin.site.register(Rol)
admin.site.register(Negocio)

# Para el Usuario personalizado, usamos una configuración extendida en el panel
@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Esto define qué campos se muestran en la lista del panel
    list_display = ('username', 'email', 'id_rol', 'id_negocio', 'estado', 'is_staff')
    
    # Esto permite editar los nuevos campos desde el formulario del administrador
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Citas', {
            'fields': ('id_rol', 'id_negocio', 'celular', 'estado'),
        }),
    )