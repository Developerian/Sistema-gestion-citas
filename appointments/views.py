# appointments/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from appointments.models import Cita
from .forms import ClienteForm, Cliente
from .forms import CitaForm
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CitaForm



@login_required
def crear_cita(request):
    negocio_usuario = request.user.negocio
    
    if request.method == 'POST':
        form = CitaForm(request.POST, negocio=negocio_usuario)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.save()
            return redirect('lista_citas')
    else:
        form = CitaForm(negocio=negocio_usuario)
        
    return render(request, 'citas/crear_cita.html', {'form': form})

@login_required
def eliminar_cita(request, id_cita):
    negocio = request.user.negocio
    cita = get_object_or_404(
        Cita, 
        id_cita = id_cita, 
        id_servicio__id_negocio = negocio
        )
    
    if request.method == "POST":
        cita.delete()
        messages.success(request, "La cita se ha eliminado exitosamente")
        return redirect("lista_citas")
    
    return render(
        request,
        "citas/eliminar_cita.html",{
            "cita" : cita
        }
    )



@login_required
def lista_citas(request):
    negocio = request.user.negocio
    citas = Cita.objects.filter(
        id_servicio__id_negocio=negocio
    )
    context = {
        "citas": citas
    }
    return render(
        request,
        "citas/lista_citas.html",
        context
    )

@login_required
def dashboard(request):
    return render(
        request,
        "dashboard/inicio.html"
    )

@login_required
def clientes_view(request):
    negocio_usuario = request.user.negocio
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.id_negocio = negocio_usuario
            cliente.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
        
    clientes_registrados = Cliente.objects.filter(id_negocio=negocio_usuario)
    
    context = {
        'form': form,
        'clientes': clientes_registrados
    }
    
    return render(request, 'citas/clientes.html', context)