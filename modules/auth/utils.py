from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .custom_token  import get_usuario_desde_token_manual
from modules.auth.models import Usuario
from modules.roles.models import Permiso, RolPermiso

def permiso_requerido(nombre_permiso):
    """
    Decorador para verificar que el usuario autenticado
    tiene el permiso necesario basado en su rol.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            try:
                usuario = get_usuario_desde_token_manual(request)
            except Exception:
                return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_401_UNAUTHORIZED)
            # sI VIENE UN NONE
            if usuario is None:
                return Response({'error': 'Token ausente o inválido'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # 2️Usuario activo
            if not usuario.estado:
                return Response({'error': 'Usuario inactivo'}, status=status.HTTP_403_FORBIDDEN)

            #si no viene permiso
            if not nombre_permiso:
                request.usuario = usuario  # instancia completa de Usuario  
                return view_func(request, *args, **kwargs)

            # Verificar permiso
            try:
                permiso = Permiso.objects.get(nombre__iexact=nombre_permiso)
            except Permiso.DoesNotExist:
                return Response({'error': f'Permiso "{nombre_permiso}" no existe'}, status=status.HTTP_403_FORBIDDEN)

            # Verificar si el rol del usuario tiene ese permiso
            tiene_permiso = RolPermiso.objects.filter(rol=usuario.rol, permiso=permiso,estado=True).exists()
            if not tiene_permiso:
                 return Response({'error': f'No tienes permiso para {nombre_permiso}'}, status=status.HTTP_403_FORBIDDEN)

            # Guardar usuario en request para la vista
            request.usuario = usuario  # instancia completa de Usuario

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator



def Auth():
    """
    Decorador para verificar que el usuario autenticado
    Pase el token 
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            try:
                usuario = get_usuario_desde_token_manual(request)
            except Exception:
                return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_401_UNAUTHORIZED)
            # sI VIENE UN NONE
            if usuario is None:
                return Response({'error': 'Token ausente o inválido'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # 2️Usuario activo
            if not usuario.estado:
                return Response({'error': 'Usuario inactivo'}, status=status.HTTP_403_FORBIDDEN)

            request.usuario = usuario  # instancia completa de Usuario

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
