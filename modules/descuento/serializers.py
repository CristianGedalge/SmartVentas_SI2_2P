from rest_framework import serializers
from .models import Descuento

from modules.producto.models import Producto

class DescuentoCreateSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    marca =serializers.CharField(source='producto.marca.nombre', read_only=True)
    fecha_inicio = serializers.DateField(format='%Y-%m-%d')
    fecha_fin = serializers.DateField(format='%Y-%m-%d')
    class Meta:
        model = Descuento
        fields = '__all__'

    
class DescuentoListSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    marca =serializers.CharField(source='producto.marca.nombre', read_only=True)
    fecha_inicio = serializers.SerializerMethodField()
    fecha_fin = serializers.SerializerMethodField()
    class Meta:
        model = Descuento
        fields = '__all__'

    def get_fecha_inicio(self, obj):
        return obj.fecha_inicio.strftime('%Y-%m-%d')
    
    
    def get_fecha_fin(self, obj):
        return obj.fecha_fin.strftime('%Y-%m-%d')
    


class CatalogoDescuentoSerializer(serializers.ModelSerializer):
    fecha = serializers.SerializerMethodField()
    descuento = serializers.SerializerMethodField()
    precio_descuento=serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio','url_img','tiempo_garantia','tipo_garantia', 'stock', 'fecha','descuento','precio_descuento']

    def get_fecha(self, obj):
        return obj.fecha.strftime('%Y-%m-%d')  # Solo año-mes-día
    
    def get_descuento(self, obj):
        # Si el producto tiene relación con Descuento (ej. related_name='descuentos')
        descuento = obj.descuentos.first()  # obtiene el primero que exista
        return descuento.porcentaje
    
    def get_precio_descuento(self, obj):
        """Calcula el precio final aplicando el porcentaje de descuento."""
        descuento = obj.descuentos.first()
        if descuento and descuento.porcentaje:
            precio_final = obj.precio - (obj.precio * (descuento.porcentaje / 100))
            return round(precio_final, 2)
        return obj.precio
