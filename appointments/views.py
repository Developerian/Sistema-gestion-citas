# appointments/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from appointments.models import Cita
from .forms import ClienteForm, Cliente
from .forms import CitaForm
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CitaForm

# === Crud de citas ===
@login_required
def editar_cita(request, id_cita):

    negocio = request.user.negocio

    cita = get_object_or_404(
        Cita,
        pk=id_cita,
        id_servicio__id_negocio=negocio
        
    )

    if request.method == "POST":

        formulario = CitaForm(
            request.POST,
            instance=cita,
            negocio=negocio
        )

        if formulario.is_valid():
            formulario.save()
            messages.success(
                request,
                "La cita se ha editado exitosamente"
            )
            return redirect("lista_citas")

    else:

        formulario = CitaForm(
            instance=cita,
            negocio=negocio
        )

    return render(
        request,
        "citas/partials/update/_formulario_cita.html",
        {
            "formulario": formulario,
            "cita": cita
        }
    )

@login_required
def crear_cita(request):
    negocio_usuario = request.user.negocio
    
    if request.method == 'POST':
        form = CitaForm(request.POST, negocio=negocio_usuario)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.save()
            messages.success(
                request,
                "La cita se creó correctamente"
            )
            return redirect('lista_citas')


    else:
        form = CitaForm(negocio=negocio_usuario)
        
    return redirect("lista_citas")

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

    buscar = request.GET.get("buscar", "").strip()
    estado = request.GET.get("estado", "")
    mostrar = int(request.GET.get("mostrar", settings.DEFAULT_PAGE_SIZE))
    orden = request.GET.get("orden", "-fecha_cita")
    page = request.GET.get("page", 1)

    queryset = (
        Cita.objects
        .filter(id_servicio__id_negocio=negocio)
        .select_related("id_cliente", "id_servicio")
    )

    if buscar:
        queryset = queryset.filter(
            Q(id_cliente__primer_nombre__icontains=buscar) |
            Q(id_cliente__primer_apellido__icontains=buscar) |
            Q(id_cliente__cedula__icontains=buscar) |
            Q(id_servicio__nombre_servicio__icontains=buscar)
        )

    # ESTE ES EL FORMULARIO QUE APARECERÁ EN EL MODAL
    formulario = CitaForm(
        negocio=negocio
    )

    context = {
        "citas": queryset,
        "buscar": buscar,
        "estado": estado,
        "mostrar": mostrar,
        "orden": orden,
        "page": page,
        "formulario": formulario,
    }

    return render(
        request,
        "citas/lista_citas.html",
        context
    )

# Dashboard
@login_required
def dashboard(request):
    return render(
        request,
        "dashboard/inicio.html"
    )



# === Crud clientes ===
@login_required
def lista_clientes(request):
    negocio = request.user.negocio

    buscar = request.GET.get("buscar", "").strip()

    clientes = Cliente.objects.filter(
        id_negocio=negocio
    )

    if buscar:
        clientes = clientes.filter(
            Q(primer_nombre__icontains=buscar) |
            Q(segundo_nombre__icontains=buscar) |
            Q(primer_apellido__icontains=buscar) |
            Q(segundo_apellido__icontains=buscar) |
            Q(cedula__icontains=buscar)
        )

    context = {
        "clientes": clientes,
        "buscar": buscar,
        "formulario": ClienteForm(),
    }

    return render(
        request,
        "citas/clientes.html",
        context
    )

@login_required
def crear_cliente(request):
    negocio = request.user.negocio

    if request.method == "POST":
        formulario = ClienteForm(request.POST)

        if formulario.is_valid():
            cliente = formulario.save(commit=False)
            cliente.id_negocio = negocio
            cliente.save()
            messages.success(request,"El cliente fue creado exitosamente")

            return redirect("clientes")

    else:
        formulario = ClienteForm()

    return render(
        request,
        "citas/partials/create/_formulario_cliente.html",
        {"formulario": formulario},
    )

@login_required
def editar_cliente(request, id_cliente):
    negocio = request.user.negocio

    cliente = get_object_or_404(
        Cliente,
        pk=id_cliente,
        id_negocio=negocio
    )

    if request.method == "POST":
        formulario = ClienteForm(
            request.POST,
            instance=cliente
        )

        if formulario.is_valid():
            formulario.save()
            return redirect("clientes")

    else:
        formulario = ClienteForm(
            instance=cliente
        )

    return render(
        request,
        "citas/partials/update/_formulario_cliente.html",
        {
            "formulario": formulario,
            "cliente": cliente,
        }
    )

@login_required
def eliminar_cliente(request, id_cliente):
    negocio = request.user.negocio

    cliente = get_object_or_404(
        Cliente,
        pk=id_cliente,
        id_negocio=negocio
    )

    cliente.delete()

    return redirect("clientes")