# appointments/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Importa tus modelos de clientes según los tengas nombrados (ej. Cliente)
# from .models import Cliente 

@login_required
def clientes_view(request):
    # Aquí irá tu lógica para listar o crear clientes del negocio
    negocio_actual = request.user.negocio
    
    context = {
        'usuario': request.user,
        'negocio': negocio_actual,
        'rol': request.user.rol,
        # 'clientes': Cliente.objects.filter(id_negocio=negocio_actual) # Filtrado SaaS seguro
    }
    # Asegúrate de tener este template creado o apunta al tuyo
    return render(request, 'appointments/clientes.html', context)