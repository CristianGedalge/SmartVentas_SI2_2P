from rest_framework import serializers
from .models import Venta, DetalleVenta

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = DetalleVenta
        fields = [
            'id',
            'producto_nombre',
            'cantidad',
            'precio_unitario',
            'subtotal',
            'porcentaje_descuento',
            'monto_descuento'
        ]

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer( many=True, read_only=True)
    fecha = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Venta
        fields = [
            'id',
            'codigo_venta',
            'fecha',
            'total',
            'detalles'
        ]