from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Marca
from .serializers import MarcaSerializer
from modules.auth.utils import permiso_requerido
from modules.bitacora.models import Bitacora
from modules.bitacora.views import get_client_ip

# Importaciones necesarias para Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    request_body=MarcaSerializer,
    responses={
        201: MarcaSerializer,
        400: 'Datos inválidos.'
    },
    operation_description="Crea una nueva marca."
)
@api_view(['POST'])
@permiso_requerido('CREAR_MARCA')
def crear_marca(request):
    try:
        serializer = MarcaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Bitacora.objects.create(
                usuario=request.usuario,
                accion='CREO_MARCA',
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
        200: MarcaSerializer(many=True),
        401: 'Token requerido'
    },
    operation_description="Lista todas las marcas activas.",
    security=[{'Bearer': []}]  
)
@api_view(['GET'])
@permiso_requerido(None)
def listar_marca(request):
    marca = Marca.objects.filter(estado=True)
    serializer = MarcaSerializer(marca, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='patch',
    # Entrada: Usa MarcaSerializer, aunque parcial (el decorador lo soporta)
    request_body=MarcaSerializer,
    # Parámetro de Ruta: Documenta el 'id'
    manual_parameters=[
        openapi.Parameter(
            'id', 
            openapi.IN_PATH, 
            description="ID de la marca a actualizar", 
            type=openapi.TYPE_INTEGER
        ),
    ],
    responses={
        200: MarcaSerializer,
        400: 'Datos inválidos.',
        404: 'marca no encontrada.'
    },
    operation_description="Actualiza parcialmente una marca."
)
@api_view(['PATCH'])
@permiso_requerido('ACTUALIZAR_MARCA')
def actualizar_marca(request, id):
    try:
        marca = Marca.objects.get(id = id, estado = True)
    except Marca.DoesNotExist:
        return Response({'mensaje':  'Marca no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MarcaSerializer(marca, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        Bitacora.objects.create(
            usuario=request.usuario,
            accion='ACTUALIZO_MARCA',
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
#             description="ID de la marca a eliminar", 
#             type=openapi.TYPE_INTEGER
#         ),
#     ],
#     responses={
#         200: 'marca eliminada (estado=False).',
#         404: 'Marca no encontrada.'
#     },
#     operation_description="Elimina lógicamente una categoría (estado=False)."
# )
@api_view(['DELETE'])
@permiso_requerido('ELIMINAR_CATEGORIA')
def eliminar_marca(request,id):
    try:
        marca = Marca.objects.get(id = id, estado = True)
    except Marca.DoesNotExist:
        return Response({'mensaje':  'Marca no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    marca.estado = False
    marca.save()
    return Response({'mensaje':  'Marca eliminado'}, status=status.HTTP_200_OK)
