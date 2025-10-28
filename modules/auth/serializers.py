from rest_framework import serializers
from .models import Usuario
from modules.roles.models import Rol
from modules.usuario.models import UsuarioInfo

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=True)
    apellido = serializers.CharField(required=True)
    telefono = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    direccion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    url_img = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    rol = serializers.IntegerField(required=False)  # opcional

    class Meta:
        model = Usuario
        fields = ['email', 'password', 'rol', 'nombre', 'apellido', 'telefono', 'direccion', 'url_img']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extraer info
        info_data = {
            'nombre': validated_data.pop('nombre'),
            'apellido': validated_data.pop('apellido'),
            'telefono': validated_data.pop('telefono', None),
            'direccion': validated_data.pop('direccion', None),
            'url_img': validated_data.pop('url_img', None),
        }

        # Asignar rol
        rol_id = validated_data.pop('rol', None)
        if rol_id:
            try:
                rol = Rol.objects.get(pk=rol_id)
            except Rol.DoesNotExist:
                raise serializers.ValidationError({'rol': 'Rol no válido'})
        else:
            rol = Rol.objects.get(nombre__iexact='Cliente')  # rol por defecto

        # Crear usuario
        usuario = Usuario.objects.create(rol=rol, **validated_data)

        # Crear info del usuario
        UsuarioInfo.objects.create(usuario=usuario, **info_data)

        return usuario
    

class UsuarioInfoListSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='usuario.email', read_only=True)
    rol = serializers.CharField(source='usuario.rol.nombre', read_only=True)

    class Meta:
        model = UsuarioInfo
        fields = ['id', 'email', 'rol', 'nombre', 'apellido', 'telefono', 'direccion', 'estado']


