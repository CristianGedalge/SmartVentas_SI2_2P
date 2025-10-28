from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Bitacora
from .serializers import BitacoraSerializer



@api_view(['GET'])
def listar_bitacora(request):
    bitacoras = Bitacora.objects.all().order_by('-fecha_registro')
    serializer = BitacoraSerializer(bitacoras, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#Funcion para obtener la IP desde la request
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')