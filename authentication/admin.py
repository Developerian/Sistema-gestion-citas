# authentication/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Rol, Negocio, Usuario

# Registramos los modelos simples

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'estado',
        'is_staff',
        'is_active',
    )


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = (
        'id_rol',
        'nombre_rol',
        'descripcion',
    )
    
@admin.register(Negocio)
class NegocioAdmin(admin.ModelAdmin):
    list_display = (
        'id_negocio',
        'nombre',
        'ruc',
        'tipo_negocio',
        'estado',
    )