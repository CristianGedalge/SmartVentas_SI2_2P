from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from modules.categoria.models import Categoria
from modules.bitacora.models import Bitacora
from modules.bitacora.views import get_client_ip
from modules.auth.utils import permiso_requerido
from .serializers import ProductoSerializer, ProductoCreateSerializer

from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone


@swagger_auto_schema(
    method='post',
    request_body=ProductoCreateSerializer,
    responses={201: ProductoCreateSerializer},
    operation_description="Crea un nuevo producto con sus datos básicos."
)
@permiso_requerido('CREAR_PRODUCTO')
@api_view(['POST'])
def crear_producto(request):
    """Crea un nuevo producto"""
    try:
        categoria = Categoria.objects.get(id = request.data.get('categoria'), estado = True)
    except Categoria.DoesNotExist:
        return Response({'mensaje':  'categoria no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductoCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        Bitacora.objects.create(
            usuario=request.usuario,
            accion='REGISTRO_PRODUCTO',
            ip=get_client_ip(request)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permiso_requerido(None)
def listar_productos(request):
    """Lista todos los productos"""
    productos = Producto.objects.all().filter(estado=True)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permiso_requerido(None)
def obtener_producto(request, id):
    """Obtiene un producto por ID"""
    try:
        producto = Producto.objects.get(pk=id,estado=True)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductoSerializer(producto)
    return Response(serializer.data)






@swagger_auto_schema(
    method='patch',
    # Entrada: Usa CategoriaSerializer, aunque parcial (el decorador lo soporta)
    request_body=ProductoCreateSerializer,
    responses={
        200: ProductoCreateSerializer,
        400: 'Datos inválidos.',
        404: 'Producto no encontrada.'
    },
    operation_description="Actualiza parcialmente una producto."
)
@api_view(['PATCH'])
@permiso_requerido('ACTUALIZAR_PRODUCTO')
def actualizar_producto(request, id):
    """Actualiza un producto existente"""
    try:
        producto = Producto.objects.get(pk=id,estado=True)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductoCreateSerializer(producto, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        Bitacora.objects.create(
            usuario=request.usuario,
            accion='ACTUALIZO_PRODUCTO',
            ip=get_client_ip(request)
        )
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permiso_requerido('ELIMINAR_PRODUCTO')
def eliminar_producto(request, id):
    """Elimina un producto"""
    try:
        producto = Producto.objects.get(pk=id,estado=True)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    producto.estado=False;
    producto.save()
    Bitacora.objects.create(
        usuario=request.usuario,
        accion='ELIMINO_PRODUCTO',
        ip=get_client_ip(request)
    )
    return Response({'message': 'Producto eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def catalogo(request):
    """Lista todos los productos disponibles (sin descuento activo) stock>0 y precio>0"""
    ahora = timezone.now()

    productos = (
        Producto.objects.filter(
            estado=True,
            stock__gt=0,
            precio__gt=0
        )
        .exclude(
            descuentos__estado=True,
            descuentos__fecha_inicio__lte=ahora,
            descuentos__fecha_fin__gte=ahora
        )
        .distinct()
    )

    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)
