# authentication/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_rol


class Negocio(models.Model):
    id_negocio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo_negocio = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=20, default='ACTIVO') # Ejemplo: ACTIVO, SUSPENDIDO

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    # Heredamos id, username, first_name, last_name, email, password, is_staff, is_active, date_joined de AbstractUser
    id_usuario = models.AutoField(primary_key=True)
    
    # Relaciones de tu DER
    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)
    id_negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, null=True, blank=True)
    
    # Campos adicionales de tu DER
    celular = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=20, default='ACTIVO') # Ejemplo: ACTIVO, VACACIONES, DE BAJA Transformar a maestro
    

    def __str__(self):
        return f"{self.username} ({self.id_rol.nombre_rol if self.id_rol else 'Sin Rol'})"