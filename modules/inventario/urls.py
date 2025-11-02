from django.urls import path
from . import views

# URLs para el módulo de Inventario
urlpatterns = [
    path('createInventario/', views.crear_inventario, name='crear-inventario'),
    
    path('findAllInventario/', views.listar_inventarios, name='listar-inventarios'),

    # path('getInventario/<int:id>/', views.obtener_inventario, name='obtener-inventario'),

    # path('updateInventario/<int:id>/', views.actualizar_inventario, name='actualizar-inventario'),

    path('deleteInventario/<int:id>/', views.eliminar_inventario, name='eliminar-inventario')

]