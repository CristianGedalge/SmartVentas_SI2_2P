from rest_framework import serializers
from .models import Marca  # Asegúrate de importar tu modelo

class MarcaSerializer(serializers.ModelSerializer):
    fecha_registro = serializers.SerializerMethodField()
    class Meta:
        # 1. Especifica el Modelo al que está asociado este Serializer
        model = Marca
        # 2. Define qué campos del modelo deben ser incluidos en la respuesta API
        #    '__all__' incluye todos los campos (id, nombre, estado, fecha)
        fields = ('id','nombre','estado','fecha_registro') 
        
        # 3. Campos de Solo Lectura (Opcional pero recomendado para campos de DB)
        #    Asegura que el cliente no pueda modificar el 'id' ni la 'fecha' de creación.
        read_only_fields = ('id','estado','fecha_registro',)

    def get_fecha_registro(self, obj):
        # obj.fecha_registro es un datetime, aquí devolvemos solo YYYY-MM-DD
        return obj.fecha_registro.date().isoformat()
    
