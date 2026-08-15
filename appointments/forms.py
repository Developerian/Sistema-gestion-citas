#forms.py

from django import forms
from .models import Cita, Cliente, Empleado, Servicio
from authentication.models import Rol, Usuario

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        # Campos que la recepcionista va a llenar en la pantalla
        fields = ['id_cliente', 'id_servicio','id_usuario', 'fecha_cita', 'hora_cita', 'observaciones', 'estado']
        
        labels = {
            'id_cliente': 'Seleccionar Cliente',
            'id_servicio': 'Servicio profesional',
            'id_usuario': 'Asignar a Empleado / Especialista',
            'fecha_cita': 'Fecha de la Cita',
            'hora_cita': 'Hora de la Cita',
            'observaciones': 'Observaciones',
        }

        widgets = {
            # Forzamos los selectores nativos de fecha y hora del navegador
            'fecha_cita': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            "id_servicio": forms.Select(attrs={"class": "form-input"}),
            'hora_cita': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Notas o requerimientos especiales...'}),
            'id_cliente': forms.Select(attrs={'class': 'form-input'}),
            'id_usuario': forms.Select(attrs={'class': 'form-input'}),
            'estado': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        # Recibimos el objeto negocio directamente
        negocio = kwargs.pop('negocio', None)
        super().__init__(*args, **kwargs)
        
        if negocio:
            # 1. Filtramos servicios que pertenecen al negocio

            self.fields["id_servicio"].queryset = Servicio.objects.filter(id_negocio=negocio)
            
            # 2. Filtramos clientes que pertenecen al negocio
            self.fields['id_cliente'].queryset = Cliente.objects.filter(id_negocio=negocio)
            
            # Empleados del negocio
            self.fields["id_usuario"].queryset = Usuario.objects.filter(
                empleado__negocio=negocio
            )
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'cedula',
            'email',
            'celular',
        ]

        labels = {
            "primer_nombre": "Primer nombre",
            "segundo_nombre": "Segundo nombre",
            "primer_apellido": "Primer apellido",
            "segundo_apellido": "Segundo apellido",
            "cedula": "Cédula",
            "email": "Correo electrónico",
            "celular": "Celular",
        }

        widgets = {
            "primer_nombre": forms.TextInput(attrs={"class": "form-input"}),
            "segundo_nombre": forms.TextInput(attrs={"class": "form-input"}),
            "primer_apellido": forms.TextInput(attrs={"class": "form-input"}),
            "segundo_apellido": forms.TextInput(attrs={"class": "form-input"}),
            "cedula": forms.TextInput(attrs={"class": "form-input"}),
            "email": forms.EmailInput(attrs={"class": "form-input"}),
            "celular": forms.TextInput(attrs={"class": "form-input"}),
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            'nombre_servicio',
            'descripcion',
            'precio',
            'duracion_minutos',
        ]

        labels = {
            'nombre_servicio': 'Nombre del servicio',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'duracion_minutos': 'Duración en minutos',
        }

        widgets = {
            'nombre_servicio': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Ej. Corte de cabello',
                }
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Descripción del servicio',
                }
            ),
            'precio': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                    'step': '0.01',
                    'min': '0',
                }
            ),
            'duracion_minutos': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                    'min': '0',
                }
            ),
        }
        
class UsuarioEmpleadoForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )
    class Meta:
        model = Usuario
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]
        
class EmpleadoForm(forms.ModelForm):

    class Meta:
        model = Empleado
        fields = [
            "rol",
            "celular",
            "estado",
        ]

    def __init__(self, *args, **kwargs):
        negocio = kwargs.pop("negocio", None)

        super().__init__(*args, **kwargs)

        if negocio:
            self.fields["rol"].queryset = Rol.objects.filter(
                negocio=negocio
            )