from django.urls import path
from . import views

# URLs para el módulo de producto
urlpatterns = [
    path('createDescuento/', views.crear_descuento, name='crear-descuento'),
    
    path('findAllDescuento/', views.listar_descuentos, name='listar-descuento'),

    path('updateDescuento/<int:id>/', views.actualizar_descuento, name='actualizar-descuento'),

    path('deleteDescuento/<int:id>/', views.eliminar_descuento, name='eliminar-descuento'),

    #para el catálogo de descuentos
    path('catalogoDescuento/', views.catalogo_descuento, name='catologo-descuento')
]