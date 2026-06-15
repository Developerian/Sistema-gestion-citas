# appointments/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, Cliente
# Importa los modelos de clientes según se tenga nombrados (ej. Cliente)
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
   
    return render(request, 'appointments/clientes.html', context)

def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nuevo_cliente = form.save(commit=False)
            # Asignar el negocio del usuario logueado
            nuevo_cliente.id_negocio = request.user.id_negocio 
            nuevo_cliente.save()
            return redirect('lista_clientes') # O a la vista de agendar cita
    else:
        form = ClienteForm()
    return render(request, 'appointments/registrar_cliente.html', {'form': form})

def lista_clientes(request):
    # Filtra por el negocio del usuario logueado para mayor seguridad
    clientes = Cliente.objects.filter(id_negocio=request.user.id_negocio)
    return render(request, 'appointments/lista_clientes.html', {'clientes': clientes})