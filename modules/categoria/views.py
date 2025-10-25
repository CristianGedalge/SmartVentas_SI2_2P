from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Categoria
from .serializers import CategoriaSerializer
from modules.auth.utils import permiso_requerido
from modules.bitacora.models import Bitacora
from modules.bitacora.views import get_client_ip

@api_view(['POST'])
@permiso_requerido('CREAR_CATEGORIA')
def crear_categoria(request):
    try:
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Bitacora.objects.create(
                usuario=request.usuario,
                accion='CREO_CATEGORIA',
                ip=get_client_ip(request)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'mensaje': f'Error interno del servidor: {str(e)}',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permiso_requerido(None)
def listar_categoria(request):
    print(request.usuario.id)
    roles = Categoria.objects.filter(estado=True)
    serializer = CategoriaSerializer(roles, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permiso_requerido('ACTUALIZAR_CATEGORIA')
def actualizar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id = id, estado = True)
    except Categoria.DoesNotExist:
        return Response({'mensaje':  'Categoria no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategoriaSerializer(categoria, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        Bitacora.objects.create(
            usuario=request.usuario,
            accion='ACTUALIZO_CATEGORIA',
            ip=get_client_ip(request)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permiso_requerido('ELIMINAR_CATEGORIA')
def eliminar_categoria(request,id):
    try:
        categoria = Categoria.objects.get(id = id, estado = True)
    except Categoria.DoesNotExist:
        return Response({'mensaje':  'Categoria no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    categoria.estado = False
    categoria.save()
    return Response({'mensaje':  'Categoria eliminado'}, status=status.HTTP_200_OK)
