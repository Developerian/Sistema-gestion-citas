# authentication/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from appointments.forms import CitaForm
from appointments.models import Cita
from django.utils.timezone import now

@login_required
def redirect_by_role(request):
    """
    Esta vista actúa como un semáforo tras el login exitoso.
    """
    # Si eres tú (Superusuario o Staff), vas al panel de Django
    if request.user.is_superuser or request.user.is_staff:
        return redirect('/admin/')
    
    # Si es un cliente/empleado final, va a su Dashboard personalizado
    return redirect('dashboard')


@login_required
def dashboard_view(request):
    """
    El panel de control privado para el dueño o empleado del negocio.
    """
    # Gracias a tu excelente diseño de BD, podemos aislar el negocio del usuario logueado:
    usuario = request.user
    negocio = usuario.negocio # Asegúrate de que así se llama tu relación
    rol = usuario.rol

    if request.method == 'POST':
        # Si el usuario hace clic en "Confirmar Reserva", pasamos el POST y el negocio
        form = CitaForm(request.POST, negocio=negocio)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.id_negocio = negocio # Blindaje: forzamos que la cita pertenezca a este negocio
            cita.save()
            return redirect('dashboard') # Recargamos la página para limpiar el form
    else:
        # GET: Si solo está entrando a la página, creamos el formulario vacío filtrado
        form = CitaForm(negocio=negocio)

    # 3. Consultamos las citas de HOY para este negocio específico
    citas_hoy = Cita.objects.filter(id_usuario__negocio=negocio, fecha_cita=now().date())
    # 4. EL PASO CRÍTICO: Empaquetar todo en el contexto
    context = {
        'form': form,           # <- SI ESTO FALTA, EL HTML SE VE VACÍO
        'citas': citas_hoy,
        'negocio': negocio,
        'usuario': usuario,
        'rol': rol,
    }
    
    return render(request, 'authentication/dashboard.html', context)