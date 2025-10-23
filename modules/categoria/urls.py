from django.urls import path
from rest_framework.routers import DefaultRouter  
from .views import CategoriaViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
# No necesitas 'urlpatterns' aquí si solo usas el Router, pero si lo tuvieras, sería:
urlpatterns = router.urls

