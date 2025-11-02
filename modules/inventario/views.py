from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from modules.producto.models import Producto
from modules.bitacora.models import Bitacora
from .models import Inventario

from drf_yasg.utils import swagger_auto_schema
from modules.auth.utils import permiso_requerido
from .serializers import InventarioCreateSerializer,InventarioListSerializer
from modules.bitacora.views import get_client_ip


@swagger_auto_schema(
    method='post',
    request_body=InventarioCreateSerializer,
    responses={201: InventarioCreateSerializer},
    operation_description="Crea un nuevo producto con sus datos básicos."
)
@api_view(['POST'])
@permiso_requerido('CREAR_INVENTARIO')
def crear_inventario(request):
    """Crea un nuevo inventario"""
    try:
        producto = Producto.objects.get(id=request.data.get('producto'), estado=True)
    except Producto.DoesNotExist:
        return Response({'mensaje': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = InventarioCreateSerializer(data=request.data)
    if serializer.is_valid():
        inventario = serializer.save()

        # Actualizar precio de venta si viene en el body
        precio_venta = request.data.get('precio_venta')
        if precio_venta:
            producto.precio = precio_venta  # actualiza campo precio de Producto
            producto.save()

        # Actualizar stock del producto (suma la cantidad ingresada)
        producto.stock += inventario.cantidad
        producto.save()
        Bitacora.objects.create(
        usuario=request.usuario,
        accion='REGISTRO_INVENTARIO',
        ip=get_client_ip(request)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
@permiso_requerido(None)
def listar_inventarios(request):
    """Lista todos los productos"""
    inventario = Inventario.objects.all().filter(estado=True)
    serializer = InventarioListSerializer(inventario, many=True)
    return Response(serializer.data)



@api_view(['DELETE'])
@permiso_requerido('ELIMINAR_INVENTARIO')
def eliminar_inventario(request, id):
    """Elimina un producto"""
    try:
        inventario = Inventario.objects.get(pk=id,estado=True)
    except Inventario.DoesNotExist:
        return Response({'error': 'Inventario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    inventario.estado=False;
    inventario.save()
    Bitacora.objects.create(
        usuario=request.usuario,
        accion='ELIMINO_INVENTARIO',
        ip=get_client_ip(request)
    )
    return Response({'message': 'Inventario eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
