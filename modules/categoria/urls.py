from django.urls import path
from . import views

# URLs para el módulo de roles
urlpatterns = [
    path('createCategoria/', views.crear_categoria, name='crear-categoria'),
    
    path('findAllCategoria/', views.listar_categoria, name='listar-categoria'),
    
    path('updateCategoria/<int:id>/', views.actualizar_categoria, name='actualizar-categoria'),

    path('deleteCategoria/<int:id>/', views.eliminar_categoria, name='eliminar-categoria'),

]