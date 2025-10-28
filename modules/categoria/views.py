from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Categoria
from .serializers import CategoriaSerializer
from modules.auth.utils import permiso_requerido
from modules.bitacora.models import Bitacora
from modules.bitacora.views import get_client_ip

# Importaciones necesarias para Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    request_body=CategoriaSerializer,
    responses={
        201: CategoriaSerializer,
        400: 'Datos inválidos.'
    },
    operation_description="Crea una nueva categoría."
)
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
    
@swagger_auto_schema(
    method='get',
    responses={
        200: CategoriaSerializer(many=True),
        401: 'Token requerido'
    },
    operation_description="Lista todas las categorías activas.",
    security=[{'Bearer': []}]  
)
@api_view(['GET'])
@permiso_requerido(None)
def listar_categoria(request):
    categoria = Categoria.objects.filter(estado=True)
    serializer = CategoriaSerializer(categoria, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='patch',
    # Entrada: Usa CategoriaSerializer, aunque parcial (el decorador lo soporta)
    request_body=CategoriaSerializer,
    # Parámetro de Ruta: Documenta el 'id'
    manual_parameters=[
        openapi.Parameter(
            'id', 
            openapi.IN_PATH, 
            description="ID de la categoría a actualizar", 
            type=openapi.TYPE_INTEGER
        ),
    ],
    responses={
        200: CategoriaSerializer,
        400: 'Datos inválidos.',
        404: 'Categoría no encontrada.'
    },
    operation_description="Actualiza parcialmente una categoría."
)
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









# @swagger_auto_schema(
#     method='delete',
#     manual_parameters=[
#         openapi.Parameter(
#             'id', 
#             openapi.IN_PATH, 
#             description="ID de la categoría a eliminar", 
#             type=openapi.TYPE_INTEGER
#         ),
#     ],
#     responses={
#         200: 'Categoría eliminada (estado=False).',
#         404: 'Categoría no encontrada.'
#     },
#     operation_description="Elimina lógicamente una categoría (estado=False)."
# )
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
