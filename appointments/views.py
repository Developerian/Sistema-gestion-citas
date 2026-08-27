# appointments/views.py
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

from appointments.decorators import negocio_required
from appointments.models import Cita, Cliente, Servicio
from .forms import *
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

# === Crud de citas ===
@negocio_required
@login_required
def editar_cita(request, id_cita):

    negocio = request.negocio

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

@negocio_required
@login_required
def crear_cita(request):
    negocio_usuario = request.negocio
    
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

@negocio_required
@login_required
def eliminar_cita(request, id_cita):
    negocio = request.negocio

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


@negocio_required
@login_required
def lista_citas(request):
    negocio = request.negocio

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
@negocio_required
@login_required
def dashboard(request):
    return render(
        request,
        "dashboard/inicio.html"
    )

# === Crud clientes ===
@negocio_required
@login_required
def lista_clientes(request):
    negocio = request.negocio

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

@negocio_required
@login_required
def crear_cliente(request):
    negocio = request.negocio

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

@negocio_required
@login_required
def editar_cliente(request, id_cliente):
    negocio = request.negocio

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

@negocio_required
@login_required
def eliminar_cliente(request, id_cliente):
    negocio = request.negocio

    cliente = get_object_or_404(
        Cliente,
        pk=id_cliente,
        id_negocio=negocio
    )

    cliente.delete()

    return redirect("clientes")

# Crud de servicios profesionales
@negocio_required
@login_required
def lista_servicios(request):
    negocio = request.negocio

    buscar = request.GET.get("buscar", "").strip()

    servicios = Servicio.objects.filter(
        id_negocio=negocio
    )

    if buscar:
        servicios = servicios.filter(
            Q(nombre_servicio__icontains=buscar) |
            Q(descripcion__icontains=buscar)
        )

    formulario = ServicioForm()

    context = {
        "servicios": servicios,
        "buscar": buscar,
        "formulario": formulario,
    }

    return render(
        request,
        "citas/servicios.html",
        context
    )

@negocio_required
@login_required
def crear_servicio(request):
    negocio = request.negocio

    if request.method == "POST":

        formulario = ServicioForm(request.POST)

        if formulario.is_valid():

            servicio = formulario.save(commit=False)
            servicio.id_negocio = negocio
            servicio.save()

            messages.success(
                request,
                "El servicio se creó correctamente."
            )

            return redirect("servicios")

    else:
        formulario = ServicioForm()

    return render(
        request,
        "citas/partials/create/_formulario_servicio.html",
        {
            "formulario": formulario
        }
    )

@negocio_required
@login_required
def editar_servicio(request, id_servicio):
    negocio = request.negocio

    servicio = get_object_or_404(
        Servicio,
        pk=id_servicio,
        id_negocio=negocio
    )

    if request.method == "POST":
        formulario = ServicioForm(
            request.POST,
            instance=servicio
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "El servicio fue editado exitosamente"
            )

            return redirect("servicios")

    else:
        formulario = ServicioForm(
            instance=servicio
        )

    return render(
        request,
        "citas/partials/update/_formulario_servicio.html",
        {
            "formulario": formulario,
            "servicio": servicio,
        }
    )

@negocio_required
@login_required
def eliminar_servicio(request, id_servicio):
    negocio = request.negocio

    servicio = get_object_or_404(
        Servicio,
        pk=id_servicio,
        id_negocio=negocio
    )

    if request.method == "POST":
        servicio.delete()

        messages.success(
            request,
            "El servicio se ha eliminado exitosamente"
        )

        return redirect("servicios")

    return render(
        request,
        "citas/eliminar_servicio.html",
        {
            "servicio": servicio,
        }
    )


# === Crud empleados ===

@permission_required(
    "appointments.add_empleado",
    raise_exception=True
    
)
@login_required
@negocio_required
def crear_empleado(request):
    negocio = request.negocio
    if request.method == "POST":
        usuario_form = UsuarioEmpleadoForm(request.POST)
        empleado_form = EmpleadoForm(
            request.POST,
            negocio=negocio
        )
        if usuario_form.is_valid() and empleado_form.is_valid():
            with transaction.atomic():
                usuario = usuario_form.save(commit=False)
                usuario.set_password(
                    usuario_form.cleaned_data["password"]
                )
                usuario.save()
                empleado = empleado_form.save(commit=False)
                empleado.usuario = usuario
                empleado.negocio = negocio
                empleado.save()
            messages.success(
                request,
                "Empleado creado correctamente."
            )
            response = HttpResponse(status=204)
            response["HX-Redirect"] = reverse("empleados")
            return response

    else:
        usuario_form = UsuarioEmpleadoForm()
        empleado_form = EmpleadoForm(
            negocio=negocio
        )
    return render(
        request,
        "empleados/partials/create/_formulario_empleado.html",
        {
            "usuario_form": usuario_form,
            "empleado_form": empleado_form,
        }
    )
    
    

@login_required
@permission_required(
    "appointments.view_empleado",
    raise_exception=True

)
@negocio_required
def lista_empleados(request):
    negocio = request.negocio
    buscar = request.GET.get("buscar", "").strip()
    empleados = Empleado.objects.filter(negocio=negocio).select_related(
        "usuario",
        "rol"
    )
    if buscar:
        empleados = empleados.filter(
            Q(usuario__first_name__icontains=buscar) |
            Q(usuario__last_name__icontains=buscar) |
            Q(usuario__username__icontains=buscar) |
            Q(rol__nombre_rol__icontains=buscar) |
            Q(celular__icontains=buscar)
        )
    formulario = EmpleadoForm(
        negocio=negocio
    )
    context = {
        "empleados": empleados,
        "buscar": buscar,
        "formulario": formulario,
    }
    return render(
        request,
        "empleados/empleados.html",
        context
    )
    
@login_required
@permission_required(
    "appointments.change_empleado",
    raise_exception=True

)
@negocio_required
def editar_empleado(request, id_empleado):

    negocio = request.negocio

    empleado = get_object_or_404(
        Empleado.objects.select_related("usuario"),
        id=id_empleado,
        negocio=negocio
    )

    usuario = empleado.usuario

    if request.method == "POST":

        usuario_form = UsuarioEmpleadoForm(
            request.POST,
            instance=usuario
        )

        empleado_form = EmpleadoForm(
            request.POST,
            instance=empleado,
            negocio=negocio
        )

        if (
            usuario_form.is_valid()
            and empleado_form.is_valid()
        ):

            with transaction.atomic():

                usuario_form.save()
                empleado_form.save()

            messages.success(
                request,
                "Empleado actualizado correctamente."
            )

            return redirect("empleados")

    else:

        usuario_form = UsuarioEmpleadoForm(
            instance=usuario
        )

        empleado_form = EmpleadoForm(
            instance=empleado,
            negocio=negocio
        )

    return render(
        request,
        "empleados/partials/update/_formulario_empleado.html",
        {
            "usuario_form": usuario_form,
            "empleado_form": empleado_form,
            "empleado": empleado,
        }
    )
    
@login_required
@permission_required(
    "appointments.delete_empleado",
    raise_exception=True

)
@negocio_required
def eliminar_empleado(request, id_empleado):
    negocio = request.negocio
    empleado = get_object_or_404(
        Empleado,
        id=id_empleado,
        negocio=negocio
    )
    if request.method == "POST":
        empleado.estado = Empleado.EstadoEmpleado.DESPEDIDO
        empleado.usuario.is_active = False
        empleado.usuario.save(
            update_fields=["is_active"]
        )
        empleado.save(
            update_fields=["estado"]
        )
        messages.success(
            request,
            "El empleado fue dado de baja."
        )
        return redirect("empleados")
    return render(
        request,
        "empleados/partials/delete/_modal_eliminar_empleado.html", {
            "empleado": empleado
        }
    )
    

