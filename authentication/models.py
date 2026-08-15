# authentication/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Negocio(models.Model):
    class EstadoNegocio(models.TextChoices):
        PRUEBA = 'PRUEBA', 'Prueba'
        ACTIVO = 'ACTIVO', 'Activo'
        PENDIENTE_PAGO = 'PENDIENTE_PAGO', 'Pendiente de pago'
        SUSPENDIDO = 'SUSPENDIDO', 'Falta de pago / infraccion'
        INACTIVO = 'INACTIVO', 'Inactivo / dado de baja'

    id_negocio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo_negocio = models.CharField(max_length=50, blank=True, null=True)

    estado = models.CharField(
        choices= EstadoNegocio.choices,
        default= EstadoNegocio.PRUEBA
    )
    
    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    class EstadoUsuario(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo / Trabajando'
        INACTIVO = 'INACTIVO', 'Inactivo'
        PRUEBA = 'PRUEBA', 'Periodo de prueba'
    estado = models.CharField(
        choices= EstadoUsuario.choices,
        default= EstadoUsuario.ACTIVO
    )
    @property
    def tipo_usuario(self):
        if hasattr(self, "propietario"):
            return "propietario"

        if hasattr(self, "empleado"):
            return "empleado"
        return None
    @property
    def nombre_rol(self):
        if hasattr(self, "propietario"):
            return "Propietario"

        if hasattr(self, "empleado"):
            return self.empleado.rol.nombre_rol
        return None

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    negocio = models.ForeignKey(
        Negocio,
        on_delete=models.CASCADE,
        related_name="roles"
    )
    nombre_rol = models.CharField(
        max_length=50
    )
    descripcion = models.CharField(
        max_length=200,
        blank=True
    )
    
    def __str__(self):
        return self.nombre_rol