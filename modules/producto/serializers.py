
from rest_framework import serializers
from .models import Producto



class ProductoCreateSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    precio = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    stock = serializers.IntegerField(read_only=True)
    fecha = serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = '__all__'

    def get_fecha(self, obj):
        return obj.fecha.strftime('%Y-%m-%d')  # Solo año-mes-día

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    fecha = serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = '__all__'

    def get_fecha(self, obj):
        return obj.fecha.strftime('%Y-%m-%d')  # Solo año-mes-día


class CatalogoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock','tiempo_garantia','tipo_garantia','url_img']
    
