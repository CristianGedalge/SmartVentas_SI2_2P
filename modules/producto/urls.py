from django.urls import path
from . import views

# URLs para el módulo de producto
urlpatterns = [
    path('createProducto/', views.crear_producto, name='crear-producto'),
    
    path('findAllProducto/', views.listar_productos, name='listar-producto'),

    path('getProducto/<int:id>/', views.obtener_producto, name='obtener-producto'),

    path('updateProducto/<int:id>/', views.actualizar_producto, name='actualizar-producto'),

    path('deleteProducto/<int:id>/', views.eliminar_producto, name='eliminar-producto'),

    #url para catalogo no requeris token xd
    path('catalogo/', views.catalogo, name='catologo')
]