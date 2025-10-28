# modules/roles/serializers.py
from rest_framework import serializers
from .models import Rol

class RolSerializer(serializers.ModelSerializer):

    fecha_registro = serializers.SerializerMethodField()
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'estado', 'fecha_registro']
        read_only_fields = ['id', 'fecha_registro']

    def get_fecha_registro(self, obj):
        # obj.fecha_registro es un datetime, aquí devolvemos solo YYYY-MM-DD
        return obj.fecha_registro.date().isoformat()
    
