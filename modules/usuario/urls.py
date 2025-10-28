from django.urls import path
from . import views

# URLs para el módulo de Usuario
urlpatterns = [
    
    path('findAllUsuario/', views.listar_usuarios, name='listar-usuario'),
    
    path('updateUsuario/<int:id>/', views.actualizar_usuario, name='actualizar-usuario'),

    path('deleteUsuario/<int:id>/', views.eliminar_usuario, name='eliminar-usuario'),

    path('perfil/', views.obtener_perfil, name='obtener-perfil'),

]