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
        VACACIONES = 'VACACIONES', 'En Vacaciones'
        PERMISO = 'PERMISO', 'Permiso Médico / Licencia'
        SUSPENDIDO = 'SUSPENDIDO', 'Suspendido Temporalmente'
        DESPEDIDO = 'DESPEDIDO', 'Despedido / Fuera de la Empresa'

    id_usuario = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, null=True, blank=True) 
    celular = models.CharField(max_length=20, blank=True, null=True)

    estado = models.CharField(
        choices= EstadoUsuario.choices,
        default= EstadoUsuario.ACTIVO
    )

    def __str__(self):
        return self.username