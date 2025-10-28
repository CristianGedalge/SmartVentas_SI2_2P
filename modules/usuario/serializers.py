from rest_framework import serializers
from .models import UsuarioInfo

class UsuarioInfoListSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='usuario.email', read_only=True)
    rol = serializers.CharField(source='usuario.rol.nombre', read_only=True)

    class Meta:
        model = UsuarioInfo
        fields = ['id', 'email', 'rol', 'nombre', 'apellido', 'telefono', 'url_img', 'direccion', 'estado']



class UsuarioActualizarSerializer(serializers.ModelSerializer):
    rol = serializers.IntegerField(required=False)  # se valida, pero se procesa en la vista

    class Meta:
        model = UsuarioInfo
        exclude = [ 'usuario']  # no modificamos imagen ni relación usuario