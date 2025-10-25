from rest_framework import serializers
from .models import Categoria  # Asegúrate de importar tu modelo

class CategoriaSerializer(serializers.ModelSerializer):
    fecha_registro = serializers.SerializerMethodField()
    class Meta:
        # 1. Especifica el Modelo al que está asociado este Serializer
        model = Categoria
        
        # 2. Define qué campos del modelo deben ser incluidos en la API
        #    '__all__' incluye todos los campos (id, nombre, estado, fecha)
        fields = '__all__' 
        
        # 3. Campos de Solo Lectura (Opcional pero recomendado para campos de DB)
        #    Asegura que el cliente no pueda modificar el 'id' ni la 'fecha' de creación.
        read_only_fields = ('id', 'fecha',)

    def get_fecha_registro(self, obj):
        # obj.fecha_registro es un datetime, aquí devolvemos solo YYYY-MM-DD
        return obj.fecha_registro.date().isoformat()
    
