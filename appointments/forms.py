from django import forms
from .models import Cita
from authentication.models import Usuario

class CitaForm(forms.ModelForm):
    
    class Meta:
        model = Cita
        # Campos que la recepcionista va a llenar en la pantalla
        fields = ['id_cliente', 'id_usuario', 'fecha_cita', 'hora_cita', 'observaciones', 'estado']
        
        labels = {
            'id_cliente': 'Seleccionar Cliente',
            'id_usuario': 'Asignar a Empleado / Especialista',
            'fecha_cita': 'Fecha de la Cita',
            'hora_cita': 'Hora de la Cita',
            'observaciones': 'Observaciones',
            'estado': 'Estado Inicial',
        }

        widgets = {
            # Forzamos los selectores nativos de fecha y hora del navegador
            'fecha_cita': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'hora_cita': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Notas o requerimientos especiales...'}),
            'id_cliente': forms.Select(attrs={'class': 'form-input'}),
            'id_usuario': forms.Select(attrs={'class': 'form-input'}),
            'estado': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        # Este truco es clave para el SaaS: pasamos el negocio actual al formulario
        negocio = kwargs.pop('negocio', None)
        super().__init__(*args, **kwargs)
        
        if negocio:
            # Filtramos los ComboBox de Clientes y Empleados para que SOLO salgan los de este negocio
            self.fields['id_cliente'].queryset = self.fields['id_cliente'].queryset.filter(id_negocio=negocio)
            self.fields['id_usuario'].queryset = Usuario.objects.filter(negocio=negocio)