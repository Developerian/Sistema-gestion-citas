from django.db import models
from django.conf import settings
from authentication.models import Negocio

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    id_negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100, blank=True)
    segundo_apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    celular = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.nombre} {self.apellido or ''}".strip()


class Cita(models.Model):
    class EstadoCita(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        EN_CURSO = 'EN_CURSO', 'En curso'
        FINALIZADA = 'FINALIZADA', 'Finalizada'
        CANCELADA = 'CANCELADA', 'Cancelada'
        REAGENDADA = 'REAGENDADA', 'Reagendada'
        NO_ASISTIO = 'NO_ASISTIO', 'Cliente no llegó'
        NO_ATENDIDA = 'NO_ATENDIDA', 'Cliente no fue atendido'

    id_cita = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='citas_asignadas')


    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='citas')
    #id_negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='citas_negocio')
    
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=20,
        choices=EstadoCita.choices,
        default=EstadoCita.PENDIENTE
    )

    def __str__(self):
        return f"Cita #{self.id_cita} - {self.id_cliente} ({self.fecha_cita} {self.hora_cita})"
    

class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_minutos = models.PositiveIntegerField(default=0, help_text="Duracion del servicio en minutos")