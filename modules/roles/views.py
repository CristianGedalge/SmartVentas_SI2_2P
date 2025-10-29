from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Rol, Permiso, RolPermiso
from .serializers import RolSerializer 
from modules.bitacora.models import Bitacora
from modules.bitacora.views import get_client_ip

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    request_body=RolSerializer,
    responses={
        201: RolSerializer,
        400: 'Datos inválidos.'
    },
    operation_description="Crea una nuevo Rol."
)
@api_view(['POST'])

def crear_rol(request):
    try:
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Bitacora.objects.create(
                usuario=request.usuario,
                accion='CREO_ROL',
                ip=get_client_ip(request)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'mensaje': f'Error interno del servidor: {str(e)}',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def listar_roles(request):
    roles = Rol.objects.filter(estado=True)
    serializer = RolSerializer(roles, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='patch',
    # Entrada: Usa MarcaSerializer, aunque parcial (el decorador lo soporta)
    request_body=RolSerializer,
    # Parámetro de Ruta: Documenta el 'id'
    manual_parameters=[
        openapi.Parameter(
            'id', 
            openapi.IN_PATH, 
            description="ID del rol a actualizar", 
            type=openapi.TYPE_INTEGER
        ),
    ],
    responses={
        200: RolSerializer,
        400: 'Datos inválidos.',
        404: 'marca no encontrada.'
    },
    operation_description="Actualiza parcialmente un rol."
)
@api_view(['PATCH'])
def actualizar_rol(request, id):
    try:
        rol = Rol.objects.get(id = id, estado = True)
    except Rol.DoesNotExist:
        return Response({'mensaje': 'Rol no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RolSerializer(rol, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        Bitacora.objects.create(
            usuario=request.usuario,
            accion='ACTUALIZO_ROL',
            ip=get_client_ip(request)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_rol(request,id):
    try:
        rol = Rol.objects.get(id = id, estado = True)
    except Rol.DoesNotExist:
        return Response({'mensaje': 'Rol no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    rol.estado = False
    rol.save()
    return Response({'mensaje': 'Rol eliminado'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def crear_permiso(request):
    try:
        nombre_permiso = request.data.get('nombre')
        if not nombre_permiso:
            return Response({'mensaje': 'El nombre del permiso es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        permiso, creado = Permiso.objects.get_or_create(nombre=nombre_permiso)
        if not creado:
            return Response({'mensaje': 'El permiso ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'Permiso creado exitosamente.', 'permiso': permiso.nombre}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({
            'mensaje': f'Error interno del servidor: {str(e)}',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def listar_permisosXRol(request, id):
    try:
        # Verificar que el rol existe
        try:
            rol = Rol.objects.get(id=id, estado=True)
        except Rol.DoesNotExist:
            return Response({
                'status': 'error',
                'mensaje': 'Rol no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener TODOS los permisos del sistema
        todos_permisos = Permiso.objects.all().order_by('nombre')

        #Obtener RolPermiso con el campo estado
        rol_permisos_dict = {}
        rol_permisos = RolPermiso.objects.filter(rol=rol).select_related('permiso')
        
        for rol_permiso in rol_permisos:
            rol_permisos_dict[rol_permiso.permiso.id] = rol_permiso.estado
        
        # Crear lista con todos los permisos y su estado desde RolPermiso
        permisos_data = []
        for permiso in todos_permisos:
            permisos_data.append({
                'id': permiso.id,
                'nombre': permiso.nombre,
                'estado': rol_permisos_dict.get(permiso.id, False)  # Usar campo estado
            })
        
        
        return Response({
            'permisos': permisos_data,
            'rol': rol.nombre,
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'mensaje': f'Error interno del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['PATCH'])
def actualizar_permisos_rol(request,id):

    try:
        # Obtener datos del request
        permisos_data = request.data.get('permisos', [])
        try:
            rol = Rol.objects.get(id=id, estado=True)
        except Rol.DoesNotExist:
            return Response({
                'status': 'error',
                'mensaje': 'Rol no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validaciones básicas
        if not permisos_data:
            return Response({
                'status': 'error',
                'mensaje': 'Lista de permisos es requerida'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Procesar cada permiso
        actualizados = []
        errores = []
        
        for permiso_item in permisos_data:
            permiso_id = permiso_item.get('id')
            nuevo_estado = permiso_item.get('estado')
            
            if permiso_id is None or nuevo_estado is None:
                errores.append(f'Permiso sin ID o estado válido: {permiso_item}')
                continue
            
            try:
                # Verificar que el permiso existe
                permiso = Permiso.objects.get(id=permiso_id)
                
                # Buscar o crear RolPermiso
                rol_permiso, creado = RolPermiso.objects.get_or_create(
                    rol=rol,
                    permiso=permiso,
                    defaults={'estado': nuevo_estado}
                )
                
                if not creado:
                    # Ya existía, actualizar estado
                    estado_anterior = rol_permiso.estado
                    rol_permiso.estado = nuevo_estado
                    rol_permiso.save()
                    
                    accion = 'actualizado' if estado_anterior != nuevo_estado else 'sin cambios'
                else:
                    accion = 'creado'
                
                actualizados.append({
                    'id': permiso.id,
                    'nombre': permiso.nombre,
                    'estado': nuevo_estado,
                    'accion': accion
                })
                
            except Permiso.DoesNotExist:
                errores.append(f'Permiso con ID {permiso_id} no encontrado')
            except Exception as e:
                errores.append(f'Error procesando permiso {permiso_id}: {str(e)}')
        

        # Preparar respuesta
        response_data = {
            'permisos_procesados': actualizados,
            'rol': rol.nombre,
        }
        
        if errores:
            response_data['errores'] = errores
            response_data['status'] = 'warning'
            response_data['mensaje'] += f' con {len(errores)} errores'
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'mensaje': f'Error interno del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)