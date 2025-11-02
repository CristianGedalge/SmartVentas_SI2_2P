from rest_framework import serializers
from .models import Inventario


class InventarioCreateSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    marca =serializers.CharField(source='producto.marca.nombre', read_only=True)
    fecha = serializers.SerializerMethodField()
    precio_compra_total = serializers.DecimalField(max_digits=12,decimal_places=2,read_only=True)
    class Meta:
        model = Inventario
        fields = '__all__'

    def get_fecha(self, obj):
        return obj.fecha.strftime('%Y-%m-%d')




class InventarioListSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    marca =serializers.CharField(source='producto.marca.nombre', read_only=True)
    fecha = serializers.SerializerMethodField()
    class Meta:
        model = Inventario
        fields = '__all__'

    def get_fecha(self, obj):
        return obj.fecha.strftime('%Y-%m-%d')
