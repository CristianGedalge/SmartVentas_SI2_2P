from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.producto.models import Producto
from modules.bitacora.models import Bitacora
from modules.bitacora.views import get_client_ip
from modules.auth.utils import permiso_requerido
from django.utils import timezone
from .models import Descuento
from .serializers import DescuentoCreateSerializer,DescuentoListSerializer,CatalogoDescuentoSerializer



from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='post',
    request_body=DescuentoCreateSerializer,
    responses={201: DescuentoCreateSerializer},
    operation_description="Crea un nuevo descuento"
)
@api_view(['POST'])
@permiso_requerido('CREAR_DESCUENTO')
def crear_descuento(request):
    """Crea un nuevo descuento"""
    try:
        producto = Producto.objects.get(id=request.data.get('producto'), estado=True)
    except Producto.DoesNotExist:
        return Response({'mensaje': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DescuentoCreateSerializer(data=request.data)
    if serializer.is_valid():
        descuento = serializer.save()

        Bitacora.objects.create(
            usuario=request.usuario,
            accion='REGISTRO_DESCUENTO',
            ip=get_client_ip(request)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_descuentos(request):
    """Lista todos los descuentos"""
    descuento = Descuento.objects.all().filter(estado=True)
    serializer = DescuentoListSerializer(descuento, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='patch',
    request_body=DescuentoCreateSerializer,
    responses={201: DescuentoCreateSerializer},
    operation_description="Actualizar un descuento"
)
@api_view(['PATCH'])
@permiso_requerido('ACTUALIZAR_DESCUENTO')
def actualizar_descuento(request, id):
    """Actualiza un Descuento existente"""
    try:
        descuento = Descuento.objects.get(pk=id,estado=True)
    except Descuento.DoesNotExist:
        return Response({'error': 'Descuento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DescuentoCreateSerializer(descuento, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        Bitacora.objects.create(
            usuario=request.usuario,
            accion='ACTUALIZACION_DESCUENTO',
            ip=get_client_ip(request)
        )
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permiso_requerido('ELIMINAR_DESCUENTO')
def eliminar_descuento(request, id):
    """Elimina un descuento"""
    try:
        descuento = Descuento.objects.get(pk=id,estado=True)
    except Descuento.DoesNotExist:
        return Response({'error': 'Descuento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    descuento.estado=False;
    descuento.save()
    Bitacora.objects.create(
        usuario=request.usuario,
        accion='ELIMINAR_DESCUENTO',
        ip=get_client_ip(request)
    )
    return Response({'message': 'Descuento eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
def catalogo_descuento(request):
    """Lista productos con descuento activo,stock>0 y precio>0"""
    ahora = timezone.now()

    productos = (
        Producto.objects.filter(
            estado=True,
            stock__gt=0,
            precio__gt=0,
            descuentos__estado=True,
            descuentos__fecha_inicio__lte=ahora,
            descuentos__fecha_fin__gte=ahora
        )
        .distinct()
    )

    serializer = CatalogoDescuentoSerializer(productos, many=True)
    return Response(serializer.data)
