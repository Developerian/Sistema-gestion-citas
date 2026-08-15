from functools import wraps
from django.shortcuts import redirect


def negocio_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        usuario = request.user

        if hasattr(usuario, "propietario"):
            negocio = usuario.propietario.negocio

        elif hasattr(usuario, "empleado"):
            negocio = usuario.empleado.negocio

        else:
            return redirect("dashboard")

        request.negocio = negocio

        return view_func(request, *args, **kwargs)

    return wrapper