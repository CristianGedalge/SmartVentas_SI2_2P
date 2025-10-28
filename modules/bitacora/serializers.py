from rest_framework import serializers
from .models import Bitacora

class BitacoraSerializer(serializers.ModelSerializer):
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    fecha = serializers.SerializerMethodField()
    hora = serializers.SerializerMethodField()

    class Meta:
        model = Bitacora
        fields = ['id', 'usuario_email', 'accion', 'ip', 'fecha', 'hora']

    def get_fecha(self, obj):
        # Solo la fecha (YYYY-MM-DD)
        return obj.fecha_registro.strftime('%Y-%m-%d')

    def get_hora(self, obj):
        # Solo la hora (HH:MM:SS)
        return obj.fecha_registro.strftime('%H:%M:%S')
