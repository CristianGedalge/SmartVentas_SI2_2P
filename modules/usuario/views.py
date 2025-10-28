from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.auth.utils import permiso_requerido
from .serializers import UsuarioInfoListSerializer,UsuarioActualizarSerializer
from .models import UsuarioInfo
from modules.auth.models import Usuario
from modules.roles.models import Rol

# Create your views here.


@api_view(['GET'])
def listar_usuarios(request):
    """
    Lista todos los usuarios con su información personal y rol.
    """
    usuarios_info = UsuarioInfo.objects.select_related('usuario__rol').filter(usuario__estado=True)

    serializer = UsuarioInfoListSerializer(usuarios_info, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK) 


@api_view(['GET'])
@permiso_requerido(None)
def obtener_perfil(request):
    userId=request.usuario.id
    usuarios_info = UsuarioInfo.objects.select_related('usuario__rol').get(usuario__id=userId)

    serializer = UsuarioInfoListSerializer(usuarios_info)
    return Response(serializer.data, status=status.HTTP_200_OK) 


@api_view(['PATCH'])
def actualizar_usuario(request, id):
    """
    Actualiza los datos de UsuarioInfo (excepto url_img)
    y permite cambiar el rol del usuario asociado.
    """
    try:
        usuario_info = UsuarioInfo.objects.select_related('usuario').get(pk=id)
    except UsuarioInfo.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # --- Validación con serializer ---
    serializer = UsuarioActualizarSerializer(data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    # --- Actualizar campos de UsuarioInfo ---
    campos_permitidos = ['nombre', 'apellido', 'telefono', 'direccion',"url_img"]
    for campo in campos_permitidos:
        if campo in data:
            setattr(usuario_info, campo, data[campo])

    # --- Actualizar rol del Usuario ---
    if 'rol' in data:
        try:
            nuevo_rol = Rol.objects.get(pk=data['rol'])
            usuario_info.usuario.rol = nuevo_rol
            usuario_info.usuario.save()
        except Rol.DoesNotExist:
            return Response({'error': 'Rol no válido'}, status=status.HTTP_400_BAD_REQUEST)

    usuario_info.save()

    return Response({'mensaje': 'Usuario actualizado correctamente'}, status=status.HTTP_200_OK)




@api_view(['DELETE'])
def eliminar_usuario(request, id):
    """
    Cambia el estado del usuario a False (borrado lógico).
    """
    try:
        usuario = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if not usuario.estado:
        return Response({'mensaje': 'El usuario ya estaba inactivo'}, status=status.HTTP_400_BAD_REQUEST)

    usuario.estado = False
    usuario.save()
    return Response({'mensaje': f'Usuario {usuario.email} desactivado correctamente'}, status=status.HTTP_200_OK)