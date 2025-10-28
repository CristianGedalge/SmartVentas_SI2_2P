from django.urls import path
from . import views

# URLs para el módulo de roles
urlpatterns = [
    path('listarBitacora/', views.listar_bitacora, name='listar-bitacora'),
]