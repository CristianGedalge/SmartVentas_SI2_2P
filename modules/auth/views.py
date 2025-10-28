from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from modules.bitacora.models import Bitacora
from modules.bitacora.views import get_client_ip
from .serializers import UsuarioRegistroSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import jwt 
import os
from datetime import datetime, timedelta,timezone

# Importaciones necesarias para Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, example='admin@test.com'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, example='password123'),
        }
    ),
    responses={200: 'Login exitoso', 400: 'Datos incorrectos', 401: 'No autorizado'}
)
@api_view(['POST'])
def login(request):
    
    email = request.data.get('email')
    password = request.data.get('password')
    #Verificar que se recibieron email y password
    if(not email) or (not password):
        return Response({'error': 'Email y password son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)

    if not usuario.estado:
        return Response({'error': 'Usuario inactivo,contactese con el administrador'}, status=status.HTTP_401_UNAUTHORIZED)
    

    if (not usuario.check_password(password)):
        return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)

    # Generar token 
    payload ={
        'user_id' : usuario.id,
        'rol' : usuario.rol.nombre,
        'iat':datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=10)
    }
    token = jwt.encode(payload,os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    Bitacora.objects.create(
        usuario=usuario,
        accion='INICIO_SESION',
        ip=get_client_ip(request)
    )
    return Response({
        'token':str(token),
        'usuario':{
            'id': usuario.id,
            'email': usuario.email,
            'rol': usuario.rol.nombre,
            'nombre': usuario.info.nombre,
            'apellido': usuario.info.apellido,
            'telefono': usuario.info.telefono,
            'direccion': usuario.info.direccion         
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def registrar_usuario(request):
    serializer = UsuarioRegistroSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        return Response({
            'id': usuario.id,
            'email': usuario.email,
            'rol': usuario.rol.nombre,
            'nombre': usuario.info.nombre,
            'apellido': usuario.info.apellido,
            'telefono': usuario.info.telefono,
            'direccion': usuario.info.direccion
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)