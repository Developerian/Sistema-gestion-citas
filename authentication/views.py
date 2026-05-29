# authentication/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
    context = {
        'usuario': request.user,
        'negocio': request.user.negocio,
        'rol': request.user.rol
    }
    return render(request, 'authentication/dashboard.html', context)