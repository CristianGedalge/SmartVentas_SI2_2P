
from rest_framework import viewsets
from .models import Categoria
from .serializers import CategoriaSerializer

# Endpoint: /api/categorias/
class CategoriaViewSet(viewsets.ModelViewSet):
    # El queryset define la colección de objetos (todas las categorías)
    queryset = Categoria.objects.all()
    # El serializer_class define cómo se formatean y validan los datos
    serializer_class = CategoriaSerializer
